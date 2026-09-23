/* DOM-тест тетради «После. Возвращение к себе».
   Запуск:  npm install jsdom && node therapy-workbooks/tests/test_recovery_workbook.js
   Сценарий «вернулся к заполненной тетради»:
     SEED_FILE=/tmp/seed.json node therapy-workbooks/tests/test_recovery_workbook.js
   Проверяет: автосохранение (включая дозапись при закрытии страницы), прогресс,
   дневник тяги, дыхательный тренажёр, печать отдельного модуля,
   переключатель размера текста, экспорт и очистку данных. */
'use strict';
const fs=require('fs');
const path=require('path');

function loadJsdom(){
  const candidates=['jsdom', process.env.JSDOM_PATH, '/tmp/jsd/node_modules/jsdom'].filter(Boolean);
  for(const c of candidates){ try{ return require(c); }catch(e){} }
  console.error('jsdom не найден. Установите: npm install jsdom');
  process.exit(2);
}
const {JSDOM, VirtualConsole}=loadJsdom();

const KEY='after_destructive_rel_v1';
const UIKEY='after_destructive_rel_ui_v1';
const file=path.resolve(__dirname,'../recovery_after_destructive_relationships.html');
const html=fs.readFileSync(file,'utf8');

const pass=[], fail=[], env=[];
const t=(name,cond)=>{ (cond?pass:fail).push(name); };

let captured=null, downloadName=null;
const vc=new VirtualConsole();
vc.on('jsdomError',e=>{ if(!/Not implemented/i.test(e.message)) env.push('jsdomError: '+e.message); });

const seed=JSON.parse(process.env.SEED_STORE || (process.env.SEED_FILE? fs.readFileSync(process.env.SEED_FILE,'utf8') : 'null'));
const seededLog=(seed && Array.isArray(seed.log))? seed.log.length : 0;
const dom=new JSDOM(html,{
  runScripts:'dangerously', url:'https://example.com/t/', pretendToBeVisual:true, virtualConsole:vc,
  beforeParse(w){
    if(seed){ try{ w.localStorage.setItem(KEY,JSON.stringify(seed)); }catch(e){ env.push('seed: '+e.message); } }
    w.scrollTo=()=>{};
    w.alert=m=>{ env.push('alert: '+m); };
    w.confirm=()=>true;
    w.print=()=>{ printCalls++; };
    w.URL.createObjectURL=()=> 'blob:fake';
    w.URL.revokeObjectURL=()=>{};
    w.HTMLAnchorElement.prototype.click=function(){ downloadName=this.download; };
    w.Blob=class{ constructor(parts){ captured=parts.join(''); } };
  }
});
let printCalls=0;
const {window}=dom, d=window.document;
const fire=(el,type)=>el.dispatchEvent(new window.Event(type,{bubbles:true}));
const store=()=>JSON.parse(window.localStorage.getItem(KEY)||'{}');

setTimeout(async ()=>{
  /* ── структура ───────────────────────────── */
  const secs=[...d.querySelectorAll('section.lec')];
  t('9 разделов', secs.length===9);
  t('стартует с титула', secs.filter(s=>s.classList.contains('act')).length===1 && d.getElementById('front').classList.contains('act'));
  t('печатная обложка есть', !!d.querySelector('.print-cover') && /Стоп-протокол/.test(d.querySelector('.print-cover').textContent));
  t('печатные шапки разделов добавлены', d.querySelectorAll('.phead').length===9);
  t('надзаголовки модулей добавлены', d.querySelectorAll('.modhead .eyebrow').length===9);
  t('номерные чипы у модулей 1–6', d.querySelectorAll('.modhead .chip').length===6);
  t('навигация между разделами', d.querySelectorAll('.lecnav').length===9);
  t('кнопка «печать этого раздела» в каждом разделе', d.querySelectorAll('.lecnav [data-print]').length===9);

  /* ── возвращение к заполненной тетради ───── */
  const seededData=!!(seed && Object.keys(seed).filter(k=>k.indexOf('__')!==0).length);
  if(seededData){
    t('восстановление: текст поля', d.getElementById('f-m1-words').value===(seed['f-m1-words']||''));
    t('восстановление: отметка чекбокса', d.getElementById('c-m1-a1').checked===true && d.getElementById('c-m1-a1').closest('label').classList.contains('on'));
    t('восстановление: значение шкалы', d.getElementById('r-m1-fear').value==='7' && d.getElementById('v-m1-fear').textContent==='7');
    t('восстановление: отрисован дневник тяги', seededLog>0 ? /ночь/.test(d.getElementById('logList').textContent) : true);
    t('восстановление: статус сообщает о восстановлении', seed.__savedAt
        ? /восстановлено/.test(d.getElementById('saveStat').textContent)
        : /автосохранение включено/.test(d.getElementById('saveStat').textContent));
    t('восстановление: прогресс учитывает старые ответы', parseInt(d.getElementById('counter').textContent,10)>=2);
  }

  /* ── автосохранение ──────────────────────── */
  const words=d.getElementById('f-m1-words');
  words.value='Сначала было тепло, потом я перестала узнавать себя.';
  fire(words,'input'); fire(words,'change');
  t('текстовое поле сохраняется', store()['f-m1-words']===words.value);
  t('поле из таблицы сохраняется', (()=>{ const c=d.getElementById('f-m3-f1'); c.value='12 сентября, 21:40, кухня.'; fire(c,'input'); fire(c,'change'); return store()['f-m3-f1']===c.value; })());
  const chk=d.getElementById('c-m1-a1'); chk.checked=true; fire(chk,'change');
  t('чекбокс сохраняется', store()['c-m1-a1']===true);
  t('чекбокс подсвечен', chk.closest('label').classList.contains('on'));
  const rng=d.getElementById('r-m1-fear'); rng.value='8'; fire(rng,'input'); fire(rng,'change');
  t('шкала сохраняется', store()['r-m1-fear']==='8');
  t('шкала: значение в пилюле', d.getElementById('v-m1-fear').textContent==='8');
  t('шкала: заливка дорожки', rng.style.getPropertyValue('--p')==='80%');
  t('метка «сохранено ✓» у поля', /сохранено/.test(d.querySelector('.sav[data-for="f-m1-words"]').textContent));
  t('время сохранения записано', typeof store().__savedAt==='number');
  t('статус в панели показывает сохранение', /сохранено/.test(d.getElementById('saveStat').textContent));

  /* дозапись при уходе со страницы (debounce не успел) */
  const late=d.getElementById('f-m4-24');
  late.value='обычно легче через сутки';
  fire(late,'input');
  const beforeFlush=!!store()['f-m4-24'];
  fire(d,'visibilitychange');
  window.dispatchEvent(new window.Event('pagehide'));
  t('дозапись при закрытии страницы (visibilitychange/pagehide)', beforeFlush || store()['f-m4-24']===late.value);

  /* ── прогресс ───────────────────────────── */
  const counterText=d.getElementById('counter').textContent;
  t('счётчик: «N из M · %»', /\d+ из \d+ · \d+%/.test(counterText));
  t('полоса прогресса заполняется', /%$/.test(d.getElementById('barFill').style.width) && parseFloat(d.getElementById('barFill').style.width)>0);
  t('прогресс по модулям в меню', d.querySelectorAll('.toc .tprog').length>=8 && /\d+\/\d+/.test([...d.querySelectorAll('.toc .tprog')].map(x=>x.textContent).join(' ')));
  t('цветовые точки разделов', [...d.querySelectorAll('.toc li')].filter(li=>li.style.getPropertyValue('--sec')).length>=8);

  /* ── дневник тяги ───────────────────────── */
  d.getElementById('logTrig').value='увидел(а) его фото в ленте';
  d.getElementById('logWish').value='напишу и всё объясню';
  d.getElementById('logForce').value='8'; d.getElementById('logAfter').value='3';
  d.getElementById('logAct').value='20 минут пешком, звонок Л.';
  d.getElementById('logAdd').click();
  t('дневник тяги: запись добавлена', (store().log||[]).length===seededLog+1);
  t('дневник тяги: отрисована', /фото в ленте/.test(d.getElementById('logList').textContent));
  d.querySelector('#logList .lx').click();
  t('дневник тяги: удаление', (store().log||[]).length===seededLog);
  d.getElementById('logAdd').click();
  t('дневник тяги: пустая запись не добавляется', (store().log||[]).length===seededLog);
  d.getElementById('logTrig').value='ночь, одна дома';
  d.getElementById('logAdd').click();
  t('дневник тяги: запись только с триггером принимается', (store().log||[]).length===seededLog+1);

  /* ── дыхание ────────────────────────────── */
  const pbtn=d.getElementById('pacerBtn');
  pbtn.click();
  t('дыхание: запуск', /pacer noprint (in|hold|out)/.test(d.getElementById('pacer').className));
  pbtn.click();
  t('дыхание: остановка', !d.getElementById('pacer').classList.contains('in') && !d.getElementById('pacer').classList.contains('out'));

  /* ── печать ─────────────────────────────── */
  const pb=d.querySelector('.lecnav [data-print="m2"]');
  const printsBefore=printCalls;
  pb.click();
  await new Promise(r=>setTimeout(r,400));
  t('печать раздела: помечен нужный раздел', d.getElementById('m2').classList.contains('act'));
  t('печать раздела: включён режим одного раздела', d.body.classList.contains('one'));
  t('печать раздела: вызвана печать', printCalls>printsBefore);
  window.dispatchEvent(new window.Event('afterprint'));
  t('печать раздела: режим снимается после печати', !d.body.classList.contains('one'));
  /* обычная печать не должна печатать один раздел */
  d.getElementById('btnPrint').click();
  await new Promise(r=>setTimeout(r,120));
  t('обычная печать печатает всю тетрадь', !d.body.classList.contains('one'));

  /* ── размер текста ──────────────────────── */
  t('размер текста: переменная задана', !!d.documentElement.style.getPropertyValue('--ui-zoom'));
  const btnScale=d.getElementById('btnScale');
  if(btnScale && btnScale.style.display!=='none'){
    const z0=d.documentElement.style.getPropertyValue('--ui-zoom');
    btnScale.click();
    t('размер текста: переключается', d.documentElement.style.getPropertyValue('--ui-zoom')!==z0);
    t('размер текста: сохраняется в настройках', !!window.localStorage.getItem(UIKEY));
  } else { env.push('zoom не поддерживается в jsdom — проверка Aa пропущена'); }

  /* ── экспорт ────────────────────────────── */
  captured=null; downloadName=null;
  d.getElementById('btnExport').click();
  const txt=captured||'';
  t('экспорт: имя файла', downloadName==='posle_moi_otvety.txt');
  t('экспорт: поле модуля 1', txt.includes('Сначала было тепло'));
  t('экспорт: поле из таблицы', txt.includes('12 сентября, 21:40'));
  t('экспорт: заголовок вопроса', txt.includes('1.3 Своими словами')||txt.includes('3.3 Что было моим'));
  t('экспорт: отметка чекбокса', /\[✓\]/.test(txt));
  t('экспорт: значения шкал', /Шкала «Страх» \(0–10\): 8/.test(txt));
  t('экспорт: дневник тяги', /Дневник тяги/.test(txt));
  t('экспорт: отмечено время выгрузки', typeof store().__exportedAt==='number');

  /* ── карта ──────────────────────────────── */
  window.location.hash='map'; fire(window,'hashchange');
  const map=d.getElementById('mapStats').textContent;
  t('карта: сводка по модулям', /Заполнено/.test(map));
  t('карта: время сохранения и экспорта', /Последнее сохранение/.test(map) && /Последний экспорт/.test(map));
  d.getElementById('f-m2-hour').value='7:00–8:00, кофе и 20 минут прогулки без телефона';
  fire(d.getElementById('f-m2-hour'),'change');
  window.location.hash='front'; fire(window,'hashchange'); window.location.hash='map'; fire(window,'hashchange');
  t('карта: опоры собираются из полей', /Мой безопасный час/.test(d.getElementById('mapAnchors').textContent));

  /* ── сохранение сейчас и очистка ────────── */
  d.getElementById('btnSaveNow').click();
  t('кнопка «Сохранить сейчас» работает', /сохранено/.test(d.getElementById('saveStat').textContent));
  d.getElementById('btnClear').click();
  t('очистка: данные удалены (остаются только служебные метки)', Object.keys(store()).filter(k=>k.indexOf('__')!==0).length===0);
  t('очистка: поля пусты', d.getElementById('f-m1-words').value==='');
  t('очистка: шкала вернулась к 5', d.getElementById('r-m1-fear').value==='5' && d.getElementById('v-m1-fear').textContent==='5');
  t('очистка: счётчик обнулён', /^0 из \d+ · 0%$/.test(d.getElementById('counter').textContent));

  /* ── отчёт ──────────────────────────────── */
  console.log('ПРОЙДЕНО: '+pass.length); pass.forEach(x=>console.log('  ✓ '+x));
  if(fail.length){ console.log('ПРОВАЛЕНО: '+fail.length); fail.forEach(x=>console.log('  ✗ '+x)); }
  if(env.length){ console.log('ЗАМЕЧАНИЯ:'); env.forEach(x=>console.log('  · '+x)); }
  process.exit(fail.length?1:0);
},350);
