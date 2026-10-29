const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  const routes = [
    '#/',
    '#/wiki/what-is-citadel',
    '#/wiki/quick-start',
    '#/wiki/architecture',
    '#/wiki/runtime',
    '#/wiki/events',
    '#/wiki/conventions',
    '#/wiki/terrain-generation',
    '#/wiki/custom-blocks',
    '#/wiki/custom-entities',
    '#/wiki/player-lifecycle',
    '#/wiki/ui-basics',
    '#/wiki/displays',
    '#/wiki/commands',
    '#/wiki/shared-stores',
    '#/wiki/guide-build-a-cottage',
    '#/wiki/cookbook-minigame-loop',
    '#/wiki/event-catalog',
    '#/wiki/limits-table',
    '#/wiki/faq',
    '#/ref',
    '#/ref/World',
    '#/ref/World/block',
    '#/ref/Player',
    '#/ref/Player/give',
    '#/ref/world',
    '#/ref/camera',
    '#/ref/Camera',
    '#/ref/tween',
  ];
  for (const r of routes) {
    await page.goto('http://localhost:3000/' + r, { waitUntil: 'networkidle', timeout: 20000 });
    await page.waitForTimeout(400);
    const h1 = await page.textContent('h1').catch(() => '(no h1)');
    console.log(r.padEnd(38), '=>', (h1 || '').trim().slice(0, 60));
  }
  console.log('\nERRORS:', errors.length ? errors.slice(0, 10) : 'none');
  await browser.close();
})();
