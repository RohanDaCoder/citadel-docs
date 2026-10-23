const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const shots = [
    ['#/', 'wiki-home'],
    ['#/wiki/architecture', 'wiki-concept'],
    ['#/wiki/events', 'wiki-events-callouts'],
    ['#/wiki/terrain-generation', 'wiki-terrain-tables'],
    ['#/wiki/guide-coin-rush', 'wiki-guide'],
    ['#/wiki/event-catalog', 'wiki-event-catalog'],
    ['#/ref', 'ref-index'],
    ['#/ref/World', 'ref-world'],
    ['#/ref/Player/give', 'ref-member'],
  ];
  for (const [route, name] of shots) {
    await page.goto('http://localhost:3000/' + route, { waitUntil: 'networkidle', timeout: 25000 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `/home/z/my-project/scripts/verify/shot-${name}.png` });
    console.log('shot', name);
  }

  // search dialog test
  await page.goto('http://localhost:3000/#/wiki/what-is-citadel', { waitUntil: 'networkidle' });
  await page.keyboard.press('Meta+k');
  await page.waitForTimeout(400);
  await page.fill('input[cmdk-input=""]', 'raycast');
  await page.waitForTimeout(300);
  await page.screenshot({ path: '/home/z/my-project/scripts/verify/shot-search.png' });
  console.log('shot search');

  // mobile
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto('http://localhost:3000/#/wiki/quick-start', { waitUntil: 'networkidle' });
  await m.waitForTimeout(400);
  await m.screenshot({ path: '/home/z/my-project/scripts/verify/shot-mobile.png' });
  await m.click('button[aria-label="Open navigation"]');
  await m.waitForTimeout(400);
  await m.screenshot({ path: '/home/z/my-project/scripts/verify/shot-mobile-nav.png' });
  console.log('shot mobile');

  await browser.close();
})();
