import { useCallback, useMemo, useSyncExternalStore } from "react";
import redirectsJson from "@/data/redirects.json";

export type Route =
  | { kind: "home" }
  | { kind: "wiki"; slug: string }
  | { kind: "reference" }
  | { kind: "ref"; name: string }
  | { kind: "refmember"; name: string; member: string };

const redirects = redirectsJson as Record<string, string>;

export function parseHash(hash: string): Route {
  const path = hash.replace(/^#/, "").replace(/^\/+|\/+$/g, "");
  if (!path) return { kind: "home" };
  const parts = path.split("/").map(decodeURIComponent);
  if (parts[0] === "wiki" && parts[1]) return { kind: "wiki", slug: parts[1] };
  if (parts[0] === "ref") {
    if (!parts[1]) return { kind: "reference" };
    if (parts[2]) return { kind: "refmember", name: parts[1], member: parts[2] };
    return { kind: "ref", name: parts[1] };
  }
  // legacy shapes from the first build
  if (parts[0] === "guides" && parts[1]) return { kind: "wiki", slug: `guide-${parts[1]}` };
  if (parts[0] === "docs" && parts[1]) {
    const leg = redirects[`/docs/citadel/${parts[1]}`];
    if (leg) {
      const target = leg.replace(/^#\/wiki\//, "");
      if (leg.startsWith("#/wiki/")) return { kind: "wiki", slug: target };
      if (leg === "#/ref") return { kind: "reference" };
    }
    return { kind: "wiki", slug: parts[1] };
  }
  if (parts[0] === "reference") {
    if (!parts[1]) return { kind: "reference" };
    if (parts[2]) return { kind: "refmember", name: parts[1], member: parts[2] };
    return { kind: "ref", name: parts[1] };
  }
  return { kind: "home" };
}

export function routeToHash(route: Route): string {
  switch (route.kind) {
    case "home":
      return "#/";
    case "wiki":
      return `#/wiki/${route.slug}`;
    case "reference":
      return "#/ref";
    case "ref":
      return `#/ref/${route.name}`;
    case "refmember":
      return `#/ref/${route.name}/${route.member}`;
  }
}

function subscribe(onChange: () => void) {
  window.addEventListener("hashchange", onChange);
  return () => window.removeEventListener("hashchange", onChange);
}

function getSnapshot(): string {
  return window.location.hash;
}

function getServerSnapshot(): string {
  return "";
}

/** Hash-based SPA router that stays SSR-safe via useSyncExternalStore. */
export function useHashRoute() {
  const hash = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  const route = useMemo(() => parseHash(hash), [hash]);

  const navigate = useCallback((target: string) => {
    const next = target.startsWith("#") ? target : `#${target}`;
    if (window.location.hash === next) {
      window.scrollTo({ top: 0 });
      return;
    }
    window.location.hash = next;
    window.scrollTo({ top: 0 });
  }, []);

  return { route, navigate };
}

export function scrollToAnchor(id: string) {
  const el = document.getElementById(id);
  if (el) {
    const y = el.getBoundingClientRect().top + window.scrollY - 84;
    window.scrollTo({ top: y, behavior: "smooth" });
  }
}

/**
 * Convert any href found in content into a local hash route.
 * Handles /wiki/..., /ref/..., /appendix/..., original /docs/citadel/... URLs
 * (via the redirect map), and bare #anchors.
 */
export function linkToHash(href: string): string | null {
  if (!href) return null;
  if (href.startsWith("#")) return href;
  if (href.startsWith("/wiki/")) return `#${href}`;
  if (href.startsWith("/appendix/")) return `#${href.replace("/appendix/", "/wiki/")}`;
  if (href.startsWith("/ref")) return `#${href}`;
  if (href.startsWith("/docs/citadel")) {
    const r = redirects[href];
    if (r) return r;
    // unmapped original URL — try closest guesses
    const rest = href.replace("/docs/citadel", "").replace(/^\/+|\/+$/g, "");
    if (!rest || rest === "docs") return "#/";
    const parts = rest.split("/");
    if (parts[0] === "reference") {
      parts.shift();
      if (parts.length === 0) return "#/ref";
      if (parts.length === 1) return `#/ref/${parts[0]}`;
      return `#/ref/${parts[0]}/${parts[1]}`;
    }
    return redirects[`/docs/citadel/${parts[0]}`] ?? null;
  }
  return null;
}
