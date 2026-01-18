"""
Setup configuration for huquqAI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#") and not line.startswith("# ")
    ]

setup(
    name="huquqai",
    version="0.1.0",
    author="huquqAI Team",
    author_email="info@huquqai.example",
    description="Legal Knowledge Base System for Karakalpak Language using SPARQL and OWL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/huquqAI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Karakalpak",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black==24.1.1",
            "pylint==3.0.3",
            "mypy==1.8.0",
            "pytest==8.0.0",
            "pytest-cov==4.1.0",
            "pytest-asyncio==0.23.4",
            "isort==5.13.2",
            "pre-commit==3.6.0",
        ],
        "nlp": [
            "sentence-transformers==2.3.1",
            "transformers==4.37.2",
            "langdetect==1.0.9",
            "torch==2.1.2",
        ],
        "db": [
            "sqlalchemy==2.0.25",
            "pymongo==4.6.1",
            "psycopg2-binary==2.9.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "huquqai=src.api.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
