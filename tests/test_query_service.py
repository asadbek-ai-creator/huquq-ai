"""
Tests for query service
"""

import pytest
from src.models.legal_entities import Query
from src.services.query_service import QueryService


@pytest.fixture
def query_service():
    """Create query service instance"""
    return QueryService()


@pytest.mark.asyncio
async def test_extract_keywords(query_service):
    """Test keyword extraction"""
    question = "Jinayattıń awır túri nedir?"
    keywords = query_service._extract_keywords(question)

    assert len(keywords) > 0
    assert any("jinayat" in k.lower() for k in keywords)


@pytest.mark.asyncio
async def test_search_interface(query_service):
    """Test search interface"""
    result = await query_service.search(
        question="Jinayat nedir?",
        language="kaa"
    )

    assert "question" in result
    assert "answer" in result
    assert "confidence" in result
    assert result["question"] == "Jinayat nedir?"


@pytest.mark.asyncio
async def test_execute_query(query_service):
    """Test query execution"""
    query = Query(
        question="Statiya 123 nedir?",
        language="kaa"
    )

    answer = await query_service.execute(query)

    assert answer is not None
    assert hasattr(answer, "answer")
    assert hasattr(answer, "confidence")
    assert isinstance(answer.confidence, float)
    assert 0.0 <= answer.confidence <= 1.0
