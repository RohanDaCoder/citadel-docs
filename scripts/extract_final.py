#!/usr/bin/env python3
"""Final extractor: convert all Citadel pages to structured JSON dataset.

Page types:
1. Guide pages (/docs/citadel/guides/*) -> markdown
2. Doc topic pages (/docs/citadel/*) -> markdown
3. Reference global/type pages (/docs/citadel/reference/X) -> markdown + structured members
4. Reference member pages (/docs/citadel/reference/X/Y) -> structured signature/params/returns
"""
import os
import re
import json
from bs4 import BeautifulSoup, NavigableString, Tag

CRAWL_DIR = "/home/z/my-project/scripts/crawl_html"
OUT_DIR = "/home/z/my-project/scripts/content"
os.makedirs(OUT_DIR, exist_ok=True)

def path_to_file(url_path):
    return os.path.join(CRAWL_DIR, url_path.strip("/").replace("/", "_") + ".html")

# ---------------- markdown conversion ----------------

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
            inner = convert_inline(child).strip()
            parts.append(f"**{inner}**" if inner else "")
        elif child.name in ('em', 'i'):
            inner = convert_inline(child).strip()
            parts.append(f"*{inner}*" if inner else "")
        elif child.name == 'a':
            href = child.get('href', '')
            # get link text WITHOUT nested code backticks doubled
            txt = child.get_text(' ', strip=True)
            if txt:
                txt = txt.replace('`', '')
            if href and txt:
                if href.startswith('#') or href.startswith('/docs'):
                    parts.append(f"[{txt}]({href})")
                else:
                    parts.append(f"[{txt}]({href})")
            elif txt:
                parts.append(txt)
        elif child.name == 'svg':
            continue
        elif child.name == 'br':
            parts.append('\n')
        else:
            parts.append(convert_inline(child))
    return ''.join(parts)

def clean_text(text):
    text = re.sub(r'[ \t]+', ' ', text)
    return text

def code_lang(classes):
    for c in classes or []:
        if c.startswith('language-'):
            lang = c.replace('language-', '')
            return 'luau' if lang == 'lua' else lang
    return ''

def convert_block(el, depth=0):
    out = []
    name = el.name
    if name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        level = int(name[1])
        text = clean_text(convert_inline(el)).strip()
        if text:
            out.append(f"{'#' * level} {text}")
    elif name == 'p':
        # Skip tiny meta spans
        text = clean_text(convert_inline(el)).strip()
        if text:
            out.append(text)
    elif name == 'pre':
        code = el.find('code')
        if code:
            lang = code_lang(code.get('class'))
            text = code.get_text()
            out.append(f"```{lang}\n{text}```")
        else:
            out.append(f"```\n{el.get_text()}```")
    elif name in ('ul', 'ol'):
        for i, li in enumerate(el.find_all('li', recursive=False)):
            prefix = f"{i+1}." if name == 'ol' else "-"
            # li text without nested list
            nested_lists = li.find_all(['ul', 'ol'], recursive=False)
            li_clone = BeautifulSoup(str(li), 'lxml')
            for n in li_clone.find_all(['ul', 'ol']):
                n.decompose()
            li_el = li_clone.find('li') or li_clone
            li_text = clean_text(convert_inline(li_el)).strip()
            out.append(f"{prefix} {li_text}")
            for nested in nested_lists:
                nested_md = convert_block(nested, depth + 1)
                out.extend(['  ' + line for line in nested_md])
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
    elif name == 'blockquote':
        text = clean_text(convert_inline(el)).strip()
        for line in text.split('\n'):
            out.append(f"> {line}")
    elif name == 'section':
        h2 = el.find(['h2', 'h3'])
        if h2:
            # section heading; strip trailing count badge
            text = clean_text(convert_inline(h2)).strip()
            text = re.sub(r'\s*\d+\s*$', '', text)
            if text:
                out.append(f"## {text}")
        for child in el.children:
            if isinstance(child, Tag) and child.name not in ('svg', 'h2', 'h3', 'nav'):
                out.extend(convert_block(child, depth))
    elif name == 'div':
        # div.card in reference pages holds member entries -> handled separately
        is_card = 'card' in (el.get('class') or [])
        if is_card:
            for a in el.find_all('a', recursive=False):
                sig_code = a.find('code')
                desc_p = a.find('p')
                if sig_code:
                    sig = clean_text(sig_code.get_text(' ', strip=True))
                    sig = re.sub(r'\s+', ' ', sig)
                    out.append(f"### {sig}")
                    if desc_p:
                        d = clean_text(convert_inline(desc_p)).strip()
                        if d:
                            out.append(d)
                    href = a.get('href', '')
                    if href:
                        out.append(f"*[Full reference: {href}]*")
                    out.append('')
        else:
            for child in el.children:
                if isinstance(child, Tag) and child.name not in ('svg', 'nav'):
                    out.extend(convert_block(child, depth))
    return out

# ---------------- reference member extraction ----------------

def clean_sig(s):
    """Clean up signature spacing: 'x : T , y' -> 'x: T, y'."""
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([,;)\]])', r'\1', s)
    s = re.sub(r'([(\[])\s+', r'\1', s)
    s = re.sub(r':\s+', ': ', s)
    s = re.sub(r'\s+→', ' →', s)
    s = re.sub(r'→\s+', '→ ', s)
    return s.strip()

def extract_signature(pre_or_code):
    """Extract signature text from a code/pre element."""
    text = pre_or_code.get_text(' ', strip=True)
    return re.sub(r'\s+', ' ', text).strip()

def extract_reference_member(url_path):
    """Extract a reference member page (function/method/field)."""
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
    for svg in article.find_all('svg'):
        svg.decompose()

    h1 = article.find('h1')
    title = h1.get_text(' ', strip=True) if h1 else url_path.split('/')[-1]

    # description lead
    lead = ''
    lead_p = article.find('p', class_='t-lead')
    if lead_p:
        lead = clean_text(convert_inline(lead_p)).strip()

    # signature
    signature = ''
    # the pre right after header
    for pre in article.find_all('pre'):
        signature = clean_sig(pre.get_text(' ', strip=True))
        break
    if not signature:
        for code in article.find_all('code'):
            txt = code.get_text(' ', strip=True)
            if '(' in txt or '→' in txt:
                signature = re.sub(r'\s+', ' ', txt)
                break

    # sections
    params = []
    returns = []
    used_in = []
    kind = ''
    # "Function of time" / "Method of Player" / "Field of X" / "Type ..."
    header = article.find('header')
    if header:
        header_text = header.get_text(' ', strip=True)
        m = re.match(r'(Function|Method|Field|Type|Global)\s+of\s+(\S+)', header_text.replace(title, '', 1).strip())
        if m:
            kind = m.group(1).lower()
            parent = m.group(2)
        else:
            # try spans in header
            for span in header.find_all('span'):
                t = span.get_text(' ', strip=True)
                m2 = re.match(r'(Function|Method|Field|Type|Global)\s+of\s+(\S+)', t)
                if m2:
                    kind = m2.group(1).lower()
                    parent = m2.group(2)
                    break

    for section in article.find_all('section'):
        h2 = section.find('h2')
        if not h2:
            continue
        sec_title = h2.get_text(' ', strip=True)
        if sec_title == 'Parameters':
            card = section.find('div', class_='card')
            if card:
                for row in card.find_all('div', recursive=False):
                    codes = row.find_all('code')
                    meta = row.find('span', class_='t-meta')
                    if not codes:
                        continue
                    pname = codes[0].get_text(strip=True)
                    ptype = codes[1].get_text(' ', strip=True) if len(codes) > 1 else ''
                    req = meta.get_text(strip=True) if meta else ''
                    params.append({
                        'name': pname,
                        'type': re.sub(r'\s+', ' ', ptype),
                        'required': 'required' in req.lower(),
                    })
            else:
                for code in section.find_all('code'):
                    params.append({'name': code.get_text(strip=True), 'type': '', 'required': True})
        elif sec_title == 'Returns':
            for code in section.find_all('code'):
                txt = code.get_text(' ', strip=True)
                if txt:
                    returns.append(re.sub(r'\s+', ' ', txt))
        elif sec_title == 'Used in':
            for a in section.find_all('a'):
                href = a.get('href', '')
                # quote line (code) + source page title
                code_el = a.find('code')
                quote = code_el.get_text(' ', strip=True) if code_el else ''
                spans = a.find_all('span')
                source = ''
                if spans:
                    source = spans[-1].get_text(' ', strip=True)
                if href:
                    used_in.append({'quote': quote, 'source': source, 'href': href})
        elif sec_title == 'Functions':
            pass  # handled by caller for type pages

    return {
        'title': title,
        'url': url_path,
        'kind': kind,
        'lead': lead,
        'signature': signature,
        'params': params,
        'returns': returns,
        'used_in': used_in,
    }

# ---------------- reference type/global page extraction ----------------

def extract_reference_parent(url_path):
    """Extract a reference global/type page: title, lead, signature, member listing."""
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
    for svg in article.find_all('svg'):
        svg.decompose()

    h1 = article.find('h1')
    title = h1.get_text(' ', strip=True) if h1 else url_path.split('/')[-1]

    # lead description: p.t-lead preferred; skip filter placeholder text
    lead = ''
    lead_p = article.find('p', class_='t-lead')
    if lead_p:
        lead = clean_text(convert_inline(lead_p)).strip()
    else:
        for p in article.find_all('p'):
            t = p.get_text(' ', strip=True)
            if t and not t.startswith('No member matches'):
                lead = clean_text(convert_inline(p)).strip()
                break

    # typedef: first pre block (type definition / union) before sections
    typedef = ''
    for pre in article.find_all('pre'):
        typedef = clean_sig(pre.get_text(' ', strip=True))
        break

    # docs cross-link: "Docs: X" anchor to a docs page
    docs_link = None
    for a in article.find_all('a'):
        href = a.get('href', '')
        text = a.get_text(' ', strip=True)
        if text.startswith('Docs:') and href.startswith('/docs/citadel/') and '/reference' not in href:
            docs_link = {'title': text.replace('Docs:', '').strip(), 'href': href}
            break

    # members from sections
    members = []
    sections_info = []
    for section in article.find_all('section'):
        h2 = section.find('h2')
        if not h2:
            continue
        sec_title = h2.get_text(' ', strip=True)
        sec_type = 'functions' if 'function' in sec_title.lower() else (
            'fields' if 'field' in sec_title.lower() else 'other')
        card = section.find('div', class_='card')
        if card:
            for a in card.find_all('a', recursive=False):
                sig_code = a.find('code')
                desc_p = a.find('p')
                sig = ''
                if sig_code:
                    sig = clean_sig(clean_text(sig_code.get_text(' ', strip=True)))
                # member name from href
                href = a.get('href', '')
                mname = href.rstrip('/').split('/')[-1] if href else sig
                desc = ''
                if desc_p:
                    desc = clean_text(convert_inline(desc_p)).strip()
                members.append({
                    'name': mname,
                    'section': sec_type,
                    'signature': sig,
                    'description': desc,
                    'href': href,
                })
        sections_info.append({'title': sec_title, 'type': sec_type})

    return {
        'title': title,
        'url': url_path,
        'lead': lead,
        'typedef': typedef,
        'docs_link': docs_link,
        'members': members,
        'sections': sections_info,
    }

# ---------------- generic page extraction ----------------

def extract_generic(url_path):
    """Extract guide/doc pages to markdown."""
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
    for svg in article.find_all('svg'):
        svg.decompose()
    for nav in article.find_all('nav'):
        nav.decompose()

    h1 = article.find('h1')
    title = h1.get_text(' ', strip=True) if h1 else url_path

    lines = []
    for child in article.children:
        if not isinstance(child, Tag):
            continue
        if child.name in ('header', 'nav'):
            continue
        block_lines = convert_block(child)
        # filter noise
        filtered = []
        for bl in block_lines:
            if bl.strip() in ('Filter members', 'Filter', '') :
                continue
            filtered.append(bl)
        if filtered:
            if lines and filtered[0].startswith('#'):
                lines.append('')
            lines.extend(filtered)
            if not lines[-1].startswith('#'):
                lines.append('')

    md = '\n'.join(lines)
    return {'title': title, 'markdown': md}

def main():
    with open("/home/z/my-project/scripts/all_urls.json") as f:
        urls = json.load(f)

    dataset = {'guides': {}, 'docs': {}, 'reference_parents': {}, 'reference_members': {}}
    md_out = os.path.join(OUT_DIR, 'md')
    os.makedirs(md_out, exist_ok=True)

    stats = {'guide': 0, 'doc': 0, 'ref_parent': 0, 'ref_member': 0, 'fail': 0}

    for url in urls:
        if url in ('/docs/citadel/llms.txt', '/docs/citadel/llms-full.txt', '/docs/citadel#docs'):
            continue
        if url.startswith('/docs/citadel/guides/'):
            r = extract_generic(url)
            if r:
                slug = url.replace('/docs/citadel/guides/', '')
                dataset['guides'][slug] = r
                stats['guide'] += 1
        elif url.startswith('/docs/citadel/reference/'):
            parts = url.replace('/docs/citadel/reference/', '').split('/')
            if len(parts) == 1:
                r = extract_reference_parent(url)
                if r:
                    dataset['reference_parents'][parts[0]] = r
                    stats['ref_parent'] += 1
            else:
                r = extract_reference_member(url)
                if r:
                    parent = parts[0]
                    member = parts[1]
                    dataset['reference_members'].setdefault(parent, {})[member] = r
                    stats['ref_member'] += 1
        elif url == '/docs/citadel':
            r = extract_generic(url)
            if r:
                dataset['docs']['index'] = r
                stats['doc'] += 1
        elif url.startswith('/docs/citadel/'):
            r = extract_generic(url)
            if r:
                slug = url.replace('/docs/citadel/', '')
                dataset['docs'][slug] = r
                stats['doc'] += 1

    with open('/home/z/my-project/scripts/dataset.json', 'w') as f:
        json.dump(dataset, f, indent=1)

    print(f"Guides: {stats['guide']}")
    print(f"Docs pages: {stats['doc']}")
    print(f"Reference parents: {stats['ref_parent']}")
    print(f"Reference members: {stats['ref_member']}")
    print(f"Failed: {stats['fail']}")
    total_size = os.path.getsize('/home/z/my-project/scripts/dataset.json')
    print(f"Dataset size: {total_size/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()
