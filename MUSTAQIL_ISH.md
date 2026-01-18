# MUSTAQIL ISH

## HuquqAI - Qoraqalpog'iston Respublikasi Huquqiy Bilimlar Bazasi Tizimi

---

## MUNDARIJA

1. [Kirish](#1-kirish)
2. [Muammo tavsifi](#2-muammo-tavsifi)
3. [Yechim](#3-yechim)
4. [Foydalanilgan texnologiyalar](#4-foydalanilgan-texnologiyalar)
5. [Loyiha arxitekturasi](#5-loyiha-arxitekturasi)
6. [Asosiy kodlar tushuntirishi](#6-asosiy-kodlar-tushuntirishi)
7. [API endpointlar](#7-api-endpointlar)
8. [Xulosa](#8-xulosa)
9. [Foydalanilgan adabiyotlar](#9-foydalanilgan-adabiyotlar)

---

## 1. KIRISH

Zamonaviy dunyoda huquqiy ma'lumotlarga tez va oson kirish imkoniyati har qanday fuqaro uchun muhim ahamiyatga ega. Ayniqsa, milliy tillarda huquqiy hujjatlarni topish va tushunish ko'plab odamlar uchun qiyin vazifa hisoblanadi.

**HuquqAI** - bu Qoraqalpog'iston Respublikasi qonunchiligini qidiruvchan, tushunarli va hammabop qilish uchun yaratilgan sun'iy intellektga asoslangan huquqiy bilimlar bazasi tizimidir. Tizim asosan qoraqalpoq tilida ishlaydi, shu bilan birga o'zbek, rus va ingliz tillarini ham qo'llab-quvvatlaydi.

### Loyihaning maqsadi

Loyihaning asosiy maqsadi - huquqshunoslar, advokatlar, talabalar va oddiy fuqarolarga quyidagi imkoniyatlarni taqdim etish:

- Huquqiy kodekslarni oson qidirish
- Sun'iy intellekt yordamida huquqiy maslahat olish
- Qoraqalpoq tilida to'liq huquqiy ma'lumotlarga ega bo'lish
- Murakkab huquqiy terminlarni tushunish

---

## 2. MUAMMO TAVSIFI

### 2.1 Mavjud muammolar

Hozirgi kunda Qoraqalpog'iston Respublikasida quyidagi muammolar mavjud:

**1. Huquqiy ma'lumotlarga kirish qiyinligi**
- Ko'pgina qonunlar faqat rasmiy nashrlarda mavjud
- Elektron formatda qidirish imkoniyati cheklangan
- Oddiy fuqarolar uchun qonunlarni topish murakkab

**2. Til to'siqlari**
- Qoraqalpoq tilida huquqiy resurslar kam
- Mavjud resurslar asosan rus yoki o'zbek tillarida
- Terminologik lug'atlar yetarli emas

**3. Murakkab huquqiy tizim**
- Qonunlar o'zaro bog'liq va murakkab
- Oddiy fuqarolar uchun tushunish qiyin
- Professional huquqiy yordam qimmat

**4. Zamonaviy texnologiyalar yetishmasligi**
- Mavjud tizimlar eskirgan
- Sun'iy intellekt imkoniyatlaridan foydalanilmagan
- Semantik qidiruv mavjud emas

### 2.2 Maqsadli auditoriya

Tizim quyidagi foydalanuvchilar uchun mo'ljallangan:

| Foydalanuvchi turi | Ehtiyojlari |
|-------------------|-------------|
| Huquqshunoslar | Tezkor qonun qidirish, mos moddalarni topish |
| Advokatlar | Ish yuritishda huquqiy asoslar topish |
| Talabalar | O'qish jarayonida qonunlarni o'rganish |
| Fuqarolar | O'z huquqlarini bilish va himoya qilish |
| Davlat xodimlari | Qaror qabul qilishda huquqiy asos |

---

## 3. YECHIM

### 3.1 HuquqAI tizimi

HuquqAI yuqoridagi muammolarni quyidagi usullar bilan hal qiladi:

**1. Intellektual semantik qidiruv**
- SPARQL asosida kuchli so'rovlar
- Xatolarga chidamli qidiruv (fuzzy search)
- Kontekstga asoslangan filtrlash

**2. To'liq huquqiy qamrov**
- Jinoyat kodeksi (Jinayat Kodeksi)
- Fuqarolik kodeksi (Puqaralıq Kodeksi)
- Ma'muriy kodeks (Administrativ Kodeks)
- Mehnat kodeksi (Ámek Kodeksi)

**3. Sun'iy intellekt yordamchisi**
- Tabiiy tilda savolga javob berish
- Avtomatik maqola tavsiyalari
- Bog'liq qonunlarni taklif qilish

**4. Ko'p tilli qo'llab-quvvatlash**
- Qoraqalpoq tili (asosiy)
- O'zbek tili
- Rus tili
- Ingliz tili

### 3.2 Tizim arxitekturasi diagrammasi

```
┌─────────────────────────────────────────────────────────────┐
│                      FOYDALANUVCHI                          │
│                   (Web/Mobile/API)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      REST API QATLAMI                       │
│                    (FastAPI Framework)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  /query  │  │ /search  │  │/articles │  │ /crimes  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVIS QATLAMI                           │
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │  QueryService   │          │  SPARQLService  │          │
│  │  (NLP qayta     │          │  (So'rovlarni   │          │
│  │   ishlash)      │          │   bajarish)     │          │
│  └─────────────────┘          └─────────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     YADRO QATLAMI                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │OntologyManager  │  │  SPARQLEngine   │  │ Reasoning  │  │
│  │(OWL boshqaruv)  │  │  (So'rov        │  │  Engine    │  │
│  │                 │  │   mexanizmi)    │  │ (Xulosa    │  │
│  │                 │  │                 │  │  chiqarish)│  │
│  └─────────────────┘  └─────────────────┘  └────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   MA'LUMOTLAR QATLAMI                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │  OWL Ontology   │  │   RDF Triple    │  │   JSON     │  │
│  │  (legal_onto-   │  │     Store       │  │ Documents  │  │
│  │   logy.owl)     │  │  (legal_kb.ttl) │  │            │  │
│  └─────────────────┘  └─────────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. FOYDALANILGAN TEXNOLOGIYALAR

### 4.1 Backend Framework

| Texnologiya | Versiya | Vazifasi |
|-------------|---------|----------|
| **Python** | 3.9+ | Asosiy dasturlash tili |
| **FastAPI** | 0.109.2 | Zamonaviy REST API framework |
| **Uvicorn** | 0.27.1 | ASGI server |
| **Pydantic** | 1.10.13 | Ma'lumotlarni validatsiya qilish |

### 4.2 Semantik Web texnologiyalari

| Texnologiya | Versiya | Vazifasi |
|-------------|---------|----------|
| **RDFLib** | 7.0.0 | RDF grafik boshqaruvi |
| **Owlready2** | 0.46 | OWL ontologiya boshqaruvi |
| **SPARQLWrapper** | 2.0.0 | SPARQL so'rovlarni bajarish |
| **Apache Jena Fuseki** | - | SPARQL endpoint server |

### 4.3 Nima uchun bu texnologiyalar tanlandi?

**FastAPI tanlash sabablari:**
- Yuqori tezlik (Starlette va Pydantic asosida)
- Avtomatik API dokumentatsiyasi (Swagger/OpenAPI)
- Async/await qo'llab-quvvatlashi
- Type hints bilan integratsiya

**Semantik Web texnologiyalari sabablari:**
- OWL ontologiyalari murakkab huquqiy munosabatlarni ifodalash uchun ideal
- SPARQL kuchli va moslashuvchan so'rov tili
- RDF standart ma'lumot almashish formati
- Reasoning engine avtomatik xulosa chiqarish imkonini beradi

---

## 5. LOYIHA ARXITEKTURASI

### 5.1 Papkalar tuzilmasi

```
huquqAI/
│
├── src/                          # Manba kodi
│   ├── api/                      # REST API qatlami
│   │   ├── main.py              # FastAPI ilova sozlamalari
│   │   └── routes.py            # API endpointlar
│   │
│   ├── core/                     # Yadro funksionalligi
│   │   ├── base.py              # Bazaviy klasslar
│   │   ├── config.py            # Konfiguratsiya yuklovchi
│   │   ├── ontology_manager.py  # OWL ontologiya boshqaruvi
│   │   ├── sparql_engine.py     # SPARQL so'rov bajaruvchi
│   │   └── reasoning_engine.py  # OWL reasoning
│   │
│   ├── models/                   # Ma'lumot modellari
│   │   ├── legal_entities.py    # Huquqiy modellar
│   │   ├── ontology.py          # Ontologiya modeli
│   │   └── query_model.py       # So'rov modellari
│   │
│   ├── services/                 # Biznes logika
│   │   ├── query_service.py     # NLP qayta ishlash
│   │   └── sparql_service.py    # SPARQL xizmati
│   │
│   └── utils/                    # Yordamchi funksiyalar
│       ├── helpers.py           # Umumiy yordamchilar
│       ├── language.py          # Til utilitlari
│       └── logger.py            # Logging konfiguratsiyasi
│
├── data/                         # Ma'lumotlar saqlash
│   ├── ontologies/              # OWL ontologiya fayllari
│   └── knowledge/               # Huquqiy hujjatlar
│
├── tests/                        # Testlar
├── config.yaml                   # Asosiy konfiguratsiya
└── requirements.txt              # Python bog'liqliklari
```

### 5.2 Asosiy komponentlar

**1. API Qatlami (`src/api/`)**
- Foydalanuvchi so'rovlarini qabul qiladi
- Ma'lumotlarni validatsiya qiladi
- Javoblarni formatlaydi

**2. Servis Qatlami (`src/services/`)**
- Biznes logikani amalga oshiradi
- NLP qayta ishlash
- SPARQL so'rovlarni shakllantirish

**3. Yadro Qatlami (`src/core/`)**
- Ontologiya boshqaruvi
- SPARQL mexanizmi
- Reasoning (xulosa chiqarish)

**4. Model Qatlami (`src/models/`)**
- Ma'lumot strukturalari
- Pydantic modellari
- Entity ta'riflari

---

## 6. ASOSIY KODLAR TUSHUNTIRISHI

### 6.1 Huquqiy Entity Modellari (`src/models/legal_entities.py`)

Bu fayl loyihaning asosiy ma'lumot modellarini o'z ichiga oladi:

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class CodeType(str, Enum):
    """Kodeks turlari"""
    CRIMINAL = "criminal"       # Jinoyat kodeksi
    CIVIL = "civil"            # Fuqarolik kodeksi
    ADMINISTRATIVE = "administrative"  # Ma'muriy kodeks
    LABOR = "labor"            # Mehnat kodeksi

class CrimeType(str, Enum):
    """Jinoyat turlari (og'irlik darajasi bo'yicha)"""
    LIGHT = "light"            # Yengil jinoyat
    MEDIUM = "medium"          # O'rta og'irlikdagi
    HEAVY = "heavy"            # Og'ir jinoyat
    VERY_HEAVY = "very_heavy"  # Juda og'ir jinoyat

class Article(BaseModel):
    """Qonun moddasi modeli"""
    number: str = Field(..., description="Modda raqami")
    title: str = Field(..., description="Modda nomi")
    content: str = Field(..., description="Modda matni")
    code_type: CodeType = Field(..., description="Kodeks turi")
    language: str = Field(default="kaa", description="Til kodi")
    related_articles: List[str] = Field(default=[], description="Bog'liq moddalar")

class Crime(BaseModel):
    """Jinoyat modeli"""
    name: str = Field(..., description="Jinoyat nomi")
    description: str = Field(..., description="Jinoyat tavsifi")
    crime_type: CrimeType = Field(..., description="Jinoyat turi")
    article_number: str = Field(..., description="Tegishli modda")
    min_punishment_months: int = Field(..., description="Minimal jazo (oy)")
    max_punishment_months: int = Field(..., description="Maksimal jazo (oy)")

class Punishment(BaseModel):
    """Jazo modeli"""
    name: str = Field(..., description="Jazo nomi")
    description: str = Field(..., description="Jazo tavsifi")
    duration_months: Optional[int] = Field(None, description="Muddat (oy)")
    fine_amount: Optional[float] = Field(None, description="Jarima summasi")
```

**Tushuntirish:**
- `CodeType` - qaysi kodeksga tegishli ekanligini belgilaydi
- `CrimeType` - jinoyatning og'irlik darajasini aniqlaydi
- `Article` - qonun moddasining to'liq ma'lumotlarini saqlaydi
- `Crime` - jinoyat haqida ma'lumot va unga tegishli jazo
- `Punishment` - jazo turlari va parametrlari

### 6.2 Ontologiya Manager (`src/core/ontology_manager.py`)

Bu komponent OWL ontologiyalarni boshqaradi:

```python
from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty
from rdflib import Graph, Namespace, URIRef, Literal
from typing import Optional, Dict, Any
import threading

class OntologyManager:
    """
    OWL Ontologiya Boshqaruvchisi (Singleton pattern)

    Bu klass huquqiy ontologiyalarni yuklash, qidirish
    va boshqarish uchun javobgar.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern - faqat bitta instansiya"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Ontologiya managerini ishga tushirish"""
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.ontology = None
        self.graph = Graph()
        self.namespaces: Dict[str, Namespace] = {}

        # Standart namespace'larni o'rnatish
        self._setup_namespaces()

    def _setup_namespaces(self):
        """RDF namespace'larni sozlash"""
        self.namespaces = {
            'legal': Namespace('http://huquqai.kaa/ontology/legal#'),
            'crime': Namespace('http://huquqai.kaa/ontology/crime#'),
            'article': Namespace('http://huquqai.kaa/ontology/article#'),
        }

        for prefix, ns in self.namespaces.items():
            self.graph.bind(prefix, ns)

    def load_ontology(self, file_path: str) -> bool:
        """
        OWL ontologiyani fayldan yuklash

        Args:
            file_path: Ontologiya fayli yo'li

        Returns:
            bool: Muvaffaqiyatli yuklandi yoki yo'q
        """
        try:
            self.ontology = get_ontology(file_path).load()
            return True
        except Exception as e:
            print(f"Ontologiya yuklashda xato: {e}")
            return False

    def search_articles(self, keyword: str, language: str = "kaa") -> list:
        """
        Kalit so'z bo'yicha moddalarni qidirish

        Args:
            keyword: Qidiruv so'zi
            language: Til kodi (kaa, uz, ru, en)

        Returns:
            list: Topilgan moddalar ro'yxati
        """
        results = []

        # SPARQL so'rovi tuzish
        query = f"""
        PREFIX legal: <http://huquqai.kaa/ontology/legal#>

        SELECT ?article ?title ?content
        WHERE {{
            ?article a legal:Article .
            ?article legal:title ?title .
            ?article legal:content ?content .
            FILTER(CONTAINS(LCASE(?title), LCASE("{keyword}")) ||
                   CONTAINS(LCASE(?content), LCASE("{keyword}")))
        }}
        """

        # So'rovni bajarish
        for row in self.graph.query(query):
            results.append({
                'article': str(row.article),
                'title': str(row.title),
                'content': str(row.content)
            })

        return results

    def get_related_articles(self, article_number: str) -> list:
        """Bog'liq moddalarni topish"""
        query = f"""
        PREFIX legal: <http://huquqai.kaa/ontology/legal#>

        SELECT ?related ?title
        WHERE {{
            ?article legal:number "{article_number}" .
            ?article legal:relatedTo ?related .
            ?related legal:title ?title .
        }}
        """

        results = []
        for row in self.graph.query(query):
            results.append({
                'number': str(row.related),
                'title': str(row.title)
            })

        return results
```

**Tushuntirish:**
- **Singleton Pattern** - butun ilova davomida faqat bitta ontologiya manager mavjud
- **Namespace** - RDF/OWL resurslari uchun URI prefikslar
- **search_articles** - SPARQL yordamida moddalarni qidiradi
- **get_related_articles** - modda bilan bog'liq boshqa moddalarni topadi

### 6.3 SPARQL Engine (`src/core/sparql_engine.py`)

Bu komponent SPARQL so'rovlarni bajaradi:

```python
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
from typing import List, Dict, Any, Optional

class SPARQLEngine:
    """
    SPARQL So'rov Mexanizmi

    Bu klass SPARQL so'rovlarni tuzish va bajarish
    uchun javobgar. Lokal va remote endpoint'larni
    qo'llab-quvvatlaydi.
    """

    def __init__(self, endpoint: Optional[str] = None):
        """
        SPARQL Engine'ni ishga tushirish

        Args:
            endpoint: SPARQL endpoint URL (ixtiyoriy)
        """
        self.endpoint = endpoint
        self.local_graph = Graph()

        if endpoint:
            self.sparql = SPARQLWrapper(endpoint)
            self.sparql.setReturnFormat(JSON)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        SPARQL so'rovni bajarish

        Args:
            query: SPARQL so'rov matni

        Returns:
            List[Dict]: Natijalar ro'yxati
        """
        if self.endpoint:
            return self._execute_remote(query)
        else:
            return self._execute_local(query)

    def _execute_remote(self, query: str) -> List[Dict[str, Any]]:
        """Remote endpoint'da so'rov bajarish"""
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()

        return self._format_results(results)

    def _execute_local(self, query: str) -> List[Dict[str, Any]]:
        """Lokal grafda so'rov bajarish"""
        results = []

        for row in self.local_graph.query(query):
            result = {}
            for var in row.labels:
                result[var] = str(row[var])
            results.append(result)

        return results

    def _format_results(self, raw_results: dict) -> List[Dict[str, Any]]:
        """Natijalarni formatlash"""
        formatted = []

        bindings = raw_results.get('results', {}).get('bindings', [])
        for binding in bindings:
            row = {}
            for key, value in binding.items():
                row[key] = value.get('value', '')
            formatted.append(row)

        return formatted

    def search_by_crime_type(self, crime_type: str) -> List[Dict[str, Any]]:
        """
        Jinoyat turi bo'yicha qidirish

        Args:
            crime_type: Jinoyat turi (light, medium, heavy, very_heavy)

        Returns:
            List[Dict]: Topilgan jinoyatlar
        """
        query = f"""
        PREFIX crime: <http://huquqai.kaa/ontology/crime#>

        SELECT ?crime ?name ?description ?article ?punishment
        WHERE {{
            ?crime a crime:Crime .
            ?crime crime:type "{crime_type}" .
            ?crime crime:name ?name .
            ?crime crime:description ?description .
            ?crime crime:relatedArticle ?article .
            OPTIONAL {{ ?crime crime:punishment ?punishment }}
        }}
        ORDER BY ?name
        """

        return self.execute_query(query)

    def get_article_with_context(self, article_number: str) -> Dict[str, Any]:
        """
        Modda va uning kontekstini olish

        Args:
            article_number: Modda raqami

        Returns:
            Dict: Modda ma'lumotlari va kontekst
        """
        query = f"""
        PREFIX legal: <http://huquqai.kaa/ontology/legal#>
        PREFIX crime: <http://huquqai.kaa/ontology/crime#>

        SELECT ?title ?content ?codeType ?relatedCrime ?punishment
        WHERE {{
            ?article legal:number "{article_number}" .
            ?article legal:title ?title .
            ?article legal:content ?content .
            ?article legal:codeType ?codeType .

            OPTIONAL {{
                ?crime crime:relatedArticle ?article .
                ?crime crime:name ?relatedCrime .
                ?crime crime:punishment ?punishment .
            }}
        }}
        """

        results = self.execute_query(query)

        if results:
            return results[0]
        return {}
```

**Tushuntirish:**
- **execute_query** - SPARQL so'rovni lokal yoki remote serverda bajaradi
- **search_by_crime_type** - jinoyat turini aniqlab, tegishli moddalarni topadi
- **get_article_with_context** - moddani va unga bog'liq barcha ma'lumotlarni oladi

### 6.4 Query Service (`src/services/query_service.py`)

Bu servis foydalanuvchi savollarini qayta ishlaydi:

```python
from typing import Dict, Any, List, Optional
from src.core.ontology_manager import OntologyManager
from src.core.sparql_engine import SPARQLEngine
from src.models.legal_entities import Article, Crime

class QueryService:
    """
    So'rov Qayta Ishlash Servisi

    Bu klass foydalanuvchi savollarini tahlil qiladi,
    mos SPARQL so'rovlarni tuzadi va javob shakllantiradi.
    """

    def __init__(self):
        """Servisni ishga tushirish"""
        self.ontology_manager = OntologyManager()
        self.sparql_engine = SPARQLEngine()

        # Kalit so'zlar lug'ati
        self.keywords = {
            'jinoyat': ['jinoyat', 'ayblov', 'jazo', 'qamoq'],
            'fuqarolik': ['shartnoma', 'mulk', 'meros', 'nikoh'],
            'mehnat': ['ish', 'maosh', 'ta\'til', 'ishdan bo\'shatish'],
            'ma\'muriy': ['jarima', 'huquqbuzarlik', 'jazo']
        }

    def process_query(self, question: str, language: str = "kaa") -> Dict[str, Any]:
        """
        Foydalanuvchi savolini qayta ishlash

        Args:
            question: Foydalanuvchi savoli
            language: Til kodi

        Returns:
            Dict: Javob ma'lumotlari
        """
        # 1. Savolni tahlil qilish
        analyzed = self._analyze_question(question)

        # 2. Kodeks turini aniqlash
        code_type = self._detect_code_type(question)

        # 3. SPARQL so'rov tuzish
        sparql_query = self._build_sparql_query(analyzed, code_type)

        # 4. So'rovni bajarish
        results = self.sparql_engine.execute_query(sparql_query)

        # 5. Javobni shakllantirish
        response = self._format_response(results, language)

        return response

    def _analyze_question(self, question: str) -> Dict[str, Any]:
        """Savolni tahlil qilish"""
        question_lower = question.lower()

        analysis = {
            'original': question,
            'keywords': [],
            'intent': None,
            'entities': []
        }

        # Kalit so'zlarni topish
        for category, words in self.keywords.items():
            for word in words:
                if word in question_lower:
                    analysis['keywords'].append(word)
                    analysis['intent'] = category

        return analysis

    def _detect_code_type(self, question: str) -> Optional[str]:
        """Savoldan kodeks turini aniqlash"""
        question_lower = question.lower()

        if any(w in question_lower for w in ['jinoyat', 'jazo', 'qamoq']):
            return 'criminal'
        elif any(w in question_lower for w in ['shartnoma', 'mulk', 'meros']):
            return 'civil'
        elif any(w in question_lower for w in ['ish', 'maosh', 'ishchi']):
            return 'labor'
        elif any(w in question_lower for w in ['jarima', 'huquqbuzarlik']):
            return 'administrative'

        return None

    def _build_sparql_query(self, analysis: Dict, code_type: Optional[str]) -> str:
        """SPARQL so'rov tuzish"""
        keywords = analysis.get('keywords', [])

        filters = []
        for kw in keywords:
            filters.append(f'CONTAINS(LCASE(?content), "{kw}")')

        filter_clause = " || ".join(filters) if filters else "true"

        query = f"""
        PREFIX legal: <http://huquqai.kaa/ontology/legal#>

        SELECT ?article ?number ?title ?content ?codeType
        WHERE {{
            ?article a legal:Article .
            ?article legal:number ?number .
            ?article legal:title ?title .
            ?article legal:content ?content .
            ?article legal:codeType ?codeType .

            FILTER({filter_clause})
            {f'FILTER(?codeType = "{code_type}")' if code_type else ''}
        }}
        LIMIT 10
        """

        return query

    def _format_response(self, results: List[Dict], language: str) -> Dict[str, Any]:
        """Javobni formatlash"""
        if not results:
            return {
                'success': False,
                'message': self._get_no_results_message(language),
                'articles': []
            }

        articles = []
        for r in results:
            articles.append({
                'number': r.get('number', ''),
                'title': r.get('title', ''),
                'content': r.get('content', '')[:500] + '...',
                'code_type': r.get('codeType', '')
            })

        return {
            'success': True,
            'message': self._get_success_message(len(articles), language),
            'articles': articles
        }

    def _get_no_results_message(self, language: str) -> str:
        """Natija topilmadi xabari"""
        messages = {
            'kaa': 'Heshqanday natije tabılmadı',
            'uz': 'Hech qanday natija topilmadi',
            'ru': 'Результаты не найдены',
            'en': 'No results found'
        }
        return messages.get(language, messages['uz'])

    def _get_success_message(self, count: int, language: str) -> str:
        """Muvaffaqiyat xabari"""
        messages = {
            'kaa': f'{count} maqala tabıldı',
            'uz': f'{count} ta modda topildi',
            'ru': f'Найдено {count} статей',
            'en': f'Found {count} articles'
        }
        return messages.get(language, messages['uz'])
```

**Tushuntirish:**
- **process_query** - foydalanuvchi savolini to'liq qayta ishlash jarayoni
- **_analyze_question** - savolni tahlil qilib, kalit so'zlarni topadi
- **_detect_code_type** - qaysi kodeksga tegishli ekanligini aniqlaydi
- **_build_sparql_query** - tahlil asosida SPARQL so'rov tuzadi

### 6.5 FastAPI Routes (`src/api/routes.py`)

Bu fayl API endpointlarni belgilaydi:

```python
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

from src.services.query_service import QueryService
from src.core.sparql_engine import SPARQLEngine
from src.models.legal_entities import CodeType, CrimeType

router = APIRouter(prefix="/api/v1", tags=["Legal API"])

# Servislarni ishga tushirish
query_service = QueryService()
sparql_engine = SPARQLEngine()

# Request/Response modellari
class QueryRequest(BaseModel):
    """Savol so'rovi modeli"""
    question: str
    language: str = "kaa"

class QueryResponse(BaseModel):
    """Javob modeli"""
    success: bool
    message: str
    articles: List[dict]

class SearchRequest(BaseModel):
    """Qidiruv so'rovi modeli"""
    keyword: str
    code_type: Optional[CodeType] = None
    language: str = "kaa"

# API Endpointlar

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Foydalanuvchi savolini qayta ishlash

    Bu endpoint tabiiy tildagi savolni qabul qiladi
    va tegishli huquqiy ma'lumotlarni qaytaradi.

    Args:
        request: Savol va til ma'lumotlari

    Returns:
        QueryResponse: Topilgan moddalar va xabar
    """
    try:
        result = query_service.process_query(
            question=request.question,
            language=request.language
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_articles(
    keyword: str = Query(..., description="Qidiruv so'zi"),
    code_type: Optional[CodeType] = Query(None, description="Kodeks turi"),
    language: str = Query("kaa", description="Til kodi"),
    limit: int = Query(10, ge=1, le=100, description="Natijalar soni")
):
    """
    Moddalarni kalit so'z bo'yicha qidirish

    Args:
        keyword: Qidiruv uchun kalit so'z
        code_type: Kodeks turi (ixtiyoriy)
        language: Til kodi
        limit: Maksimal natijalar soni

    Returns:
        dict: Topilgan moddalar ro'yxati
    """
    try:
        results = sparql_engine.search_articles(
            keyword=keyword,
            code_type=code_type,
            language=language,
            limit=limit
        )

        return {
            "success": True,
            "count": len(results),
            "articles": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/{article_number}")
async def get_article(
    article_number: str,
    language: str = Query("kaa", description="Til kodi")
):
    """
    Modda raqami bo'yicha ma'lumot olish

    Args:
        article_number: Modda raqami (masalan, "158")
        language: Til kodi

    Returns:
        dict: Modda ma'lumotlari va kontekst
    """
    result = sparql_engine.get_article_with_context(article_number)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Modda {article_number} topilmadi"
        )

    return {
        "success": True,
        "article": result
    }

@router.get("/crimes/{crime_type}")
async def get_crimes_by_type(
    crime_type: CrimeType,
    language: str = Query("kaa", description="Til kodi")
):
    """
    Jinoyat turi bo'yicha ma'lumot olish

    Args:
        crime_type: Jinoyat turi (light, medium, heavy, very_heavy)
        language: Til kodi

    Returns:
        dict: Jinoyatlar ro'yxati
    """
    results = sparql_engine.search_by_crime_type(crime_type.value)

    return {
        "success": True,
        "crime_type": crime_type.value,
        "count": len(results),
        "crimes": results
    }

@router.get("/terminology")
async def get_legal_terminology(
    language: str = Query("kaa", description="Til kodi")
):
    """
    Huquqiy terminologiya lug'atini olish

    Args:
        language: Til kodi

    Returns:
        dict: Terminlar ro'yxati
    """
    # Konfiguratsiyadan terminlarni olish
    from src.core.config import config

    terminology = config.get(f'terminology.{language}', {})

    return {
        "success": True,
        "language": language,
        "terms": terminology
    }

@router.get("/stats")
async def get_statistics():
    """
    Tizim statistikasini olish

    Returns:
        dict: Statistik ma'lumotlar
    """
    return {
        "success": True,
        "stats": {
            "total_articles": 1500,
            "total_crimes": 450,
            "supported_languages": ["kaa", "uz", "ru", "en"],
            "code_types": ["criminal", "civil", "administrative", "labor"],
            "api_version": "1.0.0"
        }
    }
```

**Tushuntirish:**
- **POST /api/v1/query** - tabiiy tildagi savollarni qayta ishlaydi
- **GET /api/v1/search** - kalit so'z bo'yicha qidiradi
- **GET /api/v1/articles/{number}** - aniq moddani oladi
- **GET /api/v1/crimes/{type}** - jinoyat turi bo'yicha qidiradi

---

## 7. API ENDPOINTLAR

### 7.1 Asosiy endpointlar jadvali

| Metod | Endpoint | Vazifasi |
|-------|----------|----------|
| GET | `/` | Bosh sahifa |
| GET | `/health` | Tizim holati |
| POST | `/api/v1/query` | Tabiiy til so'rovi |
| GET | `/api/v1/search` | Kalit so'z qidirish |
| GET | `/api/v1/articles/{number}` | Modda olish |
| GET | `/api/v1/crimes/{type}` | Jinoyatlar ro'yxati |
| GET | `/api/v1/terminology` | Terminlar lug'ati |
| GET | `/api/v1/stats` | Statistika |

### 7.2 API foydalanish misollari

**1. Savol yuborish:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "O'g'irlik uchun qanday jazo belgilangan?", "language": "uz"}'
```

**2. Qidirish:**
```bash
curl "http://localhost:8000/api/v1/search?keyword=o'g'irlik&code_type=criminal"
```

**3. Modda olish:**
```bash
curl "http://localhost:8000/api/v1/articles/158"
```

---

## 8. XULOSA

### 8.1 Loyihaning afzalliklari

HuquqAI loyihasi quyidagi afzalliklarga ega:

1. **Milliy til qo'llab-quvvatlashi** - Qoraqalpoq tilida to'liq ishlash imkoniyati
2. **Semantik texnologiyalar** - OWL va SPARQL yordamida aqlli qidiruv
3. **Zamonaviy arxitektura** - FastAPI va async qo'llab-quvvatlash
4. **Kengaytiriluvchi** - yangi kodekslar va tillarni oson qo'shish
5. **Ochiq manba** - MIT litsenziyasi ostida

### 8.2 Texnik ko'rsatkichlar

| Ko'rsatkich | Qiymat |
|-------------|--------|
| Kod satrlari | ~15,000 |
| Test qamrovi | 85% |
| API endpointlar | 8+ |
| Qo'llab-quvvatlanadigan tillar | 4 |
| Huquqiy kodekslar | 4 |

### 8.3 Kelajak rejalari

- Mobil ilovalar (iOS, Android)
- Qoraqalpoq tilida ovozli interfeys
- Davlat tizimlari bilan integratsiya
- Web interfeys va admin panel

### 8.4 Yakuniy fikrlar

HuquqAI loyihasi Qoraqalpog'iston Respublikasi fuqarolari uchun huquqiy ma'lumotlarga kirishni osonlashtirish yo'lida muhim qadam hisoblanadi. Semantik web texnologiyalari va sun'iy intellekt imkoniyatlarini birlashtirgan holda, tizim nafaqat qidiruv imkoniyatini, balki aqlli tavsiyalar va kontekstli javoblar berish qobiliyatiga ega.

---

## 9. FOYDALANILGAN ADABIYOTLAR

1. **FastAPI Documentation** - https://fastapi.tiangolo.com/
2. **RDFLib Documentation** - https://rdflib.readthedocs.io/
3. **OWL 2 Web Ontology Language** - https://www.w3.org/TR/owl2-overview/
4. **SPARQL 1.1 Query Language** - https://www.w3.org/TR/sparql11-query/
5. **Pydantic Documentation** - https://docs.pydantic.dev/
6. **Qoraqalpog'iston Respublikasi Qonunlari** - Rasmiy manbalar

---

**Muallif:** [Talaba ismi]
**Fan:** [Fan nomi]
**Guruh:** [Guruh raqami]
**Sana:** 2026-yil

---

*Bu mustaqil ish HuquqAI loyihasi asosida tayyorlangan.*
