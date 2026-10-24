// Проверка второй тетради — «14 дней бережного диалога» (уровень 2).
// Запуск:  npm install jsdom --no-save && node test_couple_workbook_2.js
//
// Что проверяем:
//   1. Структуру: 17 экранов, 14 дней, у каждого дня свой блок записи.
//   2. Разметку блоков: метка «Индивидуально» / «Вместе с партнёром», лампочка,
//      подсказка, кнопка, список записей.
//   3. Логику saveEntry(): запись добавляется, поле очищается, записи копятся.
//   4. Сохранение: записи и черновики переживают перезагрузку.
//   5. Язык: нет запрещённых формулировок и терминов, нет дат в записях.

const { JSDOM } = require('jsdom');
const fs = require('fs');

const PATH = 'therapy-workbooks/couple_workbook_2_gentle_dialogue.html';
const html = fs.readFileSync(PATH, 'utf8');

let pass = 0;
let fail = 0;

const check = (name, cond, extra = '') => {
  if (cond) {
    pass++;
    console.log(`  \u2713 ${name}`);
  } else {
    fail++;
    console.log(`  \u2717 ${name} ${extra}`);
  }
};

const ready = dom =>
  new Promise(resolve => {
    if (dom.window.document.readyState === 'complete') return resolve();
    dom.window.addEventListener('load', () => resolve());
  });

const open = async (seed = {}) => {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://workbook2.test/',
    beforeParse(win) {
      Object.keys(seed).forEach(key => win.localStorage.setItem(key, seed[key]));
    },
  });
  await ready(dom);
  return dom.window;
};

(async () => {
  const win = await open();
  const doc = win.document;
  const blocks = [...doc.querySelectorAll('.entry-block')];

  // ── 1. Структура ─────────────────────────────────────────────────────────
  console.log('— Структура —');
  check('17 экранов', doc.querySelectorAll('.page-card').length === 17,
    `получено ${doc.querySelectorAll('.page-card').length}`);
  check('14 блоков записи', blocks.length === 14, `получено ${blocks.length}`);

  const dayPages = [...doc.querySelectorAll('.page-card')].filter(p =>
    /^День \d+ из 14/.test(p.querySelector('.badge-label')?.textContent || ''));
  check('14 страниц-дней', dayPages.length === 14, `получено ${dayPages.length}`);
  check('Номера дней идут подряд с 1 по 14',
    dayPages.map(p => +/День (\d+) из 14/.exec(p.querySelector('.badge-label').textContent)[1])
      .every((n, i) => n === i + 1));
  check('На каждом дне ровно один блок записи',
    dayPages.every(p => p.querySelectorAll('.entry-block').length === 1));
  check('Ни на одном дне нет блока без записи',
    dayPages.every(p => p.querySelector('textarea.journal-entry')));

  // ── 2. Разметка блоков ───────────────────────────────────────────────────
  console.log('— Разметка блоков —');
  const ids = blocks.map(b => b.querySelector('textarea').id);
  check('Все id уникальны', new Set(ids).size === ids.length, ids.join(', '));
  check('id начинаются с q2_d', ids.every(id => /^q2_d\d{2}$/.test(id)));
  check('У каждого блока есть список записей', blocks.every(b => b.querySelector('.entry-list')));
  check('У каждого блока есть кнопка сохранения', blocks.every(b => b.querySelector('.btn-save-entry')));
  check('У каждого блока есть лампочка-подсказка', blocks.every(b => b.querySelector('.entry-lamp svg')));
  check('У каждого блока есть текст подсказки',
    blocks.every(b => (b.querySelector('.entry-hint')?.textContent.trim().length || 0) > 15));
  check('У каждого блока есть видимый заголовок-вопрос',
    blocks.every(b => {
      const card = b.previousElementSibling;
      return card && card.classList.contains('interactive-card') &&
        card.classList.contains('card-title-only') &&
        card.querySelector('h3')?.textContent.trim().length > 5;
    }));
  check('Блоки записи не вложены в карточку',
    blocks.every(b => !b.closest('.interactive-card')));

  const kinds = blocks.map(b => b.querySelector('.entry-kind span').textContent.trim());
  check('У каждого блока есть метка типа',
    kinds.every(k => k === 'Индивидуально' || k === 'Вместе с партнёром'));
  const pairs = kinds.filter(k => k === 'Вместе с партнёром').length;
  check('Парных блоков пять (дни 8–11, 13)', pairs === 5, `получено ${pairs}`);
  check('Личных блоков девять', kinds.filter(k => k === 'Индивидуально').length === 9);

  // ── 3. Навигация ─────────────────────────────────────────────────────────
  console.log('— Навигация —');
  const coverBtn = doc.querySelector('.btn-cover-start');
  check('Кнопка «Начать» ведёт на вступление (#p1)',
    coverBtn && coverBtn.getAttribute('href') === '#p1');
  const firstBack = [...doc.querySelectorAll('#p1 .btn-nav-step')]
    .find(a => /Назад/.test(a.textContent));
  check('Со вступления можно вернуться на обложку',
    firstBack && firstBack.getAttribute('href') === '#p0');
  const backToStart = [...doc.querySelectorAll('.btn-nav-step')]
    .find(a => /В начало тетради/.test(a.textContent));
  check('Кнопка «В начало тетради» ведёт на #p0',
    backToStart && backToStart.getAttribute('href') === '#p0');
  check('Все переходы — ссылки с onclick (работают без JavaScript)',
    [...doc.querySelectorAll('.btn-nav-step, .btn-cover-start')].every(a =>
      a.tagName === 'A' && /^#p\d+$/.test(a.getAttribute('href') || '') &&
      /goToPage/.test(a.getAttribute('onclick') || '')));
  check('В списке выбора 17 пунктов',
    doc.querySelectorAll('#pageSelect option').length === 17);

  // ── 4. Логика saveEntry() ────────────────────────────────────────────────
  console.log('— Логика сохранения записи —');
  ids.forEach((id, index) => {
    const textarea = doc.getElementById(id);
    const list = doc.getElementById(`list_${id}`);
    textarea.value = `  Запись номер ${index + 1}  `;
    win.saveEntry(id);
    const items = list.querySelectorAll('.entry-item');
    check(`${id}: запись добавлена, поле очищено`,
      items.length === 1 && textarea.value === '' &&
        items[0].textContent === `Запись номер ${index + 1}` &&
        !list.querySelector('.entry-empty'),
      `count=${items.length}, value="${textarea.value}"`);
    textarea.value = 'Вторая запись';
    win.saveEntry(id);
    check(`${id}: записи накапливаются`, list.querySelectorAll('.entry-item').length === 2);
    check(`${id}: в записи нет даты и времени`,
      !/\d{1,2}[.:]\d{2}|\d{4}/.test(items[0].textContent));
  });

  const firstId = ids[0];
  doc.getElementById(firstId).value = '     ';
  win.saveEntry(firstId);
  check('Пустой ввод не создаёт запись',
    doc.querySelectorAll(`#list_${firstId} .entry-item`).length === 2);

  // ── 5. Сохранение между перезагрузками ───────────────────────────────────
  console.log('— Сохранение на устройстве —');
  const field = 'q2_d08';
  const first = await open();
  first.document.getElementById(field).value = 'Через полчаса, с фразы «я вернулся»';
  first.saveEntry(field);
  first.document.getElementById(field).value = 'После прогулки';
  first.saveEntry(field);
  const draft = first.document.getElementById('q2_d05');
  draft.value = 'недописанная мысль';
  draft.dispatchEvent(new first.Event('input'));

  const store = {};
  for (let i = 0; i < first.localStorage.length; i++) {
    const key = first.localStorage.key(i);
    store[key] = first.localStorage.getItem(key);
  }
  check('Записи лежат под своим ключом второй тетради',
    !!store[`wb_couples_l2_entries_${field}`]);
  check('Ключи первой тетради не затронуты',
    !Object.keys(store).some(k => k.startsWith('wb_couples_l1_')));

  const second = await open(store);
  const doc2 = second.document;
  const restored = doc2.querySelectorAll(`#list_${field} .entry-item`);
  check('Записи восстановлены после перезагрузки', restored.length === 2, `получено ${restored.length}`);
  check('Текст записей сохранён',
    restored[0]?.textContent === 'Через полчаса, с фразы «я вернулся»' &&
      restored[1]?.textContent === 'После прогулки');
  check('Плашка «записей нет» убрана', !doc2.querySelector(`#list_${field} .entry-empty`));
  check('Другие блоки остались пустыми',
    doc2.querySelectorAll('#list_q2_d12 .entry-item').length === 0);
  check('Черновик восстановлен', doc2.getElementById('q2_d05').value === 'недописанная мысль');

  // ── 6. Переключение страниц ──────────────────────────────────────────────
  console.log('— Переключение страниц —');
  check('Функция goToPage существует', typeof win.goToPage === 'function');
  win.goToPage('p9');
  check('Активна ровно одна страница', doc.querySelectorAll('.page-card.active').length === 1);
  check('Активна именно p9', doc.getElementById('p9').classList.contains('active'));

  // ── 7. Язык и оформление ─────────────────────────────────────────────────
  console.log('— Язык и оформление —');
  const text = doc.body.textContent;
  const banned = [
    'прямо сейчас', 'в момент злости', 'в момент сильного гнева',
    'когда начинаете закипать', 'деэскалац', 'саморегуляц', 'соматич',
    'имаго', 'всадник',
  ];
  banned.forEach(word => check(`Нет формулировки «${word}»`,
    !text.toLowerCase().includes(word)));
  check('Нет эмодзи', !/[\u{1F300}-\u{1FAFF}]/u.test(text));
  check('Есть строка про безопасность', !!doc.querySelector('.safety-note'));
  check('Есть блок возврата после паузы', !!doc.querySelector('.return-box'));
  check('Есть сноска для случая «партнёр не готов»', !!doc.querySelector('.fallback-note'));

  const images = [...doc.querySelectorAll('img')];
  check('Все изображения встроены в файл', images.length > 0 && images.every(img => img.src.startsWith('data:image')));
  check('У всех изображений есть описание', images.every(img => img.alt && img.alt.length > 3));

  const words = text.split(/\s+/).filter(Boolean).length;
  check('Объём в разумных пределах (2500–6000 слов)', words > 2500 && words < 6000, `слов: ${words}`);

  console.log(`\nИтог: ${pass} прошло, ${fail} не прошло`);
  process.exit(fail ? 1 : 0);
})();
