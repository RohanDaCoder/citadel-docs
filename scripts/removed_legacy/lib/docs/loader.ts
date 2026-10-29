import { pageLoaders } from "@/data/page-loaders.generated";

export interface TocEntry {
  id: string;
  text: string;
  level: number;
}

export interface WikiPageData {
  type: "wiki";
  slug: string;
  section: string;
  title: string;
  description: string;
  tags: string[];
  markdown: string;
  toc: TocEntry[];
}

export interface RefMemberListing {
  name: string;
  section: string;
  signature: string;
  description: string;
  href: string;
  href2: string | null;
}

export interface RefPageData {
  type: "ref";
  name: string;
  kind: "global" | "type";
  assocType: string;
  title: string;
  lead: string;
  typedef: string;
  docsLink: { title: string; href: string | null } | null;
  functions: RefMemberListing[];
  fields: RefMemberListing[];
  others: RefMemberListing[];
}

export interface RefParam {
  name: string;
  type: string;
  required: boolean | null;
}

export interface RefUsedIn {
  quote: string;
  source: string;
  href: string;
}

export interface RefMemberPageData {
  type: "refmember";
  parent: string;
  name: string;
  title: string;
  kind: string;
  lead: string;
  signature: string;
  params: RefParam[];
  returns: string[];
  usedIn: RefUsedIn[];
}

export type AnyPage = WikiPageData | RefPageData | RefMemberPageData;

const loaderMap = new Map<string, (() => Promise<unknown>)>();
for (const l of pageLoaders) loaderMap.set(l.key, l.load);

const cache = new Map<string, AnyPage | null>();

function keyFor(routeKind: string, a: string, b?: string): string {
  if (routeKind === "wiki") return `wiki:${a}`;
  if (routeKind === "ref") return a;
  return `${a}.${b}`;
}

export async function loadPage(route: { kind: string; slug?: string; name?: string; member?: string }): Promise<AnyPage | null> {
  let key: string;
  if (route.kind === "wiki") key = `wiki:${route.slug}`;
  else if (route.kind === "ref") key = route.name!;
  else key = `${route.name}.${route.member}`;

  if (cache.has(key)) return cache.get(key)!;

  const loader = loaderMap.get(key);
  if (!loader) {
    // case-insensitive fallback for ref pages
    const lower = key.toLowerCase();
    for (const [k, l] of loaderMap) {
      if (k.toLowerCase() === lower) {
        const mod = (await l()) as { default: AnyPage };
        cache.set(key, mod.default);
        return mod.default;
      }
    }
    cache.set(key, null);
    return null;
  }
  const mod = (await loader()) as { default: AnyPage };
  cache.set(key, mod.default);
  return mod.default;
}

export type { keyFor };
