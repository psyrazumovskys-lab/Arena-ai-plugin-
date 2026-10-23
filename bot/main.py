"""Telegram-бот PsyLab: одна рабочая тетрадь, уровень 1.

Пока в боте открыта только тетрадь «Как вовремя остановить ссору».
Остальные тетради линейки отключены — их карточки убраны из каталога
целиком, а не спрятаны за плашкой «скоро». Когда придёт время,
достаточно добавить запись в BOOKS и раскомментировать выдачу списка.

Тетрадь не загружается в Telegram: она лежит на GitHub Pages, бот
отдаёт ссылку в WebApp. Поэтому «залить журнал в бота» = положить файл
в therapy-workbooks/ и указать его имя в BOOKS.
"""

import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
SITE_URL = os.getenv(
    "BASE_WEB_URL",
    "https://psyrazumovskys-lab.github.io/Arena-ai-plugin-",
).rstrip("/")
PORT = int(os.getenv("PORT", "10000"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Каталог. Пока одна запись — она же единственное, что видит человек.
# ─────────────────────────────────────────────────────────────────────────────
BOOKS = [
    {
        "id": "couple_l1",
        "title": "Как вовремя остановить ссору",
        "label": "Тетрадь для пар · Уровень 1",
        "file": "w.html",
        "active": True,
    },
]

ACTIVE_BOOKS = [b for b in BOOKS if b["active"]]


def book_url(book: dict) -> str:
    # w.html — короткая ссылка на тетрадь. Она работает и до перехода
    # сайта на папку docs/, и после, поэтому адрес в боте не ломается.
    return f"{SITE_URL}/{book['file']}"


def open_keyboard(book: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📖 Открыть тетрадь",
                web_app=WebAppInfo(url=book_url(book)),
            )],
            [InlineKeyboardButton(
                text="Как это работает",
                callback_data="how:open",
            )],
        ]
    )


def start_text(name: str) -> str:
    return (
        f"Здравствуйте, {name}!\n\n"
        "Это «Как вовремя остановить ссору» — короткая тетрадь для пар.\n\n"
        "Внутри шесть шагов: почему в ссоре голова перестаёт соображать, "
        "как взять паузу на 20 минут, что сказать партнёру, чтобы не обидеть, "
        "и как потом вернуться к разговору.\n\n"
        "10 минут. Записи сохраняются на вашем устройстве.\n\n"
        "Тетрадь читают в спокойный момент, а не во время ссоры: она нужна, "
        "чтобы подготовиться заранее.\n\n"
        "Если в ссорах звучат угрозы, доходит до ударов или вам страшно "
        "оставаться рядом — это не решается техникой паузы. Здесь нужна "
        "помощь специалиста."
    )


HOW_TEXT = (
    "Как это работает\n\n"
    "Тетрадь открывается прямо в Telegram. Внутри восемь экранов: обложка "
    "и семь шагов.\n\n"
    "В некоторых шагах есть поле для записи. Нажмите «Сохранить запись» — "
    "текст останется на вашем телефоне и появится списком под полем. "
    "Записи не уходят никуда и не отправляются партнёру.\n\n"
    "Проходить можно за один вечер. К любому шагу можно вернуться: внизу "
    "есть «Назад», а с последней страницы — «В начало тетради».\n\n"
    "Если тетрадь не открывается, обновите Telegram до последней версии "
    "или откройте её в браузере."
)


dp = Dispatcher()


def root_markup() -> InlineKeyboardMarkup:
    if len(ACTIVE_BOOKS) == 1:
        return open_keyboard(ACTIVE_BOOKS[0])
    buttons = [
        [InlineKeyboardButton(text=f"📖 {b['title']}", callback_data=f"open:{b['id']}")]
        for b in ACTIVE_BOOKS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(F.text.startswith("/start"))
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name or "друг"
    await message.answer(start_text(name), reply_markup=root_markup())


@dp.message(F.text.startswith("/book"))
async def cmd_book(message: Message) -> None:
    if len(ACTIVE_BOOKS) == 1:
        await message.answer("Тетрадь открывается кнопкой ниже.", reply_markup=root_markup())
        return
    await message.answer("Выберите тетрадь:", reply_markup=root_markup())


@dp.message(F.text.startswith("/help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HOW_TEXT, reply_markup=root_markup())


@dp.callback_query(F.data == "how:open")
async def how_open(callback: CallbackQuery) -> None:
    await callback.message.edit_text(HOW_TEXT, reply_markup=root_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("open:"))
async def open_book(callback: CallbackQuery) -> None:
    book_id = callback.data.split(":", 1)[1]
    book = next((b for b in ACTIVE_BOOKS if b["id"] == book_id), None)
    if not book:
        await callback.answer("Тетрадь не найдена")
        return
    await callback.message.answer(
        f"{book['title']}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text="📖 Открыть тетрадь",
                web_app=WebAppInfo(url=book_url(book)),
            )]]
        ),
    )
    await callback.answer()


@dp.message()
async def anything_else(message: Message) -> None:
    if len(ACTIVE_BOOKS) == 1:
        await message.answer(
            "Сейчас в боте одна тетрадь — «Как вовремя остановить ссору». "
            "Открыть её можно кнопкой ниже.",
            reply_markup=root_markup(),
        )
    else:
        await message.answer("Выберите тетрадь:", reply_markup=root_markup())


async def health_check(request: web.Request) -> web.Response:
    return web.Response(text="Bot is running!")


async def start_web_server() -> None:
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/healthz", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info("HTTP health-check запущен на порту %s", PORT)


async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN не задан. Добавьте переменную окружения BOT_TOKEN "
            "с токеном от @BotFather."
        )
    if not ACTIVE_BOOKS:
        raise SystemExit("В BOOKS нет ни одной активной тетради.")

    bot = Bot(token=BOT_TOKEN)
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать"),
        BotCommand(command="book", description="Открыть тетрадь"),
        BotCommand(command="help", description="Как это работает"),
    ])

    logger.info("Запуск бота. Активных тетрадей: %s", len(ACTIVE_BOOKS))
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as exc:
        logger.info("Бот остановлен: %s", exc)
