"""
Tests for OntologyManager
OntologyManager ushın testler

This module tests the OWL ontology management functionality with Karakalpak legal data.
Bu modul Qaraqalpaq huquqıy ma'limleri menen OWL ontologiya basqarıw funktsiyasın test etedi.
"""

import pytest
from pathlib import Path
from rdflib import URIRef, Literal

from src.core.ontology_manager import (
    OntologyManager,
    OntologyManagerError,
    OntologyNotLoadedError,
    get_ontology_manager
)


@pytest.fixture
def manager():
    """
    Create OntologyManager instance for testing.
    Test etiw ushın OntologyManager misalın jasawiш.
    """
    mgr = OntologyManager()
    yield mgr
    # Cleanup / Tazalaw
    mgr.clear()


@pytest.fixture
def sample_ontology_path(tmp_path):
    """
    Create a sample OWL ontology file for testing.
    Test etiw ushın misaldı OWL ontologiya faylın jasawiш.
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
        <rdfs:comment xml:lang="kaa">Huquqıy nızam</rdfs:comment>
    </owl:Class>

    <owl:Class rdf:about="http://huquqai.org/ontology#Statiya">
        <rdfs:label xml:lang="kaa">Statiya</rdfs:label>
        <rdfs:label xml:lang="en">Article</rdfs:label>
        <rdfs:comment xml:lang="kaa">Huquqıy statiya</rdfs:comment>
    </owl:Class>

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

    <!-- Object Properties / Obyekt xassalar -->
    <owl:ObjectProperty rdf:about="http://huquqai.org/ontology#hasPunishment">
        <rdfs:label xml:lang="kaa">jazaǵa iye</rdfs:label>
        <rdfs:label xml:lang="en">has punishment</rdfs:label>
        <rdfs:domain rdf:resource="http://huquqai.org/ontology#Jinayat"/>
        <rdfs:range rdf:resource="http://huquqai.org/ontology#Jaza"/>
    </owl:ObjectProperty>

    <!-- Sample Individuals / Misal individuallar -->
    <Jinayat rdf:about="http://huquqai.org/ontology#Jinayat_UrAq">
        <rdfs:label xml:lang="kaa">Urılıq</rdfs:label>
        <rdfs:label xml:lang="en">Theft</rdfs:label>
        <crimeType>medium</crimeType>
    </Jinayat>

    <Statiya rdf:about="http://huquqai.org/ontology#Statiya_123">
        <rdfs:label xml:lang="kaa">Statiya 123</rdfs:label>
        <articleNumber>123</articleNumber>
        <title xml:lang="kaa">Jinayattıń awır túri</title>
    </Statiya>

</rdf:RDF>
"""

    ontology_file = tmp_path / "test_ontology.owl"
    ontology_file.write_text(ontology_content, encoding='utf-8')
    return ontology_file


class TestOntologyManager:
    """Test suite for OntologyManager / OntologyManager test toplamı"""

    def test_singleton_pattern(self):
        """
        Test singleton pattern.
        Singleton patterndi test etiw.
        """
        manager1 = OntologyManager()
        manager2 = OntologyManager()
        manager3 = get_ontology_manager()

        assert manager1 is manager2
        assert manager1 is manager3
        assert id(manager1) == id(manager2) == id(manager3)

    def test_initialization(self, manager):
        """
        Test manager initialization.
        Menedžer inizializaciyasın test etiw.
        """
        assert manager is not None
        assert not manager.is_loaded()
        assert manager.namespaces is not None
        assert len(manager.namespaces) > 0
        assert manager.stats['loaded'] is False

    def test_load_ontology_success(self, manager, sample_ontology_path):
        """
        Test successful ontology loading.
        Tabıslı ontologiya júklewdi test etiw.
        """
        result = manager.load_ontology(sample_ontology_path)

        assert result is True
        assert manager.is_loaded()
        assert manager.stats['loaded'] is True
        assert manager.stats['triple_count'] > 0
        assert manager.stats['class_count'] >= 4  # Nızam, Statiya, Jinayat, Jaza

    def test_load_ontology_file_not_found(self, manager):
        """
        Test loading non-existent file.
        Joq fayldi júklew testı.
        """
        with pytest.raises(FileNotFoundError):
            manager.load_ontology("nonexistent_file.owl")

    def test_load_ontology_not_loaded_error(self, manager):
        """
        Test error when ontology not loaded.
        Ontologiya júklenmegen waqtında qátelik testı.
        """
        with pytest.raises(OntologyNotLoadedError):
            manager.query_sparql("SELECT * WHERE { ?s ?p ?o }")

    def test_get_class(self, manager, sample_ontology_path):
        """
        Test getting OWL class.
        OWL klass alıw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Test Karakalpak legal terms / Qaraqalpaq huquqıy terminlerin test etiw
        nizam = manager.get_class("Nızam")
        assert nizam is not None
        assert isinstance(nizam, URIRef)

        statiya = manager.get_class("Statiya")
        assert statiya is not None

        jinayat = manager.get_class("Jinayat")
        assert jinayat is not None

        jaza = manager.get_class("Jaza")
        assert jaza is not None

        # Test non-existent class / Joq klassnı test etiw
        nonexistent = manager.get_class("NonExistentClass")
        assert nonexistent is None

    def test_get_instances(self, manager, sample_ontology_path):
        """
        Test getting class instances.
        Klass misallarin alıw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Get crime instances / Jinayat misallarin alıw
        crimes = manager.get_instances("Jinayat", lang="kaa")
        assert len(crimes) > 0
        assert any('Urılıq' in str(c.get('label', '')) for c in crimes)

        # Get article instances / Statiya misallarin alıw
        articles = manager.get_instances("Statiya", lang="kaa")
        assert len(articles) > 0

    def test_search_by_label(self, manager, sample_ontology_path):
        """
        Test searching by label.
        Label boyınsha izlew testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Search in Karakalpak / Qaraqalpaqsha izlew
        results = manager.search_by_label("jinayat", lang="kaa")
        assert len(results) > 0

        # Search with fuzzy matching / Anıq emes sáykeslik menen izlew
        results_fuzzy = manager.search_by_label("jınayat", lang="kaa", fuzzy=True)
        assert len(results_fuzzy) > 0

    def test_query_sparql(self, manager, sample_ontology_path):
        """
        Test SPARQL query execution.
        SPARQL soraw orınlaw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Query all crimes / Barlıq jinayatlardı soraw
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?crime ?label
        WHERE {
            ?crime a huquq:Jinayat ;
                   rdfs:label ?label .
            FILTER(LANG(?label) = "kaa")
        }
        """

        results = manager.query_sparql(query)
        assert isinstance(results, list)
        assert len(results) > 0

    def test_add_individual(self, manager, sample_ontology_path):
        """
        Test adding new individual.
        Jańa individual qosıw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Add new article / Jańa statiya qosıw
        article_uri = manager.add_individual(
            "Statiya",
            "Statiya_456",
            {
                "articleNumber": "456",
                "title": "Jańa statiya",
                "language": "kaa"
            }
        )

        assert article_uri is not None
        assert isinstance(article_uri, URIRef)

        # Verify it was added / Qosılǵanın tastıqlaw
        articles = manager.get_instances("Statiya")
        assert any("Statiya_456" in a.get('uri', '') for a in articles)

    def test_get_related(self, manager, sample_ontology_path):
        """
        Test getting related resources.
        Baylanıslı resurslarni alıw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Get relations for crime / Jinayat ushın baylanıslarni alıw
        crime_uri = "http://huquqai.org/ontology#Jinayat_UrAq"
        relations = manager.get_related(crime_uri)

        assert isinstance(relations, list)
        assert len(relations) > 0

    def test_save_ontology(self, manager, sample_ontology_path, tmp_path):
        """
        Test saving ontology.
        Ontologiyani saqlawish testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Save to new file / Jańa faylǵa saqlawish
        output_file = tmp_path / "output_ontology.ttl"
        result = manager.save_ontology(output_file, format="turtle")

        assert result is True
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_get_statistics(self, manager, sample_ontology_path):
        """
        Test getting statistics.
        Statistikani alıw testı.
        """
        manager.load_ontology(sample_ontology_path)

        stats = manager.get_statistics()

        assert isinstance(stats, dict)
        assert stats['loaded'] is True
        assert stats['triple_count'] > 0
        assert stats['class_count'] > 0
        assert 'load_time' in stats

    def test_clear(self, manager, sample_ontology_path):
        """
        Test clearing ontology.
        Ontologiyani tazalaw testı.
        """
        manager.load_ontology(sample_ontology_path)
        assert manager.is_loaded()

        manager.clear()

        assert not manager.is_loaded()
        assert manager.stats['loaded'] is False
        assert manager.stats['triple_count'] == 0

    def test_repr(self, manager):
        """
        Test string representation.
        Júrgen shıǵı kórinisi testı.
        """
        repr_str = repr(manager)

        assert "OntologyManager" in repr_str
        assert "not loaded" in repr_str or "júklenmedi" in repr_str


class TestKarakalpakTerminology:
    """
    Test Karakalpak legal terminology.
    Qaraqalpaq huquqıy terminologiyasın test etiw.
    """

    def test_legal_terms(self, manager, sample_ontology_path):
        """
        Test all Karakalpak legal terms are loaded.
        Barlıq Qaraqalpaq huquqıy terminleriniń júklengenin test etiw.
        """
        manager.load_ontology(sample_ontology_path)

        # Test Nızam (Law) / Nızam (Huqıqlıq nızam)
        nizam = manager.get_class("Nızam")
        assert nizam is not None

        # Test Statiya (Article) / Statiya
        statiya = manager.get_class("Statiya")
        assert statiya is not None

        # Test Jinayat (Crime) / Jinayat
        jinayat = manager.get_class("Jinayat")
        assert jinayat is not None

        # Test Jaza (Punishment) / Jaza
        jaza = manager.get_class("Jaza")
        assert jaza is not None

    def test_karakalpak_labels(self, manager, sample_ontology_path):
        """
        Test Karakalpak language labels.
        Qaraqalpaq tili labelların test etiw.
        """
        manager.load_ontology(sample_ontology_path)

        # Search for Karakalpak terms / Qaraqalpaq terminlerin izlew
        results = manager.search_by_label("Nızam", lang="kaa")
        assert len(results) > 0

        results = manager.search_by_label("Statiya", lang="kaa")
        assert len(results) > 0

        results = manager.search_by_label("Jinayat", lang="kaa")
        assert len(results) > 0

    def test_utf8_encoding(self, manager, sample_ontology_path):
        """
        Test UTF-8 encoding for Karakalpak characters.
        Qaraqalpaq háripler ushın UTF-8 kodlaw testı.
        """
        manager.load_ontology(sample_ontology_path)

        # Test special Karakalpak characters / Ayrıqsha Qaraqalpaq háriplerin test etiw
        # ǵ, ń, ı, ú, ó
        results = manager.search_by_label("Jinayattıń awır túri", lang="kaa")
        # Should not crash with special characters
        assert isinstance(results, list)


# Integration test / Integratsiya testı
def test_full_workflow(tmp_path):
    """
    Test complete workflow with Karakalpak legal data.
    Qaraqalpaq huquqıy ma'limleri menen tóliq iš joli testı.
    """
    manager = get_ontology_manager()
    manager.clear()

    # Create test ontology / Test ontologiyasın jasawiш
    ontology_path = tmp_path / "test.owl"
    ontology_path.write_text("""<?xml version="1.0"?>
    <rdf:RDF xmlns="http://huquqai.org/ontology#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
        <owl:Ontology rdf:about="http://huquqai.org/ontology"/>
        <owl:Class rdf:about="http://huquqai.org/ontology#Jinayat">
            <rdfs:label xml:lang="kaa">Jinayat</rdfs:label>
        </owl:Class>
    </rdf:RDF>
    """, encoding='utf-8')

    # Load / Júklew
    manager.load_ontology(ontology_path)
    assert manager.is_loaded()

    # Query / Soraw
    jinayat = manager.get_class("Jinayat")
    assert jinayat is not None

    # Add individual / Individual qosıw
    crime_uri = manager.add_individual(
        "Jinayat",
        "Jinayat_Test",
        {"label": "Test jinayat"}
    )
    assert crime_uri is not None

    # Save / Saqlawish
    output_path = tmp_path / "updated.ttl"
    manager.save_ontology(output_path)
    assert output_path.exists()

    # Clear / Tazalaw
    manager.clear()
    assert not manager.is_loaded()
