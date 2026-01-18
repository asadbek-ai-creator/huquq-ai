"""
Usage Examples for OntologyManager
OntologyManager qollanıw misalları

This file demonstrates how to use the OntologyManager for Karakalpak legal data.
Bu fayl Qaraqalpaq huquqıy ma'limleri ushın OntologyManager qollanıwdı kórsetedi.
"""

from pathlib import Path
from src.core.ontology_manager import get_ontology_manager, OntologyManagerError


def example_1_load_ontology():
    """
    Example 1: Load and inspect ontology
    Misal 1: Ontologiyani júklew ha'm kóziw
    """
    print("=" * 60)
    print("Example 1: Loading Ontology / Misal 1: Ontologiyani júklew")
    print("=" * 60)

    # Get manager instance / Menedžer misalın alıw
    manager = get_ontology_manager()

    # Load Criminal Code ontology / Jinayat Kodeksi ontologiyasın júklew
    try:
        ontology_path = "data/ontologies/criminal_code.owl"
        print(f"\nLoading ontology / Ontologiyani júklew: {ontology_path}")

        manager.load_ontology(ontology_path)
        print("✓ Ontology loaded successfully / Ontologiya tabıslı júklendi")

        # Get statistics / Statistikani alıw
        stats = manager.get_statistics()
        print(f"\nStatistics / Statistika:")
        print(f"  Triples / Triple-lar: {stats['triple_count']}")
        print(f"  Classes / Klasslar: {stats['class_count']}")
        print(f"  Individuals / Individuallar: {stats['individual_count']}")
        print(f"  Load time / Júklew waqtı: {stats['load_time']:.2f}s")

    except FileNotFoundError:
        print("⚠ Ontology file not found / Ontologiya faylı tabılmadı")
        print("  Please ensure the file exists / Fayldıń bar ekenin tastıqlaný")
    except OntologyManagerError as e:
        print(f"✗ Error / Qátelik: {e.message}")
        print(f"  Qaraqalpaqsha: {e.message_kaa}")


def example_2_query_classes():
    """
    Example 2: Query legal classes
    Misal 2: Huquqıy klasslardı soraw
    """
    print("\n" + "=" * 60)
    print("Example 2: Querying Legal Classes / Misal 2: Huquqıy klasslardı soraw")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Get Karakalpak legal classes / Qaraqalpaq huquqıy klasslarin alıw
    legal_classes = ["Nızam", "Statiya", "Jinayat", "Jaza"]

    print("\nLegal Classes / Huquqıy Klasslar:")
    for class_name in legal_classes:
        class_uri = manager.get_class(class_name)
        if class_uri:
            print(f"  ✓ {class_name}: {class_uri}")
        else:
            print(f"  ✗ {class_name}: Not found / Tabılmadı")


def example_3_search_crimes():
    """
    Example 3: Search for crimes
    Misal 3: Jinayatlardı izlew
    """
    print("\n" + "=" * 60)
    print("Example 3: Searching Crimes / Misal 3: Jinayatlardı izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Get all crimes / Barlıq jinayatlardı alıw
    print("\nAll Crimes / Barlıq Jinayatlar:")
    crimes = manager.get_instances("Jinayat", lang="kaa", limit=5)

    if crimes:
        for i, crime in enumerate(crimes, 1):
            print(f"\n  {i}. {crime.get('label', 'No label')}")
            print(f"     URI: {crime.get('uri', 'N/A')}")
            if 'crimeType' in crime:
                print(f"     Type / Túri: {crime['crimeType']}")
    else:
        print("  No crimes found / Jinayatlar tabılmadı")

    # Search by keyword / Kalit sóz boyınsha izlew
    print("\n\nSearch for 'jinayat' / 'jinayat' sózin izlew:")
    results = manager.search_by_label("jinayat", lang="kaa")

    for result in results[:3]:
        print(f"  - {result['label']} ({result['language']})")


def example_4_sparql_query():
    """
    Example 4: Execute SPARQL query
    Misal 4: SPARQL sorawdı orınlaw
    """
    print("\n" + "=" * 60)
    print("Example 4: SPARQL Query / Misal 4: SPARQL Sorawı")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # SPARQL query to find all articles / Barlıq statiyalardı tabıw ushın SPARQL soraw
    query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?statiya ?number ?title
    WHERE {
        ?statiya a huquq:Statiya .
        OPTIONAL { ?statiya huquq:articleNumber ?number }
        OPTIONAL { ?statiya rdfs:label ?title
                   FILTER(LANG(?title) = "kaa") }
    }
    LIMIT 5
    """

    print("\nExecuting SPARQL query / SPARQL sorawdı orınlaw:")
    print("Query / Soraw: Finding articles / Statiyalardı tabıw")

    try:
        results = manager.query_sparql(query)

        print(f"\nFound {len(results)} articles / {len(results)} statiya tabıldı:")
        for i, result in enumerate(results, 1):
            number = result.get('number', 'N/A')
            title = result.get('title', 'No title')
            print(f"  {i}. Article {number}: {title}")

    except OntologyManagerError as e:
        print(f"✗ Query failed / Soraw sátsiz: {e.message}")


def example_5_add_new_article():
    """
    Example 5: Add new article to ontology
    Misal 5: Ontologiyaga jańa statiya qosıw
    """
    print("\n" + "=" * 60)
    print("Example 5: Adding New Article / Misal 5: Jańa Statiya Qosıw")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Add new article / Jańa statiya qosıw
    print("\nAdding new article / Jańa statiya qosıw:")

    try:
        article_uri = manager.add_individual(
            class_name="Statiya",
            individual_name="Statiya_999",
            properties={
                "articleNumber": "999",
                "title": "Test Statiyası",
                "description": "Bu test ushın jasalǵan statiya",
                "language": "kaa"
            }
        )

        print(f"✓ Article added / Statiya qosıldı: {article_uri}")

        # Verify it was added / Qosılǵanın tastıqlaw
        articles = manager.get_instances("Statiya", limit=100)
        new_article = next((a for a in articles if "Statiya_999" in a.get('uri', '')), None)

        if new_article:
            print(f"\n  Verified / Tastıqlandı:")
            print(f"    URI: {new_article.get('uri')}")
            print(f"    Number: {new_article.get('articleNumber', 'N/A')}")
            print(f"    Title: {new_article.get('title', 'N/A')}")
        else:
            print("⚠ Could not verify addition / Qosıwdı tastıqlaw múmkin bolmadı")

    except OntologyManagerError as e:
        print(f"✗ Failed to add article / Statiya qosıw sátsiz: {e.message}")


def example_6_get_related_resources():
    """
    Example 6: Get related legal resources
    Misal 6: Baylanıslı huquqıy resurslarni alıw
    """
    print("\n" + "=" * 60)
    print("Example 6: Related Resources / Misal 6: Baylanıslı Resurslar")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Get crimes and their relations / Jinayatlardı ha'm olardıń baylanısların alıw
    crimes = manager.get_instances("Jinayat", limit=1)

    if crimes:
        crime = crimes[0]
        crime_uri = crime.get('uri')

        print(f"\nAnalyzing crime / Jinayatni analiz etiw:")
        print(f"  URI: {crime_uri}")
        print(f"  Label: {crime.get('label', 'N/A')}")

        # Get all relations / Barlıq baylanıslarni alıw
        relations = manager.get_related(crime_uri)

        print(f"\n  Relations / Baylanıslar ({len(relations)}):")
        for subj, pred, obj in relations[:5]:  # Show first 5
            print(f"    - {pred}: {obj}")

        # Get specific relation (punishment) / Belgili baylanıs (jaza)
        punishments = manager.get_related(crime_uri, "hasPunishment")
        if punishments:
            print(f"\n  Punishments / Jazalar:")
            for _, _, punishment in punishments:
                print(f"    - {punishment}")
    else:
        print("No crimes found / Jinayatlar tabılmadı")


def example_7_save_updated_ontology():
    """
    Example 7: Save updated ontology
    Misal 7: Jańalanǵan ontologiyani saqlawish
    """
    print("\n" + "=" * 60)
    print("Example 7: Saving Ontology / Misal 7: Ontologiyani Saqlawish")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Save to different formats / Túrli formatlarda saqlawish
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    formats = [
        ("turtle", "updated_ontology.ttl", "Turtle"),
        ("xml", "updated_ontology.owl", "RDF/XML"),
    ]

    print("\nSaving ontology in different formats:")
    print("Ontologiyani túrli formatlarda saqlawish:")

    for format_name, filename, display_name in formats:
        try:
            output_path = output_dir / filename
            manager.save_ontology(output_path, format=format_name)
            print(f"  ✓ {display_name}: {output_path}")
        except OntologyManagerError as e:
            print(f"  ✗ {display_name}: Failed / Sátsiz - {e.message}")


def example_8_multilingual_search():
    """
    Example 8: Multilingual search
    Misal 8: Kóp tilli izlew
    """
    print("\n" + "=" * 60)
    print("Example 8: Multilingual Search / Misal 8: Kóp Tilli Izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    # Search in different languages / Túrli tillerde izlew
    languages = [
        ("kaa", "Qaraqalpaqsha"),
        ("uz", "Ózbekше"),
        ("ru", "Орысша"),
        ("en", "English"),
    ]

    search_term = "law"  # Or "nızam", "qonun", "закон"

    print(f"\nSearching for '{search_term}' in different languages:")
    print(f"'{search_term}' sózin túrli tillerde izlew:")

    for lang_code, lang_name in languages:
        results = manager.search_by_label(search_term, lang=lang_code)
        print(f"\n  {lang_name} ({lang_code}):")
        if results:
            for result in results[:2]:
                print(f"    - {result['label']}")
        else:
            print(f"    No results / Nátiyјe joq")


def main():
    """
    Run all examples
    Barlıq misallardı júrgiziw
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 8 + "OntologyManager Usage Examples" + " " * 19 + "║")
    print("║" + " " * 6 + "OntologyManager Qollanıw Misalları" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")

    # Run examples / Misallardı júrgiziw
    example_1_load_ontology()
    example_2_query_classes()
    example_3_search_crimes()
    example_4_sparql_query()
    example_5_add_new_article()
    example_6_get_related_resources()
    example_7_save_updated_ontology()
    example_8_multilingual_search()

    print("\n" + "=" * 60)
    print("All examples completed / Barlıq misallar tamamlandı")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
