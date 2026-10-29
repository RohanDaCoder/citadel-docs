const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const pagesDir = '/home/z/my-project/src/data/pages';
  const wikiSlugs = fs.readdirSync(pagesDir)
    .filter(f => f.startsWith('wiki-') && f.endsWith('.json'))
    .map(f => f.slice(5, -5));
  const refs = fs.readdirSync(pagesDir)
    .filter(f => (f.startsWith('ref-') || f.startsWith('refm-')) && f.endsWith('.json'))
    .sort(() => 0.5 - Math.random())
    .slice(0, 40);

  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  const failures = [];
  page.on('pageerror', e => errors.push(e.message.slice(0, 120)));

  const routes = [
    ...wikiSlugs.map(s => `#/wiki/${s}`),
    ...refs.map(f => {
      if (f.startsWith('refm-')) {
        const m = f.slice(5, -5); // Parent-member
        const idx = m.indexOf('-');
        return `#/ref/${m.slice(0, idx)}/${m.slice(idx + 1)}`;
      }
      return `#/ref/${f.slice(4, -5)}`;
    }),
  ];

  for (const r of routes) {
    try {
      await page.goto('http://localhost:3000/' + r, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(150);
      const h1 = await page.textContent('h1').catch(() => null);
      const notFound = await page.textContent('body').then(t => t.includes('does not exist in this snapshot')).catch(() => false);
      if (!h1 || notFound) failures.push(r + (notFound ? ' (404)' : ' (no h1)'));
    } catch (e) {
      failures.push(r + ' ERR ' + e.message.slice(0, 60));
    }
  }
  console.log(`checked ${routes.length} routes`);
  console.log('failures:', failures.length ? failures : 'none');
  console.log('page errors:', errors.length ? [...new Set(errors)].slice(0, 8) : 'none');
  await browser.close();
})();
