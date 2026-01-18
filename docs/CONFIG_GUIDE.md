# huquqAI Configuration Guide / Konfiguraciya Qollanba

This guide explains how to configure the huquqAI legal knowledge base system.
Bu qollanba huquqAI huqıqlıq bilimler bazası sistemasın qanday sazlawdı túsindiredi.

## Table of Contents / Mazmunı

1. [Overview / Umumiy túsinik](#overview)
2. [Database Configuration / Baza sazlawı](#database-configuration)
3. [SPARQL Endpoint Setup / SPARQL endpoint ornatiw](#sparql-endpoint-setup)
4. [API Settings / API sazlawları](#api-settings)
5. [Logging Configuration / Loglaw sazlawı](#logging-configuration)
6. [Reasoning Engine / Sebep-saldar mexanizmi](#reasoning-engine)
7. [Language Settings / Til sazlawları](#language-settings)

---

## Overview / Umumiy túsinik

The `config.yaml` file contains all system settings organized into logical sections with bilingual comments (English and Karakalpak).

`config.yaml` faylı sistema sazlawlarınıń barlıǵın eki tilli túsinilikler menen logikaǵa kiredi.

### File Location / Fayldıń orını
```
huquqAI/
└── config.yaml
```

### Loading Configuration / Konfiguraciya júklaw

```python
from src.core.config import get_config

# Load configuration / Konfiguraciya júklaw
config = get_config()

# Access settings / Sazlawlarǵa qatnas
api_host = config.api.host
db_path = config.database.files.ontology
```

---

## Database Configuration / Baza sazlawı

### Database Types / Baza túrleri

The system supports three database types:
Sistema úsh baza túrin qollap-quwatlaydı:

1. **File-based** (Default / Áhmiyetli)
2. **MongoDB**
3. **PostgreSQL**

### File-based Database / Fayl negizli baza

```yaml
database:
  type: "file"
  files:
    # Main ontology / Negizgi ontologiya
    ontology: "data/ontologies/legal_ontology.owl"

    # Criminal Code / Jinayat Kodeksi
    criminal_code: "data/ontologies/criminal_code.owl"

    # Civil Code / Puqaralıq Kodeksi
    civil_code: "data/ontologies/civil_code.owl"

    # Knowledge base / Bilimler bazası
    knowledge_base: "data/knowledge/legal_kb.ttl"
```

**File Formats / Fayl formatlari:**
- `.owl` - OWL format ontology
- `.ttl` - Turtle format RDF
- `.json` - JSON format documents
- `.db` - SQLite database

### MongoDB Configuration / MongoDB sazlawı

```yaml
database:
  type: "mongodb"
  mongodb:
    host: "localhost"
    port: 27017
    database: "huquqai_db"
    username: "${MONGO_USER}"
    password: "${MONGO_PASSWORD}"
```

**Environment Variables / Orta ózgeriywshiler:**
```bash
export MONGO_USER=your_username
export MONGO_PASSWORD=your_password
```

### PostgreSQL Configuration / PostgreSQL sazlawı

```yaml
database:
  type: "postgresql"
  postgresql:
    host: "localhost"
    port: 5432
    database: "huquqai_db"
    user: "huquqai_user"
    password: "${DB_PASSWORD}"
```

---

## SPARQL Endpoint Setup / SPARQL endpoint ornatiw

### Apache Jena Fuseki Setup / Apache Jena Fuseki ornatiw

1. **Download Jena Fuseki** / Jena Fuseki júklaw
   ```bash
   wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-4.x.x.tar.gz
   tar -xzf apache-jena-fuseki-4.x.x.tar.gz
   cd apache-jena-fuseki-4.x.x
   ```

2. **Start Fuseki Server** / Fuseki serverin júrgiziw
   ```bash
   # Unix/Linux/Mac
   ./fuseki-server --update --mem /huquqai

   # Windows
   fuseki-server.bat --update --mem /huquqai
   ```

3. **Configure Endpoints** / Endpoint sazlaw
   ```yaml
   sparql:
     endpoint: "http://localhost:3030/huquqai/sparql"
     update_endpoint: "http://localhost:3030/huquqai/update"
     graph_store: "http://localhost:3030/huquqai/data"
   ```

### SPARQL Settings / SPARQL sazlawları

```yaml
sparql:
  # Query timeout / Soraw waqtı shegi
  timeout: 30

  # Retry on failure / Qátelik boyınsha qayta urınıs
  retry_count: 3
  retry_delay: 2

  # Enable caching / Keshlawdi qosıw
  cache:
    enabled: true
    ttl: 3600  # 1 hour / 1 saat
    max_size: 100
```

### Named Graphs / Atamalı graflar

```yaml
sparql:
  graphs:
    criminal_law: "http://huquqai.org/graph/criminal"
    civil_law: "http://huquqai.org/graph/civil"
    administrative_law: "http://huquqai.org/graph/administrative"
```

**Usage Example / Qollanıw misalı:**
```python
from src.services.sparql_service import SPARQLService

service = SPARQLService()
query = """
PREFIX huquq: <http://huquqai.org/ontology#>
SELECT ?crime ?type
FROM <http://huquqai.org/graph/criminal>
WHERE {
    ?crime a huquq:Jinayat ;
           huquq:crimeType ?type .
}
"""
result = await service.execute(query)
```

---

## API Settings / API sazlawları

### Basic API Configuration / Negizgi API sazlawı

```yaml
api:
  host: "0.0.0.0"  # Listen on all interfaces / Barlıq interfeyslerde tıńlaw
  port: 8000       # Default port / Áhmiyetli port
  debug: true      # Enable debug mode / Debug tártipti qosıw
  reload: true     # Auto-reload on changes / Ózgeriste avto-qayta júklew
```

### CORS Configuration / CORS sazlawı

```yaml
api:
  cors:
    enabled: true
    origins:
      - "http://localhost:3000"
      - "https://yourdomain.com"
    allow_credentials: true
    allow_methods: ["GET", "POST", "PUT", "DELETE"]
```

### Rate Limiting / Limit sheklew

```yaml
api:
  rate_limit:
    enabled: true
    requests_per_minute: 60
    requests_per_hour: 1000
    requests_per_day: 10000
```

### Starting the API Server / API serverin júrgiziw

```bash
# Using Python / Python arqalı
python -m src.api.main

# Using uvicorn directly / Uvicorn arqalı tuwrıdan
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Using make / Make arqalı
make run  # Unix/Linux/Mac
make.bat run  # Windows
```

---

## Logging Configuration / Loglaw sazlawı

### Log Levels / Log deńgeyleri

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

**Level Descriptions / Deńgey túsinikleri:**

| Level | English | Karakalpak | Usage |
|-------|---------|------------|-------|
| DEBUG | Detailed information | Eǵjeyli málumot | Development |
| INFO | General information | Umumiy málumot | Production |
| WARNING | Warning messages | Eskertpeler | Potential issues |
| ERROR | Error messages | Qátelik xabarları | Errors |
| CRITICAL | Critical errors | Kritik qátelikler | System failures |

### Log Files / Log faylları

```yaml
logging:
  file: "logs/huquqai.log"           # Main log / Negizgi log
  error_file: "logs/error.log"       # Errors only / Tek qátelikler
  access_file: "logs/access.log"     # API access / API qatnas
  query_file: "logs/sparql_queries.log"  # SPARQL queries
```

### Log Rotation / Log aylanıw

```yaml
logging:
  rotation: "10 MB"      # Rotate when file reaches 10MB
  retention: "30 days"   # Keep logs for 30 days
  compression: "zip"     # Compress old logs
```

### Component-Specific Logging / Komponent boyınsha loglaw

```yaml
logging:
  components:
    api: "INFO"
    database: "INFO"
    sparql: "DEBUG"     # More detailed for SPARQL
    reasoner: "INFO"
    ontology: "INFO"
```

---

## Reasoning Engine / Sebep-saldar mexanizmi

### Enable Reasoning / Sebep-saldar shıǵarıwdı qosıw

```yaml
reasoning:
  enabled: true
  reasoner: "HermiT"  # Options: HermiT, Pellet, FaCT++, ELK
  profile: "OWL2_DL"  # Options: OWL2_DL, OWL2_EL, OWL2_QL, OWL2_RL
```

### Reasoner Types / Sebep-saldar shıǵarıwshı túrleri

| Reasoner | Performance | Expressiveness | Best For |
|----------|-------------|----------------|----------|
| **HermiT** | Medium | High | Complete OWL2 DL |
| **Pellet** | Medium | High | OWL2 + Rules |
| **ELK** | Fast | Medium | OWL2 EL profile |
| **FaCT++** | Fast | High | Large ontologies |

### Inference Settings / Xulasa jasawish sazlawları

```yaml
reasoning:
  inference:
    infer_properties: true   # Infer property values
    infer_classes: true      # Infer class membership
    infer_transitive: true   # Transitive properties
    infer_inverse: true      # Inverse properties
```

### Consistency Checking / Uyǵınlıǵın tekseriv

```yaml
reasoning:
  consistency_check:
    enabled: true
    on_load: true      # Check when loading ontology
    on_update: true    # Check after updates
```

### Performance Tuning / Ónimdarlıǵın sazlaw

```yaml
reasoning:
  timeout: 120          # Maximum 2 minutes
  memory_limit: 2048    # 2GB memory limit
  cache_results: true   # Cache reasoning results
  optimization:
    level: "medium"     # low, medium, high
    parallel: true      # Use parallel processing
```

---

## Language Settings / Til sazlawları

### Supported Languages / Qollanılatuǵın tiller

```yaml
language:
  default: "kaa"  # Karakalpak
  supported:
    - "kaa"  # Karakalpak
    - "uz"   # Uzbek
    - "ru"   # Russian
    - "en"   # English
  auto_detect: true
  fallback: "kaa"
```

### Language Codes / Til kodleri

| Code | Language | Native Name |
|------|----------|-------------|
| kaa | Karakalpak | Qaraqalpaq tili |
| uz | Uzbek | Oʻzbek tili |
| ru | Russian | Русский язык |
| en | English | English |

### Using Language Settings / Til sazlawların qollanıw

```python
from src.utils.language import LanguageUtils

lang_utils = LanguageUtils()

# Get supported languages
languages = lang_utils.get_supported_languages()

# Translate term
translated = lang_utils.translate_term("Nızam", from_lang="kaa", to_lang="en")
# Output: "Law"

# Detect language
detected = lang_utils.detect_language("Jinayat nedir?")
# Output: "kaa"
```

---

## Environment Variables / Orta ózgeriywshiler

Many sensitive settings can be overridden using environment variables:

### Create .env file / .env faylın jasawiш

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env  # or notepad .env on Windows
```

### Common Environment Variables

```bash
# Application
APP_ENV=production
APP_DEBUG=false

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
DB_PASSWORD=your_secure_password
MONGO_USER=mongodb_user
MONGO_PASSWORD=mongodb_password

# Security
SECRET_KEY=your-secret-key-here

# SPARQL
SPARQL_ENDPOINT=http://localhost:3030/huquqai/sparql
```

---

## Configuration Validation / Konfiguraciya tekseriv

### Validate Configuration / Konfiguraciyani tekseriv

```python
from src.core.config import get_config

try:
    config = get_config()
    print("✓ Configuration loaded successfully")
    print(f"  Database type: {config.database.type}")
    print(f"  API host: {config.api.host}:{config.api.port}")
    print(f"  Default language: {config.language.default}")
except Exception as e:
    print(f"✗ Configuration error: {e}")
```

### Check Required Files / Kerekli fayllarni tekseriv

```bash
# Run verification script
python scripts/verify_encoding.py
```

---

## Troubleshooting / Qáteliklerdi sheshiv

### Common Issues / Kóp ushıraytugın qátelikler

**1. Configuration file not found**
```
Error: Configuration file not found: config.yaml
Solution: Ensure config.yaml is in the root directory
```

**2. Invalid YAML syntax**
```
Error: YAML parsing error
Solution: Check indentation and syntax in config.yaml
```

**3. Missing environment variables**
```
Error: Environment variable not set: DB_PASSWORD
Solution: Set variable in .env file or export it
```

**4. SPARQL endpoint connection failed**
```
Error: Cannot connect to SPARQL endpoint
Solution: Ensure Fuseki server is running on the specified port
```

---

## Examples / Misallar

### Example 1: Development Setup

```yaml
application:
  environment: "development"
  debug: true

api:
  host: "localhost"
  port: 8000
  reload: true

logging:
  level: "DEBUG"
  console:
    enabled: true
```

### Example 2: Production Setup

```yaml
application:
  environment: "production"
  debug: false

api:
  host: "0.0.0.0"
  port: 80
  reload: false
  workers: 4

logging:
  level: "WARNING"
  console:
    enabled: false

security:
  enabled: true
  https_only: true
```

---

## Best Practices / Eń jaqsı tácriyбeler

1. **Never commit sensitive data** / Sezimtalli ma'lumotlardı hesh waqıt commit etpeń
   - Use environment variables for passwords
   - Keep `.env` in `.gitignore`

2. **Use appropriate log levels** / Muwapisli log deńgeylerdi qollanıń
   - DEBUG for development
   - INFO for production
   - ERROR for critical systems

3. **Enable caching in production** / Ishlab shıǵarıwda keshlawdi qosıń
   - Improves performance
   - Reduces database load

4. **Regular backups** / Mizamli zaxire jasawish
   - Enable automatic backups
   - Test restore procedures

5. **Monitor logs** / Loglardi monitoring etiv
   - Check for errors regularly
   - Set up alerts for critical issues

---

## Additional Resources / Qosımsha resurslar

- [Apache Jena Fuseki Documentation](https://jena.apache.org/documentation/fuseki2/)
- [OWL 2 Web Ontology Language](https://www.w3.org/TR/owl2-overview/)
- [SPARQL Query Language](https://www.w3.org/TR/sparql11-query/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Last Updated**: 2024
**Version**: 1.0
**Maintained by**: huquqAI Team
