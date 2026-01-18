"""
Legal entity models for huquqAI system
Huqıqlıq ma'lumotlar modelleri
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field
from src.core.base import Entity


class CrimeType(str, Enum):
    """Crime type enumeration / Jinayat túrleri"""
    LIGHT = "light"          # Jeńil jinayat
    MEDIUM = "medium"        # Orta jinayat
    HEAVY = "heavy"          # Awır jinayat
    VERY_HEAVY = "very_heavy"  # Óte awır jinayat


class CodeType(str, Enum):
    """Legal code type / Kodeks túri"""
    CRIMINAL = "criminal"    # Jinayat Kodeksi
    CIVIL = "civil"          # Puqaralıq Kodeksi
    ADMINISTRATIVE = "administrative"  # Administrativ Kodeks
    LABOR = "labor"          # Ámek Kodeksi


class Article(Entity):
    """Legal article model / Statiya modeli"""
    number: str = Field(..., description="Article number / Statiya nomeri")
    title: str = Field(..., description="Article title / Statiya ataması")
    content: str = Field(..., description="Article content / Statiya mazmunı")
    code_type: CodeType = Field(..., description="Code type / Kodeks túri")
    language: str = Field(default="kaa", description="Language / Til")

    # Translations
    translations: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="Article translations / Tárcimeler"
    )

    # Related articles
    related_articles: List[str] = Field(
        default_factory=list,
        description="Related article IDs / Baylanıslı statiyalar"
    )

    class Config:
        schema_extra = {
            "example": {
                "number": "123",
                "title": "Jinayattıń awır túri",
                "content": "Bu statiya jinayattıń awır túrin anıqlaydı...",
                "code_type": "criminal",
                "language": "kaa"
            }
        }


class Crime(Entity):
    """Crime model / Jinayat modeli"""
    name: str = Field(..., description="Crime name / Jinayat atı")
    description: str = Field(..., description="Description / Túsinik")
    crime_type: CrimeType = Field(..., description="Crime type / Jinayat túri")
    article_id: str = Field(..., description="Related article ID / Statiya ID")

    # Punishment information
    min_punishment: Optional[str] = Field(
        None,
        description="Minimum punishment / Eń kishi jaza"
    )
    max_punishment: Optional[str] = Field(
        None,
        description="Maximum punishment / Eń úlken jaza"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Urılıq",
                "description": "Basqa adamnıń múlkin urılaw",
                "crime_type": "medium",
                "article_id": "123"
            }
        }


class Punishment(Entity):
    """Punishment model / Jaza modeli"""
    name: str = Field(..., description="Punishment name / Jaza atı")
    description: str = Field(..., description="Description / Túsinik")
    duration_min: Optional[int] = Field(
        None,
        description="Minimum duration (months) / Eń kishi múddet (aylar)"
    )
    duration_max: Optional[int] = Field(
        None,
        description="Maximum duration (months) / Eń úlken múddet (aylar)"
    )
    fine_amount: Optional[float] = Field(
        None,
        description="Fine amount / Штраф mөлшери"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Azatlıqtan ayırıw",
                "description": "Qamaw ornında saqlawish",
                "duration_min": 12,
                "duration_max": 60
            }
        }


class LegalCode(Entity):
    """Legal code model / Kodeks modeli"""
    name: str = Field(..., description="Code name / Kodeks atı")
    code_type: CodeType = Field(..., description="Code type / Kodeks túri")
    language: str = Field(default="kaa", description="Language / Til")
    articles: List[str] = Field(
        default_factory=list,
        description="Article IDs / Statiya IDleri"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Jinayat Kodeksi",
                "code_type": "criminal",
                "language": "kaa"
            }
        }


class Query(Entity):
    """User query model / Soraw modeli"""
    question: str = Field(..., description="User question / Soraw")
    language: str = Field(default="kaa", description="Language / Til")
    user_id: Optional[str] = Field(None, description="User ID / Qollanıwshı ID")

    class Config:
        schema_extra = {
            "example": {
                "question": "Jinayattıń awır túri nedir?",
                "language": "kaa"
            }
        }


class Answer(Entity):
    """Answer model / Juwap modeli"""
    query_id: str = Field(..., description="Query ID / Soraw ID")
    answer: str = Field(..., description="Answer text / Juwap texti")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score / Ыshенimlilik коэффициенти"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Source article IDs / Dálil statiyalar"
    )

    class Config:
        schema_extra = {
            "example": {
                "query_id": "q123",
                "answer": "Jinayattıń awır túri...",
                "confidence": 0.95,
                "sources": ["art123", "art456"]
            }
        }
