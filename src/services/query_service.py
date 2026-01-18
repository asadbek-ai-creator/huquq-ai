"""
Query service for huquqAI system
Handles user queries and natural language processing
"""

from typing import List, Dict, Any, Optional
from loguru import logger
from src.core.base import Service, QueryResult
from src.core.config import get_config
from src.services.sparql_service import SPARQLService
from src.models.legal_entities import Query, Answer


class QueryService(Service):
    """Query processing service"""

    def __init__(self):
        self.config = get_config()
        self.sparql_service = SPARQLService()
        self.terminology = self.config.terminology.get("karakalpak", {})

    async def execute(self, query: Query) -> Answer:
        """Execute user query"""
        try:
            logger.info(f"Processing query: {query.question}")

            # Extract keywords from query
            keywords = self._extract_keywords(query.question)

            # Search for relevant articles
            results = await self._search_knowledge_base(keywords, query.language)

            # Generate answer
            answer = await self._generate_answer(query, results)

            return answer

        except Exception as e:
            logger.error(f"Query execution error: {e}")
            return Answer(
                query_id=query.id or "unknown",
                answer=f"Qátelik júz berdi: {str(e)}",
                confidence=0.0,
                sources=[]
            )

    def _extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question"""
        # Simple keyword extraction
        # In production, use NLP models
        keywords = []

        # Check for legal terms
        for term_key, term_value in self.terminology.items():
            if term_value.lower() in question.lower():
                keywords.append(term_value)

        # Add words from question (simple tokenization)
        words = question.split()
        keywords.extend([w for w in words if len(w) > 3])

        return list(set(keywords))

    async def _search_knowledge_base(self, keywords: List[str],
                                     language: str) -> List[Dict[str, Any]]:
        """Search knowledge base using keywords"""
        all_results = []

        for keyword in keywords:
            result = await self.sparql_service.search_articles(keyword, language)
            if result.success and result.data:
                all_results.extend(result.data)

        # Remove duplicates
        unique_results = {r.get('article'): r for r in all_results}.values()
        return list(unique_results)

    async def _generate_answer(self, query: Query,
                               search_results: List[Dict[str, Any]]) -> Answer:
        """Generate answer from search results"""
        if not search_results:
            return Answer(
                query_id=query.id or "unknown",
                answer="Ізленген soraw boyınsha málumot tabılmadı.",
                confidence=0.0,
                sources=[]
            )

        # Simple answer generation
        # In production, use LLM for better answers
        answer_text = "Tabılǵan nátiyјeler:\n\n"
        sources = []

        for i, result in enumerate(search_results[:3], 1):
            article_number = result.get('number', 'N/A')
            title = result.get('title', 'N/A')
            content = result.get('content', '')[:200]  # First 200 chars

            answer_text += f"{i}. Statiya {article_number}: {title}\n"
            answer_text += f"   {content}...\n\n"
            sources.append(result.get('article', ''))

        confidence = min(len(search_results) / 3.0, 1.0)

        return Answer(
            query_id=query.id or "unknown",
            answer=answer_text,
            confidence=confidence,
            sources=sources
        )

    async def search(self, question: str, language: str = "kaa") -> Dict[str, Any]:
        """Search for answers (simplified interface)"""
        query = Query(question=question, language=language)
        answer = await self.execute(query)

        return {
            "question": question,
            "answer": answer.answer,
            "confidence": answer.confidence,
            "sources": answer.sources
        }
