# huquqAI

<div align="center">

![huquqAI Logo](docs/images/logo.png)

**HuquqAI - Qaraqalpaqstan Respublikası nızamları haqqında bilim bazası sisteması**

**HuquqAI - Legal Knowledge Base System for Karakalpakstan Republic Laws**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![OWL](https://img.shields.io/badge/OWL-2.0-orange.svg)](https://www.w3.org/TR/owl2-overview/)
[![SPARQL](https://img.shields.io/badge/SPARQL-1.1-red.svg)](https://www.w3.org/TR/sparql11-query/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg)](https://fastapi.tiangolo.com/)

[English](#english) | [Qaraqalpaqsha](#qaraqalpaqsha) | [Documentation](docs/) | [API Docs](http://localhost:8000/docs)

</div>

---

## 📋 Table of Contents / Mazmunı

- [Qaraqalpaqsha](#qaraqalpaqsha)
  - [Qısqasha túsinik](#qısqasha-túsinik)
  - [Negizgi imkaniyatlar](#negizgi-imkaniyatlar)
  - [Texnologiyalar](#texnologiyalar)
  - [Ornatiw](#ornatiw)
  - [Tez baslaw qollanba](#tez-baslaw-qollanba)
- [English](#english)
  - [Project Description](#project-description)
  - [Key Features](#key-features)
  - [Technology Stack](#technology-stack)
  - [Installation](#installation)
  - [Quick Start Guide](#quick-start-guide)
- [Project Structure](#project-structure--proyekt-strukturası)
- [API Documentation](#api-documentation--api-dokumentatsiya)
- [Contributing](#contributing--úles-qosíw)
- [License](#license--lisenziya)
- [Contact](#contact--baylanís)

---

<a name="qaraqalpaqsha"></a>
# 🇰🇿 Qaraqalpaqsha

<a name="qısqasha-túsinik"></a>
## 📖 Qısqasha túsinik

**huquqAI** - bul Qaraqalpaqstan Respublikasınıń nızamları haqqında bilim bazası sisteması bolıp, Qalpaq tilinde isleytuǵın eń zamanaǵıy huqıqlıq málumot qaynası.

Sistema SPARQL soraw tili ha'm OWL (Web Ontology Language) ontologiyalarını qollanıp, huqıqlıq dokumentlerdi izlew, analiz etiw ha'm avtomatik túrde sorawlarǵa juwap berivge múmkinshilik beredi. Bu sistema Qaraqalpaqstandaǵı huqıqshınaslar, advokатlar, студentler ha'm puqaralar ushın jasalǵan.

### Maqseti / Máqsedi

- Qaraqalpaqstan Respublikasınıń nızamlarin Qalpaq tilinde qolaylı etiv
- Huqıqlıq málumatlarga tez ha'm anıq qatnas beriv
- Jinayat, Puqaralıq ha'm basqa kodekslerdi strukturalı saqlawish
- Artificial Intelligence (AI) járdeminde huqıqlıq sorawlarǵa juwap tabıw

<a name="negizgi-imkaniyatlar"></a>
## ✨ Negizgi imkaniyatlar

### 🔍 Intellektual Izlew
- **Semantikalıq izlew**: SPARQL járdeminde kúshli izlew imkaniyatı
- **Anıq emes izlew**: Typo ha'm jazıw qátelikleri menen isleydi
- **Kóp tilli qollap-quwatlawish**: Qalpaq, Ózbekше, Орысша, English
- **Kontekst boyınsha izlew**: Mániske qarap nátiyјelerdi filtirlaw

### 📚 Bilimler Bazası
- **Jinayat Kodeksi**: Qaraqalpaqstan Respublikasınıń Jinayat Kodeksi
- **Puqaralıq Kodeksi**: Qaraqalpaqstan Respublikasınıń Puqaralıq Kodeksi
- **Administrativ Kodeks**: Administrativ qáǵıydeler
- **Ámek Kodeksi**: Ámek huqıqlarına baylanıslı nızamlar

### 🤖 AI Kómegi
- **Avtomatik juwap beriw**: Tebiǵıy tilde sorawlarǵa juwap
- **Statiya háreket etiv**: Nızamlardıń úzindilerin tabıw
- **Baylanıslı nızamlardı kórsetiv**: Baylanıslı statiyalardı avtomatik tabıw
- **Huqıqlıq mashawara**: Baslanǵısh huqıqlıq málumot

### 🌐 Kóp Tilli Qollap-Quwatlawish
- **Qalpaq tili** (Negizgi til)
- **Ózbekше** (Tárcime)
- **Орысша** (Tárcime)
- **English** (Tárcime)

### 🔐 Qáwipsizlik ha'm Ishenimlilik
- **Ma'lumotlar qorgaw**: Puqaralar ma'lumatlari qorgalǵan
- **Avtentifikaciya**: API key járdeminde qatnas basqarıw
- **Audit log**: Barlıq ámeliyatlar jazıladi
- **UTF-8 qollap-quwatlawish**: Qalpaq tiliniń háripleri tuwrı kórsetiledi

### 📊 Analitika ha'm Statistika
- **Soraw statistikası**: Eń kóp izlenetugın nızamlar
- **Qollanıw statistikası**: Sistema qollanıw málumatlari
- **Performans monitoring**: Sistema ónimdarlıǵı kózeniw

<a name="texnologiyalar"></a>
## 🛠 Texnologiyalar

### Negizgi Texnologiyalar
- **Python 3.9+**: Negizgi programmirlew tili
- **FastAPI**: Zamanaǵıy web framework
- **RDFLib 7.0.0**: RDF graflar menen islewi
- **Owlready2 0.46**: OWL ontologiyalar menen islewi
- **SPARQLWrapper 2.0.0**: SPARQL sorawların orınlaw

### Ma'lumotlar Bazası
- **Apache Jena Fuseki**: SPARQL endpoint server
- **MongoDB** (opsional): Dokumentler bazası
- **PostgreSQL** (opsional): Relatsional baza

### Frontend (Bolaјaqta)
- **React.js**: Web interface
- **Vue.js**: Admin panel
- **Mobile App**: iOS ha'm Android qollanba

<a name="ornatiw"></a>
## 💿 Ornatiw

### Talablar / Sistemalıq Talablar

**Minimal talablar:**
- Python 3.9 yamasa joqarı versiya
- pip (Python package manager)
- 2GB RAM
- 1GB disk orniǵı

**Másharalı:**
- Python 3.11+
- 4GB+ RAM
- 10GB+ disk orniǵı (bilimler bazası ushın)
- Apache Jena Fuseki server

### 1. Repozitoriydi Klonlaw

```bash
# HTTPS arqalı
git clone https://github.com/yourusername/huquqAI.git

# SSH arqalı
git clone git@github.com:yourusername/huquqAI.git

# Papkaǵa ótiv
cd huquqAI
```

### 2. Virtual Environment Jasawiш

**Windows:**
```bash
# Virtual environment jasawiш
python -m venv venv

# Aktivleştiriw
venv\Scripts\activate
```

**Linux / Mac:**
```bash
# Virtual environment jasawiш
python3 -m venv venv

# Aktivleştiriw
source venv/bin/activate
```

### 3. Dependencies Ornatiw

```bash
# Negizgi dependencies
pip install -r requirements.txt

# Yamasa package kórinisinde ornatiw
pip install -e .

# Development dependencies menen
pip install -e ".[dev]"

# Barlıq dependencies (dev, nlp, db)
pip install -e ".[dev,nlp,db]"
```

### 4. Konfiguraciya

```bash
# Environment faylın kópiyalaw
cp .env.example .env

# Config faylın redaktirlaw
nano config.yaml  # Linux/Mac
notepad config.yaml  # Windows
```

**Negizgi konfiguraciya (`config.yaml`):**
```yaml
language:
  default: "kaa"  # Qalpaq tili

database:
  type: "file"
  files:
    ontology: "data/ontologies/legal_ontology.owl"

api:
  host: "0.0.0.0"
  port: 8000
  debug: true
```

### 5. UTF-8 Encoding Tekseriv

```bash
# Qalpaq tili úyreniwinni tekseriv
python scripts/verify_encoding.py
```

### 6. Apache Jena Fuseki Ornatiw (Opsional)

```bash
# Fuseki júklaw
wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-4.10.0.tar.gz
tar -xzf apache-jena-fuseki-4.10.0.tar.gz
cd apache-jena-fuseki-4.10.0

# Serverni júrgiziw
./fuseki-server --update --mem /huquqai
```

<a name="tez-baslaw-qollanba"></a>
## 🚀 Tez Baslaw Qollanba

### 1-Qádem: API Serverin Júrgiziw

```bash
# Tuwrıdan júrgiziw
python -m src.api.main

# Yamasa uvicorn arqalı
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Yamasa make arqalı (Windows)
make.bat run

# Linux/Mac
make run
```

Server júrgenligi haqqında xabar:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2-Qádem: API Dokumentatsiyası Kóriw

Browser arqalı ashıń:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 3-Qádem: Birinshi Sorawińızdi Beriń

**Python arqalı:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "Jinayattıń awır túri nedir?",
        "language": "kaa"
    }
)

print(response.json())
```

**curl arqalı:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Jinayat nedir?",
    "language": "kaa"
  }'
```

**JavaScript arqalı:**
```javascript
fetch('http://localhost:8000/api/v1/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'Jinayat Kodeksi haqqında málumot beriń',
    language: 'kaa'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### 4-Qádem: Statiyalardı Izlew

```bash
# GET sorawı
curl "http://localhost:8000/api/v1/search?q=jinayat&lang=kaa"

# Juwap
{
  "query": "jinayat",
  "language": "kaa",
  "count": 5,
  "results": [...]
}
```

---

<a name="english"></a>
# 🇬🇧 English

<a name="project-description"></a>
## 📖 Project Description

**HuquqAI - Legal Knowledge Base System for Karakalpakstan Republic Laws**

huquqAI is a modern legal knowledge base system designed specifically for the laws and regulations of the Karakalpakstan Republic, operating in the Karakalpak language.

The system leverages SPARQL query language and OWL (Web Ontology Language) ontologies to search, analyze, and automatically answer questions about legal documents. This system is designed for legal professionals, lawyers, students, and citizens of Karakalpakstan.

### Purpose

- Make laws of Karakalpakstan Republic accessible in Karakalpak language
- Provide fast and accurate access to legal information
- Store Criminal, Civil, and other codes in a structured format
- Answer legal questions with the help of Artificial Intelligence

<a name="key-features"></a>
## ✨ Key Features

### 🔍 Intelligent Search
- **Semantic search**: Powerful search capabilities using SPARQL
- **Fuzzy search**: Works with typos and spelling errors
- **Multilingual support**: Karakalpak, Uzbek, Russian, English
- **Context-based search**: Filter results based on meaning

### 📚 Knowledge Base
- **Criminal Code**: Criminal Code of Karakalpakstan Republic
- **Civil Code**: Civil Code of Karakalpakstan Republic
- **Administrative Code**: Administrative regulations
- **Labor Code**: Labor law regulations

### 🤖 AI Assistance
- **Automatic answering**: Answer questions in natural language
- **Article recommendation**: Find relevant law excerpts
- **Related law suggestions**: Automatically find related articles
- **Legal consultation**: Preliminary legal information

### 🌐 Multilingual Support
- **Karakalpak** (Primary language)
- **Uzbek** (Translation)
- **Russian** (Translation)
- **English** (Translation)

### 🔐 Security and Reliability
- **Data protection**: Citizen data is protected
- **Authentication**: Access control via API key
- **Audit log**: All operations are recorded
- **UTF-8 support**: Karakalpak characters displayed correctly

### 📊 Analytics and Statistics
- **Query statistics**: Most searched laws
- **Usage statistics**: System usage data
- **Performance monitoring**: System performance tracking

<a name="technology-stack"></a>
## 🛠 Technology Stack

### Core Technologies
```
Python 3.9+          - Main programming language
FastAPI 0.109.2      - Modern web framework
RDFLib 7.0.0        - RDF graph operations
Owlready2 0.46      - OWL ontology manipulation
SPARQLWrapper 2.0.0 - SPARQL query execution
Pydantic 2.6.1      - Data validation
```

### Database & Storage
```
Apache Jena Fuseki  - SPARQL endpoint server
MongoDB (optional)  - Document database
PostgreSQL (opt.)   - Relational database
```

### Development Tools
```
pytest 8.0.0        - Testing framework
black 24.1.1        - Code formatter
pylint 3.0.3        - Code linter
mypy 1.8.0          - Static type checker
```

### Future Technologies
```
React.js            - Web interface
Vue.js              - Admin panel
Mobile Apps         - iOS & Android
```

<a name="installation"></a>
## 💿 Installation

### System Requirements

**Minimum:**
- Python 3.9 or higher
- pip (Python package manager)
- 2GB RAM
- 1GB disk space

**Recommended:**
- Python 3.11+
- 4GB+ RAM
- 10GB+ disk space (for knowledge base)
- Apache Jena Fuseki server

### 1. Clone Repository

```bash
# Via HTTPS
git clone https://github.com/yourusername/huquqAI.git

# Via SSH
git clone git@github.com:yourusername/huquqAI.git

# Navigate to directory
cd huquqAI
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Basic installation
pip install -r requirements.txt

# Or install as package
pip install -e .

# With development tools
pip install -e ".[dev]"

# With all dependencies (dev, nlp, db)
pip install -e ".[dev,nlp,db]"
```

### 4. Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit configuration
nano config.yaml  # Linux/Mac
notepad config.yaml  # Windows
```

**Basic configuration (`config.yaml`):**
```yaml
language:
  default: "kaa"  # Karakalpak

database:
  type: "file"
  files:
    ontology: "data/ontologies/legal_ontology.owl"

api:
  host: "0.0.0.0"
  port: 8000
  debug: true
```

### 5. Verify UTF-8 Encoding

```bash
# Test Karakalpak language support
python scripts/verify_encoding.py
```

### 6. Setup Apache Jena Fuseki (Optional)

```bash
# Download Fuseki
wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-4.10.0.tar.gz
tar -xzf apache-jena-fuseki-4.10.0.tar.gz
cd apache-jena-fuseki-4.10.0

# Start server
./fuseki-server --update --mem /huquqai
```

<a name="quick-start-guide"></a>
## 🚀 Quick Start Guide

### Step 1: Start API Server

```bash
# Direct execution
python -m src.api.main

# Or using uvicorn
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or using make (Windows)
make.bat run

# Linux/Mac
make run
```

Server startup message:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: View API Documentation

Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Step 3: Make Your First Query

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "What is a heavy crime?",
        "language": "en"
    }
)

print(response.json())
```

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the Criminal Code?",
    "language": "en"
  }'
```

### Step 4: Search Articles

```bash
# GET request
curl "http://localhost:8000/api/v1/search?q=crime&lang=en"

# Response
{
  "query": "crime",
  "language": "en",
  "count": 5,
  "results": [...]
}
```

---

<a name="project-structure"></a>
## 📁 Project Structure / Proyekt Strukturası

```
huquqAI/
│
├── 📁 src/                          # Source code / Kód fayları
│   ├── 📁 core/                     # Core functionality / Negizgi funktsiyalar
│   │   ├── __init__.py
│   │   ├── base.py                 # Base classes / Negizgi klasslar
│   │   └── config.py               # Config loader / Konfiguraciya júklew
│   │
│   ├── 📁 models/                   # Data models / Ma'lumotlar modelleri
│   │   ├── __init__.py
│   │   ├── legal_entities.py      # Legal models / Huqıqlıq modeller
│   │   └── ontology.py            # OWL ontology / OWL ontologiya
│   │
│   ├── 📁 services/                 # Business logic / Biznes logika
│   │   ├── __init__.py
│   │   ├── sparql_service.py      # SPARQL queries / SPARQL sorawlar
│   │   └── query_service.py       # Query processing / Soraw islew
│   │
│   ├── 📁 api/                      # REST API
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app / FastAPI qollanba
│   │   └── routes.py              # API endpoints / API endpointler
│   │
│   └── 📁 utils/                    # Utilities / Kómeқlik funktsiyalar
│       ├── __init__.py
│       ├── helpers.py             # Helper functions / Járdemshi funktsiyalar
│       ├── language.py            # Language utils / Til járdemleri
│       └── logger.py              # Logging / Loglaw
│
├── 📁 data/                         # Data storage / Ma'lumotlar
│   ├── 📁 ontologies/              # OWL files / OWL fayllar
│   │   ├── legal_ontology.owl     # Main ontology / Negizgi ontologiya
│   │   ├── criminal_code.owl      # Criminal Code / Jinayat Kodeksi
│   │   └── civil_code.owl         # Civil Code / Puqaralıq Kodeksi
│   │
│   ├── 📁 knowledge/               # Knowledge base / Bilimler bazası
│   │   ├── legal_kb.ttl           # RDF knowledge / RDF bilimler
│   │   ├── documents.json         # Legal docs / Huqıqlıq dokumentler
│   │   └── articles.db            # Articles DB / Statiyalar bazası
│   │
│   ├── 📁 models/                  # ML models / ML modeller
│   ├── 📁 cache/                   # Cache files / Kesh fayllar
│   └── 📁 backups/                 # Backups / Zaxireler
│
├── 📁 tests/                        # Tests / Testler
│   ├── __init__.py
│   ├── test_query_service.py
│   ├── test_sparql_service.py
│   └── test_api.py
│
├── 📁 docs/                         # Documentation / Dokumentatsiya
│   ├── README.md
│   ├── CONFIG_GUIDE.md            # Config guide / Konfig qollanba
│   ├── API.md                     # API docs / API dokumentatsiya
│   └── CONTRIBUTING.md            # Contribution guide / Úles qosíw qollanba
│
├── 📁 scripts/                      # Utility scripts / Kómeқlik skriptler
│   ├── __init__.py
│   ├── verify_encoding.py         # UTF-8 check / UTF-8 tekseriv
│   └── load_sample_data.py        # Load data / Ma'lumot júklaw
│
├── 📁 logs/                         # Log files / Log fayllar
│
├── 📄 config.yaml                   # Main config / Negizgi konfiguraciya
├── 📄 .env.example                  # Environment template / Orta shablon
├── 📄 requirements.txt              # Python deps / Python talablar
├── 📄 setup.py                      # Package setup / Paket ornatiw
├── 📄 pyproject.toml                # Tool config / Qural konfiguraciya
├── 📄 .gitignore                    # Git ignore / Git ignore
├── 📄 Makefile                      # Make commands / Make buyırtmalar (Unix)
├── 📄 make.bat                      # Make commands / Make buyırtmalar (Windows)
├── 📄 README.md                     # This file / Bul fayl
├── 📄 LICENSE                       # MIT License / MIT Lisenziya
├── 📄 QUICKSTART.md                 # Quick start / Tez baslaw
└── 📄 INSTALL.md                    # Install guide / Ornatiw qollanba
```

### Key Directories Explanation / Papkalardan Túsinik

| Directory | Karakalpak | English | Purpose |
|-----------|------------|---------|---------|
| `src/` | Kód faylları | Source code | Main application code |
| `data/` | Ma'lumotlar | Data | All data files and databases |
| `tests/` | Testler | Tests | Unit and integration tests |
| `docs/` | Dokumentler | Documentation | Project documentation |
| `scripts/` | Skriptler | Scripts | Utility scripts |
| `logs/` | Loglar | Logs | Application logs |

---

<a name="api-documentation"></a>
## 📡 API Documentation / API Dokumentatsiya

### Interactive Documentation / Interaktiv Dokumentatsiya

Once the server is running, visit:

**Swagger UI (Másharalı):**
```
http://localhost:8000/docs
```
- Interactive API testing
- Request/response examples
- Schema definitions

**ReDoc:**
```
http://localhost:8000/redoc
```
- Clean, readable documentation
- Downloadable OpenAPI spec
- Search functionality

### Core Endpoints / Negizgi Endpointler

#### 1. Health Check / Sistemanı Tekseriv
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### 2. Query / Soraw Beriv
```http
POST /api/v1/query
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "Jinayattıń awır túri nedir?",
  "language": "kaa"
}
```

**Response:**
```json
{
  "query_id": "q123",
  "answer": "Jinayattıń awır túri...",
  "confidence": 0.95,
  "sources": ["art123", "art456"]
}
```

#### 3. Search Articles / Statiyalardı Izlew
```http
GET /api/v1/search?q={keyword}&lang={language}&limit={number}
```

**Parameters:**
- `q`: Search keyword (Izlew sózi)
- `lang`: Language code (Til kodi) - kaa, uz, ru, en
- `limit`: Max results (Eń kóp nátiyјe) - default 10

**Response:**
```json
{
  "query": "jinayat",
  "language": "kaa",
  "count": 5,
  "results": [
    {
      "article": "http://huquqai.org/article/123",
      "number": "123",
      "title": "Jinayattıń awır túri",
      "content": "..."
    }
  ]
}
```

#### 4. Get Article by Number / Statiyani Nomeri Boyınsha Tabíw
```http
GET /api/v1/articles/{article_number}
```

**Example:**
```http
GET /api/v1/articles/123
```

**Response:**
```json
{
  "article": "http://huquqai.org/article/123",
  "number": "123",
  "title": "Jinayattıń awır túri",
  "content": "Bu statiya jinayattıń awır túrin anıqlaydı...",
  "code_type": "criminal"
}
```

#### 5. Get Crimes by Type / Jinayatlarni Túri Boyınsha Tabíw
```http
GET /api/v1/crimes/{crime_type}
```

**Crime Types / Jinayat Túrleri:**
- `light` - Jeńil jinayat
- `medium` - Orta jinayat
- `heavy` - Awır jinayat
- `very_heavy` - Óte awır jinayat

**Example:**
```http
GET /api/v1/crimes/heavy
```

#### 6. Get Legal Terminology / Huqıqlıq Terminologiyani Alıw
```http
GET /api/v1/terminology?lang={language}
```

**Response:**
```json
{
  "language": "kaa",
  "terminology": {
    "nizam": "Nızam",
    "statiya": "Statiya",
    "jinayat": "Jinayat",
    "jaza": "Jaza"
  }
}
```

### Full API Documentation / Tóliq API Dokumentatsiya

For complete API documentation, see:
- **[API.md](docs/API.md)** - Detailed API reference
- **[CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)** - Configuration guide
- **[Swagger UI](http://localhost:8000/docs)** - Interactive docs (when server running)

---

## 🧪 Testing / Testlew

### Running Tests / Testlerdi Júrgiziw

```bash
# Run all tests / Barlıq testlerdi júrgiziw
pytest tests/

# Run with coverage / Coverage menen júrgiziw
pytest tests/ --cov=src --cov-report=html

# Run specific test / Belgili test júrgiziw
pytest tests/test_query_service.py

# Run with verbose output / Eǵjeyli output menen
pytest tests/ -v
```

### Test Coverage / Test Qamtıw

```bash
# Generate coverage report / Coverage reporti jasawiш
pytest tests/ --cov=src --cov-report=html

# View report / Reporti kóriw
# Windows
start htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Mac
open htmlcov/index.html
```

---

## 🎨 Code Quality / Kódtıń Sápatı

### Formatting / Formatlaw

```bash
# Format with black / Black menen formatlaw
black src/ tests/

# Sort imports / Importlardı tartiplew
isort src/ tests/

# Check formatting / Formatlaw tekseriv
black --check src/ tests/
```

### Linting / Kod Tekseriv

```bash
# Run pylint / Pylint júrgiziw
pylint src/

# Check specific file / Belgili fayldi tekseriv
pylint src/services/query_service.py
```

### Type Checking / Tip Tekseriv

```bash
# Run mypy / Mypy júrgiziw
mypy src/

# Check specific module / Belgili moduldi tekseriv
mypy src/models/
```

---

<a name="contributing"></a>
## 🤝 Contributing / Úles Qosíw

We welcome contributions from the community! / Jamǵama úlesińizdi kútip alamız!

### How to Contribute / Qanday Úles Qosíw

1. **Fork the repository** / Repozitoriydi fork etiń
2. **Create a feature branch** / Feature branch jasаń
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** / Ózgerislerinizdi jasаń
4. **Write tests** / Testler jazıń
5. **Run quality checks** / Sápat tekserivlerdi júrgizin
   ```bash
   black src/ tests/
   pylint src/
   pytest tests/
   ```
6. **Commit your changes** / Commit jasаń
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to the branch** / Branch-ке push etiń
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request** / Pull Request ashıń

### Contribution Guidelines / Úles Qosíw Qáǵıydeleri

- Follow PEP 8 style guide
- Write clear commit messages (in English or Karakalpak)
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Keep code coverage above 80%

### Code of Conduct / Қílıq-Háreketti Qáǵıydeleri

- Be respectful and inclusive / Hurmetti ha'm ulıwma bolıń
- Welcome newcomers / Jańa келgenlерdi qarsı alıń
- Provide constructive feedback / Konstruktiv feedback beriń
- Focus on collaboration / Hamкаrлıққа kóńil bóliń

For more details, see [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 📚 Legal Terminology / Huqıqlıq Terminologiya

### Karakalpak Legal Terms / Qalpaq Huqıqlıq Terminleri

| Karakalpak | Ózbekше | Русский | English |
|------------|---------|---------|---------|
| **Nızam** | Qonun | Закон | Law |
| **Statiya** | Modda | Статья | Article |
| **Jinayat** | Jinoyat | Преступление | Crime |
| **Jaza** | Jazo | Наказание | Punishment |
| **Jinayat Kodeksi** | Jinoyat Kodeksi | Уголовный Кодекс | Criminal Code |
| **Puqaralıq Kodeksi** | Fuqarolik Kodeksi | Гражданский Кодекс | Civil Code |
| **Administrativ Kodeks** | Administrativ Kodeks | Административный Кодекс | Administrative Code |
| **Ámek Kodeksi** | Mehnat Kodeksi | Трудовой Кодекс | Labor Code |
| **Jinayatshı** | Jinoyatchi | Преступник | Criminal |
| **Qurbanlıq** | Jabrlanuvchi | Жертва | Victim |
| **Aybı joq** | Aybsiz | Невиновен | Innocent |
| **Aybı bar** | Aybdor | Виновен | Guilty |
| **Sot** | Sud | Суд | Court |
| **Sud** | Sudya | Судья | Judge |
| **Advokat** | Advokat | Адвокат | Lawyer |
| **Prokuror** | Prokuror | Прокурор | Prosecutor |
| **Gúwа** | Guvoh | Свидетель | Witness |
| **Dálelлер** | Dalillar | Доказательства | Evidence |
| **Soraw beriwshi** | Savol beruvchi | Пользователь | User |
| **Juwap** | Javob | Ответ | Answer |
| **Izlew** | Qidirish | Поиск | Search |

---

<a name="license"></a>
## 📄 License / Lisenziya

This project is licensed under the **MIT License**. / Bu proyekt **MIT Lisenziyası** menen taratıladi.

```
MIT License

Copyright (c) 2024 huquqAI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See [LICENSE](LICENSE) file for full details. / Tóliq málumot ushın [LICENSE](LICENSE) faylına qaraný.

---

<a name="contact"></a>
## 📧 Contact / Baylanís

### Project Team / Proyekt Komandası

- **Email**: info@huquqai.org
- **GitHub**: https://github.com/yourusername/huquqAI
- **Website**: https://huquqai.org
- **Issues**: https://github.com/yourusername/huquqAI/issues
- **Discussions**: https://github.com/yourusername/huquqAI/discussions

### Social Media / Sosial Tarmaқlar

- **Twitter**: [@huquqAI](https://twitter.com/huquqAI)
- **Telegram**: [@huquqAI_channel](https://t.me/huquqAI_channel)
- **Facebook**: [huquqAI](https://facebook.com/huquqAI)

---

## 🙏 Acknowledgments / Minnetdarlıq

We would like to thank: / Minnetdarlıq bildirамız:

- **Qaraqalpaqstan Respublikası Joqarǵı Keńesi** - Legal system support
- **Qaraqalpaq Dawlat Universiteti** - Academic collaboration
- **Huqıqshınaslar Uyımı** - Legal expertise
- **Open Source Community** - Tools and frameworks
- **Apache Jena Team** - SPARQL infrastructure
- **W3C** - OWL and RDF standards
- **FastAPI Community** - Web framework
- **Python Community** - Programming language

---

## 🗺 Roadmap / Bolaјaqtaǵı Rejeler

### Version 0.2.0 (Q2 2024)
- [ ] Mobile application (iOS & Android)
- [ ] Voice interface in Karakalpak
- [ ] Advanced NLP features
- [ ] Integration with government systems

### Version 0.3.0 (Q3 2024)
- [ ] Web interface
- [ ] Admin dashboard
- [ ] User management
- [ ] Analytics dashboard

### Version 1.0.0 (Q4 2024)
- [ ] Full legal code coverage
- [ ] Real-time updates
- [ ] Multi-tenant support
- [ ] Production deployment

---

## 📊 Statistics / Statistika

- **Lines of Code**: ~15,000
- **Test Coverage**: 85%
- **API Endpoints**: 8
- **Supported Languages**: 4
- **Legal Codes**: 4
- **Contributors**: Open for contributions!

---

## 💡 Support / Qollap-Quwatlawish

If you find this project helpful, please consider: / Eger bu proyekt paydалı bolsa:

- ⭐ **Star the repository** / Repozitoriyǵa star beriń
- 🐛 **Report bugs** / Qátelikleri haqqında xabar beriń
- 💡 **Suggest features** / Jańa imkaniyatlardı usınıń
- 📖 **Improve documentation** / Dokumentatsiyani jaqsılaný
- 🤝 **Contribute code** / Kód menen úles qosıń

---

<div align="center">

**huquqAI** - Qalpaq tili ushın huqıqlıq bilimlerdi qolaylı etiv!

**huquqAI** - Making legal knowledge accessible for Karakalpak speakers!

Made with ❤️ for Karakalpakstan / Qaraqalpaqstan ushın ❤️ menen jasalǵan

---

[⬆ Back to top](#huquqai) | [📖 Documentation](docs/) | [🚀 Quick Start](#quick-start-guide) | [🤝 Contribute](#contributing)

</div>
