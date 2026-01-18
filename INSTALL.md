# huquqAI Installation Guide

This guide will help you install and set up the huquqAI legal knowledge base system.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv or virtualenv)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/huquqAI.git
cd huquqAI
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**For production:**
```bash
pip install -r requirements.txt
```

**For development (includes testing and linting tools):**
```bash
pip install -e ".[dev]"
```

**With NLP support (for advanced multilingual features):**
```bash
pip install -e ".[nlp]"
```

**With database support:**
```bash
pip install -e ".[db]"
```

**Install everything:**
```bash
pip install -e ".[dev,nlp,db]"
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# On Windows: notepad .env
# On Linux/Mac: nano .env
```

### 5. Verify Installation

```bash
# Check Python version
python --version

# Verify packages are installed
pip list | grep -E "rdflib|owlready2|SPARQLWrapper|fastapi"

# Run tests
pytest tests/
```

### 6. Initialize the System

```bash
# Create necessary directories
mkdir -p logs data/cache data/models

# Initialize the database (if using)
python scripts/init_db.py

# Load sample data (optional)
python scripts/load_sample_data.py
```

## Running the Application

### Start the API Server

```bash
# Using Python module
python -m src.api.main

# Or using the installed command
huquqai

# Or using uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## UTF-8 Encoding Verification

To ensure proper UTF-8 support for Karakalpak language:

```bash
# Check Python encoding
python -c "import sys; print(sys.getdefaultencoding())"
# Should output: utf-8

# Test Karakalpak characters
python -c "print('Nızam, Statiya, Jinayat, Jaza')"
# Should display correctly
```

## Common Issues

### Issue: UTF-8 encoding errors

**Solution:**
```bash
# Set environment variables (Windows)
set PYTHONIOENCODING=utf-8

# Set environment variables (Linux/Mac)
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Issue: Package installation fails

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install packages one by one
pip install rdflib==7.0.0
pip install owlready2==0.46
# ... etc
```

### Issue: Cannot start API server

**Solution:**
```bash
# Check if port is already in use
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Use different port
uvicorn src.api.main:app --port 8001
```

## Development Setup

### Install development tools

```bash
pip install -e ".[dev]"
```

### Configure code formatting

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Run linter
pylint src/

# Type checking
mypy src/
```

### Run tests with coverage

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=src --cov-report=html

# View coverage report
# Windows: start htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
# Mac: open htmlcov/index.html
```

## Next Steps

1. Configure your SPARQL endpoint in `.env`
2. Add legal documents to `data/knowledge/`
3. Create ontology files in `data/ontologies/`
4. Read the API documentation at `/docs`
5. Check the usage guide in `docs/usage.md`

## Getting Help

- Documentation: `docs/`
- Issues: https://github.com/yourusername/huquqAI/issues
- Email: info@huquqai.example

## License

MIT License - see LICENSE file for details
