// Проверка блоков записи в тетради «Пары: деэскалация ссор».
// Запуск:  npm install jsdom --no-save && node test_workbook_entry_blocks.js
//
// Что проверяем:
//   1. Разметку: 7 отдельных блоков записи, уникальные id, лампочка и подсказка в каждом.
//   2. Логику saveEntry(): запись добавляется в список, поле очищается, записи накапливаются.
//   3. Сохранение: записи и черновики переживают перезагрузку страницы.
//   4. Навигацию по страницам.

const { JSDOM } = require('jsdom');
const fs = require('fs');

const PATH = 'therapy-workbooks/couple_workbook_1_stop_escalation.html';
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

// jsdom дочитывает документ асинхронно — ждём полной загрузки,
// иначе обработчик DOMContentLoaded ещё не успел восстановить записи.
const ready = dom =>
  new Promise(resolve => {
    if (dom.window.document.readyState === 'complete') return resolve();
    dom.window.addEventListener('load', () => resolve());
  });

const open = async (seed = {}) => {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://workbook.test/',
    beforeParse(win) {
      // localStorage доступен только после создания окна, до разбора скриптов
      Object.keys(seed).forEach(key => win.localStorage.setItem(key, seed[key]));
    },
  });
  await ready(dom);
  return dom.window;
};

(async () => {
  // ── 1. Разметка ──────────────────────────────────────────────────────────
  console.log('— Разметка —');
  const win = await open();
  const doc = win.document;
  const blocks = [...doc.querySelectorAll('.entry-block')];

  check('7 блоков записи', blocks.length === 7, `получено ${blocks.length}`);

  const ids = blocks.map(block => block.querySelector('textarea').id);
  check('Все id уникальны', new Set(ids).size === ids.length, ids.join(', '));
  check('У каждого блока есть список записей', blocks.every(b => b.querySelector('.entry-list')));
  check('У каждого блока есть кнопка сохранения', blocks.every(b => b.querySelector('.btn-save-entry')));
  check('У каждого блока есть лампочка-подсказка', blocks.every(b => b.querySelector('.entry-lamp svg')));
  check(
    'У каждого блока есть текст подсказки',
    blocks.every(b => (b.querySelector('.entry-hint')?.textContent.trim().length || 0) > 10)
  );
  check('Блоки записи оформлены отдельно, не вложены в карточку',
    blocks.every(b => !b.closest('.interactive-card')));
  check('Перед каждым блоком стоит карточка-вопрос',
    blocks.every(b => b.previousElementSibling?.classList.contains('interactive-card')));
  check('Все блоки внутри своей страницы', blocks.every(b => b.closest('.page-card')));
  check('Страниц ровно 7', doc.querySelectorAll('.page-card').length === 7);
  check('У каждой страницы есть навигация',
    [...doc.querySelectorAll('.page-card')].every(p => p.querySelector('.page-footer-nav')));

  // ── 2. Логика saveEntry() ────────────────────────────────────────────────
  console.log('— Логика сохранения записи —');
  ids.forEach((id, index) => {
    const textarea = doc.getElementById(id);
    const list = doc.getElementById(`list_${id}`);

    textarea.value = `  Запись номер ${index + 1}  `;
    win.saveEntry(id);

    const items = list.querySelectorAll('.entry-item');
    check(
      `${id}: запись добавлена, поле очищено`,
      items.length === 1 &&
        textarea.value === '' &&
        items[0].textContent === `Запись номер ${index + 1}` &&
        !list.querySelector('.entry-empty'),
      `count=${items.length}, value="${textarea.value}", text="${items[0]?.textContent}"`
    );

    textarea.value = 'Вторая запись';
    win.saveEntry(id);
    check(`${id}: записи накапливаются`, list.querySelectorAll('.entry-item').length === 2);
    check(`${id}: запись вставлена без даты и времени`,
      !/\d{1,2}[.:]\d{2}|\d{4}/.test(items[0].textContent));
  });

  const emptyList = doc.getElementById(`list_${ids[0]}`);
  doc.getElementById(ids[0]).value = '     ';
  win.saveEntry(ids[0]);
  check('Пустой ввод не создаёт запись', emptyList.querySelectorAll('.entry-item').length === 2);

  // ── 3. Сохранение между перезагрузками ───────────────────────────────────
  console.log('— Сохранение на устройстве —');
  const field = 'q_body_signals';
  const first = await open();
  first.document.getElementById(field).value = 'Сжимаются челюсти';
  first.saveEntry(field);
  first.document.getElementById(field).value = 'Перехватывает дыхание';
  first.saveEntry(field);
  // Черновик сохраняется по событию input — имитируем реальный ввод
  const draft = first.document.getElementById('q_sos_note');
  draft.value = 'недописанная мысль';
  draft.dispatchEvent(new first.Event('input'));

  const store = {};
  for (let i = 0; i < first.localStorage.length; i++) {
    const key = first.localStorage.key(i);
    store[key] = first.localStorage.getItem(key);
  }
  check('Записи записаны в localStorage', !!store[`wb_couples_l1_entries_${field}`]);

  const second = await open(store);
  const doc2 = second.document;
  const restored = doc2.querySelectorAll(`#list_${field} .entry-item`);
  check('Записи восстановлены после перезагрузки', restored.length === 2, `получено ${restored.length}`);
  check(
    'Текст записей сохранён',
    restored[0]?.textContent === 'Сжимаются челюсти' &&
      restored[1]?.textContent === 'Перехватывает дыхание',
    [...restored].map(item => item.textContent).join(' | ')
  );
  check('Плашка «записей нет» убрана', !doc2.querySelector(`#list_${field} .entry-empty`));
  check('Другие блоки остались пустыми',
    doc2.querySelectorAll('#list_q_gratitude .entry-item').length === 0 &&
      !!doc2.querySelector('#list_q_gratitude .entry-empty'));
  check('Черновик восстановлен',
    doc2.getElementById('q_sos_note').value === 'недописанная мысль');

  // ── 4. Навигация ─────────────────────────────────────────────────────────
  console.log('— Навигация —');
  check('Функция goToPage существует', typeof win.goToPage === 'function');
  win.goToPage('p4');
  check('Активна ровно одна страница', doc.querySelectorAll('.page-card.active').length === 1);
  check('Активна именно p4', doc.getElementById('p4').classList.contains('active'));

  // ── 5. Оформление ────────────────────────────────────────────────────────
  console.log('— Оформление —');
  const text = doc.body.textContent;
  check('Нет эмодзи в тексте тетради', !/[\u{1F300}-\u{1FAFF}]/u.test(text));
  check('Нет символов табуляции', !text.includes('\t'));
  const images = [...doc.querySelectorAll('img')];
  check('Все изображения встроены в файл', images.every(img => img.src.startsWith('data:image')));
  check('У всех изображений есть описание', images.every(img => img.alt && img.alt.length > 3));

  console.log(`\nИтог: ${pass} прошло, ${fail} не прошло`);
  process.exit(fail ? 1 : 0);
})();
