"""
SPARQL query service for huquqAI system
"""

from typing import List, Dict, Any, Optional
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from loguru import logger
from src.core.config import get_config
from src.core.base import Service, QueryResult


class SPARQLService(Service):
    """SPARQL query service"""

    def __init__(self):
        self.config = get_config()
        self.endpoint = SPARQLWrapper(self.config.sparql.endpoint)
        self.endpoint.setReturnFormat(JSON)
        self.update_endpoint = SPARQLWrapper(self.config.sparql.update_endpoint)
        self.update_endpoint.setMethod(POST)

    async def execute(self, query: str, is_update: bool = False) -> QueryResult:
        """Execute SPARQL query"""
        try:
            if is_update:
                return await self._execute_update(query)
            else:
                return await self._execute_select(query)
        except Exception as e:
            logger.error(f"SPARQL query error: {e}")
            return QueryResult(
                success=False,
                data=None,
                message=f"Query execution failed: {str(e)}"
            )

    async def _execute_select(self, query: str) -> QueryResult:
        """Execute SELECT query"""
        try:
            self.endpoint.setQuery(query)
            results = self.endpoint.query().convert()

            bindings = results.get("results", {}).get("bindings", [])
            processed_results = self._process_results(bindings)

            return QueryResult(
                success=True,
                data=processed_results,
                metadata={"count": len(processed_results)}
            )
        except Exception as e:
            logger.error(f"SELECT query error: {e}")
            raise

    async def _execute_update(self, query: str) -> QueryResult:
        """Execute UPDATE query"""
        try:
            self.update_endpoint.setQuery(query)
            self.update_endpoint.query()

            return QueryResult(
                success=True,
                data=None,
                message="Update executed successfully"
            )
        except Exception as e:
            logger.error(f"UPDATE query error: {e}")
            raise

    def _process_results(self, bindings: List[Dict]) -> List[Dict[str, Any]]:
        """Process SPARQL query results"""
        processed = []
        for binding in bindings:
            row = {}
            for key, value in binding.items():
                row[key] = value.get("value")
            processed.append(row)
        return processed

    async def search_articles(self, keyword: str, language: str = "kaa") -> QueryResult:
        """Search articles by keyword"""
        query = f"""
        PREFIX huquq: <{self.config.ontology.base_uri}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?article ?number ?title ?content
        WHERE {{
            ?article a huquq:Statiya ;
                     huquq:articleNumber ?number ;
                     huquq:title ?title ;
                     huquq:content ?content .

            FILTER (
                CONTAINS(LCASE(?title), LCASE("{keyword}")) ||
                CONTAINS(LCASE(?content), LCASE("{keyword}"))
            )
        }}
        LIMIT {self.config.search.max_results}
        """

        return await self.execute(query)

    async def get_article_by_number(self, article_number: str) -> QueryResult:
        """Get article by number"""
        query = f"""
        PREFIX huquq: <{self.config.ontology.base_uri}>

        SELECT ?article ?title ?content ?codeType
        WHERE {{
            ?article a huquq:Statiya ;
                     huquq:articleNumber "{article_number}" ;
                     huquq:title ?title ;
                     huquq:content ?content ;
                     huquq:codeType ?codeType .
        }}
        """

        return await self.execute(query)

    async def get_crimes_by_type(self, crime_type: str) -> QueryResult:
        """Get crimes by type"""
        query = f"""
        PREFIX huquq: <{self.config.ontology.base_uri}>

        SELECT ?crime ?name ?description ?punishment
        WHERE {{
            ?crime a huquq:Jinayat ;
                   huquq:name ?name ;
                   huquq:description ?description ;
                   huquq:crimeType "{crime_type}" .

            OPTIONAL {{
                ?crime huquq:hasPunishment ?punishment .
            }}
        }}
        """

        return await self.execute(query)

    async def get_related_articles(self, article_id: str) -> QueryResult:
        """Get related articles"""
        query = f"""
        PREFIX huquq: <{self.config.ontology.base_uri}>

        SELECT ?relatedArticle ?number ?title
        WHERE {{
            <{article_id}> huquq:relatedTo ?relatedArticle .
            ?relatedArticle huquq:articleNumber ?number ;
                           huquq:title ?title .
        }}
        """

        return await self.execute(query)
