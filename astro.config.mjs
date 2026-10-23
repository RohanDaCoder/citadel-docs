import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const manifest = JSON.parse(
        readFileSync(
                fileURLToPath(new URL('./scripts/generated/starlight-manifest.json', import.meta.url)),
                'utf-8',
        ),
);

export default defineConfig({
        redirects: manifest.redirects,
        integrations: [
                starlight({
                        title: 'Citadel Developer Wiki',
                        description:
                                'A restructured, developer-facing reference for Minefort Citadel — the Luau scripting engine for Minecraft servers. Concepts, every API call, and working guides.',
                        tagline: 'Minefort Citadel, restructured for developers',
                        sidebar: manifest.sidebar,
                        customCss: ['./src/styles/custom.css'],
                        tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
                        pagination: true,
                        credits: true,
                }),
        ],
});
