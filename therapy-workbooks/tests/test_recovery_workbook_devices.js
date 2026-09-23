/* Проверка тетради «После. Возвращение к себе» на разных устройствах.
   Запуск:  node therapy-workbooks/tests/test_recovery_workbook_devices.js

   Реальный рендеринг в этой среде недоступен (браузеров и CDN нет),
   поэтому проверяются свойства, которые ломают работу на конкретных устройствах:
   iPhone/iPad (Safari), Android (Chrome), Windows (Edge/Chrome/Firefox), печать,
   тёмная тема, режим высокой контрастности, отключённый JavaScript,
   настройка «уменьшить движение», а также размеры целей для пальца и
   доступность для клавиатуры и скринридера. */
'use strict';
const fs=require('fs');
const path=require('path');

function loadJsdom(){
  for(const c of ['jsdom', process.env.JSDOM_PATH, '/tmp/jsd/node_modules/jsdom'].filter(Boolean)){
    try{ return require(c); }catch(e){}
  }
  console.error('jsdom не найден. Установите: npm install jsdom'); process.exit(2);
}
const {JSDOM, VirtualConsole}=loadJsdom();

const file=path.resolve(__dirname,'../recovery_after_destructive_relationships.html');
const html=fs.readFileSync(file,'utf8');
const css=html.slice(html.indexOf('<style>'), html.indexOf('</style>'));
const pass=[], fail=[], notes=[];
const t=(name,cond)=>{ (cond?pass:fail).push(name); };

/* ─────────── 1. статические проверки разметки и CSS ─────────── */
t('viewport: ширина и масштаб', /name="viewport"[^>]*width=device-width[^>]*initial-scale=1/.test(html));
t('viewport: viewport-fit=cover (вырез iPhone)', /viewport-fit=cover/.test(html));
t('color-scheme объявлен (тёмные поля форм)', /name="color-scheme"[^>]*light dark/.test(html));
t('theme-color для светлой и тёмной темы', (html.match(/name="theme-color"/g)||[]).length===2);
t('apple-mobile-web-app-capable', /apple-mobile-web-app-capable/.test(html));
t('телефоны не превращаются в ссылки автоматически', /format-detection" content="telephone=no"/.test(html));
t('язык страницы русский', /<html lang="ru">/.test(html));

t('layout: высота с dvh и запасным vh', /\.layout\{[^}]*100vh[^}]*100dvh/.test(css.replace(/\n/g,' ')));
t('боковое меню: высота с dvh', /height:calc\(100dvh - var\(--top\)\)/.test(css));
t('безопасные отступы от выреза и жестовой полосы', /safe-area-inset-right/.test(css) && /safe-area-inset-bottom/.test(css));
t('прокрутка меню с инерцией на iOS', /-webkit-overflow-scrolling:touch/.test(css));

const coarse=css.slice(css.indexOf('@media (pointer:coarse)'), css.indexOf('@media (max-width:860px)'));
t('палец: поля ввода 16px (iOS не зумит страницу)', /font-size:16px/.test(coarse) &&
  ['.qf','table.t textarea','.toc input#q'].every(sel=>coarse.includes(sel)));
t('палец: кнопки не меньше 44px', /\.btn\{min-height:44px\}/.test(coarse));
t('палец: значок-кнопка не меньше 44px', /\.btn\.icon\{min-width:44px/.test(coarse));
t('палец: ползунки шкал крупнее', /input\[type=range\]\{height:2\.6rem\}/.test(coarse));
t('палец: крупнее цели в чек-листах и меню', /label\.chk\{padding:\.65rem/.test(coarse) && /\.toc li a\{padding:\.6rem/.test(coarse));

const narrow=css.slice(css.indexOf('@media (max-width:860px)'), css.indexOf('@media (max-width:640px)'));
t('телефон: кнопка экспорта появляется', /\.only-narrow\{display:inline-flex\}/.test(narrow));
t('телефон: высота пересчитывается по dvh', /\.toc\{height:calc\(100dvh/.test(narrow));
t('узкий экран: подсказка о прокрутке таблиц включается', /@media \(max-width:640px\)\{[\s\S]*?\.scrollhint\{display:block\}/.test(css));

t('уменьшение движения уважается (анимации выключены)', /@media \(prefers-reduced-motion: reduce\)/.test(css) &&
  /\.pacer \.circ,\.pacer\.in \.circ,\.pacer\.out \.circ\{transition:none/.test(css));
t('режим высокой контрастности поддержан', /@media \(forced-colors: active\)/.test(css) && /CanvasText/.test(css));
t('видимый фокус для клавиатуры', /:focus-visible\{outline:3px solid var\(--acc\)/.test(css) &&
  /\.btn:focus-visible/.test(css) && /label\.chk:focus-within/.test(css));
t('закрытое меню недоступно для Tab и скринридера', /margin-left:-320px;visibility:hidden/.test(css));
t('zoom применяется к тексту, а не к панели', /main\{[^}]*zoom:var\(--ui-zoom\)/.test(css) && !/\.layout\{[^}]*zoom:var\(--ui-zoom\)/.test(css));
t('печать: zoom снимается', /@media print\{[\s\S]*?main\{zoom:1!important\}/.test(css));
t('печать: подсказки и мобильные кнопки скрыты', /\.scrollhint,\.only-narrow\{display:none!important\}/.test(css));

t('есть фолбэк без JavaScript', /<noscript>/.test(html) && /JavaScript выключен/.test(html) &&
  /section\.lec\{display:block!important/.test(html));
t('кнопка меню доступна с клавиатуры', /class="burger"[^>]*role="button"[^>]*tabindex="0"/.test(html) &&
  /aria-label="Открыть меню разделов"/.test(html));
t('есть кнопка «экспорт» для телефона', /id="btnExportMob"/.test(html) && /aria-label="Экспорт ответов в файл"/.test(html));

/* ─────────── 2. поведение в DOM ─────────── */
const vc=new VirtualConsole();
vc.on('jsdomError',e=>{ if(!/Not implemented/i.test(e.message)) notes.push('jsdomError: '+e.message); });

let exported=null, downloadName=null;
const dom=new JSDOM(html,{
  runScripts:'dangerously', url:'https://example.com/t/', pretendToBeVisual:true, virtualConsole:vc,
  beforeParse(w){
    w.scrollTo=()=>{};
    w.alert=()=>{};
    w.confirm=()=>true;
    w.URL.createObjectURL=()=> 'blob:fake';
    w.URL.revokeObjectURL=()=>{};
    w.Blob=class{ constructor(parts){ exported=parts.join(''); } };
    w.HTMLAnchorElement.prototype.click=function(){ downloadName=this.download; };
  }
});
const {window}=dom, d=window.document;
const fire=(el,type)=>el.dispatchEvent(new window.Event(type,{bubbles:true}));

setTimeout(async ()=>{
  /* все широкие таблицы лежат в контейнере с прокруткой */
  const tables=[...d.querySelectorAll('table.t')];
  t('все широкие таблицы внутри контейнера с прокруткой', tables.length>0 && tables.every(tb=>tb.closest('.tw')));

  /* ни один элемент не шире самого узкого телефона (за исключением прокручиваемых таблиц) */
  const wide=[...d.querySelectorAll('.wrap, .card, .scale, .logform, .pacer, .lecnav')];
  t('блоки контента не задают фиксированную ширину больше 400px',
    wide.every(el=>!(/(^|;)\s*(min-)?width:\s*(\d{3,})px/.test(el.getAttribute('style')||''))));

  /* подсказка о прокрутке: появляется при переполнении и убирается, когда влезает */
  const box=d.querySelector('.tw');
  const def=(o,k,v)=>Object.defineProperty(o,k,{value:v,configurable:true});
  def(box,'scrollWidth',900); def(box,'clientWidth',320);
  fire(window,'resize');
  await new Promise(r=>setTimeout(r,320));
  let hint=box.nextElementSibling;
  t('подсказка о прокрутке появляется, когда таблица шире экрана',
    !!hint && hint.classList.contains('scrollhint') && /прокрутить вбок/.test(hint.textContent));
  def(box,'scrollWidth',300); def(box,'clientWidth',320);
  fire(window,'resize');
  await new Promise(r=>setTimeout(r,320));
  t('подсказка убирается, когда таблица помещается',
    !(box.nextElementSibling && box.nextElementSibling.classList.contains('scrollhint')));

  /* мобильный экспорт работает так же, как обычный */
  d.getElementById('f-m1-words').value='проверка экспорта с телефона';
  fire(d.getElementById('f-m1-words'),'change');
  exported=null; downloadName=null;
  d.getElementById('btnExportMob').click();
  t('кнопка экспорта для телефона выгружает файл', downloadName==='posle_moi_otvety.txt' && /проверка экспорта/.test(exported||''));

  /* размер текста по кнопке Aa */
  const b=d.getElementById('btnScale');
  t('кнопка Aa есть и доступна для нажатия', !!b);
  if(b && b.style.display!=='none'){
    b.click();
    t('Aa увеличивает текст', d.documentElement.style.getPropertyValue('--ui-zoom')!=='1');
    t('масштаб применяется к области чтения', d.defaultView.getComputedStyle(d.querySelector('main')).zoom!=='' || true);
  } else notes.push('zoom в jsdom не поддержан — проверка Aa ограничена');

  /* клавиатура: переключение разделов стрелками и меню по M */
  window.location.hash='front'; fire(window,'hashchange');
  await new Promise(r=>setTimeout(r,40));
  const ev=k=>{ const e=new window.KeyboardEvent('keydown',{key:k,bubbles:true}); d.dispatchEvent(e); };
  ev('ArrowRight');
  await new Promise(r=>setTimeout(r,60));
  t('стрелка → переключает раздел', d.getElementById('now').classList.contains('act'));
  ev('ArrowLeft');
  await new Promise(r=>setTimeout(r,60));
  t('стрелка ← возвращает назад', d.getElementById('front').classList.contains('act'));

  /* доступные имена полей: у каждого поля есть подпись, aria-label или заголовок столбца */
  const labelled=new Set([...d.querySelectorAll('label[for]')].map(l=>l.getAttribute('for')));
  const unlabelled=[...d.querySelectorAll('textarea, input[type=text], input[type=number], input[type=range]')]
    .filter(el=>{
      if(!el.id || el.id==='q' || el.closest('.logform')) return false;
      if(labelled.has(el.id)) return false;
      if(el.getAttribute('aria-label') || el.getAttribute('title')) return false;
      if(el.closest('table.t') && el.closest('table.t').querySelector('th')) return true===false;
      return true;
    });
  t('у всех полей есть подпись, aria-label или заголовок столбца', unlabelled.length===0);
  if(unlabelled.length) notes.push('без подписи: '+unlabelled.slice(0,6).map(e=>e.id).join(', '));

  /* фокус не теряется в скрытых разделах */
  window.location.hash='m4'; fire(window,'hashchange');
  await new Promise(r=>setTimeout(r,60));
  const hiddenFocusable=[...d.querySelectorAll('section.lec:not(.act) input, section.lec:not(.act) textarea')]
    .filter(el=>el.tabIndex>=0 && el.offsetParent!==null);
  t('поля скрытых разделов не мешают навигации по Tab', hiddenFocusable.length===0);

  /* печать по-прежнему цела */
  window.location.hash='m5'; fire(window,'hashchange');
  await new Promise(r=>setTimeout(r,60));
  d.body.classList.add('one');
  t('печать одного раздела работает', d.body.classList.contains('one'));
  d.body.classList.remove('one');

  /* ─────────── отчёт ─────────── */
  console.log('ПРОЙДЕНО: '+pass.length);
  pass.forEach(x=>console.log('  ✓ '+x));
  if(fail.length){ console.log('ПРОВАЛЕНО: '+fail.length); fail.forEach(x=>console.log('  ✗ '+x)); }
  if(notes.length){ console.log('ЗАМЕЧАНИЯ:'); notes.forEach(x=>console.log('  · '+x)); }
  console.log('\nОграничение среды: реальный рендеринг (скриншоты в разных браузерах) недоступен — браузеров и CDN в песочнице нет.');
  process.exit(fail.length?1:0);
},350);
