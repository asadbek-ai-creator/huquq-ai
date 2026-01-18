"""
Usage Examples for SPARQLEngine
SPARQLEngine qollanıw misalları

This file demonstrates how to use the SPARQLEngine for querying Karakalpak legal data.
Bu fayl Qaraqalpaq huquqıy ma'limlerin soraw etiw ushın SPARQLEngine qollanıwdı kórsetedi.
"""

from pathlib import Path
from src.core.ontology_manager import get_ontology_manager, OntologyManagerError
from src.core.sparql_engine import SPARQLEngine, SPARQLEngineError


def example_1_basic_select_query():
    """
    Example 1: Basic SELECT query
    Misal 1: Baslanǵısh SELECT soraw
    """
    print("=" * 60)
    print("Example 1: Basic SELECT Query / Misal 1: Baslanǵısh SELECT Soraw")
    print("=" * 60)

    # Get ontology manager and load data
    manager = get_ontology_manager()

    try:
        manager.load_ontology("data/ontologies/criminal_code.owl")
        print("✓ Ontology loaded / Ontologiya júklendi")

        # Create SPARQL engine
        engine = SPARQLEngine(manager.graph)
        print("✓ SPARQL engine initialized / SPARQL mexanizmi inicializaciyalandı\n")

        # Execute SELECT query for all crimes
        query = """
        PREFIX huquq: <http://huquqai.org/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?jinayat ?label ?turi
        WHERE {
            ?jinayat a huquq:Jinayat .
            ?jinayat rdfs:label ?label .
            OPTIONAL { ?jinayat huquq:crimeType ?turi }
            FILTER(LANG(?label) = "kaa")
        }
        LIMIT 5
        """

        print("Executing query / Sorawdı orınlaw:")
        print("Finding all crimes / Barlıq jinayatlardı tabıw\n")

        results = engine.select(query, lang="kaa")

        print(f"Found {len(results)} crimes / {len(results)} jinayat tabıldı:\n")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.get('label', 'N/A')}")
            print(f"     URI: {result.get('jinayat', 'N/A')}")
            if 'turi' in result:
                print(f"     Type / Túri: {result['turi']}")
            print()

    except FileNotFoundError:
        print("⚠ Ontology file not found / Ontologiya faylı tabılmadı")
    except (OntologyManagerError, SPARQLEngineError) as e:
        print(f"✗ Error / Qátelik: {e}")


def example_2_ask_query():
    """
    Example 2: ASK query to check existence
    Misal 2: Bar-joqlıǵın tastıqlaw ushın ASK soraw
    """
    print("\n" + "=" * 60)
    print("Example 2: ASK Query / Misal 2: ASK Soraw")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Check if any theft crimes exist
    query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    ASK {
        ?jinayat a huquq:Jinayat .
        ?jinayat rdfs:label ?label .
        FILTER(CONTAINS(LCASE(STR(?label)), "urılıq"))
    }
    """

    print("\nChecking if theft crimes exist:")
    print("Urılıq jinayatlardıń bar ekenin tastıqlaw:\n")

    exists = engine.ask(query)

    if exists:
        print("✓ Yes, theft crimes exist in the knowledge base")
        print("  Hawa, urılıq jinayatları bilimler bazasında bar")
    else:
        print("✗ No theft crimes found")
        print("  Urılıq jinayatları tabılmadı")


def example_3_construct_query():
    """
    Example 3: CONSTRUCT query to build new graph
    Misal 3: Jańa graf quriw ushın CONSTRUCT soraw
    """
    print("\n" + "=" * 60)
    print("Example 3: CONSTRUCT Query / Misal 3: CONSTRUCT Soraw")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Construct a simplified graph with only crime labels
    query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    CONSTRUCT {
        ?jinayat rdfs:label ?label .
        ?jinayat huquq:crimeType ?turi .
    }
    WHERE {
        ?jinayat a huquq:Jinayat .
        ?jinayat rdfs:label ?label .
        OPTIONAL { ?jinayat huquq:crimeType ?turi }
        FILTER(LANG(?label) = "kaa")
    }
    LIMIT 3
    """

    print("\nConstructing simplified crime graph:")
    print("Basıtılandırılǵan jinayat grafin quriw:\n")

    try:
        result = engine.construct(query, format="turtle")

        print("Generated RDF Turtle / Jasalǵan RDF Turtle:")
        print("-" * 40)
        print(result[:500])  # Show first 500 characters
        if len(result) > 500:
            print("... (truncated / qısqartıldı)")

    except SPARQLEngineError as e:
        print(f"✗ Construction failed / Quriw sátsiz: {e}")


def example_4_search_by_karakalpak_term():
    """
    Example 4: Search using Karakalpak terms
    Misal 4: Qaraqalpaq terminler menen izlew
    """
    print("\n" + "=" * 60)
    print("Example 4: Karakalpak Term Search / Misal 4: Qaraqalpaq Termin Izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Search for different Karakalpak legal terms
    terms = ["jinayat", "jaza", "statiya", "urılıq"]

    print("\nSearching for Karakalpak legal terms:")
    print("Qaraqalpaq huquqıy terminlerin izlew:\n")

    for term in terms:
        print(f"Searching for '{term}' / '{term}' sózin izlew:")

        results = engine.search_by_term_kaa(term, limit=3)

        if results:
            print(f"  Found {len(results)} results / {len(results)} nátiyјe tabıldı:")
            for result in results:
                print(f"    - {result.get('label', 'N/A')}")
        else:
            print("  No results found / Nátiyјe tabılmadı")
        print()


def example_5_fuzzy_search():
    """
    Example 5: Fuzzy search for typos
    Misal 5: Qáteler ushın anıq emes izlew
    """
    print("\n" + "=" * 60)
    print("Example 5: Fuzzy Search / Misal 5: Anıq Emes Izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Search with intentional typos
    search_terms = [
        ("jinayat", "jınayat"),  # Correct vs typo
        ("urılıq", "uriliq"),
    ]

    print("\nTesting fuzzy search with typos:")
    print("Qáteler menen anıq emes izlewdi test etiw:\n")

    for correct, typo in search_terms:
        print(f"Correct term / Toǵrı termin: '{correct}'")
        print(f"With typo / Qáte menen: '{typo}'\n")

        # Normal search with typo (may not find results)
        normal_results = engine.search_by_term_kaa(typo, fuzzy=False, limit=3)
        print(f"  Normal search: {len(normal_results)} results")

        # Fuzzy search with typo (should find results)
        fuzzy_results = engine.search_by_term_kaa(typo, fuzzy=True, limit=3)
        print(f"  Fuzzy search: {len(fuzzy_results)} results")

        if fuzzy_results:
            print("  ✓ Fuzzy search found matches:")
            for result in fuzzy_results[:2]:
                print(f"    - {result.get('label', 'N/A')}")
        print()


def example_6_punishment_year_ranges():
    """
    Example 6: Find punishments by year ranges
    Misal 6: Jıl diapazoni boyınsha jazalar tabıw
    """
    print("\n" + "=" * 60)
    print("Example 6: Punishment Year Ranges / Misal 6: Jaza Jıl Diapazoni")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Different punishment ranges
    ranges = [
        (0, 2, "Light punishments / Jeńil jazalar (0-2 jıl)"),
        (3, 5, "Medium punishments / Orta jazalar (3-5 jıl)"),
        (5, None, "Severe punishments / Awır jazalar (5+ jıl)"),
    ]

    print("\nFinding punishments by year ranges:")
    print("Jıl diapazoni boyınsha jazalar tabıw:\n")

    for min_years, max_years, description in ranges:
        print(f"{description}:")

        results = engine.get_jaza_range(min_jıl=min_years, max_jıl=max_years)

        if results:
            print(f"  Found {len(results)} punishments / {len(results)} jaza tabıldı:")
            for result in results[:3]:  # Show first 3
                min_y = result.get('minYears', 'N/A')
                max_y = result.get('maxYears', 'N/A')
                label = result.get('label', 'N/A')
                print(f"    - {label}: {min_y}-{max_y} jıl")
        else:
            print("  No punishments found / Jazalar tabılmadı")
        print()


def example_7_search_by_crime_type():
    """
    Example 7: Search crimes by severity type
    Misal 7: Awırlıq túri boyınsha jinayatlardı izlew
    """
    print("\n" + "=" * 60)
    print("Example 7: Search by Crime Type / Misal 7: Jinayat Túri Boyınsha Izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Different crime severity types in Karakalpak
    crime_types = [
        ("jeńil", "Light crimes / Jeńil jinayatlar"),
        ("orta", "Medium crimes / Orta awırlıqtaǵı jinayatlar"),
        ("awır", "Severe crimes / Awır jinayatlar"),
        ("óte awır", "Very severe crimes / Óte awır jinayatlar"),
    ]

    print("\nSearching crimes by severity type:")
    print("Awırlıq túri boyınsha jinayatlardı izlew:\n")

    for crime_type, description in crime_types:
        print(f"{description} ('{crime_type}'):")

        results = engine.search_jinayat_turi(crime_type, limit=5)

        if results:
            print(f"  Found {len(results)} crimes / {len(results)} jinayat tabıldı:")
            for result in results:
                label = result.get('label', 'N/A')
                turi = result.get('crimeType', 'N/A')
                print(f"    - {label} (túri: {turi})")
        else:
            print("  No crimes found / Jinayatlar tabılmadı")
        print()


def example_8_search_articles():
    """
    Example 8: Search legal articles
    Misal 8: Huquqıy statiyalardı izlew
    """
    print("\n" + "=" * 60)
    print("Example 8: Search Articles / Misal 8: Statiyalardı Izlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    print("\nSearching articles by number:")
    print("Nomer boyınsha statiyalardı izlew:\n")

    # Search for specific article number
    article_number = "123"
    results = engine.search_statiya(nomer=article_number, kodeks=None)

    if results:
        print(f"Article {article_number} / Statiya {article_number}:")
        for result in results:
            label = result.get('label', 'N/A')
            code = result.get('codeType', 'N/A')
            print(f"  - {label} (Kodeks: {code})")
    else:
        print(f"  Article {article_number} not found / Statiya {article_number} tabılmadı")

    print("\nSearching articles by code type:")
    print("Kodeks túri boyınsha statiyalardı izlew:\n")

    # Search by code types
    code_types = [
        ("JK", "Criminal Code / Jinayat Kodeksi"),
        ("AK", "Administrative Code / Administrativlik Kodeksi"),
        ("ShK", "Civil Code / Shıwıllıq Kodeksi"),
    ]

    for code, description in code_types:
        print(f"{description} ({code}):")
        results = engine.search_statiya(nomer=None, kodeks=code)

        if results:
            print(f"  Found {len(results)} articles / {len(results)} statiya tabıldı")
            for result in results[:3]:  # Show first 3
                print(f"    - {result.get('label', 'N/A')}")
        else:
            print("  No articles found / Statiyalar tabılmadı")
        print()


def example_9_crime_punishment_relations():
    """
    Example 9: Get crimes with their punishments
    Misal 9: Jinayatlardı olardıń jazaları menen alıw
    """
    print("\n" + "=" * 60)
    print("Example 9: Crime-Punishment Relations / Misal 9: Jinayat-Jaza Baylanısları")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Get all crimes first
    print("\nFinding crimes and their punishments:")
    print("Jinayatlardı ha'm olardıń jazalarin tabıw:\n")

    crimes_query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    SELECT ?jinayat WHERE { ?jinayat a huquq:Jinayat } LIMIT 5
    """

    crimes = engine.select(crimes_query)

    for i, crime in enumerate(crimes, 1):
        crime_uri = crime.get('jinayat')

        print(f"{i}. Crime URI / Jinayat URI: {crime_uri}")

        # Get related punishments
        relations = engine.get_related_jinayat_jaza(crime_uri)

        if relations:
            for rel in relations:
                jinayat_label = rel.get('jinayatLabel', 'N/A')
                jaza_label = rel.get('jazaLabel', 'N/A')
                print(f"   Crime / Jinayat: {jinayat_label}")
                print(f"   Punishment / Jaza: {jaza_label}")
        else:
            print("   No punishment information / Jaza maǵlıwmatı joq")
        print()


def example_10_query_caching():
    """
    Example 10: Demonstrate query caching
    Misal 10: Soraw keshlew kórsetpesi
    """
    print("\n" + "=" * 60)
    print("Example 10: Query Caching / Misal 10: Soraw Keshlew")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    SELECT ?s WHERE { ?s a huquq:Jinayat } LIMIT 10
    """

    print("\nExecuting same query multiple times:")
    print("Bir sorawdı bir neshe ret orınlaw:\n")

    # Clear cache first
    engine.clear_cache()

    # First execution
    print("1st execution (cache miss) / 1-shi orınlaw (keshte joq):")
    stats_before = engine.get_statistics()
    engine.execute_cached(query, query_type="select")
    stats_after1 = engine.get_statistics()
    time1 = stats_after1['total_execution_time'] - stats_before['total_execution_time']
    print(f"   Time / Waqt: {time1:.4f}s")
    print(f"   Cache misses / Keshte joq: {stats_after1['cache_misses']}")

    # Second execution (should use cache)
    print("\n2nd execution (cache hit) / 2-shi orınlaw (keshte bar):")
    engine.execute_cached(query, query_type="select")
    stats_after2 = engine.get_statistics()
    time2 = stats_after2['total_execution_time'] - stats_after1['total_execution_time']
    print(f"   Time / Waqt: {time2:.4f}s")
    print(f"   Cache hits / Keshten alındı: {stats_after2['cache_hits']}")

    # Third execution (should also use cache)
    print("\n3rd execution (cache hit) / 3-shi orınlaw (keshte bar):")
    engine.execute_cached(query, query_type="select")
    stats_after3 = engine.get_statistics()
    time3 = stats_after3['total_execution_time'] - stats_after2['total_execution_time']
    print(f"   Time / Waqt: {time3:.4f}s")
    print(f"   Cache hits / Keshten alındı: {stats_after3['cache_hits']}")

    print("\n✓ Caching improves performance for repeated queries")
    print("  Keshlew qayta-qayta orınlanıwshı sorawlar ushın tabıslılıqtı jaqsılaydı")


def example_11_statistics():
    """
    Example 11: View engine statistics
    Misal 11: Mexanizm statistikasın kóriw
    """
    print("\n" + "=" * 60)
    print("Example 11: Engine Statistics / Misal 11: Mexanizm Statistikası")
    print("=" * 60)

    manager = get_ontology_manager()

    if not manager.is_loaded():
        print("⚠ Please load ontology first / Aldı bılan ontologiyani júkleń")
        return

    engine = SPARQLEngine(manager.graph)

    # Execute various queries to generate statistics
    engine.search_by_term_kaa("jinayat", limit=5)
    engine.search_jinayat_turi("orta", limit=5)
    engine.get_jaza_range(min_jıl=1, max_jıl=5)

    print("\nSPARQL Engine Statistics:")
    print("SPARQL Mexanizmi Statistikası:\n")

    stats = engine.get_statistics()

    print(f"  Total queries executed / Órınlengen sorawlar sanı:")
    print(f"    {stats['queries_executed']}")

    print(f"\n  Cache statistics / Kesh statistikası:")
    print(f"    Cache hits / Keshten alındı: {stats['cache_hits']}")
    print(f"    Cache misses / Keshte joq: {stats['cache_misses']}")

    if stats['queries_executed'] > 0:
        cache_hit_rate = (stats['cache_hits'] / stats['queries_executed']) * 100
        print(f"    Hit rate / Tabıslılıq: {cache_hit_rate:.1f}%")

    print(f"\n  Performance / Tabıslılıq:")
    print(f"    Total time / Tóliq waqt: {stats['total_execution_time']:.4f}s")
    print(f"    Average time / Ortasha waqt: {stats['average_query_time']:.4f}s")


def main():
    """
    Run all examples
    Barlıq misallardı júrgiziw
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "SPARQLEngine Usage Examples" + " " * 21 + "║")
    print("║" + " " * 8 + "SPARQLEngine Qollanıw Misalları" + " " * 19 + "║")
    print("╚" + "═" * 58 + "╝")

    # Run examples
    example_1_basic_select_query()
    example_2_ask_query()
    example_3_construct_query()
    example_4_search_by_karakalpak_term()
    example_5_fuzzy_search()
    example_6_punishment_year_ranges()
    example_7_search_by_crime_type()
    example_8_search_articles()
    example_9_crime_punishment_relations()
    example_10_query_caching()
    example_11_statistics()

    print("\n" + "=" * 60)
    print("All examples completed / Barlıq misallar tamamlandı")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
