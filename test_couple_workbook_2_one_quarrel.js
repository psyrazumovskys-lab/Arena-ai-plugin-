// Проверка второй тетради — «Одна и та же ссора».
// Запуск:  npm install jsdom --no-save && node test_couple_workbook_2_one_quarrel.js
//
// Что проверяем:
//   1. Структуру: 18 экранов (обложка + 17 страниц), 8 блоков записи.
//   2. Книжную вёрстку: бегущая строка, колонцифра «Стр. N из 17», картинки
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

  const byTitle = (fragment) =>
    pages.find(p => (p.querySelector('h1')?.textContent || '').includes(fragment));

  // ── 1. Структура ─────────────────────────────────────────────────────────
  console.log('— Структура —');
  check('18 экранов: обложка и 17 страниц', pages.length === 18, `получено ${pages.length}`);
  check(
    'Страницы идут по порядку p0…p17',
    pages.map(p => p.id).join(',') === Array.from({ length: 18 }, (_, i) => `p${i}`).join(',')
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
  check('Двадцать пять коротких строк', lines.length === 25, `получено ${lines.length}`);
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
      b.querySelector('.line-label') || b.querySelector('.line-prompt') || b.closest('.start-steps')));

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
  const noWriting = ['p0', byTitle('Содержание').id, byTitle('Если в ссоре есть страх').id];
  const pagesWithWriting = pages.filter(p =>
    !noWriting.includes(p.id) && p.querySelector('.entry-block, .line-block, .tick-list'));
  check('Везде, кроме обложки и страницы безопасности, есть где писать',
    pagesWithWriting.length === pages.length - noWriting.length,
    `без письма: ${pages.length - noWriting.length - pagesWithWriting.length}`);
  check('На странице безопасности нет заданий',
    !byTitle('Если в ссоре есть страх').querySelector('.entry-block, .line-field, .tick-list'));

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

  const p8 = byTitle('Упрёк и просьба');
  const p6Entry = p8.querySelector('.entry-block');
  const p6Check = p8.querySelector('.tick-list');
  check('Проверка просьбы стоит после записи',
    !!p6Entry && !!p6Check &&
    p6Entry.compareDocumentPosition(p6Check) === 4 /* FOLLOWING */);

  // ── 2-Б. Контекст, роли и безопасность ───────────────────────────────────
  console.log('— Контекст, роли и безопасность —');

  const safety = byTitle('Если в ссоре есть страх');
  check('Страница безопасности стоит сразу после введения',
    safety.querySelector('h1').textContent.trim() === 'Если в ссоре есть страх');
  check('На странице безопасности есть стоп-фраза',
    !!safety.querySelector('.stop-box'));
  check('На странице безопасности сказано про 112',
    safety.textContent.includes('112'));
  check('На странице безопасности сказано про алкоголь',
    /алкогол|выпил|трезв/i.test(safety.textContent));
  check('Страница безопасности предупреждает, что упражнения могут навредить',
    /могут сделать хуже/i.test(safety.textContent));

  const circle = byTitle('Круг, в который вы попадаете');
  check('Роль не назначается: на схеме «ОДИН» и «ДРУГОЙ»',
    circle.querySelector('svg').textContent.includes('ОДИН') &&
    circle.querySelector('svg').textContent.includes('ДРУГОЙ') &&
    !circle.querySelector('svg').textContent.includes('ВЫ') &&
    !circle.querySelector('svg').textContent.includes('ПАРТНЁР'));
  check('Сказано, что роль зависит от темы',
    /зависит не от характера, а от темы/.test(circle.textContent));

  const other = byTitle('Если ваш круг другой');
  check('Есть страница про другие круги', other.querySelector('h1').textContent.includes('круг другой'));
  check('Показаны три круга', other.querySelectorAll('.num-list > li').length === 3);
  check('Можно отметить свой круг', other.querySelectorAll('input[data-tick="pC_which"]').length === 4);
  check('Про 74% сказано, что это не российская выборка',
    /не российская выборка/.test(other.textContent));

  const why = byTitle('Почему она возвращается');
  check('Есть российские цифры о браках и разводах',
    /880 тысяч/.test(why.textContent) && /644 тысячи/.test(why.textContent));

  const protocol = byTitle('Тридцать минут');
  check('В протоколе есть трезвость',
    protocol.textContent.includes('Оба трезвые'));
  check('Сказано, что про третьих — через себя',
    /Про третьих — только через себя/.test(protocol.textContent));

  const request = byTitle('Упрёк и просьба');
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
  check('Колонцифры идут по порядку: «Стр. N из 17»',
    pages.slice(1).every((p, i) =>
      p.querySelector('.folio-page').textContent.trim() === `Стр. ${i + 1} из 17`));
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
  check('Часть II открывается титульным блоком', !!byTitle('Первый разговор').querySelector('.part-head'));

  // ── 4. Навигация ─────────────────────────────────────────────────────────
  console.log('— Навигация —');
  check('Кнопка «Начать» ведёт на #p1',
    doc.querySelector('.btn-cover-start')?.getAttribute('href') === '#p1');
  check('На каждой странице по две кнопки перехода',
    pages.slice(1).every(p => p.querySelectorAll('.page-footer-nav .btn-nav-step').length === 2));
  check('Последняя кнопка всегда ведёт в начало тетради',
    pages[pages.length - 1].querySelector('.page-footer-nav .btn-nav-step.primary')?.getAttribute('href') === '#p0');
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
  win.goToPage('p10');
  check('Активна ровно одна страница', doc.querySelectorAll('.page-card.active').length === 1);
  check('Активна именно p10', doc.getElementById('p10').classList.contains('active'));
  win.goToPage('p0');
  check('На обложке прячется верхняя панель', doc.body.classList.contains('on-cover'));
  win.goToPage('p5');
  check('Со страницы верхняя панель возвращается', !doc.body.classList.contains('on-cover'));

  const css = html.match(/<style>([\s\S]*?)<\/style>/)[1];

  // ── 7-А. Возврат, прогресс, короткий путь ─────────────────────────────
  console.log('— Возврат и прогресс —');

  const fresh = await open();
  const fdoc = fresh.document;
  check('На обложке есть кнопка «Продолжить»', !!fdoc.getElementById('resumeBtn'));
  check('Без истории «Продолжить» скрыта',
    !fdoc.getElementById('resumeBtn').classList.contains('show'));

  const resumeTarget = byTitle('Если ваш круг другой').id;
  const resumed = await open({ 'wb_couples_l2_one_quarrel_last_page': resumeTarget });
  const rbtn = resumed.document.getElementById('resumeBtn');
  const rstart = resumed.document.querySelector('.btn-cover-start');
  check('«Продолжить» появляется и ведёт на последнюю страницу',
    rbtn.classList.contains('show') && rbtn.getAttribute('data-page') === resumeTarget);
  check('В кнопке названа страница', /Если ваш круг другой/.test(rbtn.textContent));
  check('Возвращение стоит выше «Начать»', rbtn.nextElementSibling === rstart);
  check('«Начать» уходит на второй план',
    rstart.classList.contains('is-secondary') && rstart.textContent.trim() === 'Начать с начала');
  check('Без истории «Начать» снова главная',
    fdoc.querySelector('.btn-cover-start').textContent.trim() === 'Начать' &&
      !fdoc.querySelector('.btn-cover-start').classList.contains('is-secondary'));

  win.goToPage('p6');
  check('Страница запоминается при переходе',
    win.localStorage.getItem('wb_couples_l2_one_quarrel_last_page') === 'p6');
  win.goToPage('p0');
  check('Обложка не запоминается',
    win.localStorage.getItem('wb_couples_l2_one_quarrel_last_page') === 'p6');

  check('Пустой счётчик не показывается',
    fdoc.getElementById('progressLine').style.display === 'none' &&
      fdoc.getElementById('progressDots').style.display === 'none');
  fdoc.getElementById('q2_my_request').value = 'Когда я говорю «мне всё равно»...';
  fresh.saveEntry('q2_my_request');
  check('Счётчик появляется после первой записи',
    fdoc.getElementById('progressLine').style.display !== 'none');
  check('Счётчик считает от сделанного, а не от оставшегося',
    fdoc.getElementById('progressLine').textContent.includes('Вы уже написали 1 из 8'),
    fdoc.getElementById('progressLine').textContent);
  check('Точки прогресса отмечают сделанное',
    fdoc.querySelectorAll('#progressDots .progress-dot.done').length === 1);

  const startPage = byTitle('Если у вас 15 минут');
  check('Первая страница — короткий путь',
    startPage.querySelector('h1').textContent.includes('15 минут'));
  check('На коротком пути три вопроса с местом для ответа',
    ['l_start_name', 'l_start_step', 'l_start_request']
      .every(id => !!startPage.querySelector('#' + id)));
  check('Короткий путь отправляет к главам',
    startPage.querySelectorAll('.start-where').length === 3);

  check('На обложке обещаны разговоры, а не встречи',
    /два разговора по 30 минут/.test(doc.querySelector('.cover-meta').textContent));
  check('Объяснено слово «партнёр»',
    /значит мужа, жену или того/.test(doc.querySelector('.partner-note')?.textContent || ''));
  check('Правила умещаются в одну фразу на первой странице',
    /Читайте в спокойное время/.test(doc.getElementById('p1').textContent) &&
      !doc.querySelector('#p1 .checklist'));

  const thirty = byTitle('Тридцать минут');
  check('Сказано, что делать с детьми',
    /Если дома дети/.test(thirty.textContent));
  check('Сказано, что делать, если партнёр не хочет',
    /Если партнёр не хочет/.test(byTitle('Первый разговор').textContent));

  check('В содержании подсказка про страницу 4',
    /можно прочитать первой/.test(byTitle('Содержание').textContent));

  const toc = byTitle('Содержание');
  const tocRows = [...toc.querySelectorAll('.contents-list li[data-target]')];
  check('Есть страница содержания', !!toc);
  check('В содержании все главы, кроме обложки и самого содержания',
    tocRows.length === pages.length - 2, `строк ${tocRows.length}`);
  check('У каждой строки есть номер страницы',
    tocRows.every(li => /^\d+$/.test(li.querySelector('.toc-page').textContent.trim())));
  check('Номера в содержании совпадают с колонцифрами',
    tocRows.every(li => {
      const target = doc.getElementById(li.dataset.target);
      const folio = target.querySelector('.folio-page').textContent.match(/\d+/)[0];
      return li.querySelector('.toc-page').textContent.trim() === folio;
    }));
  check('В содержании сказано, сколько времени занимает глава',
    tocRows.every(li => /\d+\s*мин/.test(li.querySelector('.toc-min').textContent)));
  check('Парные главы помечены «вдвоём»',
    tocRows.filter(li => /вдвоём/.test(li.textContent)).length === 2);

  const month = byTitle('Вернитесь через месяц');
  check('Последняя страница — возвращение через месяц',
    month.querySelector('h1').textContent.includes('месяц'));
  check('Через месяц три вопроса',
    ['l_month_alive', 'l_month_dead', 'l_month_new']
      .every(id => !!month.querySelector('#' + id)));
  check('Есть памятка на одну страницу', month.querySelectorAll('.memo li').length === 6);
  check('Записи можно скачать', typeof win.downloadEntries === 'function');
  check('Записи можно стереть', typeof win.clearAllData === 'function');
  check('Кнопки стоят рядом', month.querySelectorAll('.tools-row .tool-btn').length === 2);
  check('Сказано, что записи не уходят в сеть',
    /только в этом браузере/i.test(month.textContent));

  // ── 7-Б. Печать ───────────────────────────────────────────────────────
  const printCss = (css.match(/@media print\s*\{[\s\S]*?\n    \}/) || [''])[0];
  check('Есть правила для печати', printCss.length > 0);
  check('При печати видны все страницы',
    /\.page-card\s*\{[^}]*display:\s*block/.test(printCss));
  check('При печати прячутся кнопки',
    /\.wb-navigation-bar|\.page-footer-nav/.test(printCss) && /display:\s*none/.test(printCss));
  check('Строки для письма печатаются по 7 мм', /7mm/.test(printCss));

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

  // Печатный набор идёт отдельным блоком в конце стилей — проверяем его.
  const edition = css.slice(css.indexOf('ПЕЧАТНОЕ ИЗДАНИЕ'));

  check('Кнопки перехода не ниже 48 px',
    /\.btn-nav-step,[\s\S]{0,400}?min-height:\s*48px/.test(edition));
  check('Лист без рамки и тени, как страница книги',
    /\.page-card\s*\{[\s\S]{0,200}?box-shadow:\s*none/.test(edition) &&
    /\.page-card\s*\{[\s\S]{0,200}?background:\s*transparent/.test(edition));
  check('Иллюстрации врезаются ровно в поля листа',
    /padding:\s*0 22px 96px/.test(edition) &&
    /\.figure-bleed\s*\{[\s\S]{0,120}?margin:\s*24px -22px/.test(edition));
  check('Есть стиль буквицы', /\.dropcap::first-letter/.test(css));
  check('Поле записи — линованная бумага, а не рамка',
    /\.journal-entry\s*\{[\s\S]{0,400}?repeating-linear-gradient/.test(edition));
  check('Подписи набраны PT Sans',
    (edition.match(/font-family:\s*"PT Sans"/g) || []).length >= 10);
  check('Номер страницы стоит по центру', /\.folio\s*\{[\s\S]{0,120}?justify-content:\s*center/.test(edition));
  check('Шрифты вложены в файл', (html.match(/@font-face/g) || []).length >= 8 && !/fonts\.googleapis/.test(html));

  console.log(`\nИтог: ${pass} прошло, ${fail} не прошло`);
  process.exit(fail ? 1 : 0);
})();
