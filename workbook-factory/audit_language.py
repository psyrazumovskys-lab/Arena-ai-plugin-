#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Аудит тетрадей: этика, непонятные термины, сленг, чистота текста.

Что делает:
  1. Извлекает ВЕСЬ текст, который видит пользователь: текстовые узлы, placeholder,
     title, alt, label, data-q (подписи полей попадают в экспорт отчёта).
  2. Проверяет приватность: нет ли в файле сетевых вызовов и внешних ресурсов
     (заявление «ответы никуда не отправляются» должно быть технически правдивым).
  3. Ищет профессиональный жаргон, сленг и поп-психологию, этические риски,
     смешение алфавитов и мусор в тексте.
  4. Пишет отчёт reports/language_ethics_audit.md и возвращает код 1,
     если найдены проблемы уровня «error».

Запуск:
    python3 audit_language.py                # все тетради репозитория
    python3 audit_language.py --client-only  # только клиентские версии
    python3 audit_language.py --json         #.machine-readable вывод
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
REPORTS = HERE / "reports"

CLIENT_FILES = [
    REPO / "therapy-workbooks" / "separation_workbook.html",
    REPO / "therapy-workbooks" / "recovery_after_destructive_relationships.html",
    REPO / "therapy-workbooks" / "people_pleasing_workbook.html",
    REPO / "therapy-workbooks" / "vda_12_steps_workbook.html",
    REPO / "books" / "12_steps_vda.html",
    REPO / "books" / "alcohol_recovery_workbook.html",
]
PRO_FILES = [
    REPO / "therapy-workbooks" / "separation_therapist_workbook.html",
    REPO / "books" / "wda_12_steps_workbook.html",
]

# --------------------------------------------------------------------------- #
#  Словари
# --------------------------------------------------------------------------- #
# Жаргон: term -> (порог аудитории, подсказка)
#   client  — недопустимо в клиентской версии без пояснения
#   pro     — допустимо у специалиста, но желательна русская замена
JARGON = {
    "парентификация": ("client", "пояснить: «ребёнок становится родителем своему родителю»"),
    "парентифицирован": ("client", "то же, прилагательное — лучше описательно"),
    "сепарация": ("client", "термин заголовка: на титуле должно быть пояснение простыми словами"),
    "дифференциация": ("pro", "заменить на «отдельность»"),
    "интроект": ("pro", "«внутренний голос», «присвоенная установка»"),
    "рескриптинг": ("pro", "описать действие словами"),
    "экстернализация": ("pro", "«отделить проблему от человека»"),
    "генограмма": ("pro", "«схема семьи на три поколения»"),
    "циркулярные вопросы": ("pro", "привести пример вопроса"),
    "экспозиция": ("pro", "«встреча с пугающим материалом»"),
    "контрперенос": ("pro", "«реакции самого терапевта»"),
    "перенос": ("pro", "пояснить в контексте"),
    "супервизия": ("pro", "норма для специалиста, в клиентском тексте — убрать"),
    "терапевтический альянс": ("pro", "«контакт и доверие с клиентом»"),
    "мишени": ("pro", "в клиентском тексте недопустимо: «то, с чем работаем»"),
    "интервенции": ("pro", "в клиентском тексте: «приёмы», «что помогает»"),
    "алекситимия": ("pro", "«трудность называть свои чувства»"),
    "ангедония": ("pro", "«ничего не радует»"),
    "диссоциация": ("pro", "описать проявления: «выключение», «не здесь»"),
    "деперсонализация": ("pro", "«ощущение нереальности себя»"),
    "аутоагрессия": ("pro", "«повреждение себе»"),
    "соматическ": ("pro", "«телесный»"),
    "вагусн": ("pro", "«успокаивающее дыхание, замедляющее пульс»"),
    "скрининг": ("pro", "«проверка», «оценка»"),
    "протокол": ("client", "в клиентском тексте звучит медицински: «порядок действий»"),
    "сеттинг": ("pro", "«условия работы»"),
    "раппорт": ("pro", "«контакт»"),
    "комплаенс": ("pro", "«соблюдение договорённостей»"),
    "ремиссия": ("pro", "«улучшение»"),
    "рецидив": ("pro", "«возврат к прежнему»"),
    "дифдиагноз": ("pro", "«различение состояний»"),
    "копинг": ("client", "«способ справляться»"),
    "когнитивн": ("client", "в клиентском тексте: «мысли», «работа с мыслями»"),
    "шкалирование": ("pro", "«оценка по шкале»"),
    "триггер": ("client", "допустимо, но лучше «что запускает реакцию»"),
    "фрустрация": ("pro", "«напряжение от неудачи»"),
    "амбивалентн": ("pro", "«одновременно два противоположных чувства»"),
    "экспансия": ("pro", "«дать чувству место»"),
    "КПТ": ("client", "расшифровать или убрать аббревиатуру"),
    "ACT": ("client", "расшифровать или убрать аббревиатуру"),
    "IFS": ("client", "расшифровать или убрать аббревиатуру"),
    "DBT": ("pro", "расшифровать"),
    "EMDR": ("pro", "расшифровать"),
    "CPT": ("pro", "расшифровать"),
    "SUD": ("pro", "расшифровать: шкала беспокойства 0–10"),
    "HALT": ("pro", "расшифровать"),
    "JADE": ("pro", "расшифровать"),
    "To-Done": ("pro", "«список сделанного»"),
    "cutoff": ("pro", "по-русски: «разрыв»"),
    "fawn": ("pro", "по-русски: «реакция угождения»"),
    "triangulat": ("pro", "по-русски: «втягивать в треугольник»"),
    "committed action": ("pro", "«действие по ценностям»"),
}

# Термины, которые обязаны быть пояснены в клиентском тексте (маркер пояснения рядом)
# Термины, допустимые в клиентском тексте, если рядом есть пояснение
EXPLAINED_OK = {
    "заземление": ["5-4-3-2-1", "назовите 5", "пять вещей"],
    "якорь": ["опора", "что помогает", "напомина"],
    "парентификация": ["ребёнок становится родителем", "ребёнок — родитель", "стала родителем своему"],
    "сепарация": ["пересборка дистанции", "не разрыв", "отделиться", "отдельн"],
}

SLANG = {
    "накроет": "разговорное; заменить на «если станет невыносимо», «нахлынет»",
    "накрывает": "разговорное; «захлёстывает», «становится невыносимо»",
    "затык": "сленг; «трудность», «место, где стопорится»",
    "сливают": "сленг; «критикуют», «обесценивают»",
    "слить": "сленг; «выплеснуть», «разгрузиться»",
    "заедать": "разговорное; допустимо в описании поведения, но лучше «есть от напряжения»",
    "скроллит": "сленг; «листает ленту»",
    "жесть": "сленг",
    "фигня": "сленг",
    "хрень": "сленг",
    "бомбит": "сленг",
    "плющит": "сленг",
    "триггерит": "сленг от термина; «запускает реакцию»",
    "токсичн": "поп-психология и оценочный ярлык; «разрушительная вина», «вредные отношения»",
    "токсич": "то же",
    "абьюз": "калька; по-русски «насилие», «жестокое обращение»",
    "абьюзер": "калька и ярлык; «человек, который причиняет вред»",
    "газлайтинг": "термин без пояснения; описать: «вам внушают, что этого не было»",
    "в ресурсе": "поп-психология; «есть силы»",
    "экологично": "поп-психология; «бережно»",
    "прожить эмоци": "поп-психология; «прочувствовать», «пройти через чувство»",
    "отработать": "профессиональный сленг; «поработать с»",
    "проработать": "допустимо у специалиста; в клиентском тексте — «разобрать», «осмотреть»",
    "кейс": "профессиональный сленг; «случай»",
    "клиентский запрос": "профессиональный сленг (ok только в версии для психолога)",
    "инсайт": "калька; «озарение», «важное понимание»",
    "валидация": "калька; «признание чувств»",
    "фрустрирован": "калька",
}

# Этические риски (regex -> уровень, описание)
ETHICS = [
    (r"гарантир\w*", "error", "обещание гарантии результата"),
    (r"(полностью|навсегда|раз и навсегда)\s+(избав|вылеч|убер)", "error", "обещание излечения"),
    (r"вылеч\w*", "error", "медицинское обещание"),
    (r"у\s+(вашей|твоей)\s+мам\w+\s+(нарциссизм|расстройств|диагноз)", "error", "диагноз третьему лицу"),
    (r"она\s+(нарцисс|психопат|социо пат)", "error", "ярлык на родителя"),
    (r"(прекратите|разорвите|оборвите)\s+(всякое\s+)?(общение|отношения|контакт)", "error", "директива разрыва отношений"),
    (r"заблокируй(те)?\s+е[ёг]", "warn", "рекомендация блокировки как нормы (допустимо только как выбор клиента)"),
    (r"(принимайте|начните принимать|увеличьте дозу|отмените препарат)\w*", "error", "назначение/отмена лекарств"),
    (r"(до|после)\s+еды\s+принимать", "error", "медицинская инструкция"),
    (r"это\s+не\s+(болезнь|расстройство)", "warn", "отрицание медицинского аспекта"),
    (r"укажите\s+свои\s+(телефон|номер)", "warn", "незаполненная заглушка вместо реальных контактов помощи"),
    (r"TODO|FIXME|XXX|Lorem ipsum", "error", "служебная заглушка в тексте"),
    (r"\b(lorem|ipsum|placeholder text)\b", "error", "рыба-текст"),
]

REQUIRED_CLIENT = [
    ("экран безопасности",
     r"экран безопасности|сначала безопасность|противопоказан|рамка безопасности|"
     r"карта риска|если опасно прямо сейчас|когда нужен специалист|план безопасности",
     "на титуле должен быть экран безопасности: когда самостоятельная работа противопоказана"),
    ("не заменяет помощь специалиста",
     r"не заменяет (терапию|лечение|помощь|консультаци\w*|психотерапи\w+)|не медицинская услуга|"
     r"не замена (помощи|терапии|лечени\w+|психотерапи\w+)|не заменит (врача|специалиста|терапию)",
     "нужен отказ от ответственности: тетрадь не замена лечению"),
    ("кризисные контакты", r"112|экстренн\w+ служб|скорая|кризисн\w+ (служб|лини|центр)|телефон доверия",
     "должен быть конкретный ориентир, куда звонить в кризисе"),
    ("приватность", r"хранятся только в (этом )?браузер|только в памяти (вашего )?браузер|локально на (вашем )?устройств",
     "должно быть честно описано, где хранятся ответы"),
    ("добровольность экспорта", r"экспорт|выгруз|скачать отчёт|отчёт психологу",
     "нужно явно сказать, что отчёт создаётся только по кнопке пользователя"),
    ("возрастная рамка", r"18\+|для взрослых|взросл\w+ (клиент|человек|доч|сын)",
     "желательно указать, что материал для взрослых"),
]
REQUIRED_PRO = [
    ("этика версий", r"не передаётся клиенту|клиенту не передаётся|клиент работает в клиентской",
     "профессиональная версия обязана предупреждать, что клиенту её не дают"),
    ("противопоказания", r"противопоказан|не проводить|сначала (стабилизация|безопасность)",
     "нужны противопоказания и условия отмены курса"),
    ("оценка риска", r"оценка риска|суицидальн\w+ риск|план безопасности",
     "нужен протокол оценки риска при суицидальных угрозах"),
    ("культурная чувствительность", r"культурн\w+ (контекст|чувствительн)|норма, а не патология",
     "важна оговорка про культуры с высокой включённостью поколений"),
]

# Сетевые вызовы и внешние ресурсы (проверка заявления о приватности)
NETWORK_PATTERNS = [
    (r"\bfetch\s*\(", "fetch()"),
    (r"XMLHttpRequest", "XMLHttpRequest"),
    (r"\bWebSocket\b", "WebSocket"),
    (r"navigator\.sendBeacon", "sendBeacon"),
    (r"EventSource", "EventSource"),
    (r"<img[^>]+src\s*=\s*[\"']?https?:", "внешняя картинка"),
    (r"<link[^>]+href\s*=\s*[\"']?https?:", "внешний link"),
    (r"<script[^>]+src\s*=\s*[\"']?https?:", "внешний скрипт"),
    (r"@import\s+url\(", "CSS @import"),
    (r"url\(\s*[\"']?https?:", "внешний ресурс в CSS"),
    (r"https?://(?!www\.w3\.org)", "ссылка на внешний домен"),
]

# Термины-основы: ищем как начало слова (остальные — только целым словом)
STEMS = {"соматическ", "когнитивн", "токсичн", "токсич", "триangulat", "triangulat", "эмпатичн",
         "амбивалентн", "рецидив", "ремиссия", "осознать", "валидация", "фрустрация",
         "проработать", "отработать", "прожить эмоци", "слива", "insight", "экспансия"}


def term_regex(term: str) -> str:
    """Целое слово, если это не основа; основа — без правой границы."""
    right = "" if term in STEMS else r"(?![А-Яа-яЁёA-Za-z])"
    return r"(?<![А-Яа-яЁёA-Za-z])" + re.escape(term) + right


MIXED_SCRIPT = re.compile(r"(?:[А-Яа-яЁё][A-Za-z]|[A-Za-z][А-Яа-яЁё])")
ALLOWED_MIXED = {"iOS", "HTML", "PDF", "txt", "JSON", "CSS", "JS", "URL", "ID", "OK"}


# --------------------------------------------------------------------------- #
#  Извлечение текста
# --------------------------------------------------------------------------- #
class TextExtractor(HTMLParser):
    """Собирает видимый текст + пользовательские атрибуты."""

    SKIP = {"script", "style", "head"}          # только парные теги!
    VOID = {"meta", "link", "br", "hr", "img", "input", "source", "base",
            "col", "embed", "param", "track", "wbr", "area"}
    TEXT_ATTRS = ("placeholder", "title", "alt", "data-q", "value", "aria-label")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip_depth = 0
        self.current_section = "?"
        self.div_stack = []      # для каждого открытого <div> — начинал ли он профессиональный блок
        self.pro_depth = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in self.SKIP and tag not in self.VOID:
            self.skip_depth += 1
        if tag == "section" and d.get("id"):
            self.current_section = d["id"]
        if tag == "div":
            cls = d.get("class", "")
            is_pro = ("pro-block" in cls) or ("therapist" in cls)
            self.div_stack.append(is_pro)
            if is_pro:
                self.pro_depth += 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "summary", "br", "section",
                   "label", "option", "button", "tr", "td", "th"):
            self.parts.append(("\n", self.current_section, self.layer()))
        for a in self.TEXT_ATTRS:
            if d.get(a):
                self.parts.append((" " + d[a] + " ", self.current_section, self.layer()))

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        if tag == "div" and self.div_stack:
            if self.div_stack.pop():
                self.pro_depth -= 1

    def layer(self):
        """«pro» — текст внутри методического блока, иначе «client»."""
        return "pro" if self.pro_depth else "client"

    def handle_data(self, data):
        if self.skip_depth:
            return
        if data.strip():
            self.parts.append((data, self.current_section, self.layer()))

    def result(self):
        """Список (фрагмент текста, id раздела, слой)."""
        out, buf, sec, layer = [], "", "?", "client"
        for text, s, lyr in self.parts:
            if text == "\n":
                if buf.strip():
                    out.append((re.sub(r"\s+", " ", buf).strip(), sec, layer))
                buf, sec, layer = "", s, lyr
            else:
                buf += text
                sec, layer = s, lyr
        if buf.strip():
            out.append((re.sub(r"\s+", " ", buf).strip(), sec, layer))
        return out


def extract(path: Path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    p = TextExtractor()
    p.feed(raw)
    p.close()
    return raw, p.result()


# --------------------------------------------------------------------------- #
#  Проверки
# --------------------------------------------------------------------------- #
def scan_terms(fragments, patterns: dict, layer: str, min_hits=1):
    """Ищет термины в фрагментах указанного слоя ('client' или 'pro')."""
    found = {}
    for term, rule in patterns.items():
        rx = term_regex(term)
        hits = []
        for text, sec, lyr in fragments:
            if lyr != layer:
                continue
            for m in re.finditer(rx, text, re.I):
                start = max(0, m.start() - 70)
                hits.append((sec, text[start:m.end() + 70]))
        if len(hits) >= min_hits:
            found[term] = hits
    return found


def scan_ethics(fragments):
    findings = []
    joined = "\n".join(t for t, _, _ in fragments)
    for pattern, level, why in ETHICS:
        for m in re.finditer(pattern, joined, re.I):
            s = max(0, m.start() - 80)
            findings.append((level, why, re.sub(r"\s+", " ", joined[s:m.end() + 80])))
    return findings


def scan_required(fragments, required):
    joined = "\n".join(t for t, _, _ in fragments)
    missing = []
    for name, pattern, why in required:
        if not re.search(pattern, joined, re.I):
            missing.append((name, why))
    return missing


def scan_privacy(raw: str):
    problems = []
    for pattern, label in NETWORK_PATTERNS:
        for m in re.finditer(pattern, raw, re.I):
            s = max(0, m.start() - 60)
            problems.append((label, re.sub(r"\s+", " ", raw[s:m.end() + 60])))
    return problems


def scan_mixed_script(fragments):
    out = []
    for text, sec, _layer in fragments:
        for m in MIXED_SCRIPT.finditer(text):
            frag = m.group(0)
            word = re.findall(r"[A-Za-zА-Яа-яЁё]+", text[max(0, m.start() - 12):m.end() + 12])
            w = max(word, key=len) if word else frag
            if w in ALLOWED_MIXED or len(w) <= 2:
                continue
            out.append((sec, w, text[max(0, m.start() - 60):m.end() + 60]))
    return out


def scan_clarity(fragments, max_sentence_chars=230):
    """Ясность текста: средняя длина предложения и доля перегруженных."""
    sentences = []
    for text, _sec, _layer in fragments:
        for s in re.split(r"(?<=[.!?…])\s+", text):
            s = s.strip(" —-–«»\"'")
            if len(s) > 25:
                sentences.append(s)
    if not sentences:
        return {"n": 0, "avg": 0, "long_share": 0.0, "longest": []}
    lengths = sorted((len(x) for x in sentences))
    long_ones = [x for x in sentences if len(x) > max_sentence_chars]
    return {
        "n": len(sentences),
        "avg": round(sum(lengths) / len(lengths)),
        "long_share": round(len(long_ones) / len(sentences) * 100, 1),
        "longest": sorted(long_ones, key=len, reverse=True)[:3],
    }


def audit(path: Path, audience: str) -> dict:
    raw, fragments = extract(path)
    text_len = sum(len(t) for t, _, _ in fragments)
    pro_len = sum(len(t) for t, _, l in fragments if l == "pro")
    client_fragments = [(t, s, "client") for t, s, l in fragments if l == "client"]

    res = {
        "file": str(path.relative_to(REPO)),
        "audience": audience,
        "bytes": len(raw.encode("utf-8")),
        "chars_of_text": text_len,
        "chars_pro_layer": pro_len,
        "fragments": len(fragments),
        # клиентский слой проверяем всегда; в pro-версии он унаследован из базовой спеки
        # и дополнен текстом шапки специалиста, поэтому такие находки — информационные
        "jargon": scan_terms(client_fragments, JARGON, "client"),
        "slang": scan_terms(client_fragments, SLANG, "client"),
        "client_layer_informational": audience == "pro",
        "ethics": scan_ethics(fragments),
        "missing": scan_required(client_fragments, REQUIRED_CLIENT),
        "privacy": scan_privacy(raw),
        "mixed": scan_mixed_script(fragments),
        "clarity": scan_clarity(fragments),
        "explained": {
            term: any(marker.lower() in " ".join(t for t, _, _ in fragments).lower() for marker in markers)
            for term, markers in EXPLAINED_OK.items()
            if term.lower() in " ".join(t for t, _, _ in fragments).lower()
        },
    }
    if audience == "pro":
        res["missing_pro"] = scan_required(fragments, REQUIRED_PRO)
        res["jargon_pro"] = scan_terms(fragments, JARGON, "pro")
        res["slang_pro"] = scan_terms(fragments, SLANG, "pro")
    else:
        res["missing_pro"], res["jargon_pro"], res["slang_pro"] = [], {}, {}

    res["errors"] = sum(1 for lvl, _, _ in res["ethics"] if lvl == "error")
    res["warnings"] = sum(1 for lvl, _, _ in res["ethics"] if lvl == "warn")
    return res


# --------------------------------------------------------------------------- #
#  Отчёт
# --------------------------------------------------------------------------- #
def md_report(results) -> str:
    lines = [
        "# Аудит тетрадей: этика, термины, сленг",
        "",
        "Сгенерировано `workbook-factory/audit_language.py`. Проверяется весь текст, который видит",
        "пользователь: содержимое узлов, `placeholder`, `title`, `data-q` (подписи полей попадают в экспорт),",
        "а также техническая правдивость заявлений о приватности.",
        "",
        "| Файл | Аудитория | Текст, знаков | Жаргон | Сленг | Этика (error/warn) | Приватность | Алфавит | Ср. предложение |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append("| `%s` | %s | %d | %d | %d | %d / %d | %d | %d | %d |" % (
            r["file"], r["audience"], r["chars_of_text"], len(r["jargon"]), len(r["slang"]),
            r["errors"], r["warnings"], len(r["privacy"]), len(r["mixed"]), r["clarity"]["avg"]))
    lines.append("")

    for r in results:
        lines.append("## %s" % r["file"])
        lines.append("")
        lines.append("Аудитория: **%s** · %d КБ · %d фрагментов текста · %d знаков%s" %
                     (r["audience"], r["bytes"] // 1024, r["fragments"], r["chars_of_text"],
                      (" (из них слой специалиста: %d знаков)" % r["chars_pro_layer"]) if r["chars_pro_layer"] else ""))
        lines.append("")

        if r["missing"] or r["missing_pro"]:
            lines.append("### Отсутствуют обязательные элементы")
            for name, why in r["missing"]:
                lines.append("- **%s** (клиентский слой) — %s" % (name, why))
            for name, why in r["missing_pro"]:
                lines.append("- **%s** (слой специалиста) — %s" % (name, why))
            lines.append("")

        if r["ethics"]:
            lines.append("### Этические находки")
            for lvl, why, ctx in r["ethics"]:
                lines.append("- `%s` **%s**: …%s…" % (lvl, why, ctx))
            lines.append("")

        if r["privacy"]:
            lines.append("### Приватность: сетевые вызовы и внешние ресурсы")
            seen = Counter(label for label, _ in r["privacy"])
            for label, n in seen.most_common():
                lines.append("- %s — %d" % (label, n))
            for label, ctx in r["privacy"][:5]:
                lines.append("  - пример: …%s…" % ctx)
            lines.append("")

        if r["jargon"]:
            lines.append("### Профессиональный жаргон")
            for term, hits in sorted(r["jargon"].items(), key=lambda kv: -len(kv[1])):
                scope, tip = JARGON[term]
                lines.append("- **%s** — %d упом. (%s); %s" % (term, len(hits), scope, tip))
                for sec, ctx in hits[:2]:
                    lines.append("  - `%s`: …%s…" % (sec, ctx))
            lines.append("")

        if r["jargon_pro"]:
            lines.append("### Жаргон в слое специалиста (информационно: аудитория — психолог)")
            for term, hits in sorted(r["jargon_pro"].items(), key=lambda kv: -len(kv[1])):
                lines.append("- **%s** — %d упом.; рекомендация: %s" % (term, len(hits), JARGON[term][1]))
            lines.append("")

        if r["slang_pro"]:
            lines.append("### Сленг в слое специалиста")
            for term, hits in sorted(r["slang_pro"].items(), key=lambda kv: -len(kv[1])):
                lines.append("- **%s** — %d упом.; %s" % (term, len(hits), SLANG[term]))
                for sec, ctx in hits[:1]:
                    lines.append("  - `%s`: …%s…" % (sec, ctx))
            lines.append("")

        if r["slang"]:
            lines.append("### Сленг, кальки и поп-психология (клиентский слой)")
            for term, hits in sorted(r["slang"].items(), key=lambda kv: -len(kv[1])):
                lines.append("- **%s** — %d упом.; %s" % (term, len(hits), SLANG[term]))
                for sec, ctx in hits[:2]:
                    lines.append("  - `%s`: …%s…" % (sec, ctx))
            lines.append("")

        if r["mixed"]:
            lines.append("### Смешение алфавитов / опечатки")
            seen = Counter(w for _, w, _ in r["mixed"])
            for w, n in seen.most_common(20):
                lines.append("- `%s` — %d" % (w, n))
            lines.append("")

        cl = r["clarity"]
        lines.append("### Ясность текста")
        lines.append("- предложений: %d · средняя длина: %d знаков · длиннее 230 знаков: %.1f%%"
                     % (cl["n"], cl["avg"], cl["long_share"]))
        for x in cl["longest"]:
            lines.append("  - перегруженное: «%s…»" % x[:190])
        lines.append("")

        if r["explained"]:
            lines.append("### Пояснения терминов (проверка маркеров)")
            for term, ok in r["explained"].items():
                lines.append("- %s `%s`" % ("✓ пояснён" if ok else "✗ БЕЗ пояснения", term))
            lines.append("")

        if not (r["missing"] or r["missing_pro"] or r["ethics"] or r["privacy"]
                or r["jargon"] or r["slang"] or r["slang_pro"] or r["mixed"]):
            lines.append("Находок нет.")
            lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-report", action="store_true")
    ap.add_argument("files", nargs="*", help="конкретные HTML-файлы")
    args = ap.parse_args(argv)

    targets = []
    if args.files:
        targets = [(Path(f).resolve(), "client") for f in args.files]
    else:
        targets = [(p, "client") for p in CLIENT_FILES]
        if not args.client_only:
            targets += [(p, "pro") for p in PRO_FILES]

    results = []
    for path, audience in targets:
        if not path.exists():
            print("! файл не найден: %s" % path)
            continue
        results.append(audit(path, audience))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1, default=str))
        return 0

    for r in results:
        print("%-46s %-6s жаргон(кл.):%-3d сленг:%-3d этика:%d/%d приватность:%d алфавит:%d%s%s" % (
            Path(r["file"]).name, r["audience"], len(r["jargon"]), len(r["slang"]) + len(r["slang_pro"]),
            r["errors"], r["warnings"], len(r["privacy"]), len(r["mixed"]),
            "  НЕ ХВАТАЕТ: " + ", ".join(n for n, _ in r["missing"] + r["missing_pro"])
            if (r["missing"] or r["missing_pro"]) else "",
            "  (жаргон клиентского слоя — информационно)" if r.get("client_layer_informational") and r["jargon"] else ""))

    if not args.no_report:
        REPORTS.mkdir(parents=True, exist_ok=True)
        out = REPORTS / "language_ethics_audit.md"
        out.write_text(md_report(results), encoding="utf-8")
        print("\nОтчёт: %s" % out)

    hard_errors = sum(r["errors"] for r in results) \
        + sum(len(r["missing"]) + len(r["missing_pro"]) for r in results) \
        + sum(1 for r in results for lbl, _ in r["privacy"] if lbl != "ссылка на внешний домен")
    return 1 if hard_errors else 0


if __name__ == "__main__":
    sys.exit(main())
