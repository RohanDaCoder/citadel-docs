import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

const manifest = JSON.parse(
  readFileSync(
    fileURLToPath(
      new URL("./scripts/generated/starlight-manifest.json", import.meta.url),
    ),
    "utf-8",
  ),
);

export default defineConfig({
  // Allow the dev server to be reached through proxied/tunnelled hosts
  // (fixes Vite's "Blocked request ... not allowed" behind gateway hosts).
  vite: {
    server: { allowedHosts: true },
  },
  redirects: manifest.redirects,
  integrations: [
    starlight({
      title: "Citadel Developer Wiki",
      description:
        "A restructured, developer-facing reference for Minefort Citadel — the Luau scripting engine for Minecraft servers. Concepts, every API call, and working guides.",
      sidebar: manifest.sidebar,
      customCss: ["./src/styles/custom.css"],
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      pagination: true,
      credits: true,
    }),
  ],
});
