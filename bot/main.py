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

TOPICS = {
    "boundaries": {
        "title": "🛡 Личные границы и автономия",
        "desc": "Практикум бережного отказа, укрепления личного суверенитета и выхода из чувства вины за своё «Нет».",
        "icon": "🛡",
        "levels": [
            {
                "level": 1,
                "title": "Уровень 1: Экспресс-интенсив",
                "timing": "5 страниц · ~120 мин",
                "price": "Бесплатно",
                "file": "workbook_1_express_no.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Практикум автономии",
                "timing": "12 страниц · ~3–4 недели",
                "price": "990 ₽",
                "file": "workbook_2_self_mastery.html",
                "is_free": False
            },
            {
                "level": 3,
                "title": "Уровень 3: Суверенитет Я",
                "timing": "18 страниц · глубокая интеграция",
                "price": "1 490 ₽",
                "file": "workbook_3_clinical_alliance.html",
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
                "title": "Уровень 1: Стоп эскалация",
                "timing": "6 страниц · протокол тайм-аута",
                "price": "Бесплатно",
                "file": "couple_workbook_1_stop_escalation.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Безопасный диалог",
                "timing": "14 страниц · практика контакта",
                "price": "990 ₽",
                "file": "couple_workbook_2_safe_dialogue.html",
                "is_free": False
            },
            {
                "level": 3,
                "title": "Уровень 3: Деконструкция цикла",
                "timing": "20 страниц · глубинная трансформация",
                "price": "1 490 ₽",
                "file": "couple_workbook_3_clinical_cycle.html",
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
                "title": "Уровень 1: Разморозка чувств",
                "timing": "5 страниц · нежные границы",
                "price": "Бесплатно",
                "file": "intimacy_workbook_1_unfreeze.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Телесность и нежность",
                "timing": "12 страниц · контакт и ласка",
                "price": "990 ₽",
                "file": "intimacy_workbook_2_tenderness.html",
                "is_free": False
            },
            {
                "level": 3,
                "title": "Уровень 3: Эротический реконнект",
                "timing": "16 страниц · новая глубина страсти",
                "price": "1 490 ₽",
                "file": "intimacy_workbook_3_reconnection.html",
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
                "title": "Уровень 1: Внутренняя опора",
                "timing": "5 страниц · базовая устойчивость",
                "price": "Бесплатно",
                "file": "self_esteem_workbook_1_anchor.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Самоценность в действии",
                "timing": "14 страниц · поведенческие практики",
                "price": "990 ₽",
                "file": "self_esteem_workbook_2_value.html",
                "is_free": False
            },
            {
                "level": 3,
                "title": "Уровень 3: Глубинная целостность",
                "timing": "22 страницы · аутентичное Я",
                "price": "1 490 ₽",
                "file": "self_esteem_workbook_3_depth.html",
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
                "title": "Уровень 1: Экспресс-адаптация",
                "timing": "5 страниц · первые 90 дней",
                "price": "Бесплатно",
                "file": "cohabitation_workbook_1_adaptation.html",
                "is_free": True
            },
            {
                "level": 2,
                "title": "Уровень 2: Архитектура дома",
                "timing": "12 страниц · семейные договоренности",
                "price": "990 ₽",
                "file": "cohabitation_workbook_2_architecture.html",
                "is_free": False
            },
            {
                "level": 3,
                "title": "Уровень 3: Глубинная интеграция",
                "timing": "16 страниц · синергия и романтика",
                "price": "1 490 ₽",
                "file": "cohabitation_workbook_3_integration.html",
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
        "Каждое направление разделено на 3 уровня глубины:\n"
        "🟢 **Уровень 1** доступен вам **абсолютно бесплатно** — чтобы познакомиться с методом и получить первые результаты.\n"
        "🔒 **Уровни 2 и 3** — глубокие терапевтические погружения.\n\n"
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
        "Выберите подходящий уровень погружения:"
    )

    buttons = []
    for item in topic["levels"]:
        lvl = item["level"]
        access_key = f"{topic_key}_{lvl}"
        is_unlocked = item["is_free"] or (access_key in user_unlocked)

        if is_unlocked:
            web_url = f"{BASE_WEB_URL}/{item['file']}"
            btn_text = f"🟢 {item['title']} · {item['timing']}"
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
        f"⏱ Объем: {level_data['timing']}\n"
        f"Стоимость: *{level_data['price']}*\n\n"
        "В этот уровень входят:\n"
        "• Интерактивная тетрадь для смартфона с автосохранением ответов;\n"
        "• Клинические карточки и протоколы;\n"
        "• Поведенческие эксперименты (In Vivo) в реальной жизни;\n"
        "• PDF-версия для печати или планшета.\n\n"
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
        f"Вам открыт: *{topic['title']} — {level_data['title']}*.\n\n"
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
        [InlineKeyboardButton(text="🔑 Активировать полный VIP-доступ (Все 15 тетрадей)", callback_data="promo:unlock_all")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="menu:root")]
    ]
    text = (
        "🎁 *Активация промокода*\n\n"
        "В боевом режиме здесь клиент вводит текстовый промокод от терапевта или из соцсетей.\n\n"
        "Для демонстрации вы можете в 1 клик активировать полный доступ ко всей библиотеке:"
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
        "✨ *Поздравляем! Полный VIP-доступ активирован.*\n\n"
        "Теперь вам открыты все 15 рабочих тетрадей на всех уровнях сложности.\n"
        "Перейдите в каталог или откройте «Мои доступы»."
    )
    buttons = [
        [InlineKeyboardButton(text="📚 Перейти в каталог", callback_data="menu:root")],
        [InlineKeyboardButton(text="📂 Мои доступы", callback_data="action:my_books")]
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await callback.answer("Все 15 тетрадей разблокированы!")

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
                btn_title = f"{t_val['icon']} {item['title']}"
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

# Простой HTTP сервер для Render Web Service (чтобы сервис не засыпал и успешно проходил Health Check)
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
    logger.info("Запуск Telegram-бота рабочей тетради...")
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
