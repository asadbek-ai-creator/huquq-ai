"""
Telegram Bot interface for HuquqAI system
Uses aiogram 3.x framework
"""

import asyncio
import os
from typing import Dict, Optional
from loguru import logger

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.services.query_service import QueryService


# User language preferences storage (in production, use database)
user_languages: Dict[int, str] = {}

# Language configurations
LANGUAGES = {
    "kaa": {
        "name": "Qaraqalpaqsha",
        "flag": "🇺🇿",
        "greeting": (
            "🏛 <b>HuquqAI sistemasına xosh kelipsiz!</b>\n\n"
            "Men — Qaraqalpaqstan Respublikası nızamları boyınsha "
            "intellektual járdemshi.\n\n"
            "📚 <b>Imkaniyatlarım:</b>\n"
            "• Jinayat Kodeksi\n"
            "• Puqaralıq Kodeksi\n"
            "• Administrativ Kodeks\n"
            "• Ámek Kodeksi\n\n"
            "💬 Soraqlarıńızdı jazıń, men járdem beremen!\n\n"
            "🌐 Tildi ózgertiw ushın: /language"
        ),
        "help": (
            "📖 <b>Járdem</b>\n\n"
            "🔹 /start — Sistemanı qayta baslat\n"
            "🔹 /language — Tildi tańlaw\n"
            "🔹 /help — Bul xabar\n\n"
            "💬 Sorawıńızdı jazıń, men izleymen!"
        ),
        "searching": "🔍 Ízleymen...",
        "no_results": "😔 Ízlengen soraw boyınsha málimot tabılmadı.",
        "error": "❌ Qátelik júz berdi. Qayta urınıp kóriń.",
        "language_changed": "✅ Til ózgertildi: Qaraqalpaqsha",
        "select_language": "🌐 Tildi tańlań:",
        "confidence": "Ishenimliligi",
    },
    "uz": {
        "name": "O'zbekcha",
        "flag": "🇺🇿",
        "greeting": (
            "🏛 <b>HuquqAI tizimiga xush kelibsiz!</b>\n\n"
            "Men — Qoraqalpog'iston Respublikasi qonunlari bo'yicha "
            "intellektual yordamchi.\n\n"
            "📚 <b>Imkoniyatlarim:</b>\n"
            "• Jinoyat Kodeksi\n"
            "• Fuqarolik Kodeksi\n"
            "• Ma'muriy Kodeks\n"
            "• Mehnat Kodeksi\n\n"
            "💬 Savollaringizni yozing, men yordam beraman!\n\n"
            "🌐 Tilni o'zgartirish: /language"
        ),
        "help": (
            "📖 <b>Yordam</b>\n\n"
            "🔹 /start — Tizimni qayta boshlash\n"
            "🔹 /language — Tilni tanlash\n"
            "🔹 /help — Bu xabar\n\n"
            "💬 Savolingizni yozing, men qidiraman!"
        ),
        "searching": "🔍 Qidirilmoqda...",
        "no_results": "😔 So'rov bo'yicha ma'lumot topilmadi.",
        "error": "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
        "language_changed": "✅ Til o'zgartirildi: O'zbekcha",
        "select_language": "🌐 Tilni tanlang:",
        "confidence": "Ishonchlilik",
    },
    "ru": {
        "name": "Русский",
        "flag": "🇷🇺",
        "greeting": (
            "🏛 <b>Добро пожаловать в систему HuquqAI!</b>\n\n"
            "Я — интеллектуальный помощник по законам "
            "Республики Каракалпакстан.\n\n"
            "📚 <b>Мои возможности:</b>\n"
            "• Уголовный Кодекс\n"
            "• Гражданский Кодекс\n"
            "• Административный Кодекс\n"
            "• Трудовой Кодекс\n\n"
            "💬 Пишите ваши вопросы, я помогу!\n\n"
            "🌐 Сменить язык: /language"
        ),
        "help": (
            "📖 <b>Помощь</b>\n\n"
            "🔹 /start — Перезапустить систему\n"
            "🔹 /language — Выбор языка\n"
            "🔹 /help — Это сообщение\n\n"
            "💬 Напишите вопрос, я найду ответ!"
        ),
        "searching": "🔍 Поиск...",
        "no_results": "😔 По вашему запросу информация не найдена.",
        "error": "❌ Произошла ошибка. Попробуйте снова.",
        "language_changed": "✅ Язык изменён: Русский",
        "select_language": "🌐 Выберите язык:",
        "confidence": "Уверенность",
    },
    "en": {
        "name": "English",
        "flag": "🇬🇧",
        "greeting": (
            "🏛 <b>Welcome to the HuquqAI system!</b>\n\n"
            "I am an intelligent assistant for the laws of the "
            "Republic of Karakalpakstan.\n\n"
            "📚 <b>My capabilities:</b>\n"
            "• Criminal Code\n"
            "• Civil Code\n"
            "• Administrative Code\n"
            "• Labor Code\n\n"
            "💬 Write your questions, I will help!\n\n"
            "🌐 Change language: /language"
        ),
        "help": (
            "📖 <b>Help</b>\n\n"
            "🔹 /start — Restart the system\n"
            "🔹 /language — Language selection\n"
            "🔹 /help — This message\n\n"
            "💬 Write your question, I'll search for answers!"
        ),
        "searching": "🔍 Searching...",
        "no_results": "😔 No information found for your query.",
        "error": "❌ An error occurred. Please try again.",
        "language_changed": "✅ Language changed: English",
        "select_language": "🌐 Select language:",
        "confidence": "Confidence",
    },
}

# Initialize router
router = Router()

# Initialize query service
query_service = QueryService()


def get_user_language(user_id: int) -> str:
    """Get user's preferred language"""
    return user_languages.get(user_id, "kaa")


def get_text(user_id: int, key: str) -> str:
    """Get localized text for user"""
    lang = get_user_language(user_id)
    return LANGUAGES.get(lang, LANGUAGES["kaa"]).get(key, "")


def create_language_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for language selection"""
    buttons = []
    for code, data in LANGUAGES.items():
        buttons.append(
            InlineKeyboardButton(
                text=f"{data['flag']} {data['name']}",
                callback_data=f"lang:{code}"
            )
        )

    # Arrange buttons in 2 columns
    keyboard = []
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def format_search_results(results: Dict, user_id: int) -> str:
    """Format search results as HTML"""
    lang = get_user_language(user_id)
    lang_data = LANGUAGES.get(lang, LANGUAGES["kaa"])

    answer = results.get("answer", "")
    confidence = results.get("confidence", 0)
    sources = results.get("sources", [])

    if not answer or confidence == 0:
        return lang_data["no_results"]

    # Build formatted response
    response = "📋 <b>Tabılǵan nátiyјeler:</b>\n\n"
    response += f"{answer}\n"

    # Add confidence indicator
    confidence_pct = int(confidence * 100)
    confidence_bar = "█" * (confidence_pct // 10) + "░" * (10 - confidence_pct // 10)
    response += f"\n📊 <b>{lang_data['confidence']}:</b> {confidence_bar} {confidence_pct}%"

    # Add sources if available
    if sources:
        response += f"\n\n📚 <b>Derekler:</b> {len(sources)} statiya"

    return response


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id

    # Set default language if not set
    if user_id not in user_languages:
        user_languages[user_id] = "kaa"

    greeting = get_text(user_id, "greeting")
    await message.answer(greeting, parse_mode=ParseMode.HTML)

    logger.info(f"User {user_id} started the bot")


@router.message(Command("language"))
async def cmd_language(message: Message):
    """Handle /language command"""
    user_id = message.from_user.id
    text = get_text(user_id, "select_language")
    keyboard = create_language_keyboard()

    await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    user_id = message.from_user.id
    help_text = get_text(user_id, "help")

    await message.answer(help_text, parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("lang:"))
async def callback_language(callback: CallbackQuery):
    """Handle language selection callback"""
    user_id = callback.from_user.id
    lang_code = callback.data.split(":")[1]

    if lang_code in LANGUAGES:
        user_languages[user_id] = lang_code
        response = LANGUAGES[lang_code]["language_changed"]

        await callback.message.edit_text(response, parse_mode=ParseMode.HTML)
        await callback.answer()

        logger.info(f"User {user_id} changed language to {lang_code}")
    else:
        await callback.answer("Unknown language")


@router.message(F.text)
async def handle_query(message: Message):
    """Handle user queries"""
    user_id = message.from_user.id
    question = message.text.strip()
    lang = get_user_language(user_id)

    # Skip if message is a command
    if question.startswith("/"):
        return

    logger.info(f"User {user_id} query: {question}")

    # Send "searching" message
    searching_msg = await message.answer(
        get_text(user_id, "searching"),
        parse_mode=ParseMode.HTML
    )

    try:
        # Call QueryService
        results = await query_service.search(question=question, language=lang)

        # Format and send results
        response = format_search_results(results, user_id)

        # Edit the searching message with results
        await searching_msg.edit_text(response, parse_mode=ParseMode.HTML)

        logger.info(f"Query processed successfully for user {user_id}")

    except Exception as e:
        logger.error(f"Error processing query for user {user_id}: {e}")
        error_text = get_text(user_id, "error")
        await searching_msg.edit_text(error_text, parse_mode=ParseMode.HTML)


async def main():
    """Main function to run the bot"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        logger.info("Please set it in .env file or export it:")
        logger.info("  export TELEGRAM_BOT_TOKEN='your-bot-token'")
        return

    # Initialize bot with default properties
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Initialize dispatcher
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Starting HuquqAI Telegram Bot...")
    logger.info("Bot is ready to receive messages")

    try:
        # Start polling
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run_bot():
    """Entry point for running the bot"""
    asyncio.run(main())


if __name__ == "__main__":
    run_bot()
