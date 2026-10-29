"use client";

import { nav } from "./Sidebar";
import type { Route } from "@/lib/docs/router";

export interface Neighbor {
  href: string;
  title: string;
}

/** Compute prev/next links for a route within its section flow. */
export function getNeighbors(route: Route): { prev: Neighbor | null; next: Neighbor | null } {
  if (route.kind === "guide") {
    const idx = nav.guides.findIndex((g) => g.slug === route.slug);
    const prev = idx > 0 ? { href: `#/guides/${nav.guides[idx - 1].slug}`, title: nav.guides[idx - 1].title } : null;
    const next =
      idx >= 0 && idx < nav.guides.length - 1
        ? { href: `#/guides/${nav.guides[idx + 1].slug}`, title: nav.guides[idx + 1].title }
        : null;
    return { prev, next };
  }
  if (route.kind === "doc") {
    const flat: { href: string; title: string }[] = [];
    for (const topic of nav.docs) {
      for (const p of topic.pages) {
        flat.push({ href: `#/docs/${p.slug}`, title: p.title });
      }
    }
    const idx = flat.findIndex((f) => f.href === `#/docs/${route.slug}`);
    return {
      prev: idx > 0 ? flat[idx - 1] : null,
      next: idx >= 0 && idx < flat.length - 1 ? flat[idx + 1] : null,
    };
  }
  return { prev: null, next: null };
}

export function getTopicOfDoc(slug: string): string | null {
  for (const topic of nav.docs) {
    if (topic.pages.some((p) => p.slug === slug)) return topic.topic;
  }
  return null;
}
