import { pageLoaders } from "@/data/page-loaders.generated";

export interface TocEntry {
  id: string;
  text: string;
  level: number;
}

export interface GuidePageData {
  type: "guide";
  slug: string;
  title: string;
  description: string;
  markdown: string;
  toc: TocEntry[];
}

export interface DocPageData {
  type: "doc";
  slug: string;
  title: string;
  topic: string;
  markdown: string;
  toc: TocEntry[];
}

export interface RefMemberListing {
  name: string;
  section: string;
  signature: string;
  description: string;
  hasPage: boolean;
}

export interface RefPageData {
  type: "ref";
  name: string;
  kind: "global" | "type";
  assocType: string;
  topic: string;
  lead: string;
  typedef: string;
  docsLink: { title: string; href: string } | null;
  functions: RefMemberListing[];
  fields: RefMemberListing[];
}

export interface RefMemberParam {
  name: string;
  type: string;
  required: boolean;
}

export interface UsedIn {
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
  params: RefMemberParam[];
  returns: string[];
  usedIn: UsedIn[];
}

export type AnyPage = GuidePageData | DocPageData | RefPageData | RefMemberPageData;

const cache = new Map<string, AnyPage | null>();

export async function loadPage(route: {
  kind: string;
  slug?: string;
  name?: string;
  member?: string;
}): Promise<AnyPage | null> {
  let id: string | null = null;
  switch (route.kind) {
    case "guide":
      id = `guide-${route.slug}`;
      break;
    case "doc":
      id = `doc-${route.slug}`;
      break;
    case "ref":
      id = `ref-${route.name}`;
      break;
    case "refmember":
      id = `refm-${route.name}-${route.member}`;
      break;
    default:
      return null;
  }
  if (!id || !pageLoaders[id]) return null;
  if (cache.has(id)) return cache.get(id)!;
  try {
    const mod = await pageLoaders[id]();
    const data = mod.default as unknown as AnyPage;
    cache.set(id, data);
    return data;
  } catch {
    cache.set(id, null);
    return null;
  }
}
