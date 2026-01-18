"""
Tests for ReasoningEngine
ReasoningEngine ushın testler

This module tests the OWL reasoning engine functionality with Karakalpak legal data.
Bu modul Qaraqalpaq huquqıy ma'limleri menen OWL mántıqlı juwmaq mexanizmi funktsiyasın test etedi.
"""

import pytest
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

from src.core.reasoning_engine import (
    ReasoningEngine,
    ReasoningEngineError,
    ConsistencyError,
    ClassificationError,
    InferenceError,
    ReasonerType,
    JinayatAwırlıǵı,
    JazaTuri,
    create_reasoning_engine
)


@pytest.fixture
def sample_ontology(tmp_path):
    """
    Create a sample OWL ontology for testing.
    Test etiw ushın misaldı OWL ontologiya jasawıш.
    """
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
    <owl:Class rdf:about="http://huquqai.org/ontology#Nızam">
        <rdfs:label xml:lang="kaa">Nızam</rdfs:label>
        <rdfs:label xml:lang="en">Law</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Statiya">
        <rdfs:label xml:lang="kaa">Statiya</rdfs:label>
        <rdfs:label xml:lang="en">Article</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Jinayat">
        <rdfs:label xml:lang="kaa">Jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Crime</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#JeńilJinayat">
        <rdfs:subClassOf rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:label xml:lang="kaa">Jeńil Jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Light Crime</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#OrtaJinayat">
        <rdfs:subClassOf rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:label xml:lang="kaa">Orta Jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Medium Crime</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#AwırJinayat">
        <rdfs:subClassOf rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:label xml:lang="kaa">Awır Jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Severe Crime</rdfs:label>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Jaza">
        <rdfs:label xml:lang="kaa">Jaza</rdfs:label>
        <rdfs:label xml:lang="en">Punishment</rdfs:label>
    </owl:Class>

    <!-- Properties / Xassalar -->
    <owl:ObjectProperty rdf:about="http://huquqai.org/ontology#hasPunishment">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:range rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:label xml:lang="kaa">jazaǵa iye</rdfs:label>
    </owl:ObjectProperty>

    <owl:ObjectProperty rdf:about="http://huquqai.org/ontology#hasArticle">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Nızam"/>
        <rdfs:range rdf:resource="http://huquqai.org/ontology#Statiya"/>
        <rdfs:label xml:lang="kaa">statiyaǵa iye</rdfs:label>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#crimeType">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:label xml:lang="kaa">jinayat túri</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#minYears">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
        <rdfs:label xml:lang="kaa">minimal jıllar</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#maxYears">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
        <rdfs:label xml:lang="kaa">maksimal jıllar</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#articleNumber">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Statiya"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:label xml:lang="kaa">statiya nomeri</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#effectiveDate">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Nızam"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#date"/>
        <rdfs:label xml:lang="kaa">kúsh kirisiw sánesi</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#conditional">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label xml:lang="kaa">shartı</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#compulsoryLabor">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label xml:lang="kaa">shimeli jumıs</rdfs:label>
    </owl:DatatypeProperty>

    <owl:DatatypeProperty rdf:about="http://huquqai.org/ontology#punishmentType">
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jaza"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:label xml:lang="kaa">jaza túri</rdfs:label>
    </owl:DatatypeProperty>

    <!-- Individuals / Individuallar -->

    <!-- Law: Criminal Code / Nızam: Jinayat Kodeksi -->
    <Nızam rdf:about="http://huquqai.org/ontology#Nızam_JinayatKodeksi">
        <rdfs:label xml:lang="kaa">Qaraqalpaqstan Respublikası Jinayat Kodeksi</rdfs:label>
        <rdfs:label xml:lang="en">Criminal Code of the Republic of Karakalpakstan</rdfs:label>
        <effectiveDate rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2020-01-01</effectiveDate>
        <hasArticle rdf:resource="http://huquqai.org/ontology#Statiya_123"/>
        <hasArticle rdf:resource="http://huquqai.org/ontology#Statiya_456"/>
    </Nızam>

    <!-- Articles / Statiyalar -->
    <Statiya rdf:about="http://huquqai.org/ontology#Statiya_123">
        <rdfs:label xml:lang="kaa">Statiya 123</rdfs:label>
        <articleNumber>123</articleNumber>
    </Statiya>

    <Statiya rdf:about="http://huquqai.org/ontology#Statiya_456">
        <rdfs:label xml:lang="kaa">Statiya 456</rdfs:label>
        <articleNumber>456</articleNumber>
    </Statiya>

    <!-- Light crime: 1 year punishment / Jeńil jinayat: 1 jıl jaza -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Jeńil">
        <rdfs:label xml:lang="kaa">Jeńil jinayat</rdfs:label>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Jeńil"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Jeńil">
        <rdfs:label xml:lang="kaa">Jeńil jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">0</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</maxYears>
    </Jaza>

    <!-- Medium crime: 3-5 years / Orta jinayat: 3-5 jıl -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Urılıq">
        <rdfs:label xml:lang="kaa">Urılıq</rdfs:label>
        <rdfs:label xml:lang="en">Theft</rdfs:label>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Urılıq"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Urılıq">
        <rdfs:label xml:lang="kaa">Urılıq ushın jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">3</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">5</maxYears>
    </Jaza>

    <!-- Severe crime: 10-15 years / Awır jinayat: 10-15 jıl -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_Awır">
        <rdfs:label xml:lang="kaa">Awır jinayat</rdfs:label>
        <rdfs:label xml:lang="en">Severe crime</rdfs:label>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_Awır"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Awır">
        <rdfs:label xml:lang="kaa">Awır jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">10</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">15</maxYears>
    </Jaza>

    <!-- Very severe crime: 20 years / Óte awır jinayat: 20 jıl -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_OteAwır">
        <rdfs:label xml:lang="kaa">Óte awır jinayat</rdfs:label>
        <hasPunishment rdf:resource="http://huquqai.org/ontology#Jaza_OteAwır"/>
    </Jinayat>

    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_OteAwır">
        <rdfs:label xml:lang="kaa">Óte awır jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">20</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">25</maxYears>
    </Jaza>

    <!-- Fine punishment / Jarıma jazası -->
    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Jarıma">
        <rdfs:label xml:lang="kaa">Jarıma</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">0</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">0</maxYears>
    </Jaza>

    <!-- Conditional punishment / Shartı jaza -->
    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_Shartı">
        <rdfs:label xml:lang="kaa">Shartı jaza</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">3</maxYears>
        <conditional rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</conditional>
    </Jaza>

    <!-- Compulsory labor / Shimeli jumıs -->
    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_ShimeliJumıs">
        <rdfs:label xml:lang="kaa">Shimeli jumıs</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</maxYears>
        <compulsoryLabor rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</compulsoryLabor>
    </Jaza>

    <!-- Imprisonment / Azatlıqtan ayırıw -->
    <Jaza rdf:about="http://huquqai.org/ontology#Jaza_AzatlıqtanAyırıw">
        <rdfs:label xml:lang="kaa">Azatlıqtan ayırıw</rdfs:label>
        <minYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</minYears>
        <maxYears rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">5</maxYears>
    </Jaza>

</rdf:RDF>
"""

    ontology_file = tmp_path / "test_reasoning.owl"
    ontology_file.write_text(ontology_content, encoding='utf-8')
    return ontology_file


@pytest.fixture
def graph_from_ontology(sample_ontology):
    """Create RDF graph from ontology file"""
    g = Graph()
    g.parse(str(sample_ontology), format="xml")
    return g


@pytest.fixture
def engine_with_graph(graph_from_ontology):
    """Create reasoning engine with RDF graph"""
    engine = ReasoningEngine(graph=graph_from_ontology)
    return engine


@pytest.fixture
def engine_with_ontology(sample_ontology):
    """Create reasoning engine with ontology file"""
    engine = ReasoningEngine(ontology_path=sample_ontology, reasoner=ReasonerType.PELLET)
    return engine


class TestReasoningEngine:
    """Test suite for ReasoningEngine / ReasoningEngine test toplamı"""

    def test_initialization_with_graph(self, graph_from_ontology):
        """Test initialization with RDF graph"""
        engine = ReasoningEngine(graph=graph_from_ontology)

        assert engine is not None
        assert engine.graph is graph_from_ontology
        assert engine.reasoner_type == ReasonerType.PELLET
        assert len(engine.inferred_facts) == 0

    def test_initialization_with_ontology(self, sample_ontology):
        """Test initialization with ontology file"""
        engine = ReasoningEngine(ontology_path=sample_ontology)

        assert engine is not None
        assert engine.onto is not None
        assert engine.world is not None

    def test_invalid_ontology_path(self):
        """Test loading non-existent ontology"""
        with pytest.raises(ReasoningEngineError):
            ReasoningEngine(ontology_path="nonexistent.owl")

    def test_consistency_check_consistent(self, engine_with_ontology):
        """Test consistency check on valid ontology"""
        is_consistent = engine_with_ontology.check_consistency()

        assert is_consistent is True
        assert engine_with_ontology.stats['reasoning_runs'] >= 1

    def test_consistency_check_no_ontology(self):
        """Test consistency check without ontology"""
        engine = ReasoningEngine()

        with pytest.raises(ConsistencyError):
            engine.check_consistency()

    def test_classification(self, engine_with_ontology):
        """Test classification reasoning"""
        result = engine_with_ontology.classify(explain=False)

        assert result.success is True
        assert isinstance(result.inferences, list)
        assert result.execution_time > 0
        assert result.reasoner_type in ["pellet", "hermit"]

    def test_classification_with_explanations(self, engine_with_ontology):
        """Test classification with explanations"""
        result = engine_with_ontology.classify(explain=True)

        assert result.success is True
        assert isinstance(result.explanations, list)

    def test_infer_facts(self, engine_with_ontology):
        """Test fact inference"""
        result = engine_with_ontology.infer_facts()

        assert result.success is True
        assert isinstance(result.inferences, list)

    def test_classify_jinayat_light_crime(self, engine_with_graph):
        """Test classifying light crime (jeńil jinayat)"""
        crime_uri = "http://huquqai.org/ontology#Jinayat_Jeńil"
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity == JinayatAwırlıǵı.JENIL
        assert len(engine_with_graph.inferred_facts) > 0

    def test_classify_jinayat_medium_crime(self, engine_with_graph):
        """Test classifying medium crime (orta jinayat)"""
        crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity == JinayatAwırlıǵı.ORTA

    def test_classify_jinayat_severe_crime(self, engine_with_graph):
        """Test classifying severe crime (awır jinayat)"""
        crime_uri = "http://huquqai.org/ontology#Jinayat_Awır"
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity == JinayatAwırlıǵı.AWIR

    def test_classify_jinayat_very_severe_crime(self, engine_with_graph):
        """Test classifying very severe crime (óte awır jinayat)"""
        crime_uri = "http://huquqai.org/ontology#Jinayat_OteAwır"
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity == JinayatAwırlıǵı.OTE_AWIR

    def test_classify_jinayat_no_punishment(self, engine_with_graph):
        """Test classifying crime without punishment info"""
        # Add crime without punishment
        huquq = Namespace("http://huquqai.org/ontology#")
        crime_uri = "http://huquqai.org/ontology#Jinayat_Unknown"

        engine_with_graph.graph.add((
            URIRef(crime_uri),
            RDF.type,
            huquq.Jinayat
        ))

        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity is None

    def test_infer_jaza_fine(self, engine_with_graph):
        """Test inferring fine punishment (jarıma)"""
        jaza_uri = "http://huquqai.org/ontology#Jaza_Jarıma"
        pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)

        assert pun_type == JazaTuri.JARIMA

    def test_infer_jaza_conditional(self, engine_with_graph):
        """Test inferring conditional punishment (shartı jaza)"""
        jaza_uri = "http://huquqai.org/ontology#Jaza_Shartı"
        pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)

        assert pun_type == JazaTuri.SHARTI_JAZA

    def test_infer_jaza_compulsory_labor(self, engine_with_graph):
        """Test inferring compulsory labor (shimeli jumıs)"""
        jaza_uri = "http://huquqai.org/ontology#Jaza_ShimeliJumıs"
        pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)

        assert pun_type == JazaTuri.SHIMELI_JUMIS

    def test_infer_jaza_imprisonment(self, engine_with_graph):
        """Test inferring imprisonment (azatlıqtan ayırıw)"""
        jaza_uri = "http://huquqai.org/ontology#Jaza_AzatlıqtanAyırıw"
        pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)

        assert pun_type == JazaTuri.AZATLIQTAN_AYIRIW

    def test_check_nızam_consistency_valid(self, engine_with_graph):
        """Test consistency check on valid law"""
        nızam_uri = "http://huquqai.org/ontology#Nızam_JinayatKodeksi"
        is_consistent, issues = engine_with_graph.check_nızam_consistency(nızam_uri)

        assert is_consistent is True
        assert len(issues) == 0

    def test_check_nızam_consistency_missing_label(self, engine_with_graph):
        """Test consistency check on law without label"""
        # Add law without label
        huquq = Namespace("http://huquqai.org/ontology#")
        nızam_uri = "http://huquqai.org/ontology#Nızam_Invalid"

        engine_with_graph.graph.add((
            URIRef(nızam_uri),
            RDF.type,
            huquq.Nızam
        ))

        is_consistent, issues = engine_with_graph.check_nızam_consistency(nızam_uri)

        assert is_consistent is False
        assert len(issues) > 0
        assert any("label" in issue.lower() for issue in issues)

    def test_check_nızam_consistency_missing_date(self, engine_with_graph):
        """Test consistency check on law without effective date"""
        huquq = Namespace("http://huquqai.org/ontology#")
        nızam_uri = "http://huquqai.org/ontology#Nızam_NoDate"

        # Add law with label but no date
        engine_with_graph.graph.add((URIRef(nızam_uri), RDF.type, huquq.Nızam))
        engine_with_graph.graph.add((
            URIRef(nızam_uri),
            RDFS.label,
            Literal("Test Law", lang="kaa")
        ))

        is_consistent, issues = engine_with_graph.check_nızam_consistency(nızam_uri)

        assert is_consistent is False
        assert any("effective date" in issue.lower() for issue in issues)

    def test_explain_inference_crime_type(self, engine_with_graph):
        """Test explaining crime type inference"""
        # First make an inference
        crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        # Now explain it
        explanation = engine_with_graph.explain_inference(
            crime_uri,
            "http://huquqai.org/ontology#crimeType",
            severity.value
        )

        assert explanation is not None
        assert explanation.subject == crime_uri
        assert explanation.explanation_en != ""
        assert explanation.explanation_kaa != ""
        assert 0.0 <= explanation.confidence <= 1.0

    def test_explain_inference_punishment_type(self, engine_with_graph):
        """Test explaining punishment type inference"""
        jaza_uri = "http://huquqai.org/ontology#Jaza_Jarıma"
        pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)

        explanation = engine_with_graph.explain_inference(
            jaza_uri,
            "http://huquqai.org/ontology#punishmentType",
            pun_type.value
        )

        assert explanation is not None
        assert "punishment" in explanation.explanation_en.lower()
        assert "jaza" in explanation.explanation_kaa.lower()

    def test_explain_inference_not_found(self, engine_with_graph):
        """Test explaining non-existent inference"""
        explanation = engine_with_graph.explain_inference(
            "http://example.org/NotExist",
            "http://example.org/prop",
            "value"
        )

        assert explanation is None

    def test_get_all_inferences(self, engine_with_graph):
        """Test getting all inferred facts"""
        # Make some inferences
        engine_with_graph.classify_jinayat_awırlıǵı("http://huquqai.org/ontology#Jinayat_Urılıq")
        engine_with_graph.infer_jaza_turi("http://huquqai.org/ontology#Jaza_Jarıma")

        inferences = engine_with_graph.get_all_inferences()

        assert isinstance(inferences, list)
        assert len(inferences) > 0
        for inf in inferences:
            assert len(inf) == 3  # (subject, predicate, object)

    def test_clear_inferences(self, engine_with_graph):
        """Test clearing inferred facts"""
        # Make some inferences
        engine_with_graph.classify_jinayat_awırlıǵı("http://huquqai.org/ontology#Jinayat_Urılıq")

        assert len(engine_with_graph.inferred_facts) > 0

        # Clear
        engine_with_graph.clear_inferences()

        assert len(engine_with_graph.inferred_facts) == 0

    def test_get_statistics(self, engine_with_ontology):
        """Test getting engine statistics"""
        # Perform some reasoning
        engine_with_ontology.check_consistency()
        engine_with_ontology.classify()

        stats = engine_with_ontology.get_statistics()

        assert isinstance(stats, dict)
        assert 'reasoning_runs' in stats
        assert 'inferences_made' in stats
        assert 'inconsistencies_found' in stats
        assert 'total_reasoning_time' in stats
        assert 'average_reasoning_time' in stats
        assert stats['reasoning_runs'] >= 2

    def test_multiple_reasoning_runs(self, engine_with_ontology):
        """Test multiple reasoning operations"""
        # Run multiple times
        for _ in range(3):
            engine_with_ontology.check_consistency()

        stats = engine_with_ontology.get_statistics()

        assert stats['reasoning_runs'] >= 3
        assert stats['total_reasoning_time'] > 0

    def test_repr(self, engine_with_ontology):
        """Test string representation"""
        repr_str = repr(engine_with_ontology)

        assert "ReasoningEngine" in repr_str
        assert "pellet" in repr_str.lower() or "hermit" in repr_str.lower()
        assert "loaded" in repr_str.lower() or "júklendi" in repr_str.lower()


class TestKarakalpakReasoningRules:
    """Test Karakalpak-specific reasoning rules"""

    def test_crime_severity_classification_rules(self, engine_with_graph):
        """Test all crime severity classification rules"""
        test_cases = [
            ("http://huquqai.org/ontology#Jinayat_Jeńil", JinayatAwırlıǵı.JENIL),
            ("http://huquqai.org/ontology#Jinayat_Urılıq", JinayatAwırlıǵı.ORTA),
            ("http://huquqai.org/ontology#Jinayat_Awır", JinayatAwırlıǵı.AWIR),
            ("http://huquqai.org/ontology#Jinayat_OteAwır", JinayatAwırlıǵı.OTE_AWIR),
        ]

        for crime_uri, expected_severity in test_cases:
            severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)
            assert severity == expected_severity, \
                f"Expected {expected_severity} for {crime_uri}, got {severity}"

    def test_punishment_type_inference_rules(self, engine_with_graph):
        """Test all punishment type inference rules"""
        test_cases = [
            ("http://huquqai.org/ontology#Jaza_Jarıma", JazaTuri.JARIMA),
            ("http://huquqai.org/ontology#Jaza_Shartı", JazaTuri.SHARTI_JAZA),
            ("http://huquqai.org/ontology#Jaza_ShimeliJumıs", JazaTuri.SHIMELI_JUMIS),
            ("http://huquqai.org/ontology#Jaza_AzatlıqtanAyırıw", JazaTuri.AZATLIQTAN_AYIRIW),
        ]

        for jaza_uri, expected_type in test_cases:
            pun_type = engine_with_graph.infer_jaza_turi(jaza_uri)
            assert pun_type == expected_type, \
                f"Expected {expected_type} for {jaza_uri}, got {pun_type}"

    def test_utf8_karakalpak_characters(self, engine_with_graph):
        """Test handling of Karakalpak special characters"""
        # URIs and values with Karakalpak characters should work
        crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"

        # Should not crash with special characters
        severity = engine_with_graph.classify_jinayat_awırlıǵı(crime_uri)

        assert severity is not None


class TestCreateReasoningEngine:
    """Test module-level convenience function"""

    def test_create_reasoning_engine(self, sample_ontology):
        """Test create_reasoning_engine function"""
        engine = create_reasoning_engine(sample_ontology, ReasonerType.PELLET)

        assert engine is not None
        assert engine.onto is not None
        assert engine.reasoner_type == ReasonerType.PELLET

    def test_create_reasoning_engine_default_reasoner(self, sample_ontology):
        """Test create_reasoning_engine with default reasoner"""
        engine = create_reasoning_engine(sample_ontology)

        assert engine.reasoner_type == ReasonerType.PELLET


# Integration test
def test_full_reasoning_workflow(sample_ontology):
    """
    Test complete reasoning workflow with Karakalpak legal data.
    Qaraqalpaq huquqıy ma'limleri menen tóliq mántıqlı juwmaq iš jolin test etiw.
    """
    # Create engine
    engine = create_reasoning_engine(sample_ontology, ReasonerType.PELLET)

    # Check consistency
    is_consistent = engine.check_consistency()
    assert is_consistent is True

    # Classify ontology
    result = engine.classify(explain=True)
    assert result.success is True

    # Classify specific crimes
    crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
    severity = engine.classify_jinayat_awırlıǵı(crime_uri)
    assert severity == JinayatAwırlıǵı.ORTA

    # Infer punishment types
    jaza_uri = "http://huquqai.org/ontology#Jaza_Jarıma"
    pun_type = engine.infer_jaza_turi(jaza_uri)
    assert pun_type == JazaTuri.JARIMA

    # Check law consistency
    nızam_uri = "http://huquqai.org/ontology#Nızam_JinayatKodeksi"
    is_valid, issues = engine.check_nızam_consistency(nızam_uri)
    assert is_valid is True

    # Get statistics
    stats = engine.get_statistics()
    assert stats['reasoning_runs'] > 0
    assert stats['inferences_made'] > 0

    # Get all inferences
    inferences = engine.get_all_inferences()
    assert len(inferences) > 0
