// Проверка второй тетради — «Одна и та же ссора».
// Запуск:  npm install jsdom --no-save && node test_couple_workbook_2_one_quarrel.js
//
// Что проверяем:
//   1. Структуру: 16 экранов (обложка + 15 страниц), 8 блоков записи.
//   2. Книжную вёрстку: бегущая строка, колонцифра «Стр. N из 15», картинки
//      в тексте, а не только сверху.
//   2-А. Точки письма: 8 больших записей, короткие строки без кнопки и списки с отметками.
//   2-Б. Контекст и роли: страница безопасности, другие круги, трезвость, российские цифры.
//   3. Логику saveEntry(): запись добавляется, поле очищается, записи копятся.
//   4. Сохранение: записи и черновики переживают перезагрузку.
//   5. Язык: нет запрещённых формулировок и терминов.

const { JSDOM } = require('jsdom');
const fs = require('fs');

const PATH = 'therapy-workbooks/couple_workbook_2_one_quarrel.html';
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
  const pages = [...doc.querySelectorAll('.page-card')];
  const blocks = [...doc.querySelectorAll('.entry-block')];

  // ── 1. Структура ─────────────────────────────────────────────────────────
  console.log('— Структура —');
  check('16 экранов: обложка и 15 страниц', pages.length === 16, `получено ${pages.length}`);
  check(
    'Страницы идут по порядку p0…p15',
    pages.map(p => p.id).join(',') === Array.from({ length: 16 }, (_, i) => `p${i}`).join(',')
  );
  check('8 блоков записи', blocks.length === 8, `получено ${blocks.length}`);
  check('Обложка — отдельная поверхность', doc.getElementById('p0').classList.contains('cover-card'));
  check('Без JavaScript обложка активна', doc.getElementById('p0').classList.contains('active'));

  // ── 2. Блоки записи ──────────────────────────────────────────────────────
  console.log('— Блоки записи —');
  const ids = blocks.map(b => b.querySelector('textarea').id);
  check('Все id уникальны', new Set(ids).size === ids.length, ids.join(', '));
  check('Все id начинаются с q2_', ids.every(id => /^q2_[a-z_]+$/.test(id)), ids.join(', '));
  check('У каждого блока есть метка типа задания', blocks.every(b => b.querySelector('.entry-kind')));
  check('Метки только «Индивидуально» и «Вместе с партнёром»',
    blocks.every(b => /Индивидуально|Вместе с партнёром/.test(b.querySelector('.entry-kind').textContent)));
  check('Парная метка одна — у договора',
    blocks.filter(b => b.querySelector('.entry-kind.kind-pair')).length === 1 &&
    blocks.filter(b => b.querySelector('.entry-kind.kind-pair'))[0].querySelector('textarea').id === 'q2_our_agreement');
  check('У каждого блока есть список записей', blocks.every(b => b.querySelector('.entry-list')));
  check('У каждого блока есть кнопка сохранения', blocks.every(b => b.querySelector('.btn-save-entry')));
  check('У каждого блока есть лампочка-подсказка', blocks.every(b => b.querySelector('.entry-lamp svg')));
  check('У каждого блока есть текст подсказки',
    blocks.every(b => (b.querySelector('.entry-hint')?.textContent.trim().length || 0) > 15));
  check('Блоки записи не вложены в карточку',
    blocks.every(b => !b.closest('.interactive-card')));
  check('Перед каждым блоком стоит карточка-вопрос',
    blocks.every(b => b.previousElementSibling?.classList.contains('interactive-card')));
  check('У каждого вопроса есть номер записи',
    blocks.every(b => /^Запись \d$/.test(b.previousElementSibling.querySelector('.ask-num')?.textContent.trim() || '')));
  check('Номера записей идут подряд',
    blocks.map(b => +b.previousElementSibling.querySelector('.ask-num').textContent.replace(/\D/g, ''))
      .every((n, i) => n === i + 1));
  check('Пустой список показывает подсказку',
    blocks.every(b => !!b.querySelector('.entry-empty')));

  // ── 2-А. Короткие строки и отметки ───────────────────────────────────────
  console.log('— Короткие строки и отметки —');
  const lines = [...doc.querySelectorAll('.line-field')];
  check('Двадцать коротких строк', lines.length === 20, `получено ${lines.length}`);
  check('У каждой строки свой id', new Set(lines.map(l => l.id)).size === lines.length);
  check('Строки не пересекаются с большими записями',
    lines.every(l => !ids.includes(l.id)));
  check('У каждой строки есть вопрос или начало фразы',
    lines.every(l => (l.getAttribute('placeholder') || '').length > 6));
  check('Короткие строки без кнопки сохранения',
    [...doc.querySelectorAll('.line-block')].every(b => !b.querySelector('.btn-save-entry')));
  check('Короткие строки не оформлены как большие записи',
    [...doc.querySelectorAll('.line-block')].every(b => !b.classList.contains('entry-block')));
  check('У коротких строк есть подпись блока или вопрос',
    [...doc.querySelectorAll('.line-block')].every(b =>
      b.querySelector('.line-label') || b.querySelector('.line-prompt')));

  const ticks = [...doc.querySelectorAll('.tick-item input[type=checkbox]')];
  const groups = [...new Set(ticks.map(t => t.getAttribute('data-tick')))];
  check('Пять списков с отметками', groups.length === 5, groups.join(', '));
  check('Отметок всего двадцать шесть', ticks.length === 26, `получено ${ticks.length}`);
  check('У каждой отметки есть подпись рядом',
    [...doc.querySelectorAll('.tick-item')].every(t => t.textContent.trim().length > 8));
  check('У каждой отметки свой номер внутри списка',
    groups.every(g => {
      const vals = ticks.filter(t => t.getAttribute('data-tick') === g).map(t => t.value);
      return new Set(vals).size === vals.length;
    }));

  // Плотность: писать есть где везде, кроме обложки и страницы безопасности
  const noWriting = ['p0', 'p2'];
  const pagesWithWriting = pages.filter(p =>
    !noWriting.includes(p.id) && p.querySelector('.entry-block, .line-block, .tick-list'));
  check('Везде, кроме обложки и страницы безопасности, есть где писать',
    pagesWithWriting.length === pages.length - noWriting.length,
    `без письма: ${pages.length - noWriting.length - pagesWithWriting.length}`);
  check('На странице безопасности нет заданий',
    !doc.querySelector('#p2 .entry-block, #p2 .line-field, #p2 .tick-list'));

  // Вопрос, обращённый к читателю, не остаётся без места для ответа
  const askItems = [...doc.querySelectorAll('.ask-list > li')];
  check('Пять вопросов — у каждого своя строка',
    askItems.length === 5 && askItems.every(li => li.querySelector('.line-field')));
  check('Строка стоит под вопросом, а не отдельно',
    askItems.every(li => {
      const q = li.querySelector('.ask-q');
      return q && q.nextElementSibling &&
        q.nextElementSibling.classList.contains('line-field');
    }));
  check('Ответы на пять вопросов — отдельные ключи',
    new Set(askItems.map(li => li.querySelector('.line-field').id)).size === 5);

  const p8 = doc.getElementById('p8');
  const p6Entry = p8.querySelector('.entry-block');
  const p6Check = p8.querySelector('.tick-list');
  check('Проверка просьбы стоит после записи',
    !!p6Entry && !!p6Check &&
    p6Entry.compareDocumentPosition(p6Check) === 4 /* FOLLOWING */);

  // ── 2-Б. Контекст, роли и безопасность ───────────────────────────────────
  console.log('— Контекст, роли и безопасность —');

  const safety = doc.getElementById('p2');
  check('Страница безопасности стоит сразу после введения',
    safety.querySelector('h1').textContent.trim() === 'Если это не ссора');
  check('На странице безопасности есть стоп-фраза',
    !!safety.querySelector('.stop-box'));
  check('На странице безопасности сказано про 112',
    safety.textContent.includes('112'));
  check('На странице безопасности сказано про алкоголь',
    /алкогол|выпил|трезв/i.test(safety.textContent));
  check('Страница безопасности предупреждает, что упражнения могут навредить',
    /могут сделать хуже/i.test(safety.textContent));

  const circle = doc.getElementById('p5');
  check('Роль не назначается: на схеме «ОДИН» и «ДРУГОЙ»',
    circle.querySelector('svg').textContent.includes('ОДИН') &&
    circle.querySelector('svg').textContent.includes('ДРУГОЙ') &&
    !circle.querySelector('svg').textContent.includes('ВЫ') &&
    !circle.querySelector('svg').textContent.includes('ПАРТНЁР'));
  check('Сказано, что роль зависит от темы',
    /зависит не от характера, а от темы/.test(circle.textContent));

  const other = doc.getElementById('p6');
  check('Есть страница про другие круги', other.querySelector('h1').textContent.includes('круг другой'));
  check('Показаны три круга', other.querySelectorAll('.num-list > li').length === 3);
  check('Можно отметить свой круг', other.querySelectorAll('input[data-tick="pC_which"]').length === 4);
  check('Про 74% сказано, что это не российская выборка',
    /не российская выборка/.test(other.textContent));

  const why = doc.getElementById('p4');
  check('Есть российские цифры о браках и разводах',
    /880 тысяч/.test(why.textContent) && /644 тысячи/.test(why.textContent));

  const protocol = doc.getElementById('p9');
  check('В протоколе есть трезвость',
    protocol.textContent.includes('Оба трезвые'));
  check('Сказано, что про третьих — через себя',
    /Про третьих — только через себя/.test(protocol.textContent));

  const request = doc.getElementById('p8');
  check('Честно сказано, что форма просьбы решает не всё',
    /дело уже не в словах/.test(request.textContent));

  check('Цепочка переходов непрерывна',
    pages.slice(1, -1).every((p, i) =>
      p.querySelector('.btn-nav-step.primary').getAttribute('href') === '#' + pages[i + 2].id &&
      p.querySelector('.btn-nav-step.back').getAttribute('href') === '#' + pages[i].id));

  // ── 3. Книжная вёрстка ───────────────────────────────────────────────────
  console.log('— Книжная вёрстка —');
  check('На каждой странице есть бегущая строка',
    pages.slice(1).every(p => !!p.querySelector('.running-head')));
  check('На обложке бегущей строки нет', !doc.querySelector('#p0 .running-head'));
  check('У каждой страницы есть колонцифра',
    pages.slice(1).every(p => !!p.querySelector('.folio-page')));
  check('Колонцифры идут по порядку: «Стр. N из 15»',
    pages.slice(1).every((p, i) =>
      p.querySelector('.folio-page').textContent.trim() === `Стр. ${i + 1} из 15`));
  check('На обложке нет колонцифры', !doc.querySelector('#p0 .folio'));

  const figures = [...doc.querySelectorAll('figure')];
  check('Шесть иллюстраций', figures.length === 6, `получено ${figures.length}`);
  check('У каждой иллюстрации есть подпись',
    figures.every(f => (f.querySelector('figcaption')?.textContent.trim().length || 0) > 10));
  check('Иллюстрации не только сверху: минимум три стоят посреди текста',
    figures.filter(f => f.previousElementSibling?.tagName === 'P').length >= 3,
    `посреди текста: ${figures.filter(f => f.previousElementSibling?.tagName === 'P').length}`);
  check('Есть буквица', doc.querySelectorAll('.dropcap').length >= 10);
  check('Есть врезки на полях', doc.querySelectorAll('.margin-note').length >= 5);
  check('Есть разворот «до/после» с двумя колонками',
    doc.querySelectorAll('.compare').length >= 3);
  check('Есть протокол на 30 минут', doc.querySelectorAll('.protocol-step').length === 5);
  check('В протоколе пять отрезков времени по порядку',
    [...doc.querySelectorAll('.protocol-step .protocol-time')].map(el => el.textContent.replace(/\s|мин/g, '')).join('|')
      === '0–3|3–12|12–21|21–27|27–30');
  check('Часть II открывается титульным блоком', !!doc.querySelector('#p11 .part-head'));

  // ── 4. Навигация ─────────────────────────────────────────────────────────
  console.log('— Навигация —');
  check('Кнопка «Начать» ведёт на #p1',
    doc.querySelector('.btn-cover-start')?.getAttribute('href') === '#p1');
  check('На каждой странице по две кнопки перехода',
    pages.slice(1).every(p => p.querySelectorAll('.page-footer-nav .btn-nav-step').length === 2));
  check('Последняя кнопка всегда ведёт в начало тетради',
    doc.querySelector('#p15 .page-footer-nav .btn-nav-step.primary')?.getAttribute('href') === '#p0');
  check('Все кнопки перехода — ссылки с onclick',
    [...doc.querySelectorAll('.btn-nav-step')].every(a =>
      a.tagName === 'A' && a.getAttribute('href')?.startsWith('#p') && /goToPage/.test(a.getAttribute('onclick') || '')));

  // ── 5. Логика saveEntry() ────────────────────────────────────────────────
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
      `count=${items.length}, value="${textarea.value}"`
    );

    textarea.value = 'Вторая запись';
    win.saveEntry(id);
    check(`${id}: записи накапливаются`, list.querySelectorAll('.entry-item').length === 2);
  });

  const firstId = ids[0];
  doc.getElementById(firstId).value = '     ';
  win.saveEntry(firstId);
  check('Пустой ввод не создаёт запись',
    doc.querySelectorAll(`#list_${firstId} .entry-item`).length === 2);

  // ── 6. Сохранение между перезагрузками ───────────────────────────────────
  console.log('— Сохранение на устройстве —');
  const field = 'q2_my_circle';
  const first = await open();
  first.document.getElementById(field).value = 'Я начинаю с вопросов';
  first.saveEntry(field);
  first.document.getElementById(field).value = 'Партнёр замолкает';
  first.saveEntry(field);
  const draft = first.document.getElementById('q2_our_agreement');
  draft.value = 'недописанный договор';
  draft.dispatchEvent(new first.Event('input'));

  const store = {};
  for (let i = 0; i < first.localStorage.length; i++) {
    const key = first.localStorage.key(i);
    store[key] = first.localStorage.getItem(key);
  }
  check('Записи записаны в localStorage', !!store[`wb_couples_l2_one_quarrel_entries_${field}`]);

  const second = await open(store);
  const doc2 = second.document;
  const restored = doc2.querySelectorAll(`#list_${field} .entry-item`);
  check('Записи восстановлены после перезагрузки', restored.length === 2, `получено ${restored.length}`);
  check('Текст записей сохранён',
    restored[0]?.textContent === 'Я начинаю с вопросов' &&
      restored[1]?.textContent === 'Партнёр замолкает');
  check('Черновик восстановлен',
    doc2.getElementById('q2_our_agreement').value === 'недописанный договор');

  // ── 6-А. Короткие строки и отметки переживают перезагрузку ───────────────
  console.log('— Короткие строки сохраняются сами —');
  const third = await open();
  const line = third.document.getElementById('l11_noticed');
  line.value = 'Начинаю с вопросов, партнёр замолкает';
  line.dispatchEvent(new third.Event('input'));
  const tick = third.document.querySelector('input[data-tick="p2_signs"][value="3"]');
  tick.checked = true;
  tick.dispatchEvent(new third.Event('change'));

  const store2 = {};
  for (let i = 0; i < third.localStorage.length; i++) {
    const key = third.localStorage.key(i);
    store2[key] = third.localStorage.getItem(key);
  }
  check('Строка записана без кнопки', !!store2['wb_couples_l2_one_quarrel_line_l11_noticed']);
  check('Отметка записана', store2['wb_couples_l2_one_quarrel_tick_p2_signs_3'] === '1');

  const fourth = await open(store2);
  check('Строка восстановлена',
    fourth.document.getElementById('l11_noticed').value === 'Начинаю с вопросов, партнёр замолкает');
  check('Отметка восстановлена',
    fourth.document.querySelector('input[data-tick="p2_signs"][value="3"]').checked === true);
  check('Соседние отметки остались пустыми',
    fourth.document.querySelector('input[data-tick="p2_signs"][value="4"]').checked === false);
  check('Пустая строка в том же блоке не помечена',
    !fourth.document.getElementById('l11_helped').classList.contains('is-written'));
  check('Заполненная строка помечена, соседние — нет',
    fourth.document.getElementById('l11_noticed').classList.contains('is-written'));

  // ── 7. Навигация в работе ────────────────────────────────────────────────
  console.log('— Переходы —');
  win.goToPage('p9');
  check('Активна ровно одна страница', doc.querySelectorAll('.page-card.active').length === 1);
  check('Активна именно p9', doc.getElementById('p9').classList.contains('active'));
  win.goToPage('p0');
  check('На обложке прячется верхняя панель', doc.body.classList.contains('on-cover'));
  win.goToPage('p4');
  check('Со страницы верхняя панель возвращается', !doc.body.classList.contains('on-cover'));

  // ── 8. Язык и оформление ─────────────────────────────────────────────────
  console.log('— Язык и оформление —');
  const text = doc.body.textContent;
  check('Нет эмодзи', !/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(text));
  check('Нет символов табуляции', !text.includes('\t'));

  const banned = [
    'деэскалац', 'саморегуляц', 'соматич', 'имаго', 'всадник',
    'прямо сейчас', 'в момент злости', 'в момент сильного гнева',
    'когда начинаете закипать', 'оцените напряжение сейчас',
    'если партнёр пока не готов',
  ];
  const lower = text.toLowerCase();
  const found = banned.filter(word => lower.includes(word));
  check('Нет запрещённых слов и формулировок', found.length === 0, found.join(', '));

  const images = [...doc.querySelectorAll('img')];
  check('Все изображения встроены в файл', images.every(img => img.src.startsWith('data:image')));
  check('У всех изображений есть описание', images.every(img => img.alt && img.alt.length > 10));
  check('Все иллюстрации стоят внутри figure (кроме обложки)',
    images.every(img => img.closest('figure') || img.classList.contains('cover-image')));
  check('Нет внешних скриптов', !/<script[^>]+src=/.test(html));

  const css = html.match(/<style>([\s\S]*?)<\/style>/)[1];
  check('Кнопки перехода не ниже 48 px', /\.btn-nav-step\s*\{[^}]*min-height:\s*48px/.test(css));
  check('Иллюстрации врезаются в поля страницы', /\.figure-bleed\s*\{[^}]*margin:[^;]*-22px/.test(css));
  check('Есть стиль буквицы', /\.dropcap::first-letter/.test(css));

  console.log(`\nИтог: ${pass} прошло, ${fail} не прошло`);
  process.exit(fail ? 1 : 0);
})();
