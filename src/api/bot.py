"""
Telegram Bot interface for HuquqAI system
Uses aiogram 3.x framework with direct RDF graph access
"""

import asyncio
import os
from typing import Dict
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

from loguru import logger
from rdflib import Graph

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# User language preferences storage
user_languages: Dict[int, str] = {}

# Global RDF graph
graph: Graph = None

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
            "💬 Tómendegi túymelerden birini basıń yáki soraw jazıń!"
        ),
        "help": (
            "📖 <b>Járdem</b>\n\n"
            "🔹 /start — Sistemanı qayta baslat\n"
            "🔹 /language — Tildi tańlaw\n"
            "🔹 /menu — Bas menyu\n"
            "🔹 /stats — Statistika\n"
            "🔹 /help — Bul xabar\n\n"
            "💬 Yáki tikkeley soraw jazıń!"
        ),
        "menu": "📋 <b>MENYU</b>\n\nTómendegi túymelerden birini tańlań:",
        "searching": "🔍 Ízleymen...",
        "no_results": "😔 Hesh nárse tabılmadı.",
        "error": "❌ Qátelik júz berdi.",
        "language_changed": "✅ Til ózgertildi: Qaraqalpaqsha",
        "select_language": "🌐 Tildi tańlań:",
        "results_found": "✅ Tabılǵan",
        "article": "Statiya",
        "crime_type": "Jinayat túri",
        "severity": "Awırlıq",
        "punishment": "Jaza",
        "years": "jıl",
        "enter_keyword": "🔎 Kalit sózdi jazıń:",
        "enter_article": "🔢 Statiya nómirin jazıń:",
        "enter_min_year": "📊 Minimal jılnı jazıń (masalan: 1):",
        "enter_max_year": "📊 Maksimal jılnı jazıń (masalan: 10):",
        "select_severity": "⚖️ Awırlıq dárejesin tańlań:",
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
            "💬 Quyidagi tugmalardan birini bosing yoki savol yozing!"
        ),
        "help": (
            "📖 <b>Yordam</b>\n\n"
            "🔹 /start — Tizimni qayta boshlash\n"
            "🔹 /language — Tilni tanlash\n"
            "🔹 /menu — Bosh menyu\n"
            "🔹 /stats — Statistika\n"
            "🔹 /help — Bu xabar\n\n"
            "💬 Yoki to'g'ridan-to'g'ri savol yozing!"
        ),
        "menu": "📋 <b>MENYU</b>\n\nQuyidagi tugmalardan birini tanlang:",
        "searching": "🔍 Qidirilmoqda...",
        "no_results": "😔 Hech narsa topilmadi.",
        "error": "❌ Xatolik yuz berdi.",
        "language_changed": "✅ Til o'zgartirildi: O'zbekcha",
        "select_language": "🌐 Tilni tanlang:",
        "results_found": "✅ Topildi",
        "article": "Modda",
        "crime_type": "Jinoyat turi",
        "severity": "Og'irlik",
        "punishment": "Jazo",
        "years": "yil",
        "enter_keyword": "🔎 Kalit so'zni yozing:",
        "enter_article": "🔢 Modda raqamini yozing:",
        "enter_min_year": "📊 Minimal yilni yozing (masalan: 1):",
        "enter_max_year": "📊 Maksimal yilni yozing (masalan: 10):",
        "select_severity": "⚖️ Og'irlik darajasini tanlang:",
    },
    "ru": {
        "name": "Русский",
        "flag": "🇷🇺",
        "greeting": (
            "🏛 <b>Добро пожаловать в HuquqAI!</b>\n\n"
            "Я — интеллектуальный помощник по законам "
            "Республики Каракалпакстан.\n\n"
            "📚 <b>Мои возможности:</b>\n"
            "• Уголовный Кодекс\n"
            "• Гражданский Кодекс\n"
            "• Административный Кодекс\n"
            "• Трудовой Кодекс\n\n"
            "💬 Нажмите кнопку или напишите вопрос!"
        ),
        "help": (
            "📖 <b>Помощь</b>\n\n"
            "🔹 /start — Перезапуск\n"
            "🔹 /language — Выбор языка\n"
            "🔹 /menu — Главное меню\n"
            "🔹 /stats — Статистика\n"
            "🔹 /help — Это сообщение\n\n"
            "💬 Или напишите вопрос напрямую!"
        ),
        "menu": "📋 <b>МЕНЮ</b>\n\nВыберите действие:",
        "searching": "🔍 Поиск...",
        "no_results": "😔 Ничего не найдено.",
        "error": "❌ Произошла ошибка.",
        "language_changed": "✅ Язык изменён: Русский",
        "select_language": "🌐 Выберите язык:",
        "results_found": "✅ Найдено",
        "article": "Статья",
        "crime_type": "Тип преступления",
        "severity": "Тяжесть",
        "punishment": "Наказание",
        "years": "лет",
        "enter_keyword": "🔎 Введите ключевое слово:",
        "enter_article": "🔢 Введите номер статьи:",
        "enter_min_year": "📊 Введите минимальный срок (например: 1):",
        "enter_max_year": "📊 Введите максимальный срок (например: 10):",
        "select_severity": "⚖️ Выберите степень тяжести:",
    },
    "en": {
        "name": "English",
        "flag": "🇬🇧",
        "greeting": (
            "🏛 <b>Welcome to HuquqAI!</b>\n\n"
            "I am an intelligent assistant for the laws of the "
            "Republic of Karakalpakstan.\n\n"
            "📚 <b>My capabilities:</b>\n"
            "• Criminal Code\n"
            "• Civil Code\n"
            "• Administrative Code\n"
            "• Labor Code\n\n"
            "💬 Press a button or write your question!"
        ),
        "help": (
            "📖 <b>Help</b>\n\n"
            "🔹 /start — Restart\n"
            "🔹 /language — Language selection\n"
            "🔹 /menu — Main menu\n"
            "🔹 /stats — Statistics\n"
            "🔹 /help — This message\n\n"
            "💬 Or write a question directly!"
        ),
        "menu": "📋 <b>MENU</b>\n\nSelect an action:",
        "searching": "🔍 Searching...",
        "no_results": "😔 Nothing found.",
        "error": "❌ An error occurred.",
        "language_changed": "✅ Language changed: English",
        "select_language": "🌐 Select language:",
        "results_found": "✅ Found",
        "article": "Article",
        "crime_type": "Crime type",
        "severity": "Severity",
        "punishment": "Punishment",
        "years": "years",
        "enter_keyword": "🔎 Enter keyword:",
        "enter_article": "🔢 Enter article number:",
        "enter_min_year": "📊 Enter minimum years (e.g.: 1):",
        "enter_max_year": "📊 Enter maximum years (e.g.: 10):",
        "select_severity": "⚖️ Select severity level:",
    },
}

# User states for conversation
user_states: Dict[int, str] = {}
user_data: Dict[int, dict] = {}

# Initialize router
router = Router()


def load_knowledge_base() -> Graph:
    """Load ontology and data into RDF graph"""
    logger.info("Loading knowledge base...")

    g = Graph()
    base_path = Path(__file__).parent.parent.parent

    # Load ontology
    ontology_file = base_path / "data" / "ontologies" / "legal_ontology.owl"
    if ontology_file.exists():
        g.parse(str(ontology_file), format='xml')
        logger.info(f"Loaded ontology: {ontology_file}")

    # Load criminal code data
    data_file = base_path / "data" / "knowledge" / "criminal_code.ttl"
    if data_file.exists():
        g.parse(str(data_file), format='turtle')
        logger.info(f"Loaded data: {data_file}")

    logger.info(f"Total triples loaded: {len(g)}")
    return g


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
    keyboard = [buttons[:2], buttons[2:]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create main menu inline keyboard"""
    lang = get_user_language(user_id)

    if lang == "kaa":
        buttons = [
            [InlineKeyboardButton(text="📜 Barlıq jinayatlar", callback_data="action:all")],
            [InlineKeyboardButton(text="🔎 Kalit sóz izlew", callback_data="action:search")],
            [InlineKeyboardButton(text="🔢 Statiya nómiri", callback_data="action:article")],
            [InlineKeyboardButton(text="⚖️ Awırlıq boyınsha", callback_data="action:severity")],
            [InlineKeyboardButton(text="📊 Jaza diapazoni", callback_data="action:punishment")],
            [InlineKeyboardButton(text="📈 Statistika", callback_data="action:stats")],
            [InlineKeyboardButton(text="🌐 Tildi ózgertiw", callback_data="action:language")],
        ]
    elif lang == "uz":
        buttons = [
            [InlineKeyboardButton(text="📜 Barcha jinoyatlar", callback_data="action:all")],
            [InlineKeyboardButton(text="🔎 Kalit so'z qidirish", callback_data="action:search")],
            [InlineKeyboardButton(text="🔢 Modda raqami", callback_data="action:article")],
            [InlineKeyboardButton(text="⚖️ Og'irlik bo'yicha", callback_data="action:severity")],
            [InlineKeyboardButton(text="📊 Jazo diapazoni", callback_data="action:punishment")],
            [InlineKeyboardButton(text="📈 Statistika", callback_data="action:stats")],
            [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="action:language")],
        ]
    elif lang == "ru":
        buttons = [
            [InlineKeyboardButton(text="📜 Все преступления", callback_data="action:all")],
            [InlineKeyboardButton(text="🔎 Поиск по слову", callback_data="action:search")],
            [InlineKeyboardButton(text="🔢 Номер статьи", callback_data="action:article")],
            [InlineKeyboardButton(text="⚖️ По тяжести", callback_data="action:severity")],
            [InlineKeyboardButton(text="📊 Диапазон наказания", callback_data="action:punishment")],
            [InlineKeyboardButton(text="📈 Статистика", callback_data="action:stats")],
            [InlineKeyboardButton(text="🌐 Сменить язык", callback_data="action:language")],
        ]
    else:  # en
        buttons = [
            [InlineKeyboardButton(text="📜 All crimes", callback_data="action:all")],
            [InlineKeyboardButton(text="🔎 Keyword search", callback_data="action:search")],
            [InlineKeyboardButton(text="🔢 Article number", callback_data="action:article")],
            [InlineKeyboardButton(text="⚖️ By severity", callback_data="action:severity")],
            [InlineKeyboardButton(text="📊 Punishment range", callback_data="action:punishment")],
            [InlineKeyboardButton(text="📈 Statistics", callback_data="action:stats")],
            [InlineKeyboardButton(text="🌐 Change language", callback_data="action:language")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_severity_keyboard() -> InlineKeyboardMarkup:
    """Create severity selection keyboard"""
    buttons = [
        [InlineKeyboardButton(text="🟢 Jeńil / Light", callback_data="severity:Jeńil")],
        [InlineKeyboardButton(text="🟡 Orta / Medium", callback_data="severity:Orta")],
        [InlineKeyboardButton(text="🔴 Awır / Heavy", callback_data="severity:Awır")],
        [InlineKeyboardButton(text="⬅️ Artqa", callback_data="action:menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_article_html(row, user_id: int) -> str:
    """Format article information as HTML"""
    lang = get_user_language(user_id)
    txt = LANGUAGES.get(lang, LANGUAGES["kaa"])

    nomiri = row.get('nomiri', 'N/A')
    sarelaw = row.get('sarelaw', 'N/A')
    jaza_min = row.get('jaza_min', 'N/A')
    jaza_max = row.get('jaza_max', 'N/A')
    jinayat_turi = row.get('jinayat_turi', 'N/A')
    awirliq = row.get('awirliq', 'N/A')

    return (
        f"📜 <b>{txt['article']} {nomiri}:</b> {sarelaw}\n"
        f"   ├─ {txt['crime_type']}: {jinayat_turi}\n"
        f"   ├─ {txt['severity']}: {awirliq}\n"
        f"   └─ {txt['punishment']}: {jaza_min}-{jaza_max} {txt['years']}\n"
    )


def query_all_crimes() -> list:
    """Get all crimes from knowledge base"""
    query = """
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .
    }
    ORDER BY ?nomiri
    LIMIT 15
    """

    results = []
    for row in graph.query(query):
        results.append({
            'nomiri': str(row.nomiri),
            'sarelaw': str(row.sarelaw),
            'jinayat_turi': str(row.jinayat_turi),
            'awirliq': str(row.awirliq),
            'jaza_min': str(row.jaza_min),
            'jaza_max': str(row.jaza_max),
        })
    return results


def query_by_keyword(keyword: str) -> list:
    """Search by keyword"""
    query = f"""
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {{
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .

        OPTIONAL {{ ?statiya kk:tekstı ?teksti }}

        FILTER (
            CONTAINS(LCASE(?sarelaw), LCASE("{keyword}")) ||
            CONTAINS(LCASE(COALESCE(?teksti, "")), LCASE("{keyword}"))
        )
    }}
    ORDER BY ?nomiri
    LIMIT 10
    """

    results = []
    for row in graph.query(query):
        results.append({
            'nomiri': str(row.nomiri),
            'sarelaw': str(row.sarelaw),
            'jinayat_turi': str(row.jinayat_turi),
            'awirliq': str(row.awirliq),
            'jaza_min': str(row.jaza_min),
            'jaza_max': str(row.jaza_max),
        })
    return results


def query_by_article_number(article_num: str) -> list:
    """Search by article number"""
    query = f"""
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?teksti ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {{
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .

        OPTIONAL {{ ?statiya kk:tekstı ?teksti }}

        FILTER (STR(?nomiri) = "{article_num}")
    }}
    """

    results = []
    for row in graph.query(query):
        result = {
            'nomiri': str(row.nomiri),
            'sarelaw': str(row.sarelaw),
            'jinayat_turi': str(row.jinayat_turi),
            'awirliq': str(row.awirliq),
            'jaza_min': str(row.jaza_min),
            'jaza_max': str(row.jaza_max),
        }
        if row.teksti:
            result['teksti'] = str(row.teksti)
        results.append(result)
    return results


def query_by_severity(severity: str) -> list:
    """Search by severity"""
    query = f"""
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {{
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .

        FILTER (CONTAINS(LCASE(?awirliq), LCASE("{severity}")))
    }}
    ORDER BY ?nomiri
    LIMIT 15
    """

    results = []
    for row in graph.query(query):
        results.append({
            'nomiri': str(row.nomiri),
            'sarelaw': str(row.sarelaw),
            'jinayat_turi': str(row.jinayat_turi),
            'awirliq': str(row.awirliq),
            'jaza_min': str(row.jaza_min),
            'jaza_max': str(row.jaza_max),
        })
    return results


def query_by_punishment_range(min_years: int, max_years: int) -> list:
    """Search by punishment range"""
    query = f"""
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {{
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .

        FILTER (?jaza_min >= {min_years} && ?jaza_max <= {max_years})
    }}
    ORDER BY DESC(?jaza_max)
    LIMIT 15
    """

    results = []
    for row in graph.query(query):
        results.append({
            'nomiri': str(row.nomiri),
            'sarelaw': str(row.sarelaw),
            'jinayat_turi': str(row.jinayat_turi),
            'awirliq': str(row.awirliq),
            'jaza_min': str(row.jaza_min),
            'jaza_max': str(row.jaza_max),
        })
    return results


def get_statistics() -> dict:
    """Get knowledge base statistics"""
    stats = {'triples': len(graph)}

    # Count articles
    query_count = """
    PREFIX kk: <http://karakalpak.law/ontology#>
    SELECT (COUNT(?s) as ?count) WHERE { ?s a kk:Statiya }
    """
    result = list(graph.query(query_count))
    stats['articles'] = int(result[0][0]) if result else 0

    # Count by severity
    query_severity = """
    PREFIX kk: <http://karakalpak.law/ontology#>
    SELECT ?awirliq (COUNT(?s) as ?count)
    WHERE {
        ?s a kk:Statiya ;
           kk:awırlıq_dárejesi ?awirliq .
    }
    GROUP BY ?awirliq
    """
    stats['by_severity'] = {}
    for row in graph.query(query_severity):
        stats['by_severity'][str(row.awirliq)] = int(row['count'])

    return stats


# ============ HANDLERS ============

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    user_languages.setdefault(user_id, "kaa")
    user_states[user_id] = None

    greeting = get_text(user_id, "greeting")
    keyboard = create_main_menu_keyboard(user_id)

    await message.answer(greeting, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    logger.info(f"User {user_id} started the bot")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Handle /menu command"""
    user_id = message.from_user.id
    user_states[user_id] = None

    text = get_text(user_id, "menu")
    keyboard = create_main_menu_keyboard(user_id)

    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


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


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Handle /stats command"""
    user_id = message.from_user.id

    try:
        stats = get_statistics()

        text = (
            "📊 <b>STATISTIKA</b>\n\n"
            f"📚 Triple-lar: {stats['triples']}\n"
            f"📜 Statiyalar: {stats['articles']}\n\n"
            "<b>Awırlıq boyınsha:</b>\n"
        )

        for severity, count in stats.get('by_severity', {}).items():
            text += f"  • {severity}: {count}\n"

        await message.answer(text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Stats error: {e}")
        await message.answer(get_text(user_id, "error"), parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("lang:"))
async def callback_language(callback: CallbackQuery):
    """Handle language selection"""
    user_id = callback.from_user.id
    lang_code = callback.data.split(":")[1]

    if lang_code in LANGUAGES:
        user_languages[user_id] = lang_code
        response = LANGUAGES[lang_code]["language_changed"]

        await callback.message.edit_text(response, parse_mode=ParseMode.HTML)
        await callback.answer()

        # Show menu
        text = get_text(user_id, "menu")
        keyboard = create_main_menu_keyboard(user_id)
        await callback.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@router.callback_query(F.data.startswith("action:"))
async def callback_action(callback: CallbackQuery):
    """Handle menu actions"""
    user_id = callback.from_user.id
    action = callback.data.split(":")[1]

    await callback.answer()

    if action == "menu":
        user_states[user_id] = None
        text = get_text(user_id, "menu")
        keyboard = create_main_menu_keyboard(user_id)
        await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    elif action == "all":
        # Show all crimes
        searching = await callback.message.answer(get_text(user_id, "searching"))

        results = query_all_crimes()

        if results:
            text = f"📜 <b>{get_text(user_id, 'results_found')}: {len(results)}</b>\n\n"
            for r in results:
                text += format_article_html(r, user_id) + "\n"
        else:
            text = get_text(user_id, "no_results")

        await searching.edit_text(text, parse_mode=ParseMode.HTML)

    elif action == "search":
        user_states[user_id] = "waiting_keyword"
        await callback.message.answer(get_text(user_id, "enter_keyword"))

    elif action == "article":
        user_states[user_id] = "waiting_article"
        await callback.message.answer(get_text(user_id, "enter_article"))

    elif action == "severity":
        text = get_text(user_id, "select_severity")
        keyboard = create_severity_keyboard()
        await callback.message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    elif action == "punishment":
        user_states[user_id] = "waiting_min_year"
        user_data[user_id] = {}
        await callback.message.answer(get_text(user_id, "enter_min_year"))

    elif action == "stats":
        stats = get_statistics()
        text = (
            "📊 <b>STATISTIKA</b>\n\n"
            f"📚 Triple-lar: {stats['triples']}\n"
            f"📜 Statiyalar: {stats['articles']}\n\n"
            "<b>Awırlıq boyınsha:</b>\n"
        )
        for severity, count in stats.get('by_severity', {}).items():
            text += f"  • {severity}: {count}\n"

        await callback.message.answer(text, parse_mode=ParseMode.HTML)

    elif action == "language":
        text = get_text(user_id, "select_language")
        keyboard = create_language_keyboard()
        await callback.message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("severity:"))
async def callback_severity(callback: CallbackQuery):
    """Handle severity selection"""
    user_id = callback.from_user.id
    severity = callback.data.split(":")[1]

    await callback.answer()

    searching = await callback.message.answer(get_text(user_id, "searching"))

    results = query_by_severity(severity)

    if results:
        text = f"⚖️ <b>{severity} - {get_text(user_id, 'results_found')}: {len(results)}</b>\n\n"
        for r in results:
            text += format_article_html(r, user_id) + "\n"
    else:
        text = get_text(user_id, "no_results")

    await searching.edit_text(text, parse_mode=ParseMode.HTML)


@router.message(F.text)
async def handle_text(message: Message):
    """Handle text messages based on user state"""
    user_id = message.from_user.id
    text = message.text.strip()
    state = user_states.get(user_id)

    if text.startswith("/"):
        return

    searching_msg = await message.answer(get_text(user_id, "searching"))

    try:
        if state == "waiting_keyword":
            # Keyword search
            user_states[user_id] = None
            results = query_by_keyword(text)

            if results:
                response = f"🔎 <b>'{text}' - {get_text(user_id, 'results_found')}: {len(results)}</b>\n\n"
                for r in results:
                    response += format_article_html(r, user_id) + "\n"
            else:
                response = get_text(user_id, "no_results")

        elif state == "waiting_article":
            # Article number search
            user_states[user_id] = None
            results = query_by_article_number(text)

            if results:
                response = f"🔢 <b>{get_text(user_id, 'article')} {text}</b>\n\n"
                for r in results:
                    response += format_article_html(r, user_id)
                    if 'teksti' in r:
                        teksti = r['teksti'][:300] + "..." if len(r['teksti']) > 300 else r['teksti']
                        response += f"\n📄 {teksti}\n"
            else:
                response = get_text(user_id, "no_results")

        elif state == "waiting_min_year":
            # Punishment range - min year
            if text.isdigit():
                user_data[user_id]['min_year'] = int(text)
                user_states[user_id] = "waiting_max_year"
                await searching_msg.delete()
                await message.answer(get_text(user_id, "enter_max_year"))
                return
            else:
                response = "⚠️ Nómirdi durus kirgiziń!"

        elif state == "waiting_max_year":
            # Punishment range - max year
            if text.isdigit():
                min_year = user_data[user_id].get('min_year', 0)
                max_year = int(text)
                user_states[user_id] = None

                results = query_by_punishment_range(min_year, max_year)

                if results:
                    response = f"📊 <b>{min_year}-{max_year} jıl - {get_text(user_id, 'results_found')}: {len(results)}</b>\n\n"
                    for r in results:
                        response += format_article_html(r, user_id) + "\n"
                else:
                    response = get_text(user_id, "no_results")
            else:
                response = "⚠️ Nómirdi durus kirgiziń!"

        else:
            # Default: keyword search
            results = query_by_keyword(text)

            if results:
                response = f"🔎 <b>'{text}' - {get_text(user_id, 'results_found')}: {len(results)}</b>\n\n"
                for r in results:
                    response += format_article_html(r, user_id) + "\n"
            else:
                response = get_text(user_id, "no_results")

        await searching_msg.edit_text(response, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await searching_msg.edit_text(get_text(user_id, "error"), parse_mode=ParseMode.HTML)


async def main():
    """Main function"""
    global graph

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    # Load knowledge base
    graph = load_knowledge_base()

    if len(graph) == 0:
        logger.error("Knowledge base is empty!")
        return

    # Initialize bot
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Starting HuquqAI Telegram Bot...")
    logger.info(f"Knowledge base loaded: {len(graph)} triples")
    logger.info("Bot is ready!")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run_bot():
    """Entry point"""
    asyncio.run(main())


if __name__ == "__main__":
    run_bot()
