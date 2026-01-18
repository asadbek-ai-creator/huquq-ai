"""
API routes for huquqAI system
"""

from fastapi import APIRouter, HTTPException, Query as QueryParam
from typing import Optional, List
from loguru import logger

from src.models.legal_entities import Query, Answer, Article
from src.services.query_service import QueryService
from src.services.sparql_service import SPARQLService


router = APIRouter()
query_service = QueryService()
sparql_service = SPARQLService()


@router.post("/query", response_model=Answer)
async def process_query(query: Query):
    """
    Process user query and return answer
    Qollanıwshı sorawın islep shıǵıw
    """
    try:
        answer = await query_service.execute(query)
        return answer
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_articles(
    q: str = QueryParam(..., description="Search query / Izlew sorawı"),
    lang: str = QueryParam("kaa", description="Language / Til"),
    limit: int = QueryParam(10, ge=1, le=100)
):
    """
    Search articles by keyword
    Statiyalardı kalit sóz boyınsha izlew
    """
    try:
        result = await sparql_service.search_articles(q, lang)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)

        # Limit results
        data = result.data[:limit] if result.data else []

        return {
            "query": q,
            "language": lang,
            "count": len(data),
            "results": data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/articles/{article_number}")
async def get_article(article_number: str):
    """
    Get article by number
    Statiyani nomeri boyınsha tabıw
    """
    try:
        result = await sparql_service.get_article_by_number(article_number)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Article {article_number} not found"
            )

        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Article retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crimes/{crime_type}")
async def get_crimes_by_type(
    crime_type: str = QueryParam(..., description="Crime type: light, medium, heavy, very_heavy")
):
    """
    Get crimes by type
    Jinayatlarni túri boyınsha tabıw
    """
    try:
        valid_types = ["light", "medium", "heavy", "very_heavy"]
        if crime_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid crime type. Must be one of: {', '.join(valid_types)}"
            )

        result = await sparql_service.get_crimes_by_type(crime_type)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)

        return {
            "crime_type": crime_type,
            "count": len(result.data) if result.data else 0,
            "crimes": result.data or []
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Crime retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/terminology")
async def get_terminology(lang: Optional[str] = None):
    """
    Get legal terminology
    Huqıqlıq terminologiyani алиw
    """
    from src.core.config import get_config
    config = get_config()

    terminology = config.terminology.get("karakalpak", {})
    translations = config.terminology.get("translations", {})

    if lang and lang != "kaa":
        # Return translations for specific language
        translated = {}
        for term, term_value in terminology.items():
            trans = translations.get(term, {})
            translated[term] = trans.get(lang, term_value)
        return {"language": lang, "terminology": translated}

    return {"language": "kaa", "terminology": terminology}


@router.get("/stats")
async def get_statistics():
    """
    Get system statistics
    Sistema statistikası
    """
    # This is a placeholder - implement actual statistics
    return {
        "total_articles": 0,
        "total_crimes": 0,
        "total_queries": 0,
        "supported_languages": ["kaa", "uz", "ru", "en"]
    }
