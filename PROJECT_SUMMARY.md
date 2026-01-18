# huquqAI Project Summary

## Overview

**huquqAI** is a professional legal knowledge base system designed for the Karakalpak language, using SPARQL queries and OWL ontologies. The system follows clean architecture principles and supports multilingual legal document search and question answering.

## Key Features

✅ **Karakalpak Language Support** - Full UTF-8 encoding with native Karakalpak legal terminology
✅ **Semantic Web Technologies** - RDF, OWL, and SPARQL for intelligent knowledge representation
✅ **RESTful API** - FastAPI-based modern API with automatic documentation
✅ **Clean Architecture** - Separated concerns with layers for core, models, services, and API
✅ **Production Ready** - Pinned dependencies, comprehensive testing, and code quality tools
✅ **Multilingual** - Support for Karakalpak, Uzbek, Russian, and English

## Technology Stack

### Core Dependencies (Production)
```
rdflib==7.0.0              # RDF/OWL graph management
owlready2==0.46            # OWL ontology reasoning
SPARQLWrapper==2.0.0       # SPARQL query execution
fastapi==0.109.2           # Web framework
pydantic==2.6.1            # Data validation
python-dotenv==1.0.1       # Configuration management
pyyaml==6.0.1              # YAML configuration
loguru==0.7.2              # Logging
uvicorn==0.27.1            # ASGI server
```

### Development Tools
```
pytest==8.0.0              # Testing framework
black==24.1.1              # Code formatting
pylint==3.0.3              # Code linting
mypy==1.8.0                # Type checking
isort==5.13.2              # Import sorting
```

## Project Structure

```
huquqAI/
│
├── src/                           # Source code
│   ├── __init__.py
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── base.py               # Base classes (Entity, Repository, Service)
│   │   └── config.py             # Configuration loader
│   │
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   ├── legal_entities.py    # Legal domain models
│   │   └── ontology.py          # OWL ontology manager
│   │
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── sparql_service.py    # SPARQL query service
│   │   └── query_service.py     # NLP query processing
│   │
│   ├── api/                       # REST API
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   └── routes.py            # API endpoints
│   │
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── helpers.py           # Helper functions
│       ├── language.py          # Language utilities
│       └── logger.py            # Logging setup
│
├── data/                          # Data storage
│   ├── ontologies/               # OWL ontology files
│   │   └── README.md
│   ├── knowledge/                # Legal documents
│   │   └── README.md
│   ├── cache/                    # Cache files
│   └── models/                   # ML models
│
├── tests/                         # Test suite
│   ├── __init__.py
│   └── test_query_service.py
│
├── docs/                          # Documentation
│   └── README.md
│
├── scripts/                       # Utility scripts
│   ├── __init__.py
│   └── verify_encoding.py       # UTF-8 encoding verification
│
├── logs/                          # Log files
│
├── config.yaml                    # Main configuration
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
├── pyproject.toml                 # Tool configurations
├── .gitignore                     # Git ignore rules
│
├── README.md                      # Main documentation (bilingual)
├── INSTALL.md                     # Installation guide
├── QUICKSTART.md                  # Quick start guide
├── PROJECT_SUMMARY.md             # This file
│
├── Makefile                       # Unix/Linux commands
└── make.bat                       # Windows commands
```

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/api/v1/query` | Process user query |
| GET | `/api/v1/search` | Search articles |
| GET | `/api/v1/articles/{number}` | Get article by number |
| GET | `/api/v1/crimes/{type}` | Get crimes by type |
| GET | `/api/v1/terminology` | Get legal terminology |
| GET | `/api/v1/stats` | Get system statistics |

### Documentation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

## Data Models

### Core Entities

1. **Article** - Legal article model
   - Fields: number, title, content, code_type, language, translations
   - Represents individual legal articles

2. **Crime** - Criminal offense model
   - Fields: name, description, crime_type, article_id, punishments
   - Represents criminal offenses

3. **Punishment** - Punishment model
   - Fields: name, description, duration_min, duration_max, fine_amount
   - Represents legal punishments

4. **LegalCode** - Legal code model
   - Fields: name, code_type, language, articles
   - Represents legal code collections

5. **Query** - User query model
   - Fields: question, language, user_id
   - Represents user questions

6. **Answer** - Answer model
   - Fields: query_id, answer, confidence, sources
   - Represents system responses

## Configuration

### Main Config (config.yaml)

```yaml
application:
  name: huquqAI
  version: 0.1.0

language:
  default: kaa
  supported: [kaa, uz, ru, en]

terminology:
  karakalpak:
    nizam: "Nızam"
    statiya: "Statiya"
    jinayat: "Jinayat"
    jaza: "Jaza"
    # ... more terms
```

### Environment (.env)

```bash
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
DEFAULT_LANGUAGE=kaa
SPARQL_ENDPOINT=http://localhost:3030/huquqai/sparql
```

## Karakalpak Legal Terminology

| Karakalpak | Uzbek | Russian | English |
|------------|-------|---------|---------|
| Nızam | Qonun | Закон | Law |
| Statiya | Modda | Статья | Article |
| Jinayat | Jinoyat | Преступление | Crime |
| Jaza | Jazo | Наказание | Punishment |
| Jinayat Kodeksi | Jinoyat Kodeksi | Уголовный Кодекс | Criminal Code |
| Puqaralıq Kodeksi | Fuqarolik Kodeksi | Гражданский Кодекс | Civil Code |
| Soraw beriwshi | Savol beruvchi | Пользователь | User |
| Juwap | Javob | Ответ | Answer |
| Izlew | Qidirish | Поиск | Search |
| Jinayattıń awır túri | Og'ir jinoyat | Тяжкое преступление | Heavy crime |

## Development Workflow

### 1. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Verify UTF-8 encoding
python scripts/verify_encoding.py
```

### 2. Code Quality Workflow

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
pylint src/

# Type check
mypy src/

# Run tests
pytest tests/ --cov=src
```

### 3. Development Server

```bash
# Start development server
uvicorn src.api.main:app --reload

# Or use make command
make dev  # Unix/Linux/Mac
make.bat dev  # Windows
```

## Testing

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Test UTF-8 Encoding
```bash
python scripts/verify_encoding.py
```

## Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Set `APP_ENV=production` in `.env`
- [ ] Configure SPARQL endpoint
- [ ] Set up database (if using)
- [ ] Add legal documents to `data/knowledge/`
- [ ] Create OWL ontologies in `data/ontologies/`
- [ ] Configure logging paths
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Enable HTTPS
- [ ] Configure CORS origins
- [ ] Set up monitoring
- [ ] Configure backups

## Performance Considerations

- Use connection pooling for SPARQL endpoints
- Implement caching for frequently accessed articles
- Use async operations for I/O-bound tasks
- Index legal documents for faster search
- Consider using Redis for session management
- Monitor API response times

## Security Considerations

- Validate all user inputs
- Sanitize SPARQL queries to prevent injection
- Use environment variables for sensitive data
- Implement rate limiting
- Enable CORS with specific origins
- Use HTTPS in production
- Regular security audits

## Future Enhancements

1. **NLP Integration**: Add advanced NLP for better question understanding
2. **Vector Search**: Implement semantic search using embeddings
3. **Multi-tenancy**: Support multiple legal jurisdictions
4. **Mobile App**: Develop mobile application
5. **Real-time Updates**: WebSocket support for live updates
6. **Analytics**: Usage analytics and reporting
7. **Voice Interface**: Voice-based queries in Karakalpak
8. **Machine Learning**: Automated document classification

## Contributing

See `CONTRIBUTING.md` for contribution guidelines.

## License

MIT License - See `LICENSE` file for details.

## Support

- **Documentation**: `/docs` directory
- **Issues**: GitHub Issues
- **Email**: info@huquqai.example

## Acknowledgments

- Karakalpak legal terminology contributors
- Open source community
- RDF/OWL standards organizations

---

**Version**: 0.1.0
**Last Updated**: 2024
**Maintained by**: huquqAI Team
