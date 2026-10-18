const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const html = pathToFileURL(path.join(__dirname, '..', 'Plugin_Navigator_Full.html')).href;

async function check(browser, name, viewport, mobile) {
  const page = await browser.newPage({ viewport });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  await page.goto(html);
  await page.waitForSelector('#content .hero');

  const version = await page.locator('#db').evaluate(el => JSON.parse(el.textContent).version);
  if (version !== '2.8.3') throw new Error(`${name}: wrong version ${version}`);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (overflow > 2) throw new Error(`${name}: horizontal overflow ${overflow}px`);

  if (mobile) {
    if (!(await page.locator('#bottomNav').isVisible())) throw new Error(`${name}: bottom navigation is hidden`);
    await page.locator('#bottomNav [data-view="more"]').click();
    await page.getByRole('button', { name: /Резервная копия/ }).waitFor();
    await page.locator('#bottomNav [data-view="plugins"]').click();
    await page.locator('#devFilter').selectOption('Waves');
  } else {
    if (!(await page.locator('#sidebar').isVisible())) throw new Error(`${name}: sidebar is hidden`);
    await page.locator('#nav [data-view="ai"]').click();
    await page.getByRole('heading', { name: 'Локальный ИИ-помощник' }).waitFor();
    if (!(await page.locator('#content').getByText(/ИИ доступен в Windows-приложении/).isVisible())) throw new Error(`${name}: file fallback for local AI is missing`);
    await page.locator('#nav [data-view="plugins"]').click();
    await page.locator('#devFilter').selectOption('FabFilter');
  }

  if (errors.length) throw new Error(`${name}: ${errors.join(' | ')}`);
  await page.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    await check(browser, 'desktop', { width: 1440, height: 900 }, false);
    await check(browser, 'mobile', { width: 390, height: 844 }, true);
    console.log(JSON.stringify({ status: 'PASS', version: '2.8.3', viewports: ['1440x900', '390x844'] }));
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error('FAIL', error.stack || error);
  process.exitCode = 1;
});
