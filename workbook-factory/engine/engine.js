/* ==========================================================================
   WORKBOOK ENGINE · engine.js
   Универсальный рантайм терапевтической тетради.
   Читает window.WB_SPEC ( injecting сборщиком ) и разметку data-*.
   Возможности:
     · навигация по шагам (drawer-меню, поиск, ←/→, M, хэш)
     · темы light / dark / auto
     · автосохранение всех полей, чекбоксов и шкал в localStorage
     · счётчик заполнения + экран «Моя карта» с прогрессом по шагам
     · реестр интерактивных механик (виджетов) с собственным состоянием
     · экспорт ответов текстовым файлом (.txt) для психолога
     · подготовка к печати (раскрытие блоков глубины)
   ========================================================================== */
(function () {
  'use strict';

  var SPEC = window.WB_SPEC || {};
  var STEPS = SPEC.steps || [];
  var ORDER = STEPS.map(function (s) { return s.id; });

  /* ------------------------------------------------------------------ */
  /* 0. Хранилище                                                        */
  /* ------------------------------------------------------------------ */
  var KEY = SPEC.storageKey || 'workbook-v1';
  var THEME_KEY = SPEC.themeKey || (KEY + '-theme');
  var store = {};
  try { store = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { store = {}; }
  if (!store.__w) store.__w = {};

  function saveAll() {
    try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) { /* приватный режим */ }
  }

  function plural(n, one, few, many) {
    var m10 = n % 10, m100 = n % 100;
    if (m10 === 1 && m100 !== 11) return one;
    if (m10 >= 2 && m10 <= 4 && (m100 < 10 || m100 >= 20)) return few;
    return many;
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function nowStamp() {
    var d = new Date();
    return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: '2-digit' }) + ' ' +
      d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  }

  /* ------------------------------------------------------------------ */
  /* 1. Навигация по шагам                                               */
  /* ------------------------------------------------------------------ */
  var secs = [].slice.call(document.querySelectorAll('section.lec'));
  var items = [].slice.call(document.querySelectorAll('#tocList li'));
  var counter = document.getElementById('counter');

  function stepTitle(id) {
    for (var i = 0; i < STEPS; i++) { if (STEPS[i].id === id) return STEPS[i].name; }
    var li = items.filter(function (x) { return x.getAttribute('data-t') === id; })[0];
    return li ? li.textContent.trim() : id;
  }

  function buildNavs() {
    secs.forEach(function (s, idx) {
      if (s.querySelector('.lecnav')) return;
      var d = document.createElement('div');
      d.className = 'lecnav';
      var h = '';
      var prev = ORDER[idx - 1], next = ORDER[idx + 1];
      if (prev) h += '<a href="#' + prev + '">← ' + esc(stepTitle(prev)) + '</a>';
      h += '<span class="cnt">' + (idx + 1) + ' / ' + ORDER.length + '</span>';
      if (next) h += '<a href="#' + next + '">' + esc(stepTitle(next)) + ' →</a>';
      d.innerHTML = h;
      s.appendChild(d);
    });
  }

  function answeredCount() {
    return [].slice.call(document.querySelectorAll('.qf')).filter(function (t) {
      return String(t.value || '').trim() !== '';
    }).length;
  }

  function updateCounter() {
    if (!counter) return;
    counter.textContent = 'заполнено: ' + answeredCount() + ' / ' + document.querySelectorAll('.qf').length;
  }

  function show(id) {
    if (ORDER.indexOf(id) < 0) id = ORDER[0];
    secs.forEach(function (s) { s.classList.toggle('act', s.id === id); });
    items.forEach(function (li) { li.classList.toggle('on', li.getAttribute('data-t') === id); });
    updateCounter();
    window.scrollTo(0, 0);
    var cb = document.getElementById('menu');
    if (cb) cb.checked = false;
    if (id === 'map') renderMap();
  }

  function move(delta) {
    var cur = secs.filter(function (s) { return s.classList.contains('act'); })[0];
    var idx = cur ? ORDER.indexOf(cur.id) : 0;
    var next = ORDER[Math.min(Math.max(idx + delta, 0), ORDER.length - 1)];
    if (next) location.hash = '#' + next;
  }

  window.addEventListener('hashchange', function () { show(location.hash.slice(1) || ORDER[0]); });

  var q = document.getElementById('q');
  if (q) q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase();
    items.forEach(function (li) {
      li.classList.toggle('hide', !!v && li.textContent.toLowerCase().indexOf(v) < 0);
    });
  });

  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t && (t.tagName === 'TEXTAREA' || t.tagName === 'INPUT' || t.tagName === 'SELECT')) return;
    if (e.key === 'm' || e.key === 'M' || e.key === 'ь' || e.key === 'Ь') {
      var m = document.getElementById('menu');
      if (m) m.checked = !m.checked;
    } else if (e.key === 'ArrowRight') { move(1); }
    else if (e.key === 'ArrowLeft') { move(-1); }
  });

  /* ------------------------------------------------------------------ */
  /* 2. Темы                                                             */
  /* ------------------------------------------------------------------ */
  var themeBtn = document.getElementById('themeToggle');
  var savedTheme = localStorage.getItem(THEME_KEY) || 'auto';
  document.documentElement.setAttribute('data-theme', savedTheme);
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : (cur === 'light' ? 'auto' : 'dark');
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem(THEME_KEY, next);
    themeBtn.title = 'Тема: ' + next;
  });

  /* ------------------------------------------------------------------ */
  /* 3. Поля, чекбоксы, шкалы                                            */
  /* ------------------------------------------------------------------ */
  var fields = [].slice.call(document.querySelectorAll('.qf'));
  var checks = [].slice.call(document.querySelectorAll('.chk-card input[type=checkbox]'));
  var ranges = [].slice.call(document.querySelectorAll('input.rng'));

  function flashSaved(id) {
    var s = document.querySelector('.sav[data-for="' + id + '"]');
    if (!s) return;
    s.classList.add('visible');
    setTimeout(function () { s.classList.remove('visible'); }, 1800);
  }

  fields.forEach(function (f) {
    if (!f.id) return;
    if (typeof store[f.id] === 'string') f.value = store[f.id];
    f.addEventListener('input', function () {
      store[f.id] = f.value;
      saveAll(); updateCounter(); flashSaved(f.id);
    });
  });

  checks.forEach(function (c) {
    if (!c.id) return;
    if (store[c.id] === true) c.checked = true;
    c.addEventListener('change', function () {
      store[c.id] = c.checked; saveAll(); updateCounter();
    });
  });

  ranges.forEach(function (r) {
    var out = document.querySelector('output[data-for="' + r.id + '"]');
    function sync() { if (out) out.textContent = r.value; }
    if (typeof store[r.id] !== 'undefined') { r.value = store[r.id]; }
    sync();
    r.addEventListener('input', function () {
      store[r.id] = r.value; saveAll(); sync(); flashSaved(r.id); updateCounter();
    });
  });

  /* ------------------------------------------------------------------ */
  /* 4. Реестр механик (виджетов)                                        */
  /* ------------------------------------------------------------------ */
  var WB = { widgets: {} };
  WB.widget = function (type, impl) { WB.widgets[type] = impl; };

  function apiFor(el) {
    var wid = el.getAttribute('data-wid');
    var spec = {};
    try { spec = JSON.parse(el.getAttribute('data-spec') || '{}'); } catch (e) { spec = {}; }
    return {
      wid: wid,
      spec: spec,
      get: function () { return store.__w[wid]; },
      set: function (v) { store.__w[wid] = v; saveAll(); },
      state: function (fallback) {
        if (typeof store.__w[wid] === 'undefined') store.__w[wid] = fallback;
        return store.__w[wid];
      },
      el: el
    };
  }

  /* --- 4.1 Сортировочная матрица ------------------------------------ */
  WB.widget('sort_matrix', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({});
      var host = el.querySelector('.matrix');
      spec.items.forEach(function (item) {
        var row = document.createElement('div');
        row.className = 'matrix-row';
        row.setAttribute('data-item', item.id);
        var h = '<div class="matrix-item-label">' + esc(item.label) + '</div>' +
          (item.hint ? '<div class="matrix-item-hint">' + esc(item.hint) + '</div>' : '') +
          '<div class="matrix-choices">';
        spec.columns.forEach(function (c) {
          h += '<button type="button" class="matrix-btn" data-col="' + esc(c.key) + '">' + esc(c.label) + '</button>';
        });
        h += '<span class="matrix-chosen"></span></div>';
        row.innerHTML = h;
        host.appendChild(row);

        function paint() {
          var val = st[item.id];
          [].slice.call(row.querySelectorAll('.matrix-btn')).forEach(function (b) {
            b.classList.toggle('on', b.getAttribute('data-col') === val);
          });
          var chosen = row.querySelector('.matrix-chosen');
          var col = spec.columns.filter(function (c) { return c.key === val; })[0];
          chosen.textContent = val ? ('→ ' + col.label) : '';
        }
        [].slice.call(row.querySelectorAll('.matrix-btn')).forEach(function (b) {
          b.addEventListener('click', function () {
            var col = b.getAttribute('data-col');
            st[item.id] = (st[item.id] === col) ? null : col;
            api.set(st); paint();
          });
        });
        paint();
      });
    },
    exportLines: function (el, api) {
      var spec = api.spec, st = api.get() || {}, out = [];
      spec.items.forEach(function (item) {
        var col = spec.columns.filter(function (c) { return c.key === st[item.id]; })[0];
        out.push('  ' + item.label + ' — ' + (col ? col.label : 'не выбрано'));
      });
      return out;
    }
  });

  /* --- 4.2 Когнитивная таблица -------------------------------------- */
  WB.widget('cog_table', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({ rows: [] });
      if (!st.rows) st.rows = [];
      var host = el.querySelector('.ctable');
      var addBtn = el.querySelector('[data-act="add-row"]');

      function blank() {
        var r = {};
        spec.columns.forEach(function (c) { r[c.key || c.label] = ''; });
        return r;
      }
      function key(col) { return col.key || col.label; }

      function render() {
        host.innerHTML = '';
        if (!st.rows.length) {
          host.innerHTML = '<div class="diary-empty">Строк пока нет — добавьте первую ситуацию кнопкой ниже.</div>';
          return;
        }
        st.rows.forEach(function (row, idx) {
          var d = document.createElement('div');
          d.className = 'ctable-row';
          var h = '<div class="ctable-row-head"><span>Ситуация ' + (idx + 1) + '</span>' +
            '<button type="button" class="btn-del" data-act="del-row" data-idx="' + idx + '" title="Удалить строку">✕</button></div>' +
            '<div class="ctable-cols">';
          spec.columns.forEach(function (c) {
            h += '<div class="ctable-col"><label>' + esc(c.label) + '</label>' +
              '<textarea rows="2" data-col="' + esc(key(c)) + '" placeholder="' + esc(c.placeholder || '') + '">' +
              esc(row[key(c)] || '') + '</textarea></div>';
          });
          h += '</div>';
          d.innerHTML = h;
          host.appendChild(d);
          [].slice.call(d.querySelectorAll('textarea')).forEach(function (t) {
            t.addEventListener('input', function () {
              st.rows[idx][t.getAttribute('data-col')] = t.value;
              api.set(st);
            });
          });
        });
        [].slice.call(host.querySelectorAll('[data-act="del-row"]')).forEach(function (b) {
          b.addEventListener('click', function () {
            st.rows.splice(parseInt(b.getAttribute('data-idx'), 10), 1);
            api.set(st); render();
          });
        });
      }

      if (addBtn) addBtn.addEventListener('click', function () {
        var max = spec.max_rows || 12;
        if (st.rows.length >= max) { alert('Максимум строк: ' + max + '. Удалите лишние.'); return; }
        st.rows.push(blank()); api.set(st); render();
      });
      while (st.rows.length < (spec.rows || 1)) st.rows.push(blank());
      api.set(st);
      render();
    },
    exportLines: function (el, api) {
      var spec = api.spec, st = api.get() || { rows: [] }, out = [];
      function key(c) { return c.key || c.label; }
      (st.rows || []).forEach(function (row, i) {
        var filled = spec.columns.some(function (c) { return String(row[key(c)] || '').trim(); });
        if (!filled) return;
        out.push('  ' + (i + 1) + ') ' + spec.columns.map(function (c) {
          return c.label + ': ' + (String(row[key(c)] || '').trim() || '—');
        }).join(' | '));
      });
      return out;
    }
  });

  /* --- 4.3 Дневник повторяющихся записей ---------------------------- */
  WB.widget('diary', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({ entries: [] });
      if (!st.entries) st.entries = [];
      var list = el.querySelector('.diary-list');
      var countEl = el.querySelector('[data-role="count"]');
      var addBtn = el.querySelector('[data-act="add-entry"]');
      var formHost = el.querySelector('.diary-form-grid');

      spec.fields.forEach(function (f) {
        var w = document.createElement('div');
        var lab = '<label for="' + esc(api.wid + '_' + f.key) + '">' + esc(f.label) + '</label>';
        var ctl;
        if (f.options && f.options.length) {
          ctl = '<select id="' + esc(api.wid + '_' + f.key) + '" data-f="' + esc(f.key) + '">' +
            '<option value="">— выберите —</option>' +
            f.options.map(function (o) { return '<option>' + esc(o) + '</option>'; }).join('') + '</select>';
        } else if (f.kind === 'textarea') {
          ctl = '<textarea id="' + esc(api.wid + '_' + f.key) + '" data-f="' + esc(f.key) + '" rows="2" placeholder="' + esc(f.placeholder || '') + '"></textarea>';
        } else {
          ctl = '<input type="text" id="' + esc(api.wid + '_' + f.key) + '" data-f="' + esc(f.key) + '" placeholder="' + esc(f.placeholder || '') + '">';
        }
        w.innerHTML = lab + ctl;
        formHost.appendChild(w);
      });

      function fieldEl(k) { return formHost.querySelector('[data-f="' + k + '"]'); }

      (spec.quick || []).forEach(function (chip) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'chip'; b.textContent = chip.label || chip.value;
        b.addEventListener('click', function () {
          var el2 = fieldEl(chip.field);
          if (!el2) return;
          el2.value = chip.value; el2.focus();
        });
        el.querySelector('.chip-container').appendChild(b);
      });

      function render() {
        if (countEl) {
          countEl.textContent = st.entries.length + ' ' + plural(st.entries.length, 'запись', 'записи', 'записей');
        }
        if (!st.entries.length) {
          list.innerHTML = '<div class="diary-empty">' + esc(spec.empty || 'Записей пока нет. Добавьте первую — это занимает меньше минуты.') + '</div>';
          return;
        }
        list.innerHTML = '';
        st.entries.forEach(function (e, idx) {
          var d = document.createElement('div');
          d.className = 'diary-item';
          var head = '<div class="diary-item-header"><span>🕒 ' + esc(e.__time || '—') + '</span>' +
            '<span style="display:flex;align-items:center;gap:.5rem;">' +
            (e[spec.badge_field] ? '<span class="diary-badge">' + esc(spec.badge_label || '') + ' ' + esc(e[spec.badge_field]) + '</span>' : '') +
            '<button type="button" class="btn-del" data-idx="' + idx + '" title="Удалить запись">✕</button></span></div>';
          var body = spec.fields.map(function (f) {
            if (!e[f.key]) return '';
            var cls = f.kind === 'textarea' ? 'diary-item-line' : 'diary-item-line';
            return '<div class="' + cls + '"><b>' + esc(f.label) + ':</b> ' + esc(e[f.key]) + '</div>';
          }).join('');
          d.innerHTML = head + body;
          list.appendChild(d);
        });
        [].slice.call(list.querySelectorAll('.btn-del')).forEach(function (b) {
          b.addEventListener('click', function () {
            st.entries.splice(parseInt(b.getAttribute('data-idx'), 10), 1);
            api.set(st); render();
          });
        });
      }

      if (addBtn) addBtn.addEventListener('click', function () {
        var e = { __time: nowStamp() };
        var any = false;
        spec.fields.forEach(function (f) {
          var el2 = fieldEl(f.key);
          e[f.key] = el2 ? el2.value.trim() : '';
          if (e[f.key]) any = true;
        });
        if (!any) { alert('Заполните хотя бы одно поле записи.'); return; }
        st.entries.unshift(e); api.set(st); render();
        spec.fields.forEach(function (f) { var el2 = fieldEl(f.key); if (el2) el2.value = ''; });
      });

      render();
    },
    exportLines: function (el, api) {
      var spec = api.spec, st = api.get() || { entries: [] }, out = [];
      (st.entries || []).forEach(function (e, i) {
        out.push('  ' + (i + 1) + '. [' + (e.__time || '') + '] ' + spec.fields.map(function (f) {
          return f.label + ': ' + (e[f.key] || '—');
        }).join(' · '));
      });
      return out;
    }
  });

  /* --- 4.4 Круги близости ------------------------------------------- */
  WB.widget('circles', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({});
      var host = el.querySelector('.rings');
      spec.rings.forEach(function (ring) {
        if (!st[ring.key]) st[ring.key] = [];
        var d = document.createElement('div');
        d.className = 'ring';
        d.setAttribute('data-tone', ring.tone || 'middle');
        d.innerHTML = '<div class="ring-head">' + esc(ring.label) + '</div>' +
          (ring.hint ? '<div class="ring-hint">' + esc(ring.hint) + '</div>' : '') +
          '<div class="ring-input"><input type="text" placeholder="' + esc(ring.placeholder || 'Имя или роль…') + '">' +
          '<button type="button" class="btn btn-sm">Добавить</button></div>' +
          '<div class="ring-items"></div>';
        host.appendChild(d);

        var input = d.querySelector('input');
        var itemsHost = d.querySelector('.ring-items');

        function render() {
          itemsHost.innerHTML = '';
          if (!st[ring.key].length) {
            itemsHost.innerHTML = '<span class="ring-empty">пока пусто</span>';
            return;
          }
          st[ring.key].forEach(function (name, i) {
            var c = document.createElement('span');
            c.className = 'ring-chip';
            c.innerHTML = esc(name) + ' <button type="button" title="Убрать">✕</button>';
            c.querySelector('button').addEventListener('click', function () {
              st[ring.key].splice(i, 1); api.set(st); render();
            });
            itemsHost.appendChild(c);
          });
        }
        function add() {
          var v = input.value.trim();
          if (!v) return;
          st[ring.key].push(v); api.set(st); input.value = ''; render(); input.focus();
        }
        d.querySelector('button.btn').addEventListener('click', add);
        input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); add(); } });
        render();
      });
      api.set(st);
    },
    exportLines: function (el, api) {
      var spec = api.spec, st = api.get() || {}, out = [];
      spec.rings.forEach(function (r) {
        out.push('  ' + r.label + ': ' + ((st[r.key] || []).join(', ') || '—'));
      });
      return out;
    }
  });

  /* --- 4.5 Карточки-разрешения -------------------------------------- */
  WB.widget('permission_cards', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({ custom: [] });
      if (!st.custom) st.custom = [];
      var host = el.querySelector('.pcards');
      var input = el.querySelector('[data-role="new-card"]');
      var addBtn = el.querySelector('[data-act="add-card"]');

      function render() {
        host.innerHTML = '';
        (spec.preset || []).forEach(function (t) {
          var d = document.createElement('div');
          d.className = 'pcard';
          d.innerHTML = '<b>Разрешение</b><span>' + esc(t) + '</span>';
          host.appendChild(d);
        });
        st.custom.forEach(function (t, i) {
          var d = document.createElement('div');
          d.className = 'pcard pcard-custom';
          d.innerHTML = '<b>Моя формулировка</b><span>' + esc(t) + '</span>' +
            '<button type="button" class="btn-del pcard-del" data-idx="' + i + '" title="Удалить">✕</button>';
          host.appendChild(d);
        });
        [].slice.call(host.querySelectorAll('.pcard-del')).forEach(function (b) {
          b.addEventListener('click', function () {
            st.custom.splice(parseInt(b.getAttribute('data-idx'), 10), 1);
            api.set(st); render();
          });
        });
      }
      function add() {
        var v = input.value.trim();
        if (!v) return;
        st.custom.push(v); api.set(st); input.value = ''; render();
      }
      if (addBtn) addBtn.addEventListener('click', add);
      if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); add(); } });
      render();
    },
    exportLines: function (el, api) {
      var st = api.get() || { custom: [] };
      return (st.custom || []).map(function (t, i) { return '  ' + (i + 1) + '. ' + t; });
    }
  });

  /* --- 4.6 Диалоговый тренажёр -------------------------------------- */
  WB.widget('dialog_trainer', {
    mount: function (el, api) {
      var target = el.querySelector('[data-role="target-field"]');
      [].slice.call(el.querySelectorAll('.dlg-opt')).forEach(function (b) {
        b.addEventListener('click', function () {
          var text = b.getAttribute('data-text') || b.textContent.trim();
          if (!target) return;
          target.value = (target.value.trim() ? target.value.trim().replace(/\s+$/, '') + '\n' : '') + '— ' + text;
          target.dispatchEvent(new Event('input'));
          target.focus();
          target.scrollTop = target.scrollHeight;
        });
      });
    },
    exportLines: function () { return []; }
  });

  /* --- 4.7 Рейтинги зон (телесная карта и др.) ---------------------- */
  WB.widget('rating_list', {
    mount: function (el, api) {
      var spec = api.spec;
      var st = api.state({});
      var host = el.querySelector('.rating-list');
      spec.items.forEach(function (item) {
        var row = document.createElement('div');
        row.className = 'rating-row';
        var h = '<span class="rating-label">' + esc(item.label) + '</span><span class="rating-btns">';
        spec.levels.forEach(function (lv) {
          h += '<button type="button" class="rating-btn" data-v="' + esc(lv.value) + '" data-tone="' + esc(lv.tone || 'acc') + '">' + esc(lv.label) + '</button>';
        });
        h += '</span>';
        row.innerHTML = h;
        host.appendChild(row);
        function paint() {
          [].slice.call(row.querySelectorAll('.rating-btn')).forEach(function (b) {
            b.classList.toggle('on', String(st[item.id]) === b.getAttribute('data-v'));
          });
        }
        [].slice.call(row.querySelectorAll('.rating-btn')).forEach(function (b) {
          b.addEventListener('click', function () {
            var v = b.getAttribute('data-v');
            st[item.id] = (String(st[item.id]) === v) ? null : v;
            api.set(st); paint();
          });
        });
        paint();
      });
    },
    exportLines: function (el, api) {
      var spec = api.spec, st = api.get() || {}, out = [];
      spec.items.forEach(function (item) {
        var lv = spec.levels.filter(function (l) { return String(l.value) === String(st[item.id]); })[0];
        out.push('  ' + item.label + ' — ' + (lv ? lv.label : 'не отмечено'));
      });
      return out;
    }
  });

  /* --- 4.8 Дыхание и таймер паузы ----------------------------------- */
  WB.widget('breather', {
    mount: function (el, api) {
      var spec = api.spec;
      var inhale = spec.inhale || 4, hold = spec.hold || 2, exhale = spec.exhale || 6;
      var circle = el.querySelector('.breather-circle');
      var text = el.querySelector('.breather-text');
      var startBtn = el.querySelector('[data-act="start"]');
      var pauseBtn = el.querySelector('[data-act="pause"]');
      var resetBtn = el.querySelector('[data-act="reset"]');
      var display = el.querySelector('.timer-display');
      var totalMin = spec.countdown_minutes || 0;
      var left = totalMin * 60, timer = null, breath = null;

      function ui() {
        if (!display) return;
        var m = Math.floor(left / 60), s = left % 60;
        display.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
      }
      function stopBreath(msg) {
        if (breath) clearTimeout(breath);
        breath = null;
        if (circle) circle.className = 'breather-circle';
        if (text) text.textContent = msg || 'Дышите в своём ритме.';
      }
      function startBreath() {
        // фазы идут своими таймерами: вдох / задержка / выдох — ровно столько секунд, сколько задано
        var phases = [
          { cls: 'inhale', secs: inhale, text: 'Вдох через нос… (' + inhale + ' сек)' },
          { cls: 'hold', secs: hold, text: 'Мягкая задержка… (' + hold + ' сек)' },
          { cls: 'exhale', secs: exhale, text: 'Длинный плавный выдох… (' + exhale + ' сек)' }
        ].filter(function (p) { return p.secs > 0; });
        var i = 0;
        function cycle() {
          var p = phases[i % phases.length];
          circle.className = 'breather-circle ' + p.cls;
          circle.style.transitionDuration = p.secs + 's, 2s, ' + p.secs + 's';
          text.textContent = p.text;
          i++;
          breath = setTimeout(cycle, p.secs * 1000);
        }
        cycle();
      }
      ui();
      if (startBtn) startBtn.addEventListener('click', function () {
        if (timer) return;
        startBtn.style.display = 'none';
        if (pauseBtn) pauseBtn.style.display = 'inline-flex';
        startBreath();
        if (!totalMin) return;
        timer = setInterval(function () {
          if (left > 0) { left--; ui(); }
          else {
            clearInterval(timer); timer = null; stopBreath('🎉 Пауза выдержана. Острая волна спала.');
            startBtn.style.display = 'inline-flex';
            if (pauseBtn) pauseBtn.style.display = 'none';
          }
        }, 1000);
      });
      if (pauseBtn) pauseBtn.addEventListener('click', function () {
        if (timer) { clearInterval(timer); timer = null; }
        stopBreath('Пауза. Можно продолжить, когда будете готовы.');
        pauseBtn.style.display = 'none';
        if (startBtn) startBtn.style.display = 'inline-flex';
      });
      if (resetBtn) resetBtn.addEventListener('click', function () {
        if (timer) { clearInterval(timer); timer = null; }
        stopBreath('Нажмите «Начать», когда будете готовы.');
        left = totalMin * 60; ui();
        if (pauseBtn) pauseBtn.style.display = 'none';
        if (startBtn) startBtn.style.display = 'inline-flex';
      });
    },
    exportLines: function () { return []; }
  });

  /* Монтируем все виджеты на странице */
  [].slice.call(document.querySelectorAll('[data-widget]')).forEach(function (el) {
    var impl = WB.widgets[el.getAttribute('data-widget')];
    if (!impl) { if (window.console) console.warn('Неизвестная механика:', el.getAttribute('data-widget')); return; }
    try { impl.mount(el, apiFor(el)); } catch (err) { if (window.console) console.error(err); }
  });

  /* ------------------------------------------------------------------ */
  /* 5. Экран «Моя карта»: прогресс по шагам                             */
  /* ------------------------------------------------------------------ */
  function stepStats(stepId) {
    var root = document.getElementById(stepId);
    if (!root) return { filled: 0, total: 0, checks: 0, checksTotal: 0 };
    var fs = [].slice.call(root.querySelectorAll('.qf'));
    var cs = [].slice.call(root.querySelectorAll('.chk-card input[type=checkbox]'));
    return {
      filled: fs.filter(function (f) { return String(f.value || '').trim(); }).length,
      total: fs.length,
      checks: cs.filter(function (c) { return c.checked; }).length,
      checksTotal: cs.length
    };
  }

  function renderMap() {
    var host = document.getElementById('mapStats');
    if (!host) return;
    var html = '<h3 style="margin-top:0;">Прогресс по шагам</h3>', totF = 0, totA = 0;
    STEPS.forEach(function (s) {
      if (s.id === 'front' || s.id === 'map') return;
      var st = stepStats(s.id);
      totF += st.total; totA += st.filled;
      var pct = st.total ? Math.round(st.filled / st.total * 100) : 0;
      html += '<div class="map-row"><span><b>' + esc(s.name) + '</b>' +
        '<span class="map-bar" style="display:block;"><i style="width:' + pct + '%"></i></span></span>' +
        '<span>полей: ' + st.filled + '/' + st.total +
        (st.checksTotal ? ' · отметок: ' + st.checks + '/' + st.checksTotal : '') + '</span></div>';
    });
    html += '<div style="margin-top:1rem;font-size:.98rem;">Всего заполнено полей: <b>' + totA + '</b> из ' + totF + '</div>';
    host.innerHTML = html;
  }

  /* ------------------------------------------------------------------ */
  /* 6. Экспорт отчёта                                                   */
  /* ------------------------------------------------------------------ */
  function collectStep(stepId) {
    var root = document.getElementById(stepId);
    if (!root) return [];
    var lines = [];
    [].slice.call(root.querySelectorAll('[data-export]')).forEach(function (n) {
      var kind = n.getAttribute('data-export');
      var label = n.getAttribute('data-q') || '';
      if (kind === 'section') {
        lines.push('');
        lines.push('  ' + label.toUpperCase());
      } else if (kind === 'field') {
        if (n.classList.contains('rng')) { lines.push('• ' + label + ': ' + n.value); }
        else { lines.push('• ' + label + ':'); lines.push(String(n.value || '').trim() || '—'); }
      } else if (kind === 'checklist') {
        lines.push('• ' + label + ':');
        [].slice.call(n.querySelectorAll('input[type=checkbox]')).forEach(function (c) {
          var span = c.parentNode.querySelector('span');
          var text = span ? span.textContent.replace(/\s+/g, ' ').trim() : c.id;
          lines.push('   ' + (c.checked ? '[✓] ' : '[ ] ') + text);
        });
      } else if (kind === 'widget') {
        var impl = WB.widgets[n.getAttribute('data-widget')];
        if (!impl || !impl.exportLines) return;
        var sub = impl.exportLines(n, apiFor(n));
        if (sub && sub.length) { lines.push('• ' + label + ':'); lines = lines.concat(sub); }
      }
    });
    return lines;
  }

  function doExport() {
    var lines = [
      SPEC.exportTitle || 'ОТЧЁТ ПО РАБОЧЕЙ ТЕТРАДИ',
      'Дата экспорта: ' + new Date().toLocaleString('ru-RU'),
      'Устройство/браузер: ' + navigator.userAgent,
      '====================================================================',
      ''
    ];
    STEPS.forEach(function (s) {
      var body = collectStep(s.id);
      if (!body.length && s.id !== 'front') return;
      lines.push('─── ' + (s.exportName || s.name).toUpperCase() + ' ───');
      lines = lines.concat(body);
      lines.push('');
    });
    var blob = new Blob(['\ufeff' + lines.join('\n')], { type: 'text/plain;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = SPEC.exportFilename || 'otchet.txt';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
  }

  ['btnExport', 'btnExportTop'].forEach(function (id) {
    var b = document.getElementById(id);
    if (b) b.addEventListener('click', doExport);
  });
  var pb = document.getElementById('btnPrint');
  if (pb) pb.addEventListener('click', function () { window.print(); });

  var clr = document.getElementById('btnClear');
  if (clr) clr.addEventListener('click', function () {
    if (!confirm('Стереть ВСЕ записи этой тетради на данном устройстве? Действие необратимо.')) return;
    store = { __w: {} };
    saveAll();
    fields.forEach(function (f) { f.value = ''; });
    checks.forEach(function (c) { c.checked = false; });
    ranges.forEach(function (r) {
      r.value = r.min || 0;
      var out = document.querySelector('output[data-for="' + r.id + '"]');
      if (out) out.textContent = r.value;
    });
    location.reload();
  });

  /* ------------------------------------------------------------------ */
  /* 7. Печать: раскрываем блоки глубины                                 */
  /* ------------------------------------------------------------------ */
  var openedByPrint = [];
  window.addEventListener('beforeprint', function () {
    openedByPrint = [];
    [].slice.call(document.querySelectorAll('details.deeper')).forEach(function (d) {
      if (!d.open) { d.open = true; openedByPrint.push(d); }
    });
    renderMap();
  });
  window.addEventListener('afterprint', function () {
    openedByPrint.forEach(function (d) { d.open = false; });
    openedByPrint = [];
  });

  /* ------------------------------------------------------------------ */
  /* 8. Старт                                                            */
  /* ------------------------------------------------------------------ */
  buildNavs();
  renderMap();
  updateCounter();
  show(location.hash.slice(1) || ORDER[0]);

  window.WB = WB;
})();
