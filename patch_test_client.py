import pathlib

p = pathlib.Path("test_couple_workbook_2_one_quarrel.js")
s = p.read_text(encoding="utf-8")

# 1. Кнопка возвращения — главная
old = """  check('«Продолжить» появляется и ведёт на последнюю страницу',
    rbtn.classList.contains('show') && rbtn.getAttribute('data-page') === resumeTarget);
  check('В кнопке названа страница', /Если ваш круг другой/.test(rbtn.textContent));
"""
new = """  const rstart = resumed.document.querySelector('.btn-cover-start');
  check('«Продолжить» появляется и ведёт на последнюю страницу',
    rbtn.classList.contains('show') && rbtn.getAttribute('data-page') === resumeTarget);
  check('В кнопке названа страница', /Если ваш круг другой/.test(rbtn.textContent));
  check('Возвращение стоит выше «Начать»', rbtn.nextElementSibling === rstart);
  check('«Начать» уходит на второй план',
    rstart.classList.contains('is-secondary') && rstart.textContent.trim() === 'Начать с начала');
  check('Без истории «Начать» снова главная',
    fdoc.querySelector('.btn-cover-start').textContent.trim() === 'Начать' &&
      !fdoc.querySelector('.btn-cover-start').classList.contains('is-secondary'));
"""
assert old in s
s = s.replace(old, new, 1)

# 2. Счётчик: ноль не показывается
old2 = """  check('Счётчик записей стартует с нуля',
    fdoc.getElementById('progressLine').textContent.trim() === 'Записей пока нет');
  fdoc.getElementById('q2_my_request').value = 'Когда я говорю «мне всё равно»...';
  fresh.saveEntry('q2_my_request');
  check('Счётчик растёт после записи',
    fdoc.getElementById('progressLine').textContent.includes('1 из 8'),
    fdoc.getElementById('progressLine').textContent);
  check('Точки прогресса отмечают сделанное',
    fdoc.querySelectorAll('#progressDots .progress-dot.done').length === 1);
"""
new2 = """  check('Пустой счётчик не показывается',
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
"""
assert old2 in s
s = s.replace(old2, new2, 1)

# 3. Новые содержательные блоки
anchor = "  const toc = byTitle('Содержание');"
add = """  check('На обложке обещаны разговоры, а не встречи',
    /два разговора по 30 минут/.test(doc.querySelector('.cover-meta').textContent));
  check('Введение объясняет слово «партнёр»',
    /это муж, жену или того/.test(doc.querySelector('.partner-note')?.textContent || ''));
  check('Правил стало четыре',
    doc.querySelectorAll('#p2 .rules-list li, #p2 .key-list li').length >= 4 &&
      /Четыре правила/.test(doc.getElementById('p2').textContent));

  const thirty = byTitle('Тридцать минут');
  check('Сказано, что делать с детьми',
    /Если дома дети/.test(thirty.textContent));
  check('Сказано, что делать, если партнёр не хочет',
    /Если партнёр не хочет/.test(byTitle('Первый разговор').textContent));

  check('В содержании подсказка про страницу 4',
    /можно прочитать первой/.test(toc.textContent));

"""
assert anchor in s
s = s.replace(anchor, add + anchor, 1)

p.write_text(s, encoding="utf-8")
print("tests patched")
