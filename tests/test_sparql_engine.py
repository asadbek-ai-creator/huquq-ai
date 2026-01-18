"""
Tests for SPARQLEngine
SPARQLEngine ushın testler

This module tests the SPARQL query engine functionality with Karakalpak legal data.
Bu modul Qaraqalpaq huquqıy ma'limleri menen SPARQL soraw mexanizmi funktsiyasın test etedi.
"""

import pytest
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

from src.core.sparql_engine import (
    SPARQLEngine,
    SPARQLEngineError,
    QueryValidationError
)
from src.core.ontology_manager import OntologyManager


@pytest.fixture
def sample_graph(tmp_path):
    """
    Create a sample RDF graph with Karakalpak legal data for testing.
    Test etiw ushın Qaraqalpaq huquqıy ma'limleri menen RDF grafın jasawıش.
    """
    # Create ontology file
    ontology_content = """<?xml version="1.0"?>
<rdf:RDF xmlns="http://huquqai.org/ontology#"
     xml:base="http://huquqai.org/ontology"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#">

    <owl:Ontology rdf:about="http://huquqai.org/ontology">
        <rdfs:label xml:lang="kaa">Huquqıy Ontologiya</rdfs:label>
        <rdfs:label xml:lang="en">Legal Ontology</rdfs:label>
    </owl:Ontology>

    <!-- Classes / Klasslar -->
    <owl:Class rdf:about="http://huquqai.org/ontology#Jinayat">
        <rdfs:label xml:lang="kaa">Jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Crime</rdfs:label>
        <rdfs:comment xml:lang="kaa">Jinayat túsinigi</rdfs:comment>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Jaza">
        <rdfs:label xml:lang="kaa">Jaza</rdfs:label>
        <rdfs:label xml:lang="en">Punishment</rdfs:label>
        <rdfs:comment xml:lang="kaa">Huquqıy jaza</rdfs:comment>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Statiya">
        <rdfs:label xml:lang="kaa">Statiya</rdfs:label>
        <rdfs:label xml:lang="en">Article</rdfs:label>
    </owl:Class>

    <!-- Properties / Xassalar -->
    <owl:ObjectProperty rdf:about="http://huquqai.org/ontology#hasPunishment">
        <rdfs:label xml:lang="kaa">jazaǵa iye</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:range rdf:resource="http://huquqai.org/ontology#Jaza"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#crimeType">
        <rdfs:label xml:lang="kaa">jinayat túri</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#minYears">
        <rdfs:label xml:lang="kaa">minimal jıllar</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#maxYears">
        <rdfs:label xml:lang="kaa">maksimal jıllar</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#articleNumber">
        <rdfs:label xml:lang="kaa">statiya nomeri</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Statiya"/>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#codeType">
        <rdfs:label xml:lang="kaa">kodeks túri</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Statiya"/>
    </owl:DatatypeProperty>

    <!-- Individuals / Individuallar -->

    <!-- Crime 1: Theft / Urılıq -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Urılıq">
        <rdfs:label xml:lang="kaa">Urılıq</rdfs:label>
        <rdfs:label xml:lang="en">Theft</rdfs:label>
        <rdfs:comment xml:lang="kaa">Basqa adamdıń menshigin urlaw</rdfs:comment>
        <crimeType>orta</crimeType>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Urılıq"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Urılıq">
        <rdfs:label xml:lang="kaa">Urılıq ushın jaza</rdfs:label>
        <rdfs:comment xml:lang="kaa">1 ten 5 jılǵa shekemgi azatlıqtan ayırıw</rdfs:comment>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">5</maxYears>
    </Jaza>

    <!-- Crime 2: Light crime / Jeńil jinayat -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Jeńil">
        <rdfs:label xml:lang="kaa">Jeńil jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Light crime</rdfs:label>
        <crimeType>jeńil</crimeType>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Jeńil"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Jeńil">
        <rdfs:label xml:lang="kaa">Jeńil jinayat ushın jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">0</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</maxYears>
    </Jaza>

    <!-- Crime 3: Severe crime / Awır jinayat -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Awır">
        <rdfs:label xml:lang="kaa">Awır jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Severe crime</rdfs:label>
        <crimeType>awır</crimeType>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Awır"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Awır">
        <rdfs:label xml:lang="kaa">Awır jinayat ushın jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">5</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">15</maxYears>
    </Jaza>

    <!-- Article examples / Statiya misalları -->
    <Statiya rdf:about="http://huquqai.org/ontology#Statiya_123">
        <rdfs:label xml:lang="kaa">Statiya 123</rdfs:label>
        <articleNumber>123</articleNumber>
        <codeType>JK</codeType>
        <rdfs:comment xml:lang="kaa">Jinayat Kodeksi 123-statiya</rdfs:comment>
    </Statiya>

    <Statiya rdf:about="http://huquqai.org/ontology#Statiya_456">
        <rdfs:label xml:lang="kaa">Statiya 456</rdfs:label>
        <articleNumber>456</articleNumber>
        <codeType>AK</codeType>
        <rdfs:comment xml:lang="kaa">Administrativlik Kodeksi 456-statiya</rdfs:comment>
    </Statiya>

</rdf:RDF>
"""

    ontology_file = tmp_path / "test_ontology.owl"
    ontology_file.write_text(ontology_content, encoding='utf-8')

    # Load into OntologyManager
    manager = OntologyManager()
    manager.clear()
    manager.load_ontology(ontology_file)

    return manager.graph


@pytest.fixture
def engine(sample_graph):
    """
    Create SPARQLEngine instance with sample graph.
    Misaldı graf menen SPARQLEngine misalın jasawıш.
    """
    eng = SPARQLEngine(sample_graph)
    yield eng
    # Clear cache after each test
    eng.clear_cache()


class TestSPARQLEngine:
    """Test suite for SPARQLEngine / SPARQLEngine test toplamı"""

    def test_initialization(self, sample_graph):
        """
        Test engine initialization.
        Mexanizm inizializaciyasın test etiw.
        """
        engine = SPARQLEngine(sample_graph)

        assert engine is not None
        assert engine.graph is sample_graph
        assert engine.stats['queries_executed'] == 0
        assert engine.stats['cache_hits'] == 0
        assert engine.stats['cache_misses'] == 0

    def test_select_query_basic(self, engine):
        """
        Test basic SELECT query.
        Baslanǵısh SELECT sorawdı test etiw.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jinayat ?label
        WHERE {
            ?jinayat a huquq:Jinayat .
            ?jinayat rdfs:label ?label .
            FILTER(LANG(?label) = "kaa")
        }
        """

        results = engine.select(query)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all('jinayat' in r for r in results)
        assert all('label' in r for r in results)

        # Check statistics
        stats = engine.get_statistics()
        assert stats['queries_executed'] >= 1

    def test_select_query_with_lang(self, engine):
        """
        Test SELECT query with language parameter.
        Til parametri menen SELECT sorawdı test etiw.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jinayat ?label
        WHERE {
            ?jinayat a huquq:Jinayat .
            ?jinayat rdfs:label ?label .
            FILTER(LANG(?label) = "%%LANG%%")
        }
        """

        # Test with Karakalpak
        results_kaa = engine.select(query, lang="kaa")
        assert len(results_kaa) > 0

        # Test with English
        results_en = engine.select(query, lang="en")
        assert len(results_en) > 0

    def test_ask_query_true(self, engine):
        """
        Test ASK query that returns true.
        True qaytarıwshı ASK sorawdı test etiw.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>

        ASK {
            ?jinayat a huquq:Jinayat .
        }
        """

        result = engine.ask(query)

        assert isinstance(result, bool)
        assert result is True

    def test_ask_query_false(self, engine):
        """
        Test ASK query that returns false.
        False qaytarıwshı ASK sorawdı test etiw.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>

        ASK {
            ?x a huquq:NonExistentClass .
        }
        """

        result = engine.ask(query)

        assert isinstance(result, bool)
        assert result is False

    def test_construct_query(self, engine):
        """
        Test CONSTRUCT query.
        CONSTRUCT sorawdı test etiw.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        CONSTRUCT {
            ?jinayat rdfs:label ?label .
        }
        WHERE {
            ?jinayat a huquq:Jinayat .
            ?jinayat rdfs:label ?label .
            FILTER(LANG(?label) = "kaa")
        }
        """

        result = engine.construct(query, format="turtle")

        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain RDF/Turtle syntax
        assert "Jinayat" in result or "@prefix" in result

    def test_query_validation_invalid_syntax(self, engine):
        """
        Test query validation with invalid syntax.
        Notoǵrı sintaksis menen soraw tastıqlaw testı.
        """
        invalid_query = "INVALID SPARQL QUERY { ?s ?p ?o }"

        with pytest.raises(QueryValidationError):
            engine.select(invalid_query)

    def test_query_validation_empty(self, engine):
        """
        Test query validation with empty query.
        Bos soraw menen tastıqlaw testı.
        """
        with pytest.raises(QueryValidationError):
            engine.select("")

    def test_search_by_term_kaa(self, engine):
        """
        Test searching by Karakalpak term.
        Qaraqalpaq termin boyınsha izlew testı.
        """
        # Search for "jinayat"
        results = engine.search_by_term_kaa("jinayat")

        assert isinstance(results, list)
        assert len(results) > 0

        # Check result structure
        for result in results:
            assert 'resource' in result
            assert 'label' in result
            assert 'comment' in result or result['comment'] is None

    def test_search_by_term_kaa_fuzzy(self, engine):
        """
        Test fuzzy search by Karakalpak term.
        Anıq emes izlew testı.
        """
        # Search with fuzzy matching
        results = engine.search_by_term_kaa("jınayat", fuzzy=True)

        assert isinstance(results, list)
        # Fuzzy search should still find results despite typo

    def test_search_by_term_kaa_with_limit(self, engine):
        """
        Test search with result limit.
        Nátiyјe shektewi menen izlew testı.
        """
        results = engine.search_by_term_kaa("jinayat", limit=2)

        assert len(results) <= 2

    def test_get_jaza_range_both_limits(self, engine):
        """
        Test getting punishments within year range.
        Jıl diapazonı ishinde jazalar alıw testı.
        """
        # Get punishments between 1 and 5 years
        results = engine.get_jaza_range(min_jıl=1, max_jıl=5)

        assert isinstance(results, list)
        assert len(results) > 0

        # Check result structure
        for result in results:
            assert 'jaza' in result
            assert 'label' in result
            assert 'minYears' in result
            assert 'maxYears' in result

    def test_get_jaza_range_min_only(self, engine):
        """
        Test getting punishments with minimum years only.
        Tek minimal jıllar menen jazalar alıw testı.
        """
        results = engine.get_jaza_range(min_jıl=5, max_jıl=None)

        assert isinstance(results, list)
        # Should return severe punishments (5+ years)

    def test_get_jaza_range_max_only(self, engine):
        """
        Test getting punishments with maximum years only.
        Tek maksimal jıllar menen jazalar alıw testı.
        """
        results = engine.get_jaza_range(min_jıl=None, max_jıl=2)

        assert isinstance(results, list)
        # Should return light punishments (up to 2 years)

    def test_search_jinayat_turi_jenil(self, engine):
        """
        Test searching for light crimes.
        Jeńil jinayatlardı izlew testı.
        """
        results = engine.search_jinayat_turi("jeńil")

        assert isinstance(results, list)
        assert len(results) > 0

        # All results should be light crimes
        for result in results:
            assert result['crimeType'] == 'jeńil'

    def test_search_jinayat_turi_orta(self, engine):
        """
        Test searching for medium crimes.
        Orta awırlıqtaǵı jinayatlardı izlew testı.
        """
        results = engine.search_jinayat_turi("orta")

        assert isinstance(results, list)

        # Check result structure
        for result in results:
            assert 'jinayat' in result
            assert 'label' in result
            assert 'crimeType' in result
            assert result['crimeType'] == 'orta'

    def test_search_jinayat_turi_awir(self, engine):
        """
        Test searching for severe crimes.
        Awır jinayatlardı izlew testı.
        """
        results = engine.search_jinayat_turi("awır")

        assert isinstance(results, list)
        assert len(results) > 0

    def test_search_jinayat_turi_with_limit(self, engine):
        """
        Test crime type search with limit.
        Shektew menen jinayat túri boyınsha izlew testı.
        """
        results = engine.search_jinayat_turi("orta", limit=1)

        assert len(results) <= 1

    def test_search_statiya_by_number(self, engine):
        """
        Test searching articles by number.
        Nomer boyınsha statiyalardı izlew testı.
        """
        results = engine.search_statiya(nomer="123", kodeks=None)

        assert isinstance(results, list)
        assert len(results) > 0

        # Check that article 123 is found
        for result in results:
            assert 'statiya' in result
            assert 'articleNumber' in result

    def test_search_statiya_by_code(self, engine):
        """
        Test searching articles by code type.
        Kodeks túri boyınsha statiyalardı izlew testı.
        """
        results = engine.search_statiya(nomer=None, kodeks="JK")

        assert isinstance(results, list)

        # All results should be from Criminal Code (JK)
        for result in results:
            assert result.get('codeType') == 'JK'

    def test_search_statiya_both_params(self, engine):
        """
        Test searching articles with both parameters.
        Eki parametr menen statiyalardı izlew testı.
        """
        results = engine.search_statiya(nomer="123", kodeks="JK")

        assert isinstance(results, list)

    def test_get_related_jinayat_jaza(self, engine):
        """
        Test getting crime with related punishments.
        Jinayat penen baylanıslı jazalardı alıw testı.
        """
        jinayat_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
        results = engine.get_related_jinayat_jaza(jinayat_uri)

        assert isinstance(results, list)
        assert len(results) > 0

        # Check result structure
        result = results[0]
        assert 'jinayat' in result
        assert 'jinayatLabel' in result
        assert 'jaza' in result
        assert 'jazaLabel' in result

    def test_execute_cached(self, engine):
        """
        Test cached query execution.
        Keshlengen soraw orınlaw testı.
        """
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        SELECT ?s WHERE { ?s a huquq:Jinayat }
        """

        # First execution - cache miss
        result1 = engine.execute_cached(query, query_type="select")
        stats1 = engine.get_statistics()
        cache_misses1 = stats1['cache_misses']

        # Second execution - cache hit
        result2 = engine.execute_cached(query, query_type="select")
        stats2 = engine.get_statistics()
        cache_hits2 = stats2['cache_hits']

        # Results should be identical
        assert result1 == result2

        # Cache hits should have increased
        assert cache_hits2 > stats1['cache_hits']

    def test_clear_cache(self, engine):
        """
        Test clearing query cache.
        Soraw keshın tazalaw testı.
        """
        query = "SELECT ?s WHERE { ?s ?p ?o } LIMIT 1"

        # Execute to populate cache
        engine.execute_cached(query)

        # Clear cache
        engine.clear_cache()

        # Execute again - should be cache miss
        stats_before = engine.get_statistics()
        engine.execute_cached(query)
        stats_after = engine.get_statistics()

        assert stats_after['cache_misses'] > stats_before['cache_misses']

    def test_get_statistics(self, engine):
        """
        Test getting engine statistics.
        Mexanizm statistikasın alıw testı.
        """
        # Execute some queries
        engine.select("SELECT ?s WHERE { ?s ?p ?o } LIMIT 1")
        engine.ask("ASK { ?s ?p ?o }")

        stats = engine.get_statistics()

        assert isinstance(stats, dict)
        assert 'queries_executed' in stats
        assert 'cache_hits' in stats
        assert 'cache_misses' in stats
        assert 'total_execution_time' in stats
        assert 'average_query_time' in stats

        assert stats['queries_executed'] >= 2

    def test_performance_logging(self, engine):
        """
        Test that performance is logged.
        Tabıslılıq jurnalanıwın test etiw.
        """
        query = "SELECT ?s WHERE { ?s ?p ?o } LIMIT 1"

        initial_time = engine.stats['total_execution_time']

        engine.select(query)

        final_time = engine.stats['total_execution_time']

        # Execution time should have increased
        assert final_time > initial_time

    def test_karakalpak_utf8_support(self, engine):
        """
        Test UTF-8 support for Karakalpak characters.
        Qaraqalpaq háripler ushın UTF-8 qollawdı test etiw.
        """
        # Search with special Karakalpak characters: ǵ, ń, ı, ú, ó
        results = engine.search_by_term_kaa("jazaǵa")

        # Should not crash with special characters
        assert isinstance(results, list)

    def test_result_type_conversion(self, engine):
        """
        Test proper type conversion in results.
        Nátiyјelerde toǵrı túr ózgeristiw testı.
        """
        results = engine.get_jaza_range(min_jıl=1, max_jıl=5)

        if len(results) > 0:
            result = results[0]

            # Integer fields should be converted to int
            if 'minYears' in result and result['minYears'] is not None:
                assert isinstance(result['minYears'], int)

            if 'maxYears' in result and result['maxYears'] is not None:
                assert isinstance(result['maxYears'], int)


class TestKarakalpakLegalQueries:
    """
    Test Karakalpak-specific legal queries.
    Qaraqalpaq huquqıy sorawların test etiw.
    """

    def test_theft_crime_search(self, engine):
        """
        Test searching for theft (urılıq).
        Urılıq jinayatın izlew testı.
        """
        results = engine.search_by_term_kaa("urılıq")

        assert len(results) > 0
        # Should find the theft crime
        assert any('Urılıq' in str(r.get('label', '')) for r in results)

    def test_light_crime_category(self, engine):
        """
        Test light crime category (jeńil).
        Jeńil jinayat kategoriyasın test etiw.
        """
        results = engine.search_jinayat_turi("jeńil")

        assert len(results) > 0
        assert all(r['crimeType'] == 'jeńil' for r in results)

    def test_punishment_years_filtering(self, engine):
        """
        Test filtering punishments by years.
        Jıllar boyınsha jazalardı filtrlew testı.
        """
        # Short punishments (0-2 years)
        short_punishments = engine.get_jaza_range(min_jıl=0, max_jıl=2)

        # Long punishments (5+ years)
        long_punishments = engine.get_jaza_range(min_jıl=5, max_jıl=None)

        assert isinstance(short_punishments, list)
        assert isinstance(long_punishments, list)

    def test_article_code_types(self, engine):
        """
        Test different article code types.
        Túrli statiya kodeks túrlerin test etiw.
        """
        # Criminal Code articles (JK - Jinayat Kodeksi)
        jk_articles = engine.search_statiya(nomer=None, kodeks="JK")

        # Administrative Code articles (AK)
        ak_articles = engine.search_statiya(nomer=None, kodeks="AK")

        assert isinstance(jk_articles, list)
        assert isinstance(ak_articles, list)


# Integration test / Integratsiya testı
def test_full_sparql_workflow(tmp_path):
    """
    Test complete SPARQL workflow with Karakalpak legal data.
    Qaraqalpaq huquqıy ma'limleri menen tóliq SPARQL iš joli testı.
    """
    # Create minimal test ontology
    ontology_content = """<?xml version="1.0"?>
    <rdf:RDF xmlns="http://huquqai.org/ontology#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
        <owl:Ontology rdf:about="http://huquqai.org/ontology"/>
        <owl:Class rdf:about="http://huquqai.org/ontology#Jinayat">
            <rdfs:label xml:lang="kaa">Jinayat</rdfs:label>
        </owl:Class>
        <Jinayat rdf:about="http://huquqai.org/ontology#Test">
            <rdfs:label xml:lang="kaa">Test jinayat</rdfs:label>
            <crimeType>orta</crimeType>
        </Jinayat>
    </rdf:RDF>
    """

    ontology_file = tmp_path / "test.owl"
    ontology_file.write_text(ontology_content, encoding='utf-8')

    # Load ontology
    manager = OntologyManager()
    manager.clear()
    manager.load_ontology(ontology_file)

    # Create engine
    engine = SPARQLEngine(manager.graph)

    # Test SELECT query
    select_results = engine.select("""
        PREFIX huquq: <http://huquqai.org/ontology#>
        SELECT ?s WHERE { ?s a huquq:Jinayat }
    """)
    assert len(select_results) > 0

    # Test ASK query
    exists = engine.ask("""
        PREFIX huquq: <http://huquqai.org/ontology#>
        ASK { ?s a huquq:Jinayat }
    """)
    assert exists is True

    # Test Karakalpak search
    kaa_results = engine.search_by_term_kaa("jinayat")
    assert len(kaa_results) > 0

    # Test crime type search
    type_results = engine.search_jinayat_turi("orta")
    assert len(type_results) > 0

    # Test statistics
    stats = engine.get_statistics()
    assert stats['queries_executed'] >= 4

    # Clear cache
    engine.clear_cache()
