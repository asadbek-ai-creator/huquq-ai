@echo off
REM Batch file for huquqAI project (Windows alternative to Makefile)
REM Usage: make.bat [target]

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="install-all" goto install-all
if "%1"=="verify-encoding" goto verify-encoding
if "%1"=="test" goto test
if "%1"=="test-cov" goto test-cov
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="type-check" goto type-check
if "%1"=="clean" goto clean
if "%1"=="run" goto run
if "%1"=="dev" goto dev
if "%1"=="init" goto init
goto help

:help
echo huquqAI - Legal Knowledge Base System
echo.
echo Available targets:
echo   install          - Install production dependencies
echo   install-dev      - Install with development dependencies
echo   install-all      - Install all dependencies (dev, nlp, db)
echo   verify-encoding  - Verify UTF-8 encoding support
echo   test             - Run tests
echo   test-cov         - Run tests with coverage report
echo   lint             - Run pylint
echo   format           - Format code with black and isort
echo   type-check       - Run mypy type checking
echo   clean            - Remove cache and build files
echo   run              - Start the API server
echo   dev              - Start server in development mode
echo   init             - Create necessary directories
echo.
echo Usage: make.bat [target]
goto end

:install
echo Installing production dependencies...
pip install -r requirements.txt
goto end

:install-dev
echo Installing development dependencies...
pip install -e ".[dev]"
goto end

:install-all
echo Installing all dependencies...
pip install -e ".[dev,nlp,db]"
goto end

:verify-encoding
echo Verifying UTF-8 encoding support...
python scripts\verify_encoding.py
goto end

:test
echo Running tests...
pytest tests\ -v
goto end

:test-cov
echo Running tests with coverage...
pytest tests\ -v --cov=src --cov-report=term-missing --cov-report=html
goto end

:lint
echo Running pylint...
pylint src\
goto end

:format
echo Formatting code...
black src\ tests\
isort src\ tests\
goto end

:type-check
echo Running type checking...
mypy src\
goto end

:clean
echo Cleaning cache and build files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (htmlcov) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q .coverage 2>nul
if exist build rd /s /q build
if exist dist rd /s /q dist
echo Clean complete.
goto end

:run
echo Starting API server...
python -m src.api.main
goto end

:dev
echo Starting development server...
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
goto end

:init
echo Creating necessary directories...
if not exist logs mkdir logs
if not exist data\cache mkdir data\cache
if not exist data\models mkdir data\models
if not exist data\ontologies mkdir data\ontologies
if not exist data\knowledge mkdir data\knowledge
echo Directories created.
goto end

:end
