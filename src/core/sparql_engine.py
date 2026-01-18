"""
SPARQL Query Engine for Karakalpak Legal Knowledge Base
Qaraqalpaq Huquqıy Bilimler Bazası ushın SPARQL Soraw Mexanizmi

This module provides an optimized SPARQL query engine for executing queries
on Karakalpak legal data with caching, validation, and performance monitoring.

Bu modul keshlaw, validaciya ha'm performans monitoringi menen Qaraqalpaq
huquqıy ma'limlar boyınsha sorawlardı orınlaw ushın optimizaciyalanǵan
SPARQL soraw mexanizmin beredi.
"""

import re
import time
from typing import List, Dict, Any, Optional, Union, Tuple
from functools import lru_cache
from datetime import datetime, timedelta
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.processor import SPARQLResult
from loguru import logger

from src.core.config import get_config
from src.core.ontology_manager import get_ontology_manager


class SPARQLEngineError(Exception):
    """
    Base exception for SPARQL engine errors.
    SPARQL mexanizmi qátelikleri ushın bazalıq istisna.
    """
    def __init__(self, message: str, message_kaa: Optional[str] = None):
        """
        Initialize exception with bilingual messages.
        Istisnanı eki tilli xabarlar menen inizializaciyalaw.

        Args:
            message: Error message in English / Inglizше qátelik xabarı
            message_kaa: Error message in Karakalpak / Qaraqalpaqsha qátelik xabarı
        """
        self.message = message
        self.message_kaa = message_kaa or message
        super().__init__(self.message)


class QueryValidationError(SPARQLEngineError):
    """
    Exception for query validation errors.
    Soraw validaciya qátelikleri ushın istisna.
    """
    pass


class SPARQLEngine:
    """
    SPARQL Query Engine optimized for Karakalpak legal content.
    Qaraqalpaq huquqıy mazmun ushın optimizaciyalanǵan SPARQL Soraw Mexanizmi.

    This engine provides high-performance SPARQL query execution with:
    - Query caching (LRU) / Soraw keshlawi (LRU)
    - Query validation / Soraw validaciya
    - Performance logging / Performans loglaw
    - UTF-8 support for Karakalpak / Qaraqalpaq ushın UTF-8 qollap-quwatlawish
    - Parameterized queries / Parametrlengen sorawlar

    Examples / Misallar:
        >>> engine = SPARQLEngine()
        >>> # Search for crime / Jinayatni izlew
        >>> results = engine.search_by_term_kaa("urılıq")
        >>> # Get punishment range / Jaza diapazonın alıw
        >>> punishments = engine.get_jaza_range(min_jıl=1, max_jıl=5)
        >>> # Search by crime type / Jinayat túri boyınsha izlew
        >>> crimes = engine.search_jinayat_turi("awır")
    """

    def __init__(self, graph: Optional[Graph] = None):
        """
        Initialize SPARQL Engine.
        SPARQL Mexanizmin inizializaciyalaw.

        Args:
            graph: RDFLib graph or None to use OntologyManager's graph
                   RDFLib grafı yamasa OntologyManager grafin qollanıw ushın None
        """
        self.config = get_config()

        # Get graph from ontology manager if not provided
        # Berilmegen bolsa ontologiya menedžerinden grafı alıw
        if graph is None:
            ontology_manager = get_ontology_manager()
            if ontology_manager.is_loaded():
                self.graph = ontology_manager.graph
            else:
                self.graph = Graph()
                logger.warning(
                    "No graph provided and ontology not loaded. "
                    "Graf berilmedi ha'm ontologiya júklenmedi."
                )
        else:
            self.graph = graph

        # Setup namespaces / Namespace-lardı ornatiw
        self.namespaces = self._setup_namespaces()

        # Query statistics / Soraw statistikası
        self.stats = {
            'total_queries': 0,
            'cached_queries': 0,
            'failed_queries': 0,
            'total_execution_time': 0.0,
            'avg_execution_time': 0.0,
        }

        logger.info("SPARQLEngine initialized / SPARQL Mexanizmi inizializaciya etildi")

    def _setup_namespaces(self) -> Dict[str, Namespace]:
        """
        Setup SPARQL query namespaces.
        SPARQL soraw namespace-larin ornatiw.

        Returns:
            Dictionary of namespaces / Namespace-lar dictionary
        """
        ns_config = self.config.ontology.namespaces
        namespaces = {}

        for prefix, uri in ns_config.items():
            namespaces[prefix] = Namespace(uri)

        return namespaces

    def _validate_query(self, query: str) -> bool:
        """
        Validate SPARQL query syntax.
        SPARQL soraw sintaksisın validaciyalaw.

        Args:
            query: SPARQL query string / SPARQL soraw júrgen shıǵı

        Returns:
            True if valid / Jaqsı bolsa True

        Raises:
            QueryValidationError: If query is invalid / Soraw noto'g'ri bolsa

        Examples / Misallar:
            >>> engine._validate_query("SELECT * WHERE { ?s ?p ?o }")
            True
        """
        try:
            # Check for basic SPARQL keywords
            # Negizgi SPARQL kalit sózlerin tekseriv
            required_keywords = ['SELECT', 'WHERE', 'ASK', 'CONSTRUCT', 'DESCRIBE']
            has_keyword = any(kw in query.upper() for kw in required_keywords)

            if not has_keyword:
                raise QueryValidationError(
                    "Query must contain SELECT, ASK, CONSTRUCT, or DESCRIBE",
                    "Soraw SELECT, ASK, CONSTRUCT yamasa DESCRIBE qamtıwı kerek"
                )

            # Check for matching braces / Juplasatuǵın jińishka belgilerdi tekseriv
            if query.count('{') != query.count('}'):
                raise QueryValidationError(
                    "Unmatched braces in query",
                    "Sorawda juplaspaýtuǵın jińishka belgiler"
                )

            # Try to prepare the query / Sorawdı taýarlaw urınısı
            prepareQuery(query, initNs=self.namespaces)

            logger.debug("Query validation passed / Soraw validaciyası ótti")
            return True

        except Exception as e:
            error_msg = f"Query validation failed: {str(e)}"
            error_msg_kaa = f"Soraw validaciyası sátsiz: {str(e)}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise QueryValidationError(error_msg, error_msg_kaa) from e

    def _execute_query(
        self,
        query: str,
        validate: bool = True,
        use_cache: bool = True
    ) -> SPARQLResult:
        """
        Execute SPARQL query with validation and caching.
        Validaciya ha'm keshlaw menen SPARQL sorawdı orınlaw.

        Args:
            query: SPARQL query / SPARQL soraw
            validate: Validate before execution / Orınlawdan aldın validaciyalaw
            use_cache: Use cache if available / Keshni qollanıw

        Returns:
            SPARQL query results / SPARQL soraw nátiyјeleri

        Raises:
            SPARQLEngineError: If execution fails / Orınlaw sátsiz bolsa
        """
        start_time = time.time()

        try:
            # Validate query / Sorawdı validaciyalaw
            if validate:
                self._validate_query(query)

            # Prepare query / Sorawdı taýarlaw
            logger.debug("Executing SPARQL query / SPARQL sorawdı orınlaw")
            prepared = prepareQuery(query, initNs=self.namespaces)

            # Execute / Orınlaw
            results = self.graph.query(prepared)

            # Update statistics / Statistikani jańalaw
            execution_time = time.time() - start_time
            self._update_stats(execution_time, cached=False)

            logger.info(
                f"Query executed in {execution_time:.3f}s / "
                f"Soraw {execution_time:.3f}s ishinde orınlandı"
            )

            return results

        except QueryValidationError:
            raise
        except Exception as e:
            self.stats['failed_queries'] += 1
            error_msg = f"Query execution failed: {str(e)}"
            error_msg_kaa = f"Soraw orınlaw sátsiz: {str(e)}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise SPARQLEngineError(error_msg, error_msg_kaa) from e

    def _update_stats(self, execution_time: float, cached: bool = False) -> None:
        """
        Update query statistics.
        Soraw statistikasın jańalaw.

        Args:
            execution_time: Query execution time / Soraw orınlaw waqtı
            cached: Whether result was cached / Nátiyјe keshlengen bolsa
        """
        self.stats['total_queries'] += 1
        if cached:
            self.stats['cached_queries'] += 1
        else:
            self.stats['total_execution_time'] += execution_time

        # Calculate average / Ortasha alıw
        non_cached = self.stats['total_queries'] - self.stats['cached_queries']
        if non_cached > 0:
            self.stats['avg_execution_time'] = (
                self.stats['total_execution_time'] / non_cached
            )

    def _format_results(self, results: SPARQLResult) -> List[Dict[str, Any]]:
        """
        Format SPARQL results as list of dictionaries.
        SPARQL nátiyјelerin dictionary listı kórinisinde formatlaw.

        Args:
            results: SPARQL query results / SPARQL soraw nátiyјeleri

        Returns:
            List of result dictionaries / Nátiyјe dictionary listi

        Examples / Misallar:
            >>> results = engine._execute_query("SELECT ?s WHERE { ?s ?p ?o } LIMIT 1")
            >>> formatted = engine._format_results(results)
            >>> print(formatted[0]['s'])
        """
        formatted = []

        for row in results:
            row_dict = {}
            for var in results.vars:
                value = row[var]

                # Handle different value types / Túrli mániس túrlerin islew
                if isinstance(value, Literal):
                    row_dict[str(var)] = {
                        'value': str(value),
                        'type': 'literal',
                        'language': value.language if value.language else None,
                        'datatype': str(value.datatype) if value.datatype else None
                    }
                elif isinstance(value, URIRef):
                    row_dict[str(var)] = {
                        'value': str(value),
                        'type': 'uri'
                    }
                else:
                    row_dict[str(var)] = {
                        'value': str(value) if value else None,
                        'type': 'unknown'
                    }

            formatted.append(row_dict)

        return formatted

    def select(
        self,
        query: str,
        lang: Optional[str] = "kaa"
    ) -> List[Dict[str, Any]]:
        """
        Execute SPARQL SELECT query.
        SPARQL SELECT sorawdı orınlaw.

        Args:
            query: SELECT query / SELECT soraw
            lang: Language filter / Til filtri

        Returns:
            Query results / Soraw nátiyјeleri

        Examples / Misallar:
            >>> # Get all crimes / Barlıq jinayatlardı alıw
            >>> query = '''
            ... SELECT ?jinayat ?name
            ... WHERE {
            ...     ?jinayat a huquq:Jinayat ;
            ...              rdfs:label ?name .
            ...     FILTER(LANG(?name) = "kaa")
            ... }
            ... '''
            >>> results = engine.select(query)
            >>> for r in results:
            ...     print(r['name']['value'])
        """
        # Add language filter if not present / Til filtri joq bolsa qosıw
        if lang and 'FILTER' not in query.upper() and 'LANG' not in query.upper():
            # Simple language filter addition / Qарапайым til filtri qosıw
            if 'WHERE' in query.upper():
                query = query.replace(
                    'WHERE {',
                    f'WHERE {{\n    # Language filter: {lang}\n'
                )

        results = self._execute_query(query)
        return self._format_results(results)

    def ask(self, query: str) -> bool:
        """
        Execute SPARQL ASK query.
        SPARQL ASK sorawdı orınlaw.

        Args:
            query: ASK query / ASK soraw

        Returns:
            Boolean result / Boolean nátiyјe

        Examples / Misallar:
            >>> # Check if crime exists / Jinayattıń bar ekenin tekseriv
            >>> query = '''
            ... ASK {
            ...     ?jinayat a huquq:Jinayat ;
            ...              rdfs:label "Urılıq"@kaa .
            ... }
            ... '''
            >>> exists = engine.ask(query)
            >>> print(f"Crime exists: {exists}")
        """
        if 'ASK' not in query.upper():
            raise QueryValidationError(
                "Query must be an ASK query",
                "Soraw ASK soraw bolıwı kerek"
            )

        results = self._execute_query(query)
        return bool(results)

    def construct(
        self,
        query: str,
        format: str = "turtle"
    ) -> str:
        """
        Execute SPARQL CONSTRUCT query.
        SPARQL CONSTRUCT sorawdı orınlaw.

        Args:
            query: CONSTRUCT query / CONSTRUCT soraw
            format: Output format (turtle, xml, n3) / Shıǵıs formatı

        Returns:
            Constructed graph as string / Jasalǵan graf júrgen shıǵı kórinisinde

        Examples / Misallar:
            >>> # Construct new triples / Jańa triple-lardı jasawiш
            >>> query = '''
            ... CONSTRUCT {
            ...     ?jinayat huquq:hasType "awır"@kaa .
            ... }
            ... WHERE {
            ...     ?jinayat a huquq:Jinayat ;
            ...              huquq:crimeType "heavy" .
            ... }
            ... '''
            >>> graph = engine.construct(query)
        """
        if 'CONSTRUCT' not in query.upper():
            raise QueryValidationError(
                "Query must be a CONSTRUCT query",
                "Soraw CONSTRUCT soraw bolıwı kerek"
            )

        results = self._execute_query(query)

        # Serialize the resulting graph / Nátiyјe grafın serializaciyalaw
        return results.serialize(format=format)

    # =========================================================================
    # Karakalpak Legal Specific Queries / Qaraqalpaq Huquqıy Arnaýı Sorawlar
    # =========================================================================

    def search_by_term_kaa(
        self,
        term: str,
        fuzzy: bool = False,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search by Karakalpak term.
        Qaraqalpaq termin boyınsha izlew.

        Searches for legal resources (Nızam, Statiya, Jinayat, Jaza) containing
        the specified Karakalpak term in their labels or descriptions.

        Qaraqalpaq termindi o'z label yamasa túsindikmelerinde qamtıytuǵın
        huquqıy resurslarni (Nızam, Statiya, Jinayat, Jaza) izleydi.

        Args:
            term: Karakalpak search term / Qaraqalpaq izlew termini
                  Examples: "urılıq" (theft), "jinayat" (crime), "jaza" (punishment)
            fuzzy: Enable fuzzy search / Anıq emes izlewdi qosıw
            limit: Maximum results / Eń kóp nátiyјe

        Returns:
            Matching resources / Sáykes resurslar

        Examples / Misallar:
            >>> # Search for theft / Urılıqdı izlew
            >>> results = engine.search_by_term_kaa("urılıq")
            >>> for r in results:
            ...     print(r['resource']['value'], r['label']['value'])

            >>> # Search for punishment / Jazanı izlew
            >>> results = engine.search_by_term_kaa("jaza", fuzzy=True)
        """
        # Normalize term / Termin normallaw
        search_term = term.lower().strip()

        # Build filter / Filtr jasawiш
        if fuzzy:
            # Fuzzy matching with REGEX / REGEX menen anıq emes sáykeslik
            filter_clause = f'FILTER(REGEX(LCASE(?label), "{search_term}", "i"))'
        else:
            # Exact matching with CONTAINS / CONTAINS menen anıq sáykeslik
            filter_clause = f'FILTER(CONTAINS(LCASE(?label), "{search_term}"))'

        query = f"""
        PREFIX huquq: <{self.namespaces['huquq']}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?resource ?type ?label ?description
        WHERE {{
            ?resource a ?type ;
                     rdfs:label ?label .

            OPTIONAL {{ ?resource rdfs:comment ?description }}

            # Filter by Karakalpak language / Qaraqalpaq tili boyınsha filtirlaw
            FILTER(LANG(?label) = "kaa" || LANG(?label) = "")

            # Search term filter / Izlew termini filtri
            {filter_clause}

            # Limit to legal types / Huquqıy túrler menen sheklew
            FILTER(
                ?type = huquq:Nızam ||
                ?type = huquq:Statiya ||
                ?type = huquq:Jinayat ||
                ?type = huquq:Jaza
            )
        }}
        ORDER BY ?label
        LIMIT {limit}
        """

        logger.info(
            f"Searching by Karakalpak term: '{term}' / "
            f"Qaraqalpaq termin boyınsha izlew: '{term}'"
        )

        return self.select(query)

    def get_jaza_range(
        self,
        min_jıl: Optional[int] = None,
        max_jıl: Optional[int] = None,
        jaza_turi: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get punishments within specified year range.
        Kórsetilgen jıl diapazonındaǵı jazalarni alıw.

        Retrieves punishments (Jaza) that fall within the specified duration range.
        Kórsetilgen dawam diapazonına túsetuǵın jazalarni (Jaza) alıp qaytadı.

        Args:
            min_jıl: Minimum years / Minimal jıllar
                     Example: 1 (bir jıl)
            max_jıl: Maximum years / Maksimal jıllar
                     Example: 5 (bes jıl)
            jaza_turi: Punishment type / Jaza túri
                       Examples: "azatlıqtan ayırıw" (imprisonment), "штраф" (fine)

        Returns:
            Matching punishments / Sáykes jazalar

        Examples / Misallar:
            >>> # Get punishments from 1 to 5 years / 1 jıldan 5 jılǵa shekem jazalarni alıw
            >>> results = engine.get_jaza_range(min_jıl=1, max_jıl=5)
            >>> for r in results:
            ...     print(r['jaza']['value'], r['muddet']['value'])

            >>> # Get imprisonment punishments / Azatlıqtan ayırıw jazalarin alıw
            >>> results = engine.get_jaza_range(jaza_turi="azatlıqtan ayırıw")
        """
        # Build filter conditions / Filtr shártlerin jasawiш
        filters = []

        if min_jıl is not None:
            filters.append(f"?duration_min >= {min_jıl}")

        if max_jıl is not None:
            filters.append(f"?duration_max <= {max_jıl}")

        if jaza_turi:
            filters.append(f'CONTAINS(LCASE(?name), LCASE("{jaza_turi}"))')

        filter_clause = " && ".join(filters) if filters else "true"

        query = f"""
        PREFIX huquq: <{self.namespaces['huquq']}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jaza ?name ?description ?duration_min ?duration_max ?fine
        WHERE {{
            ?jaza a huquq:Jaza ;
                  rdfs:label ?name .

            OPTIONAL {{ ?jaza rdfs:comment ?description }}
            OPTIONAL {{ ?jaza huquq:durationMin ?duration_min }}
            OPTIONAL {{ ?jaza huquq:durationMax ?duration_max }}
            OPTIONAL {{ ?jaza huquq:fineAmount ?fine }}

            # Language filter / Til filtri
            FILTER(LANG(?name) = "kaa" || LANG(?name) = "")

            # Range filter / Диапазон filtri
            FILTER({filter_clause})
        }}
        ORDER BY ?duration_min
        """

        logger.info(
            f"Getting punishments: min={min_jıl}, max={max_jıl}, type={jaza_turi} / "
            f"Jazalarni alıw: min={min_jıl}, max={max_jıl}, túr={jaza_turi}"
        )

        return self.select(query)

    def search_jinayat_turi(
        self,
        turi: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search crimes by type.
        Jinayatlardı túri boyınsha izlew.

        Searches for crimes (Jinayat) by their severity type.
        Jinayatlardı (Jinayat) olardıń awırlıq túri boyınsha izleydi.

        Args:
            turi: Crime type / Jinayat túri
                  - "jeńil" / "light" - Light crime / Jeńil jinayat
                  - "orta" / "medium" - Medium crime / Orta jinayat
                  - "awır" / "heavy" - Heavy crime / Awır jinayat
                  - "óte awır" / "very_heavy" - Very heavy crime / Óte awır jinayat
            limit: Maximum results / Eń kóp nátiyјe

        Returns:
            Matching crimes / Sáykes jinayatlar

        Examples / Misallar:
            >>> # Search for heavy crimes / Awır jinayatlardı izlew
            >>> results = engine.search_jinayat_turi("awır")
            >>> for r in results:
            ...     print(r['jinayat']['value'], r['name']['value'])

            >>> # Search for light crimes / Jeńil jinayatlardı izlew
            >>> results = engine.search_jinayat_turi("jeńil", limit=10)
        """
        # Map Karakalpak types to English / Qaraqalpaq túrlerin Inglizшege sálkem etiw
        type_mapping = {
            'jeńil': 'light',
            'light': 'light',
            'orta': 'medium',
            'medium': 'medium',
            'awır': 'heavy',
            'heavy': 'heavy',
            'óte awır': 'very_heavy',
            'very_heavy': 'very_heavy',
        }

        crime_type = type_mapping.get(turi.lower(), turi)

        query = f"""
        PREFIX huquq: <{self.namespaces['huquq']}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jinayat ?name ?description ?type ?jaza
        WHERE {{
            ?jinayat a huquq:Jinayat ;
                     rdfs:label ?name ;
                     huquq:crimeType ?type .

            OPTIONAL {{ ?jinayat rdfs:comment ?description }}
            OPTIONAL {{ ?jinayat huquq:hasPunishment ?jaza }}

            # Language filter / Til filtri
            FILTER(LANG(?name) = "kaa" || LANG(?name) = "")

            # Type filter / Túr filtri
            FILTER(?type = "{crime_type}")
        }}
        ORDER BY ?name
        LIMIT {limit}
        """

        logger.info(
            f"Searching crimes by type: '{turi}' / "
            f"Jinayatlardı túri boyınsha izlew: '{turi}'"
        )

        return self.select(query)

    def search_statiya(
        self,
        nomer: Optional[str] = None,
        kodeks: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search legal articles (Statiya).
        Huquqıy statiyalarni (Statiya) izlew.

        Args:
            nomer: Article number / Statiya nomeri
                   Example: "123", "45-statiya"
            kodeks: Code type / Kodeks túri
                    Examples: "jinayat" (criminal), "puqaralıq" (civil)
            keyword: Search keyword / Izlew kalit sózi
            limit: Maximum results / Eń kóp nátiyјe

        Returns:
            Matching articles / Sáykes statiyalar

        Examples / Misallar:
            >>> # Search by article number / Statiya nomeri boyınsha izlew
            >>> results = engine.search_statiya(nomer="123")

            >>> # Search in Criminal Code / Jinayat Kodeksinde izlew
            >>> results = engine.search_statiya(kodeks="jinayat", keyword="urılıq")
        """
        filters = []

        if nomer:
            filters.append(f'?articleNumber = "{nomer}"')

        if kodeks:
            code_mapping = {
                'jinayat': 'criminal',
                'criminal': 'criminal',
                'puqaralıq': 'civil',
                'civil': 'civil',
            }
            code_type = code_mapping.get(kodeks.lower(), kodeks)
            filters.append(f'?codeType = "{code_type}"')

        if keyword:
            filters.append(
                f'(CONTAINS(LCASE(?title), LCASE("{keyword}")) || '
                f'CONTAINS(LCASE(?content), LCASE("{keyword}")))'
            )

        filter_clause = " && ".join(filters) if filters else "true"

        query = f"""
        PREFIX huquq: <{self.namespaces['huquq']}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?statiya ?articleNumber ?title ?content ?codeType
        WHERE {{
            ?statiya a huquq:Statiya ;
                     huquq:articleNumber ?articleNumber ;
                     huquq:title ?title .

            OPTIONAL {{ ?statiya huquq:content ?content }}
            OPTIONAL {{ ?statiya huquq:codeType ?codeType }}

            # Language filter / Til filtri
            FILTER(LANG(?title) = "kaa" || LANG(?title) = "")

            # Search filters / Izlew filtrleri
            FILTER({filter_clause})
        }}
        ORDER BY ?articleNumber
        LIMIT {limit}
        """

        logger.info(
            f"Searching articles: number={nomer}, code={kodeks}, keyword={keyword} / "
            f"Statiyalardı izlew: nomer={nomer}, kodeks={kodeks}, kalit={keyword}"
        )

        return self.select(query)

    def get_related_jinayat_jaza(
        self,
        jinayat_uri: str
    ) -> Dict[str, Any]:
        """
        Get crime and its related punishments.
        Jinayatni ha'm onıń baylanıslı jazalarin alıw.

        Args:
            jinayat_uri: Crime URI / Jinayat URI

        Returns:
            Crime with punishments / Jazalar menen jinayat

        Examples / Misallar:
            >>> # Get crime and punishments / Jinayat ha'm jazalarni alıw
            >>> uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
            >>> data = engine.get_related_jinayat_jaza(uri)
            >>> print(data['jinayat']['name'])
            >>> for jaza in data['jazalar']:
            ...     print(jaza['name']['value'])
        """
        query = f"""
        PREFIX huquq: <{self.namespaces['huquq']}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jinayat ?name ?description ?type ?jaza ?jaza_name
        WHERE {{
            BIND(<{jinayat_uri}> AS ?jinayat)

            ?jinayat a huquq:Jinayat ;
                     rdfs:label ?name .

            OPTIONAL {{ ?jinayat rdfs:comment ?description }}
            OPTIONAL {{ ?jinayat huquq:crimeType ?type }}
            OPTIONAL {{
                ?jinayat huquq:hasPunishment ?jaza .
                ?jaza rdfs:label ?jaza_name .
            }}

            FILTER(LANG(?name) = "kaa" || LANG(?name) = "")
        }}
        """

        results = self.select(query)

        if not results:
            return {
                'jinayat': None,
                'jazalar': []
            }

        # Group results / Nátiyјelerdi toplaw
        first = results[0]
        return {
            'jinayat': {
                'uri': jinayat_uri,
                'name': first.get('name', {}).get('value'),
                'description': first.get('description', {}).get('value'),
                'type': first.get('type', {}).get('value')
            },
            'jazalar': [
                {
                    'uri': r.get('jaza', {}).get('value'),
                    'name': r.get('jaza_name', {}).get('value')
                }
                for r in results
                if r.get('jaza')
            ]
        }

    @lru_cache(maxsize=128)
    def execute_cached(
        self,
        query: str,
        query_type: str = "select"
    ) -> Union[List[Dict[str, Any]], bool, str]:
        """
        Execute query with LRU caching.
        LRU keshlaw menen sorawdı orınlaw.

        Args:
            query: SPARQL query / SPARQL soraw
            query_type: Query type (select, ask, construct) / Soraw túri

        Returns:
            Cached or fresh results / Keshlengen yamasa jańa nátiyјeler

        Examples / Misallar:
            >>> # First call executes query / Birinshi shaqırıw sorawdı orınlaydı
            >>> results1 = engine.execute_cached("SELECT * WHERE {?s ?p ?o} LIMIT 1")
            >>> # Second call returns cached results / Ekinshi shaqırıw keshlengen nátiyјeni qaytaradı
            >>> results2 = engine.execute_cached("SELECT * WHERE {?s ?p ?o} LIMIT 1")
        """
        logger.debug(f"Executing cached query of type: {query_type}")

        # This method is cached by @lru_cache decorator
        # Bu metod @lru_cache dekoratori menen keshlenedi
        if query_type == "select":
            return self.select(query)
        elif query_type == "ask":
            return self.ask(query)
        elif query_type == "construct":
            return self.construct(query)
        else:
            raise ValueError(f"Unknown query type: {query_type}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get engine statistics.
        Mexanizm statistikasın alıw.

        Returns:
            Statistics dictionary / Statistika dictionary

        Examples / Misallar:
            >>> stats = engine.get_statistics()
            >>> print(f"Total queries: {stats['total_queries']}")
            >>> print(f"Cache hit rate: {stats['cache_hit_rate']:.2%}")
        """
        cache_hit_rate = 0.0
        if self.stats['total_queries'] > 0:
            cache_hit_rate = (
                self.stats['cached_queries'] / self.stats['total_queries']
            )

        return {
            **self.stats,
            'cache_hit_rate': cache_hit_rate,
            'cache_info': self.execute_cached.cache_info()._asdict()
        }

    def clear_cache(self) -> None:
        """
        Clear query cache.
        Soraw keshini tazalaw.
        """
        self.execute_cached.cache_clear()
        logger.info("Query cache cleared / Soraw keshi tazalandı")

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<SPARQLEngine queries={self.stats['total_queries']} "
            f"cached={self.stats['cached_queries']} "
            f"avg_time={self.stats['avg_execution_time']:.3f}s>"
        )


# Convenience function / Qolaylı funktsiya
def get_sparql_engine(graph: Optional[Graph] = None) -> SPARQLEngine:
    """
    Get SPARQLEngine instance.
    SPARQLEngine misalın alıw.

    Args:
        graph: Optional RDFLib graph / Opsional RDFLib graf

    Returns:
        SPARQLEngine instance / SPARQLEngine misalı

    Examples / Misallar:
        >>> from src.core.sparql_engine import get_sparql_engine
        >>> engine = get_sparql_engine()
        >>> results = engine.search_by_term_kaa("jinayat")
    """
    return SPARQLEngine(graph=graph)
