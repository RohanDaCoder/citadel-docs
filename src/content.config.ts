import { defineCollection } from "astro:content";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";

export const collections = {
  docs: defineCollection({
    loader: docsLoader({
      // Preserve the exact case of file paths in page slugs.
      // The default implementation lowercases every path segment, which would
      // collapse Citadel's case-distinct API reference pages (e.g. `Camera` the
      // type vs `camera` the global, `World` vs `world`).
      generateId({ entry }) {
        // `entry` is the file path relative to the collection base,
        // e.g. `ref/World/index.md` or `systems/storage.md`.
        const withoutExt = entry.replace(/\.[^./]+$/, "");
        return withoutExt === "index"
          ? "index"
          : withoutExt.replace(/\/index$/, "");
      },
    }),
    schema: docsSchema(),
  }),
};
