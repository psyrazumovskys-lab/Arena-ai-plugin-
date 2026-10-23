# ВНИМАНИЕ: файл устарел и ничего не загружает.
#
# 1) Скрипт только читает локальные файлы и печатает их длину — вызовов Drive API
#    здесь нет, загрузку он никогда не выполнял.
# 2) Все file_id в mapping ниже указывают на файлы, перемещённые в корзину
#    23.10.2026 при реструктуризации каталога на папки
#    «01 · Пары и деэскалация ссор», «02 · Близость и сексуальность»,
#    «03 · Быт, романтика и совместный дом».
#
# Актуальная загрузка выполняется через коннектор Google Drive.
# Журнал «Пары: деэскалация ссор, уровень 1» (папка 1e9ICbUM2oZaIHTba9uxQZZzlxT4EwTfp):
#   HTML  1iv0pREARLeuGkyXDQvq6hgA1fkS_0Bse   1 390 893 байт
#   PDF   1FOJZajnZ-IM1DAZI-yzmFAdQ9KibM7nw   1 247 975 байт
#
# Остальные строки mapping требуют перепривязки к новым file_id.

import json

mapping = [
    # Series 1: Boundaries
    ('therapy-workbooks/workbook_1_express_no.html', '1X2fplaT7QTDogWM3L8NanSRUUjMYkCRS', '01_Личные_границы_Уровень_1_Экспресс_интенсив_Интерактив_3стр.html'),
    ('therapy-workbooks/workbook_2_self_mastery.html', '1mE4qK0_MH3edtlbErGoGWw0spIKap3WO', '02_Личные_границы_Уровень_2_Практикум_автономии_Интерактив_6стр.html'),
    ('therapy-workbooks/workbook_3_clinical_alliance.html', '1V0zePUsnvUHPgTjhr_IaGpyZmwPm-w7p', '03_Личные_границы_Уровень_3_Суверенитет_Я_Интерактив_8стр.html'),

    # Series 2: Couple Quarrels
    ('therapy-workbooks/couple_workbook_1_stop_escalation.html', '1iv0pREARLeuGkyXDQvq6hgA1fkS_0Bse', '04_Пары_и_ссоры_Уровень_1_Стоп_эскалация_Интерактив.html'),
    ('therapy-workbooks/couple_workbook_2_safe_dialogue.html', '1UlW5lfzW3P8395Gve2AnV93UzxsYEKdv', '05_Пары_Ссоры_Уровень_2_Безопасный_диалог_Интерактив_6стр.html'),
    ('therapy-workbooks/couple_workbook_3_clinical_cycle.html', '1ZpHivAjfVusrBDXzQaZRJx7N9QDKKJ8k', '06_Пары_Ссоры_Уровень_3_Деконструкция_цикла_Интерактив_8стр.html'),

    # Series 3: Intimacy
    ('therapy-workbooks/intimacy_workbook_1_unfreeze.html', '1RVROZ18cI9Hg-0LudeCjEJxdAGK9ry88', '07_Близость_Уровень_1_Разморозка_Интерактив_3стр.html'),
    ('therapy-workbooks/intimacy_workbook_2_tenderness.html', '1jC-Y04ANjLihymjWDklLIjW5w5-1R7Yt', '08_Близость_Уровень_2_Территория_нежности_Интерактив_6стр.html'),
    ('therapy-workbooks/intimacy_workbook_3_reconnection.html', '1aHqmJcs1GPbQ9crE8mQddWXkhWzy-ujm', '09_Близость_Уровень_3_Эротический_реконнект_Интерактив_8стр.html'),

    # Series 4: Self-Esteem
    ('therapy-workbooks/self_esteem_workbook_1_anchor.html', '16J9kxMfEgFnZMUbCor4jq8Lk60f9J4uD', '10_Самооценка_Уровень_1_Внутренняя_опора_Интерактив_3стр.html'),
    ('therapy-workbooks/self_esteem_workbook_2_value.html', '1h9I2VkxjoFLraSCQ4vOvxA0Qi7M0Qosz', '11_Самооценка_Уровень_2_Право_на_ценность_Интерактив_6стр.html'),
    ('therapy-workbooks/self_esteem_workbook_3_depth.html', '1ygBVGEozFHMeIV3xScssYakxngMQYEPh', '12_Самооценка_Уровень_3_Архитектура_Я_Интерактив_8стр.html'),
]

for local_path, file_id, gname in mapping:
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f'Ready for {gname}: len={len(content)}')
