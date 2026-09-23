/**
 * Функциональные тесты готовых тетрадей в jsdom.
 * Проверяют, что собранный single-file HTML действительно работает:
 * навигация, автосохранение, все интерактивные механики, экспорт, печать, темы.
 *
 * Запуск:  node test_workbook_runtime.js [путь1.html путь2.html ...]
 * Без аргументов тестирует обе тетради сепарации в ../../therapy-workbooks.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require(path.join(__dirname, 'test-runtime', 'node_modules', 'jsdom'));

const DEFAULT_TARGETS = [
  path.join(__dirname, '..', 'therapy-workbooks', 'separation_workbook.html'),
  path.join(__dirname, '..', 'therapy-workbooks', 'separation_therapist_workbook.html'),
];

let passed = 0;
const failures = [];

function check(name, cond, extra) {
  if (cond) { passed++; return true; }
  failures.push(name + (extra ? ' — ' + extra : ''));
  return false;
}

function eq(name, actual, expected) {
  check(name + ' (ожидается ' + JSON.stringify(expected) + ', получено ' + JSON.stringify(actual) + ')',
    actual === expected);
}

function fire(el, type) {
  const w = el.ownerDocument.defaultView;
  el.dispatchEvent(new w.Event(type, { bubbles: true }));
}

async function loadDoc(file) {
  const html = fs.readFileSync(file, 'utf8');
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => {
    const msg = String(e && e.message || e);
    if (/Not implemented: (navigation|window\.scrollTo|window\.print)/.test(msg)) return;
    errors.push(msg);
  });
  vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    url: 'https://localhost/workbook.html',
    virtualConsole: vc,
    beforeParse(window) { stubBrowserApis(window); },
  });
  // ждём, пока скрипты отработают
  await new Promise((r) => setTimeout(r, 60));
  return { dom, win: dom.window, doc: dom.window.document, errors };
}

/** jsdom не реализует часть браузерных API — подменяем их заглушками, чтобы шум не мешал тестам. */
function stubBrowserApis(window) {
  window.scrollTo = () => {};
  window.print = () => {};
  window.alert = () => {};
  window.confirm = () => true;
}

function storeOf(win, key) {
  try { return JSON.parse(win.localStorage.getItem(key) || '{}'); } catch (e) { return {}; }
}

async function testWorkbook(file) {
  const base = path.basename(file);
  console.log('\n=== ' + base + ' ===');
  if (!fs.existsSync(file)) { failures.push(base + ': файл не найден'); return; }

  const { win, doc, errors } = await loadDoc(file);
  const spec = win.WB_SPEC;

  check('WB_SPEC доступен', !!spec);
  const sections = doc.querySelectorAll('section.lec');
  eq('число разделов = число шагов в WB_SPEC', sections.length, spec.steps.length);
  eq('число пунктов оглавления', doc.querySelectorAll('#tocList li').length, spec.steps.length);
  check('первый раздел активен', doc.querySelector('section.lec').classList.contains('act'));
  check('оглавление содержит активный пункт', !!doc.querySelector('#tocList li.on'));
  check('нет незаполненных токенов шаблона', !/@@[A-Z_]+@@/.test(doc.documentElement.outerHTML));
  if (errors.length) console.log('  [ошибки консоли] ' + errors.slice(0, 4).join(' | '));
  eq('ошибок консоли при загрузке', errors.length, 0);

  /* --- навигация --- */
  win.location.hash = '#s3';
  win.dispatchEvent(new win.Event('hashchange'));
  check('переход к шагу s3', doc.getElementById('s3').classList.contains('act'));
  check('шаг s1 скрыт после перехода', !doc.getElementById('s1').classList.contains('act'));
  eq('счётчик разделов в нижней навигации', doc.querySelectorAll('.lecnav').length, sections.length);

  /* --- автосохранение полей --- */
  const ta = doc.getElementById('s1_week');
  check('поле s1_week существует', !!ta);
  ta.value = 'Она звонит каждый вечер в 21:00';
  fire(ta, 'input');
  let store = storeOf(win, spec.storageKey);
  eq('поле сохранено в localStorage', store['s1_week'], ta.value);
  check('появился индикатор «сохранено»',
    doc.querySelector('.sav[data-for="s1_week"]').classList.contains('visible'));
  check('счётчик заполнения обновлён', /заполнено: [1-9]/.test(doc.getElementById('counter').textContent));

  /* --- чекбоксы --- */
  const cb = doc.getElementById('s1_c3');
  cb.checked = true;
  fire(cb, 'change');
  store = storeOf(win, spec.storageKey);
  eq('чекбокс сохранён', store['s1_c3'], true);

  /* --- шкала --- */
  const rng = doc.getElementById('s1_scale_sep');
  rng.value = '7';
  fire(rng, 'input');
  store = storeOf(win, spec.storageKey);
  eq('шкала сохранена', store['s1_scale_sep'], '7');
  eq('output шкалы обновлён', doc.querySelector('output[data-for="s1_scale_sep"]').textContent, '7');

  /* --- матрица --- */
  const matrixBtn = doc.querySelector('[data-widget="sort_matrix"] .matrix-btn');
  matrixBtn.click();
  check('кнопка матрицы стала активной', matrixBtn.classList.contains('on'));
  store = storeOf(win, spec.storageKey);
  const matrixState = Object.values(store.__w).find((v) => v && typeof v === 'object' && v.mood);
  check('состояние матрицы записано', !!matrixState);

  /* --- когнитивная таблица --- */
  const ct = doc.querySelector('[data-widget="cog_table"]');
  const before = ct.querySelectorAll('.ctable-row').length;
  ct.querySelector('[data-act="add-row"]').click();
  eq('строка таблицы добавлена', ct.querySelectorAll('.ctable-row').length, before + 1);
  const cta = ct.querySelector('.ctable-col textarea');
  cta.value = 'Звонок в 21:00';
  fire(cta, 'input');
  store = storeOf(win, spec.storageKey);
  check('текст строки таблицы сохранён',
    JSON.stringify(store.__w).indexOf('Звонок в 21:00') >= 0);

  /* --- дневник --- */
  const dg = doc.querySelector('[data-widget="diary"]');
  dg.querySelector('[data-f="sit"]').value = 'Просила приехать в субботу';
  dg.querySelector('[data-f="body"]').value = 'Сжало челюсти';
  dg.querySelector('[data-act="add-entry"]').click();
  eq('запись дневника появилась', dg.querySelectorAll('.diary-item').length, 1);
  check('в записи есть текст', dg.querySelector('.diary-item').textContent.indexOf('Суббот') >= 0 ||
    dg.querySelector('.diary-item').textContent.indexOf('челюсти') >= 0);
  dg.querySelectorAll('.diary-item .btn-del')[0].click();
  eq('запись дневника удалена', dg.querySelectorAll('.diary-item').length, 0);

  /* --- круги близости --- */
  const ring = doc.querySelector('[data-widget="circles"] .ring');
  const ringInput = ring.querySelector('input');
  ringInput.value = 'Мама';
  ring.querySelector('button.btn').click();
  eq('имя добавлено в круг', ring.querySelectorAll('.ring-chip').length, 1);
  ring.querySelector('.ring-chip button').click();
  eq('имя убрано из круга', ring.querySelectorAll('.ring-chip').length, 0);

  /* --- карточки-разрешения --- */
  const pc = doc.querySelector('[data-widget="permission_cards"]');
  const presetCount = pc.querySelectorAll('.pcard').length;
  check('пресетные карточки отрисованы', presetCount >= 5);
  pc.querySelector('[data-role="new-card"]').value = 'Я имею право отдыхать';
  pc.querySelector('[data-act="add-card"]').click();
  eq('своя карточка добавлена', pc.querySelectorAll('.pcard-custom').length, 1);

  /* --- рейтинги зон --- */
  const rl = doc.querySelector('[data-widget="rating_list"] .rating-btn');
  rl.click();
  check('рейтинг зоны отмечен', rl.classList.contains('on'));

  /* --- диалоговый тренажёр --- */
  const dlg = doc.querySelector('[data-widget="dialog_trainer"]');
  if (dlg) {
    const opt = dlg.querySelector('.dlg-opt');
    opt.click();
    const target = dlg.querySelector('[data-role="target-field"]');
    check('фраза вставлена в скрипт разговора', target.value.length > 5);
    store = storeOf(win, spec.storageKey);
    check('скрипт разговора сохранён', typeof store[target.id] === 'string' && store[target.id].length > 5);
  }

  /* --- дыхательный виджет --- */
  const br = doc.querySelector('[data-widget="breather"]');
  if (br) {
    br.querySelector('[data-act="start"]').click();
    const circle = br.querySelector('.breather-circle');
    check('дыхание запустилось (круг в фазе вдоха)', circle.className.indexOf('inhale') >= 0);
    check('длительность фазы вдоха выставлена в transition',
      (circle.style.transitionDuration || '').indexOf('4s') === 0, circle.style.transitionDuration);
    br.querySelector('[data-act="pause"]').click();
    check('дыхание остановлено',
      br.querySelector('.breather-circle').className.indexOf('inhale') < 0);
  }

  /* --- блоки глубины и печать --- */
  const details = doc.querySelectorAll('details.deeper');
  check('есть блоки глубины', details.length >= 3);
  const closedBefore = [].filter.call(details, (d) => !d.open).length;
  win.dispatchEvent(new win.Event('beforeprint'));
  const openAfterPrint = [].filter.call(details, (d) => d.open).length;
  eq('печать раскрывает все блоки глубины', openAfterPrint, details.length);
  win.dispatchEvent(new win.Event('afterprint'));
  eq('после печати состояние восстановлено',
    [].filter.call(details, (d) => !d.open).length, closedBefore);

  /* --- темы --- */
  const themeBefore = doc.documentElement.getAttribute('data-theme');
  doc.getElementById('themeToggle').click();
  check('тема переключается', doc.documentElement.getAttribute('data-theme') !== themeBefore);
  check('тема сохранена', !!win.localStorage.getItem(spec.themeKey));

  /* --- сводка «Моя карта» --- */
  win.location.hash = '#map';
  win.dispatchEvent(new win.Event('hashchange'));
  const mapHtml = doc.getElementById('mapStats').innerHTML;
  check('сводка показывает прогресс по шагам', mapHtml.indexOf('Прогресс') >= 0 && mapHtml.indexOf('map-bar') >= 0);
  check('в сводке учтено заполненное поле', mapHtml.indexOf('полей:') >= 0);

  /* --- экспорт --- */
  let captured = null;
  win.URL.createObjectURL = (b) => { captured = b; return 'blob:test'; };
  win.URL.revokeObjectURL = () => {};
  doc.getElementById('btnExport').click();
  check('экспорт создал Blob', !!captured);
  if (captured) {
    const text = await new Promise((resolve, reject) => {
      const fr = new win.FileReader();
      fr.onload = () => resolve(String(fr.result));
      fr.onerror = () => reject(new Error('FileReader не прочитал Blob'));
      fr.readAsText(captured);
    });
    check('в отчёте есть заголовок', text.indexOf(spec.exportTitle) >= 0);
    check('в отчёте есть раздел шага 1', text.indexOf('ШАГ 1') >= 0);
    check('в отчёте есть ответ клиента', text.indexOf('Она звонит каждый вечер в 21:00') >= 0);
    check('в отчёте есть чек-лист с отметкой', /\[✓\]/.test(text));
    check('в отчёте есть значение шкалы', /Насколько я чувствую себя отдельным.*: 7/.test(text));
    check('в отчёте есть метка блока «Для встречи»', text.indexOf('★ ДЛЯ ВСТРЕЧИ') >= 0);
    check('в отчёте есть метка блока глубины', text.indexOf('[ПОЛНЫЙ ФОРМАТ]') >= 0 || text.indexOf('[ИЗ ДЕТСТВА]') >= 0);
    check('в отчёте есть разбор матрицы', text.indexOf('Моё настроение после нашего разговора') >= 0 ||
      text.indexOf('Моё решение') >= 0 || text.indexOf('Переплетено') >= 0);
  }

  /* --- восстановление при «перезагрузке» --- */
  const saved = win.localStorage.getItem(spec.storageKey);
  win.close();
  const { win: win3, doc: doc3 } = await loadDocWithStorage(file, spec.storageKey, saved);
  eq('после перезагрузки поле восстановлено', doc3.getElementById('s1_week').value, 'Она звонит каждый вечер в 21:00');
  eq('после перезагрузки чекбокс восстановлен', doc3.getElementById('s1_c3').checked, true);
  eq('после перезагрузки шкала восстановлена', doc3.getElementById('s1_scale_sep').value, '7');
  win3.close();

  check('нет ошибок рантайма за всё время теста', errors.length === 0, errors.slice(0, 3).join(' | '));
}

/** Загружает тетрадь, предварительно положив данные в localStorage (имитация повторного открытия). */
async function loadDocWithStorage(file, key, saved) {
  const html = fs.readFileSync(file, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    url: 'https://localhost/workbook.html',
    beforeParse(window) { stubBrowserApis(window); window.localStorage.setItem(key, saved); },
  });
  await new Promise((r) => setTimeout(r, 60));
  return { win: dom.window, doc: dom.window.document };
}

(async function main() {
  const targets = process.argv.slice(2).length ? process.argv.slice(2) : DEFAULT_TARGETS;
  for (const t of targets) {
    try { await testWorkbook(path.resolve(t)); }
    catch (e) { failures.push(path.basename(t) + ': исключение в тесте — ' + (e && e.stack || e)); }
  }
  console.log('\n-----------------------------');
  console.log('Проверок пройдено: ' + passed);
  if (failures.length) {
    console.log('Провалено: ' + failures.length);
    failures.forEach((f) => console.log('  ✗ ' + f));
    process.exit(1);
  }
  console.log('Все проверки пройдены ✓');
})();
