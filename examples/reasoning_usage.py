"""
Usage Examples for ReasoningEngine
ReasoningEngine qollanıw misalları

This file demonstrates how to use the OWL reasoning engine for Karakalpak legal data.
Bu fayl Qaraqalpaq huquqıy ma'limleri ushın OWL mántıqlı juwmaq mexanizmin qollanıwdı kórsetedi.
"""

from pathlib import Path
from src.core.ontology_manager import get_ontology_manager, OntologyManagerError
from src.core.reasoning_engine import (
    ReasoningEngine,
    ReasoningEngineError,
    ReasonerType,
    JinayatAwırlıǵı,
    JazaTuri,
    create_reasoning_engine
)


def example_1_check_consistency():
    """
    Example 1: Check ontology consistency
    Misal 1: Ontologiya úyelisligin tastıqlaw
    """
    print("=" * 60)
    print("Example 1: Consistency Check / Misal 1: Úyelislik Tastıqlaw")
    print("=" * 60)

    try:
        # Load ontology
        ontology_path = "data/ontologies/criminal_code.owl"
        print(f"\nLoading ontology / Ontologiyani júklew: {ontology_path}")

        engine = create_reasoning_engine(ontology_path, ReasonerType.PELLET)
        print("✓ Reasoning engine created / Mántıqlı juwmaq mexanizmi jasaldı")

        # Check consistency
        print("\nChecking consistency / Úyelislikti tastıqlaw...")
        is_consistent = engine.check_consistency()

        if is_consistent:
            print("✓ Ontology is consistent! / Ontologiya úyelisli!")
            print("  No logical contradictions found.")
            print("  Logikalıq qarama-qarsılıqlar tabılmadı.")
        else:
            print("✗ Ontology has inconsistencies!")
            print("  Ontologiyada úyelisliksizlikler bar!")

        # Show statistics
        stats = engine.get_statistics()
        print(f"\nStatistics / Statistika:")
        print(f"  Reasoning time / Mántıq juwmaq waqtı: {stats['last_reasoning_time']:.4f}s")

    except FileNotFoundError:
        print("⚠ Ontology file not found / Ontologiya faylı tabılmadı")
    except ReasoningEngineError as e:
        print(f"✗ Reasoning error / Mántıq juwmaq qáteligi: {e}")


def example_2_classify_ontology():
    """
    Example 2: Perform classification reasoning
    Misal 2: Klassifikaciya mántıq juwmaǵın orınlaw
    """
    print("\n" + "=" * 60)
    print("Example 2: Classification / Misal 2: Klassifikaciya")
    print("=" * 60)

    try:
        ontology_path = "data/ontologies/criminal_code.owl"
        engine = create_reasoning_engine(ontology_path)

        print("\nRunning classification reasoning...")
        print("Klassifikaciya mántıq juwmaǵın júrgiziwde...")

        result = engine.classify(explain=True)

        if result.success:
            print(f"\n✓ Classification completed successfully!")
            print(f"  Klassifikaciya tabıslı tamamlandı!")
            print(f"\n  Inferences made / Jasalǵan qorıtındılar: {len(result.inferences)}")
            print(f"  Execution time / Orınlaw waqtı: {result.execution_time:.4f}s")
            print(f"  Reasoner / Mántıq juwmaqshı: {result.reasoner_type}")

            if result.inferences:
                print("\n  Sample inferences / Misal qorıtındılar:")
                for i, inf in enumerate(result.inferences[:5], 1):
                    print(f"    {i}. {inf.get('individual', 'N/A')} → {inf.get('class', 'N/A')}")

            if result.explanations:
                print(f"\n  Explanations / Túsindirmeler:")
                for expl in result.explanations[:3]:
                    print(f"    - {expl}")

    except Exception as e:
        print(f"✗ Classification failed / Klassifikaciya sátsiz: {e}")


def example_3_classify_crime_severity():
    """
    Example 3: Classify crimes by severity
    Misal 3: Jinayatlardı awırlıǵı boyınsha klassifikaciyalaw
    """
    print("\n" + "=" * 60)
    print("Example 3: Crime Severity Classification")
    print("Misal 3: Jinayat Awırlıǵı Klassifikaciyası")
    print("=" * 60)

    try:
        # Create engine with RDF graph
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)
        print("✓ Engine initialized / Mexanizm inicializaciyalandı\n")

        # Test crimes with different severities
        crimes = [
            ("http://huquqai.org/ontology#Jinayat_Jeńil", "Light crime / Jeńil jinayat"),
            ("http://huquqai.org/ontology#Jinayat_Urılıq", "Theft / Urılıq"),
            ("http://huquqai.org/ontology#Jinayat_Awır", "Severe crime / Awır jinayat"),
            ("http://huquqai.org/ontology#Jinayat_OteAwır", "Very severe / Óte awır"),
        ]

        print("Classifying crimes by punishment duration:")
        print("Jinayatlardı jaza uzaqlıǵı boyınsha klassifikaciyalaw:\n")

        for crime_uri, description in crimes:
            severity = engine.classify_jinayat_awırlıǵı(crime_uri)

            if severity:
                # Map severity to Karakalpak description
                severity_map = {
                    JinayatAwırlıǵı.JENIL: ("Light", "Jeńil (0-2 jıl)"),
                    JinayatAwırlıǵı.ORTA: ("Medium", "Orta (2-5 jıl)"),
                    JinayatAwırlıǵı.AWIR: ("Severe", "Awır (5-15 jıl)"),
                    JinayatAwırlıǵı.OTE_AWIR: ("Very Severe", "Óte awır (15+ jıl)"),
                }

                en_label, kaa_label = severity_map[severity]

                print(f"  {description}:")
                print(f"    Severity / Awırlıq: {en_label} / {kaa_label}")
                print(f"    Classification / Klassifikaciya: {severity.value}")
            else:
                print(f"  {description}: Could not classify / Klassifikaciyalaw múmkin emes")

            print()

        # Show reasoning rules used
        print("Reasoning Rules Applied / Qollanılǵan Mántıq Qáǵıydaları:")
        print("  • 0-2 years → jeńil jinayat (light crime)")
        print("  • 2-5 years → orta jinayat (medium crime)")
        print("  • 5-15 years → awır jinayat (severe crime)")
        print("  • 15+ years → óte awır jinayat (very severe crime)")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def example_4_infer_punishment_types():
    """
    Example 4: Infer punishment types
    Misal 4: Jaza túrlerin qorıtındılaw
    """
    print("\n" + "=" * 60)
    print("Example 4: Punishment Type Inference")
    print("Misal 4: Jaza Túri Qorıtındılawı")
    print("=" * 60)

    try:
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)
        print("✓ Engine ready / Mexanizm tayar\n")

        # Different punishment examples
        punishments = [
            ("http://huquqai.org/ontology#Jaza_Jarıma", "Fine / Jarıma"),
            ("http://huquqai.org/ontology#Jaza_Shartı", "Conditional / Shartı jaza"),
            ("http://huquqai.org/ontology#Jaza_ShimeliJumıs", "Compulsory labor / Shimeli jumıs"),
            ("http://huquqai.org/ontology#Jaza_AzatlıqtanAyırıw", "Imprisonment / Azatlıqtan ayırıw"),
        ]

        print("Inferring punishment types from properties:")
        print("Xassalardan jaza túrlerin qorıtındılaw:\n")

        for jaza_uri, description in punishments:
            pun_type = engine.infer_jaza_turi(jaza_uri)

            if pun_type:
                # Map to bilingual labels
                type_map = {
                    JazaTuri.JARIMA: ("Fine", "Jarıma - Puldı tólaw"),
                    JazaTuri.SHARTI_JAZA: ("Conditional", "Shartı jaza - Erkin, biraq qadaǵalawda"),
                    JazaTuri.SHIMELI_JUMIS: ("Compulsory Labor", "Shimeli jumıs - Májburiy jumıs"),
                    JazaTuri.AZATLIQTAN_AYIRIW: ("Imprisonment", "Azatlıqtan ayırıw - Apsanada"),
                    JazaTuri.ERTE_JIBERILIW: ("Early Release", "Erte jiberiliw"),
                }

                en_label, kaa_label = type_map[pun_type]

                print(f"  {description}:")
                print(f"    Type / Túri: {en_label}")
                print(f"    Qaraqalpaqsha: {kaa_label}")
                print(f"    Code / Kod: {pun_type.value}")
            else:
                print(f"  {description}: Type unknown / Túri belgisiz")

            print()

        # Show inference rules
        print("Inference Rules / Qorıtındılaw Qáǵıydaları:")
        print("  • minYears=0 ∧ maxYears=0 → jarıma (fine)")
        print("  • conditional=true → shartı jaza")
        print("  • compulsoryLabor=true → shimeli jumıs")
        print("  • minYears>0 → azatlıqtan ayırıw")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def example_5_check_law_consistency():
    """
    Example 5: Check law (nızam) consistency
    Misal 5: Nızam úyelisligin tastıqlaw
    """
    print("\n" + "=" * 60)
    print("Example 5: Law Consistency Check")
    print("Misal 5: Nızam Úyelislik Tastıqlawı")
    print("=" * 60)

    try:
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)

        # Check Criminal Code
        nızam_uri = "http://huquqai.org/ontology#Nızam_JinayatKodeksi"

        print("\nChecking Criminal Code of Karakalpakstan:")
        print("Qaraqalpaqstan Jinayat Kodeksin tastıqlaw:\n")
        print(f"URI: {nızam_uri}\n")

        is_consistent, issues = engine.check_nızam_consistency(nızam_uri)

        if is_consistent:
            print("✓ Law is consistent! / Nızam úyelisli!")
            print("\n  Validation checks passed / Tastıqlaw tekseriwleri ótti:")
            print("    ✓ Has required labels (kaa, en)")
            print("    ✓ Has effective date / Kúsh kirisiw sánesi bar")
            print("    ✓ Referenced articles exist / Siltelme jasalǵan statiyalar bar")
            print("    ✓ No duplicate article numbers / Qaytalanıwshı nomerler joq")
        else:
            print("✗ Law has consistency issues! / Nızamda úyelislik máseleri bar!")
            print(f"\n  Found {len(issues)} issues / {len(issues)} mákele tabıldı:")
            for i, issue in enumerate(issues, 1):
                print(f"    {i}. {issue}")

        # Show what was checked
        print("\nConsistency Criteria / Úyelislik Kriterileri:")
        print("  1. Law must have rdfs:label / Nızam label-ǵa iye bolıwı kerek")
        print("  2. Must have Karakalpak label / Qaraqalpaq label-i bolıwı kerek")
        print("  3. Must have effective date / Kúsh kirisiw sánesi bolıwı kerek")
        print("  4. Referenced articles must exist / Siltelme jasalǵan statiyalar bar bolıwı kerek")
        print("  5. Article numbers must be unique / Statiya nomerleri únikal bolıwı kerek")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def example_6_explain_inferences():
    """
    Example 6: Explain reasoning inferences
    Misal 6: Mántıqlı juwmaq qorıtındılarin túsindiriw
    """
    print("\n" + "=" * 60)
    print("Example 6: Inference Explanations")
    print("Misal 6: Qorıtındı Túsindirmeleri")
    print("=" * 60)

    try:
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)

        # Make an inference
        crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
        print("\nClassifying theft crime:")
        print("Urılıq jinayatın klassifikaciyalaw:\n")

        severity = engine.classify_jinayat_awırlıǵı(crime_uri)

        if severity:
            print(f"  Crime classified as: {severity.value}")
            print(f"  Jinayat klassifikaciyalandı: {severity.value}\n")

            # Get explanation
            explanation = engine.explain_inference(
                crime_uri,
                "http://huquqai.org/ontology#crimeType",
                severity.value
            )

            if explanation:
                print("Explanation / Túsindirme:")
                print(f"\n  Rule / Qáǵıyda: {explanation.rule}")
                print(f"\n  English:")
                print(f"    {explanation.explanation_en}")
                print(f"\n  Qaraqalpaqsha:")
                print(f"    {explanation.explanation_kaa}")
                print(f"\n  Confidence / Isenem: {explanation.confidence * 100:.0f}%")

        # Show all inferences
        all_inferences = engine.get_all_inferences()
        print(f"\n\nTotal inferences made / Jası qorıtındılar sanı: {len(all_inferences)}")

        if all_inferences:
            print("\nAll inferred facts / Barlıq qorıtındılanǵan faktlar:")
            for i, (subj, pred, obj) in enumerate(all_inferences[:5], 1):
                # Shorten URIs for display
                subj_short = subj.split('#')[-1] if '#' in subj else subj
                pred_short = pred.split('#')[-1] if '#' in pred else pred
                print(f"  {i}. {subj_short} → {pred_short} → {obj}")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def example_7_reasoning_statistics():
    """
    Example 7: View reasoning engine statistics
    Misal 7: Mántıqlı juwmaq mexanizmi statistikasın kóriw
    """
    print("\n" + "=" * 60)
    print("Example 7: Reasoning Statistics")
    print("Misal 7: Mántıqlı Juwmaq Statistikası")
    print("=" * 60)

    try:
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)

        # Perform various reasoning tasks
        print("\nPerforming reasoning tasks...")
        print("Mántıqlı juwmaq wazıypalarni orınlaw...\n")

        # Task 1: Classify crimes
        crimes = [
            "http://huquqai.org/ontology#Jinayat_Jeńil",
            "http://huquqai.org/ontology#Jinayat_Urılıq",
            "http://huquqai.org/ontology#Jinayat_Awır",
        ]
        for crime in crimes:
            engine.classify_jinayat_awırlıǵı(crime)

        # Task 2: Infer punishment types
        punishments = [
            "http://huquqai.org/ontology#Jaza_Jarıma",
            "http://huquqai.org/ontology#Jaza_Shartı",
        ]
        for pun in punishments:
            engine.infer_jaza_turi(pun)

        # Get statistics
        stats = engine.get_statistics()

        print("Reasoning Engine Statistics:")
        print("Mántıqlı Juwmaq Mexanizmi Statistikası:\n")

        print(f"  Total reasoning runs / Mántıq juwmaq júrgiziwler:")
        print(f"    {stats['reasoning_runs']}")

        print(f"\n  Inferences made / Jasalǵan qorıtındılar:")
        print(f"    {stats['inferences_made']}")

        print(f"\n  Total inferred facts / Jası qorıtındılanǵan faktlar:")
        print(f"    {stats['total_inferred_facts']}")

        print(f"\n  Inconsistencies found / Tabılǵan úyelisliksizlikler:")
        print(f"    {stats['inconsistencies_found']}")

        print(f"\n  Total reasoning time / Jası mántıq juwmaq waqtı:")
        print(f"    {stats['total_reasoning_time']:.4f}s")

        print(f"\n  Average reasoning time / Ortasha mántıq juwmaq waqtı:")
        print(f"    {stats['average_reasoning_time']:.4f}s")

        print(f"\n  Last reasoning time / Sońǵı mántıq juwmaq waqtı:")
        print(f"    {stats['last_reasoning_time']:.4f}s")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def example_8_compare_reasoners():
    """
    Example 8: Compare different reasoners
    Misal 8: Túrli mántıq juwmaqshıları salıstırıw
    """
    print("\n" + "=" * 60)
    print("Example 8: Comparing Reasoners")
    print("Misal 8: Mántıq Juwmaqshılardı Salıstırıw")
    print("=" * 60)

    ontology_path = "data/ontologies/criminal_code.owl"

    reasoners = [
        (ReasonerType.PELLET, "Pellet"),
        (ReasonerType.HERMIT, "HermiT"),
    ]

    print("\nComparing reasoner performance:")
    print("Mántıq juwmaqshı tabıslılıǵın salıstırıw:\n")

    results = []

    for reasoner_type, reasoner_name in reasoners:
        try:
            print(f"Testing {reasoner_name}...")
            print(f"{reasoner_name} test etiwde...")

            engine = create_reasoning_engine(ontology_path, reasoner_type)

            # Run consistency check
            import time
            start = time.time()
            is_consistent = engine.check_consistency()
            duration = time.time() - start

            results.append({
                'name': reasoner_name,
                'type': reasoner_type,
                'consistent': is_consistent,
                'time': duration
            })

            print(f"  ✓ Completed in {duration:.4f}s")
            print()

        except Exception as e:
            print(f"  ✗ Failed: {e}")
            print()

    # Show comparison
    if len(results) > 0:
        print("\nComparison Results / Salıstırıw Nátiyјeleri:")
        print("-" * 50)
        print(f"{'Reasoner':<15} {'Status':<12} {'Time (s)':<10}")
        print("-" * 50)

        for result in results:
            status = "Consistent" if result['consistent'] else "Inconsistent"
            print(f"{result['name']:<15} {status:<12} {result['time']:<10.4f}")

        print("\nRecommendation / Tawsıya:")
        fastest = min(results, key=lambda x: x['time'])
        print(f"  Fastest reasoner: {fastest['name']}")
        print(f"  Eń tez mántıq juwmaqshı: {fastest['name']}")


def example_9_batch_classification():
    """
    Example 9: Batch classification of crimes
    Misal 9: Jinayatlardıń toplamın klassifikaciyalaw
    """
    print("\n" + "=" * 60)
    print("Example 9: Batch Crime Classification")
    print("Misal 9: Jinayatlardıń Toplamın Klassifikaciyalaw")
    print("=" * 60)

    try:
        manager = get_ontology_manager()
        manager.load_ontology("data/ontologies/criminal_code.owl")

        engine = ReasoningEngine(graph=manager.graph)

        # Get all crimes from ontology
        from rdflib import Namespace
        huquq = Namespace("http://huquqai.org/ontology#")

        crimes = list(manager.graph.subjects(
            predicate=manager.graph.namespace_manager.store.namespace("rdf").type,
            object=huquq.Jinayat
        ))

        print(f"\nFound {len(crimes)} crimes to classify")
        print(f"{len(crimes)} jinayat klassifikaciyalaw ushın tabıldı\n")

        # Classify all
        results = {}
        for crime_uri in crimes:
            severity = engine.classify_jinayat_awırlıǵı(str(crime_uri))
            if severity:
                results[str(crime_uri)] = severity

        # Group by severity
        grouped = {}
        for uri, severity in results.items():
            if severity not in grouped:
                grouped[severity] = []
            grouped[severity].append(uri)

        # Display results
        print("Classification Summary / Klassifikaciya Juwmaǵı:")
        print()

        severity_labels = {
            JinayatAwırlıǵı.JENIL: "Light Crimes / Jeńil Jinayatlar",
            JinayatAwırlıǵı.ORTA: "Medium Crimes / Orta Jinayatlar",
            JinayatAwırlıǵı.AWIR: "Severe Crimes / Awır Jinayatlar",
            JinayatAwırlıǵı.OTE_AWIR: "Very Severe Crimes / Óte Awır Jinayatlar",
        }

        for severity in [JinayatAwırlıǵı.JENIL, JinayatAwırlıǵı.ORTA,
                         JinayatAwırlıǵı.AWIR, JinayatAwırlıǵı.OTE_AWIR]:
            count = len(grouped.get(severity, []))
            label = severity_labels[severity]
            print(f"  {label}: {count}")

        print(f"\n  Total classified / Jası klassifikaciyalanǵanlar: {len(results)}")

    except Exception as e:
        print(f"✗ Error / Qátelik: {e}")


def main():
    """
    Run all examples
    Barlıq misallardı júrgiziw
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "ReasoningEngine Usage Examples" + " " * 18 + "║")
    print("║" + " " * 8 + "ReasoningEngine Qollanıw Misalları" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")

    # Run examples
    example_1_check_consistency()
    example_2_classify_ontology()
    example_3_classify_crime_severity()
    example_4_infer_punishment_types()
    example_5_check_law_consistency()
    example_6_explain_inferences()
    example_7_reasoning_statistics()
    example_8_compare_reasoners()
    example_9_batch_classification()

    print("\n" + "=" * 60)
    print("All examples completed / Barlıq misallar tamamlandı")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
