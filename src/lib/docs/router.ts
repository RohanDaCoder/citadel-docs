import { useCallback, useMemo, useSyncExternalStore } from "react";

export type Route =
  | { kind: "home" }
  | { kind: "guide"; slug: string }
  | { kind: "doc"; slug: string }
  | { kind: "reference" }
  | { kind: "ref"; name: string }
  | { kind: "refmember"; name: string; member: string };

export function parseHash(hash: string): Route {
  const path = hash.replace(/^#/, "").replace(/^\/+|\/+$/g, "");
  if (!path) return { kind: "home" };
  const parts = path.split("/").map(decodeURIComponent);
  if (parts[0] === "guides" && parts[1]) return { kind: "guide", slug: parts[1] };
  if (parts[0] === "docs" && parts[1]) return { kind: "doc", slug: parts[1] };
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
    case "guide":
      return `#/guides/${route.slug}`;
    case "doc":
      return `#/docs/${route.slug}`;
    case "reference":
      return "#/reference";
    case "ref":
      return `#/reference/${route.name}`;
    case "refmember":
      return `#/reference/${route.name}/${route.member}`;
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

/** Convert original minefort docs URLs into local hash routes. */
export function docsUrlToHash(href: string): string | null {
  if (!href.startsWith("/docs/citadel")) return null;
  let rest = href.replace("/docs/citadel", "").replace(/^\/+|\/+$/g, "");
  if (!rest || rest === "docs") return "#/";
  const parts = rest.split("/");
  if (parts[0] === "guides" && parts[1]) return `#/guides/${parts[1]}`;
  if (parts[0] === "reference") {
    parts.shift();
    if (parts.length === 0) return "#/reference";
    if (parts.length === 1) return `#/reference/${parts[0]}`;
    return `#/reference/${parts[0]}/${parts[1]}`;
  }
  return `#/docs/${rest}`;
}
