#!/usr/bin/env python3
"""Extract all Citadel docs pages to structured Markdown files."""
import os
import re
import json
from bs4 import BeautifulSoup, NavigableString, Tag

CRAWL_DIR = "/home/z/my-project/scripts/crawl_html"
OUT_DIR = "/home/z/my-project/scripts/content"
os.makedirs(OUT_DIR, exist_ok=True)

def path_to_file(url_path):
    return os.path.join(CRAWL_DIR, url_path.strip("/").replace("/", "_") + ".html")

def url_to_outfile(url_path):
    """Map URL to output markdown path preserving hierarchy."""
    rel = url_path.replace("/docs/citadel", "").strip("/")
    if not rel:
        rel = "index"
    return os.path.join(OUT_DIR, rel + ".md")

def convert_inline(el):
    """Convert inline elements to markdown text."""
    if isinstance(el, NavigableString):
        return str(el)
    if el.name is None:
        return ""
    if el.name == 'svg':
        return ""
    parts = []
    for child in el.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif child.name == 'code':
            txt = child.get_text()
            parts.append(f"`{txt}`")
        elif child.name in ('strong', 'b'):
            parts.append(f"**{convert_inline(child).strip()}**")
        elif child.name in ('em', 'i'):
            parts.append(f"*{convert_inline(child).strip()}*")
        elif child.name == 'a':
            href = child.get('href', '')
            txt = convert_inline(child).strip()
            if href and txt:
                parts.append(f"[{txt}]({href})")
            elif txt:
                parts.append(txt)
        elif child.name == 'svg':
            continue
        else:
            parts.append(convert_inline(child))
    return ''.join(parts)

def clean_text(text):
    """Normalize whitespace in markdown text."""
    text = re.sub(r'[ \t]+', ' ', text)
    return text

def convert_block(el, depth=0):
    """Convert a block element to markdown lines."""
    out = []
    name = el.name
    if name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        level = int(name[1])
        # Keep h1 as page title marker; demote others by one to fit under it
        text = clean_text(convert_inline(el)).strip()
        if text:
            out.append(f"{'#' * level} {text}")
    elif name == 'p':
        text = clean_text(convert_inline(el)).strip()
        if text:
            out.append(text)
    elif name == 'pre':
        code = el.find('code')
        if code:
            classes = code.get('class', [])
            lang = ''
            for c in classes:
                if c.startswith('language-'):
                    lang = c.replace('language-', '')
                    if lang == 'lua':
                        lang = 'luau'
                    break
            text = code.get_text()
            out.append(f"```{lang}\n{text}\n```")
        else:
            text = el.get_text()
            out.append(f"```\n{text}\n```")
    elif name in ('ul', 'ol'):
        for i, li in enumerate(el.find_all('li', recursive=False)):
            prefix = f"{i+1}." if name == 'ol' else "-"
            li_text = clean_text(convert_inline(li)).strip()
            # Handle nested lists inside li
            nested = li.find(['ul', 'ol'], recursive=False)
            if nested:
                if nested in li.children:
                    li_text = clean_text(convert_inline(_strip_nested(li, nested))).strip()
                out.append(f"{prefix} {li_text}")
                nested_md = convert_block(nested, depth + 1)
                indented = ['  ' + line for line in nested_md]
                out.extend(indented)
            else:
                out.append(f"{prefix} {li_text}")
    elif name == 'table':
        rows = el.find_all('tr')
        if rows:
            headers = rows[0].find_all(['th', 'td'])
            header_texts = [clean_text(convert_inline(c)).strip() for c in headers]
            out.append('| ' + ' | '.join(header_texts) + ' |')
            out.append('| ' + ' | '.join(['---'] * len(header_texts)) + ' |')
            for row in rows[1:]:
                cells = row.find_all(['th', 'td'])
                cell_texts = [clean_text(convert_inline(c)).strip().replace('\n', ' ') for c in cells]
                out.append('| ' + ' | '.join(cell_texts) + ' |')
    elif name in ('div', 'section'):
        for child in el.children:
            if isinstance(child, Tag) and child.name not in ('svg', 'nav'):
                out.extend(convert_block(child, depth))
    elif name == 'blockquote':
        text = clean_text(convert_inline(el)).strip()
        for line in text.split('\n'):
            out.append(f"> {line}")
    return out

def _strip_nested(li, nested):
    """Clone li without the nested list for text extraction."""
    clone = BeautifulSoup(str(li), 'lxml')
    for n in clone.find_all(['ul', 'ol']):
        n.decompose()
    return clone.find('li') or clone

def extract_page(url_path):
    """Extract one page to markdown."""
    fpath = path_to_file(url_path)
    if not os.path.exists(fpath):
        return None
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    if len(html) < 5000:
        return None
    soup = BeautifulSoup(html, 'lxml')
    article = soup.find('article')
    if not article:
        return None

    # Remove decorative/noise elements
    for svg in article.find_all('svg'):
        svg.decompose()
    for nav in article.find_all('nav'):
        nav.decompose()

    # Extract breadcrumb for hierarchy info
    crumbs = []
    crumb_nav = soup.find('nav', class_='crumbs')
    if crumb_nav:
        for a in crumb_nav.find_all('a'):
            crumbs.append(a.get_text(strip=True))
        for span in crumb_nav.find_all('span'):
            t = span.get_text(strip=True)
            if t and t not in crumbs:
                crumbs.append(t)

    # Convert content after the header
    # Find h1 first
    h1 = article.find('h1')
    title = h1.get_text(' ', strip=True) if h1 else url_path

    lines = []
    # Walk article children, skipping the decorative header block (contains stage SVG)
    started = False
    for child in article.children:
        if not isinstance(child, Tag):
            continue
        if child.name == 'header':
            # Title lives in header; extract h1 only
            continue
        if child.name == 'nav':
            continue
        block_lines = convert_block(child)
        if block_lines:
            if lines and block_lines[0].startswith('#'):
                lines.append('')
            lines.extend(block_lines)
            lines.append('')

    md = f"---\ntitle: \"{title.replace('"', '\\'+'\"')}\"\nurl: {url_path}\n---\n\n# {title}\n\n" + '\n'.join(lines)
    return {'title': title, 'markdown': md, 'breadcrumbs': crumbs}

def main():
    with open("/home/z/my-project/scripts/all_urls.json") as f:
        urls = json.load(f)

    stats = {'ok': 0, 'fail': 0, 'empty': 0}
    manifest = []
    for url in urls:
        if url in ('/docs/citadel/llms.txt', '/docs/citadel/llms-full.txt'):
            continue
        result = extract_page(url)
        if result is None:
            stats['fail'] += 1
            continue
        out_file = url_to_outfile(url)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(result['markdown'])
        if len(result['markdown']) < 400:
            stats['empty'] += 1
        stats['ok'] += 1
        manifest.append({'url': url, 'title': result['title'], 'file': out_file.replace(OUT_DIR + '/', ''),
                         'breadcrumbs': result['breadcrumbs'], 'size': len(result['markdown'])})

    with open("/home/z/my-project/scripts/manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Extracted: {stats['ok']} pages ({stats['empty']} near-empty), failed: {stats['fail']}")
    # Show hierarchy
    cats = {}
    for m in manifest:
        bc = ' > '.join(m['breadcrumbs'][:3]) if m['breadcrumbs'] else 'root'
        cats[bc] = cats.get(bc, 0) + 1
    for k, v in sorted(cats.items()):
        print(f"  {v:4d}  {k}")

if __name__ == "__main__":
    main()
