import asyncio
import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    CallbackQuery,
    Message
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8548203879:AAFtNeBxzTnEt-DFQMt2mjMCkmE2kHwBXDc")
BASE_WEB_URL = os.getenv(
    "BASE_WEB_URL",
    "https://psyrazumovskys-lab.github.io/Arena-ai-plugin-/therapy-workbooks"
)
PORT = int(os.getenv("PORT", 10000))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База данных тем и тетрадей (Только Уровни 1 и 2)
# Уровень 3 вынесен для персональной клинической работы с терапевтом
TOPICS = {
    "boundaries": {
        "title": "🛡 Личные границы и автономия",
        "desc": "Практикум бережного отказа, укрепления личного суверенитета и выхода из чувства вины за своё «Нет».",
        "icon": "🛡",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Экспресс-интенсив (Скорая помощь)",
                "timing": "Экспресс-старт · ~48 часов",
                "price": "Бесплатно",
                "file": "workbook_1_express_no.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: 14-дневный практикум автономии",
                "timing": "Полный курс · 14 дней трансформации",
                "price": "990 ₽",
                "file": "workbook_2_self_mastery.html",
                "is_free": False
            }
        ]
    },
    "couples": {
        "title": "💬 Пары и деэскалация конфликтов",
        "desc": "Инструменты остановки разрушительных циклов ссор, переход от претензий к безопасному эмоциональному диалогу.",
        "icon": "💬",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Стоп эскалация (SOS-протокол)",
                "timing": "Остановка ссоры · протокол тайм-аута",
                "price": "Бесплатно",
                "file": "couple_workbook_1_stop_escalation.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Безопасный парный диалог",
                "timing": "Практикум контакта · 14 дней",
                "price": "990 ₽",
                "file": "couple_workbook_2_safe_dialogue.html",
                "is_free": False
            }
        ]
    },
    "intimacy": {
        "title": "🕯 Эмоциональная и сексуальная близость",
        "desc": "Бережная разморозка чувств, телесный контакт без давления, восстановление доверия и взаимного влечения.",
        "icon": "🕯",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Разморозка чувств (Бережный старт)",
                "timing": "Чувственный чек-ин · без давления",
                "price": "Бесплатно",
                "file": "intimacy_workbook_1_unfreeze.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Телесность, нежность и контакт",
                "timing": "Практикум доверия · 14 дней",
                "price": "990 ₽",
                "file": "intimacy_workbook_2_tenderness.html",
                "is_free": False
            }
        ]
    },
    "self_esteem": {
        "title": "💎 Самооценка и безусловная самоценность",
        "desc": "Опора на внутреннюю устойчивость, преодоление синдрома самозванца и привычки заслуживать любовь.",
        "icon": "💎",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Внутренняя опора (Детектор критика)",
                "timing": "Базовое заземление · 48 часов",
                "price": "Бесплатно",
                "file": "self_esteem_workbook_1_anchor.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Самоценность в действии",
                "timing": "14 дней перепрошивки реакций",
                "price": "990 ₽",
                "file": "self_esteem_workbook_2_value.html",
                "is_free": False
            }
        ]
    },
    "cohabitation": {
        "title": "🏠 Быт, романтика и сожительство",
        "desc": "Сохранение влечения и тепла в совместном проживании, справедливое распределение быта без выгорания.",
        "icon": "🏠",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Экспресс-адаптация (Аудит триггеров)",
                "timing": "Быстрый аудит быта · первые 90 дней",
                "price": "Бесплатно",
                "file": "cohabitation_workbook_1_adaptation.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Архитектура совместного дома",
                "timing": "Семейные договоренности и романтика",
                "price": "990 ₽",
                "file": "cohabitation_workbook_2_architecture.html",
                "is_free": False
            }
        ]
    }
}

UNLOCKED_ACCESS = {}

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🛡 1. Личные границы и отказ", callback_data="topic:boundaries")],
        [InlineKeyboardButton(text="💬 2. Пары и ссоры (деэскалация)", callback_data="topic:couples")],
        [InlineKeyboardButton(text="🕯 3. Близость и сексуальность", callback_data="topic:intimacy")],
        [InlineKeyboardButton(text="💎 4. Самооценка и самоценность", callback_data="topic:self_esteem")],
        [InlineKeyboardButton(text="🏠 5. Быт и совместная жизнь", callback_data="topic:cohabitation")],
        [
            InlineKeyboardButton(text="🎁 Активировать промокод", callback_data="action:promocode"),
            InlineKeyboardButton(text="📂 Мои доступы", callback_data="action:my_books")
        ],
        [
            InlineKeyboardButton(
                text="📱 Открыть интерактивную витрину",
                web_app=WebAppInfo(url=f"{BASE_WEB_URL}/index.html")
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name or "друг"
    welcome_text = (
        f"Здравствуйте, {user_name}! 🌿\n\n"
        "Добро пожаловать в пространство терапевтических практикумов и рабочих тетрадей.\n\n"
        "Здесь собраны структурированные пошаговые материалы с практическими упражнениями, "
        "поведенческими экспериментами и автосохранением ваших заметок прямо на телефоне.\n\n"
        "В каждом направлении выстроена двухступенчатая система:\n"
        "🟢 **Уровень 1** — Экспресс-интенсив доступен вам **абсолютно бесплатно**, чтобы снять острое напряжение и сделать первый шаг.\n"
        "⭐ **Уровень 2** — 14-дневный системный практикум глубокой трансформации привычек.\n\n"
        "👇 **Выберите интересующую вас тему:**"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("topic:"))
async def show_topic(callback: CallbackQuery):
    topic_key = callback.data.split(":")[1]
    topic = TOPICS.get(topic_key)
    if not topic:
        await callback.answer("Тема не найдена")
        return

    user_id = callback.from_user.id
    user_unlocked = UNLOCKED_ACCESS.get(user_id, set())

    text = (
        f"*{topic['title']}*\n\n"
        f"{topic['desc']}\n\n"
        "Выберите формат работы:"
    )

    buttons = []
    for item in topic["levels"]:
        lvl = item["level"]
        access_key = f"{topic_key}_{lvl}"
        is_unlocked = item["is_free"] or (access_key in user_unlocked)

        if is_unlocked:
            web_url = f"{BASE_WEB_URL}/{item['file']}"
            btn_text = f"🟢 {item['title']} (Открыть)"
            buttons.append([InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=web_url))])
        else:
            btn_text = f"🔒 {item['title']} · {item['price']}"
            cb_data = f"buy:{topic_key}:{lvl}"
            buttons.append([InlineKeyboardButton(text=btn_text, callback_data=cb_data)])

    buttons.append([InlineKeyboardButton(text="◀️ Назад в каталог", callback_data="menu:root")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("buy:"))
async def handle_buy_level(callback: CallbackQuery):
    parts = callback.data.split(":")
    topic_key, lvl_str = parts[1], parts[2]
    lvl = int(lvl_str)
    topic = TOPICS[topic_key]
    level_data = next((x for x in topic["levels"] if x["level"] == lvl), None)

    text = (
        f"🔒 *{topic['title']}*\n"
        f"*{level_data['title']}*\n\n"
        f"⏱ Формат: {level_data['timing']}\n"
        f"Стоимость: *{level_data['price']}*\n\n"
        "В практикум входят:\n"
        "• 14 пошаговых дней практики (1 день = 1 страница);\n"
        "• Телесные протоколы и карта соматических маркеров;\n"
        "• Реальные поведенческие эксперименты (In Vivo);\n"
        "• Разбор срывов без чувства вины и личный Кодекс;\n"
        "• Интерактивная тетрадь для смартфона + PDF-версия для печати.\n\n"
        "💳 Для тестирования вы можете активировать доступ бесплатно по кнопке ниже:"
    )

    buttons = [
        [InlineKeyboardButton(
            text=f"🎁 Разблокировать для теста ({level_data['title']})",
            callback_data=f"unlock_test:{topic_key}:{lvl}"
        )],
        [InlineKeyboardButton(text="◀️ Назад к уровням", callback_data=f"topic:{topic_key}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("unlock_test:"))
async def unlock_for_test(callback: CallbackQuery):
    parts = callback.data.split(":")
    topic_key, lvl_str = parts[1], parts[2]
    lvl = int(lvl_str)
    user_id = callback.from_user.id

    if user_id not in UNLOCKED_ACCESS:
        UNLOCKED_ACCESS[user_id] = set()
    UNLOCKED_ACCESS[user_id].add(f"{topic_key}_{lvl}")

    topic = TOPICS[topic_key]
    level_data = next((x for x in topic["levels"] if x["level"] == lvl), None)
    web_url = f"{BASE_WEB_URL}/{level_data['file']}"

    text = (
        f"🎉 *Доступ успешно открыт!*\n\n"
        f"Вам открыт практикум: *{topic['title']} — {level_data['title']}*.\n\n"
        "Нажмите кнопку ниже, чтобы запустить интерактивную тетрадь прямо в Telegram:"
    )
    buttons = [
        [InlineKeyboardButton(text="📖 Открыть рабочую тетрадь", web_app=WebAppInfo(url=web_url))],
        [InlineKeyboardButton(text="◀️ Вернуться в меню", callback_data="menu:root")]
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await callback.answer("Доступ успешно открыт!")

@dp.callback_query(F.data == "action:promocode")
async def handle_promocode(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="🔑 Активировать полный доступ (Все 10 практикумов Ур. 1-2)", callback_data="promo:unlock_all")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="menu:root")]
    ]
    text = (
        "🎁 *Активация промокода*\n\n"
        "В боевом режиме здесь клиент вводит текстовый промокод от терапевта или из блога.\n\n"
        "Для демонстрации вы можете в 1 клик активировать полный доступ ко всей линейке Уровней 1 и 2:"
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "promo:unlock_all")
async def promo_unlock_all(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in UNLOCKED_ACCESS:
        UNLOCKED_ACCESS[user_id] = set()

    for t_key, t_val in TOPICS.items():
        for item in t_val["levels"]:
            UNLOCKED_ACCESS[user_id].add(f"{t_key}_{item['level']}")

    text = (
        "✨ *Поздравляем! Полный доступ активирован.*\n\n"
        "Теперь вам открыты все 10 рабочих тетрадей (Уровни 1 и 2) по всем 5 направлениям.\n"
        "Перейдите в каталог или откройте раздел «Мои доступы»."
    )
    buttons = [
        [InlineKeyboardButton(text="📚 Перейти в каталог", callback_data="menu:root")],
        [InlineKeyboardButton(text="📂 Мои доступы", callback_data="action:my_books")]
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await callback.answer("Все тетради Уровня 1 и 2 разблокированы!")

@dp.callback_query(F.data == "action:my_books")
async def show_my_books(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_unlocked = UNLOCKED_ACCESS.get(user_id, set())

    text = "📂 *Ваша личная библиотека практик:*\n\n"
    buttons = []

    for t_key, t_val in TOPICS.items():
        for item in t_val["levels"]:
            access_key = f"{t_key}_{item['level']}"
            if item["is_free"] or (access_key in user_unlocked):
                web_url = f"{BASE_WEB_URL}/{item['file']}"
                status_icon = "🟢" if item["is_free"] else "⭐"
                btn_title = f"{status_icon} {t_val['icon']} {item['title']}"
                buttons.append([InlineKeyboardButton(text=btn_title, web_app=WebAppInfo(url=web_url))])

    buttons.append([InlineKeyboardButton(text="◀️ В главное меню", callback_data="menu:root")])
    text += "Все материалы, к которым у вас есть доступ, сохраняются здесь бессрочно:"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu:root")
async def return_to_root(callback: CallbackQuery):
    welcome_text = (
        "🌿 *Главное меню каталога*\n\n"
        "Выберите интересующее вас направление практик:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    await callback.answer()

async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/healthz", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Health check HTTP server started on port {PORT}")

async def main():
    logger.info("Запуск Telegram-бота рабочей тетради (Уровни 1 и 2)...")
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
