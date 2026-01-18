# huquqAI Quick Start Guide

Get up and running with huquqAI in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Quick Installation

### 1. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify UTF-8 Encoding

```bash
python scripts/verify_encoding.py
```

You should see:
```
✓ ALL TESTS PASSED
Your system is properly configured for Karakalpak language!
```

### 4. Configure Environment

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` if needed (default values work for development).

### 5. Start the Server

**Using make (Windows):**
```cmd
make.bat run
```

**Using make (Linux/Mac):**
```bash
make run
```

**Or directly:**
```bash
python -m src.api.main
```

### 6. Test the API

Open your browser and visit:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Quick API Examples

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

### 2. Get Terminology

```bash
curl http://localhost:8000/api/v1/terminology
```

### 3. Search Articles

```bash
curl "http://localhost:8000/api/v1/search?q=jinayat&lang=kaa"
```

### 4. Ask a Question (using Python)

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

### 5. Ask a Question (using curl)

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Jinayat nedir?",
    "language": "kaa"
  }'
```

## Development Commands

### Run Tests
```bash
# Windows
make.bat test

# Linux/Mac
make test
```

### Format Code
```bash
# Windows
make.bat format

# Linux/Mac
make format
```

### Run Linter
```bash
# Windows
make.bat lint

# Linux/Mac
make lint
```

### Clean Cache
```bash
# Windows
make.bat clean

# Linux/Mac
make clean
```

## Project Structure

```
huquqAI/
├── src/               # Source code
│   ├── api/          # REST API endpoints
│   ├── core/         # Core functionality
│   ├── models/       # Data models & ontology
│   ├── services/     # Business logic
│   └── utils/        # Utilities
├── data/             # Data files
│   ├── ontologies/   # OWL files
│   └── knowledge/    # Legal documents
├── tests/            # Test files
└── docs/             # Documentation
```

## Key Files

- `config.yaml` - Main configuration file
- `.env` - Environment variables
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Tool configurations

## Karakalpak Legal Terminology

| Karakalpak | English | Usage |
|------------|---------|-------|
| Nızam | Law | Legal statute |
| Statiya | Article | Legal article |
| Jinayat | Crime | Criminal offense |
| Jaza | Punishment | Legal punishment |
| Jinayat Kodeksi | Criminal Code | Criminal law code |
| Puqaralıq Kodeksi | Civil Code | Civil law code |
| Soraw beriwshi | User/Questioner | Person asking questions |
| Juwap | Answer | Response |
| Izlew | Search | Search operation |
| Jinayattıń awır túri | Heavy crime | Serious criminal offense |

## Next Steps

1. **Add Legal Data**: Place legal documents in `data/knowledge/`
2. **Create Ontology**: Define legal concepts in `data/ontologies/`
3. **Configure SPARQL**: Set up your SPARQL endpoint in `.env`
4. **Customize**: Modify `config.yaml` for your needs
5. **Read Documentation**: Check `docs/` for detailed guides

## Troubleshooting

### UTF-8 Encoding Issues

**Windows:**
```cmd
set PYTHONIOENCODING=utf-8
chcp 65001
```

**Linux/Mac:**
```bash
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Port Already in Use

Change the port in `.env`:
```
API_PORT=8001
```

Or run with different port:
```bash
uvicorn src.api.main:app --port 8001
```

### Package Installation Fails

Upgrade pip first:
```bash
pip install --upgrade pip setuptools wheel
```

## Getting Help

- 📖 Full documentation: `INSTALL.md`
- 🐛 Report issues: GitHub Issues
- 📧 Email: info@huquqai.example

## License

MIT License - See LICENSE file for details

---

**Happy coding with huquqAI!** 🚀
