#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HuquqAI - Qaraqalpaq Huquqıy Bilim Bazası
Simple working CLI interface
"""

import sys
import os
from pathlib import Path1


# Fix Windows console encoding for UTF-8
if sys.platform == 'win32':
    try:
        # Set console to UTF-8 mode
        os.system('chcp 65001 >nul 2>&1')
        # Reconfigure stdout and stderr for UTF-8
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, RDF, OWL


def load_knowledge_base():
    """Load ontology and data into RDF graph"""
    print("\n⏳ Ma'limleri júklew / Loading data...")

    graph = Graph()

    # Load ontology
    ontology_file = Path("data/ontologies/legal_ontology.owl")
    if ontology_file.exists():
        graph.parse(str(ontology_file), format='xml')
        print(f"✅ Ontologiya júklendi: {ontology_file}")
    else:
        print(f"⚠️  Ontologiya tabılmadı: {ontology_file}")

    # Load criminal code data
    data_file = Path("data/knowledge/criminal_code.ttl")
    if data_file.exists():
        graph.parse(str(data_file), format='turtle')
        print(f"✅ Ma'limler júklendi: {data_file}")
    else:
        print(f"⚠️  Ma'limler tabılmadı: {data_file}")

    print(f"✅ Jámi {len(graph)} triple júklendi\n")
    return graph


def show_welcome():
    """Display welcome banner"""
    print("\n" + "=" * 70)
    print("🏛️  HuquqAI - Qaraqalpaq Huquqıy Bilim Bazası")
    print("    Karakalpak Legal Knowledge Base System")
    print("=" * 70)


def show_menu():
    """Display menu"""
    print("\n" + "─" * 70)
    print("📋 MENYU:")
    print("─" * 70)
    print("  1️⃣  Barlıq jinayatlardı kórsetiw (Show all crimes)")
    print("  2️⃣  Kalit sóz boyınsha izlew (Search by keyword)")
    print("  3️⃣  Jaza diapazonı (Punishment range)")
    print("  4️⃣  Statiya nómiri boyınsha (Search by article number)")
    print("  5️⃣  Jinayat túri boyınsha (Search by crime type)")
    print("  6️⃣  Statistika (Show statistics)")
    print("  7️⃣  Ontologiya ma'limatlari (Ontology info)")
    print("  0️⃣  Shıǵıw (Exit)")
    print("─" * 70)


def format_article(row):
    """Format article information for display"""
    nomiri = row.get('nomiri', 'N/A')
    sarelaw = row.get('sarelaw', 'N/A')
    jaza_min = row.get('jaza_min', 'N/A')
    jaza_max = row.get('jaza_max', 'N/A')
    jinayat_turi = row.get('jinayat_turi', 'N/A')
    awirliq = row.get('awirliq', 'N/A')

    print(f"\n📜 Statiya {nomiri}: {sarelaw}")
    print(f"   ├─ Jinayat túri: {jinayat_turi}")
    print(f"   ├─ Awırlıq: {awirliq}")
    print(f"   └─ Jaza: {jaza_min}-{jaza_max} jıl")


def option_show_all(graph):
    """Show all crimes"""
    print("\n🔍 Barlıq jinayatlar...")

    query = """
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .
    }
    ORDER BY ?nomiri
    """

    try:
        results = graph.query(query)
        count = 0
        for row in results:
            count += 1
            format_article(row)

        if count == 0:
            print("⚠️  Statiyalar tabılmadı")
        else:
            print(f"\n✅ Jámi: {count} statiya")

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_search_keyword(graph):
    """Search by keyword"""
    keyword = input("\n🔎 Kalit sózdi kirgiziń: ").strip()
    if not keyword:
        print("⚠️  Kalit sóz kirigilmedi!")
        return

    print(f"\n🔍 '{keyword}' izlenip atır...")

    query = f"""
    PREFIX kk: <http://karakalpak.law/ontology#>

    SELECT ?nomiri ?sarelaw ?teksti ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
    WHERE {{
        ?statiya a kk:Statiya ;
                 kk:nómiri ?nomiri ;
                 kk:sárelaw ?sarelaw ;
                 kk:tekstı ?teksti ;
                 kk:jinayat_turi ?jinayat_turi ;
                 kk:awırlıq_dárejesi ?awirliq ;
                 kk:jaza_min ?jaza_min ;
                 kk:jaza_max ?jaza_max .

        FILTER (
            CONTAINS(LCASE(?teksti), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?sarelaw), LCASE("{keyword}"))
        )
    }}
    ORDER BY ?nomiri
    """

    try:
        results = graph.query(query)
        count = 0
        for row in results:
            count += 1
            format_article(row)
            # Show text snippet if available
            if hasattr(row, 'teksti') and row.teksti:
                teksti = str(row.teksti)
                if len(teksti) > 100:
                    teksti = teksti[:100] + "..."
                print(f"   📄 {teksti}")

        if count == 0:
            print(f"⚠️  '{keyword}' ushın hesh nárse tabılmadı")
        else:
            print(f"\n✅ Tabılǵan: {count} statiya")

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_punishment_range(graph):
    """Search by punishment range"""
    try:
        print("\n🔢 Jaza diapazonı:")
        min_jil = input("   Minimal jıl (kem): ").strip()
        max_jil = input("   Maksimal jıl (kóp): ").strip()

        if not min_jil.isdigit() or not max_jil.isdigit():
            print("⚠️  Nómirlerdi durus kirgiziń!")
            return

        min_jil = int(min_jil)
        max_jil = int(max_jil)

        print(f"\n🔍 {min_jil}-{max_jil} jıl aralıǵında jinayatlar...")

        query = f"""
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
        WHERE {{
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nomiri ;
                     kk:sárelaw ?sarelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awirliq ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            FILTER (?jaza_min >= {min_jil} && ?jaza_max <= {max_jil}) .
        }}
        ORDER BY DESC(?jaza_max)
        """

        results = graph.query(query)
        count = 0
        for row in results:
            count += 1
            format_article(row)

        if count == 0:
            print(f"⚠️  {min_jil}-{max_jil} jıl aralıǵında jinayatlar tabılmadı")
        else:
            print(f"\n✅ Tabılǵan: {count} statiya")

    except ValueError:
        print("❌ Nómirlerdi durus kirgiziń!")
    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_search_by_article(graph):
    """Search by article number"""
    try:
        print("\n🔢 Statiya nómiri:")
        nomer = input("   Statiya nómirin kirgiziń: ").strip()

        if not nomer:
            print("⚠️  Statiya nómiri kirigilmedi!")
            return

        print(f"\n🔍 Statiya {nomer} izlenip atır...")

        query = f"""
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nomiri ?sarelaw ?teksti ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
        WHERE {{
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nomiri ;
                     kk:sárelaw ?sarelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awirliq ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            OPTIONAL {{ ?statiya kk:tekstı ?teksti }}

            FILTER (STR(?nomiri) = "{nomer}")
        }}
        """

        results = graph.query(query)
        count = 0
        for row in results:
            count += 1
            format_article(row)
            # Show text if available
            if hasattr(row, 'teksti') and row.teksti:
                teksti = str(row.teksti)
                if len(teksti) > 200:
                    teksti = teksti[:200] + "..."
                print(f"   📄 {teksti}")

        if count == 0:
            print(f"⚠️  Statiya {nomer} tabılmadı")
        else:
            print(f"\n✅ Tabılǵan: {count} statiya")

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_search_by_crime_type(graph):
    """Search by crime type"""
    try:
        print("\n🔍 Jinayat túri:")
        print("   ├─ Jeńil (Light)")
        print("   ├─ Orta (Medium)")
        print("   └─ Awır (Heavy)")

        turi = input("\n   Awırlıq dárejesin tańlań: ").strip()

        if not turi:
            print("⚠️  Awırlıq dárejesi tańlanmadı!")
            return

        print(f"\n🔍 {turi} awırlıqlı jinayatlar izlenip atır...")

        query = f"""
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nomiri ?sarelaw ?jinayat_turi ?awirliq ?jaza_min ?jaza_max
        WHERE {{
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nomiri ;
                     kk:sárelaw ?sarelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awirliq ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            FILTER (CONTAINS(LCASE(?awirliq), LCASE("{turi}")))
        }}
        ORDER BY ?nomiri
        LIMIT 20
        """

        results = graph.query(query)
        count = 0
        for row in results:
            count += 1
            format_article(row)

        if count == 0:
            print(f"⚠️  {turi} awırlıqlı jinayatlar tabılmadı")
        else:
            print(f"\n✅ Tabılǵan: {count} jinayat")

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_show_statistics(graph):
    """Show statistics"""
    try:
        print("\n📊 STATISTIKA / STATISTICS")
        print("=" * 70)

        # Graph statistics
        print("\n📚 Ma'limler bazası / Knowledge Base:")
        print(f"   ├─ Triple-lar / Triples: {len(graph)}")

        # Count articles
        query_articles = """
        PREFIX kk: <http://karakalpak.law/ontology#>
        SELECT (COUNT(?statiya) as ?count)
        WHERE {
            ?statiya a kk:Statiya .
        }
        """
        result = list(graph.query(query_articles))
        article_count = int(result[0][0]) if result and result[0][0] else 0
        print(f"   ├─ Statiyalar / Articles: {article_count}")

        # Count by severity
        query_severity = """
        PREFIX kk: <http://karakalpak.law/ontology#>
        SELECT ?awirliq (COUNT(?statiya) as ?count)
        WHERE {
            ?statiya a kk:Statiya ;
                     kk:awırlıq_dárejesi ?awirliq .
        }
        GROUP BY ?awirliq
        ORDER BY ?awirliq
        """
        severity_results = graph.query(query_severity)
        print(f"   ├─ Awırlıq boyınsha / By severity:")
        for row in severity_results:
            severity = str(row.awirliq)
            count = int(row['count'])
            print(f"   │  ├─ {severity}: {count}")

        # Count by crime type
        query_types = """
        PREFIX kk: <http://karakalpak.law/ontology#>
        SELECT ?jinayat_turi (COUNT(?statiya) as ?count)
        WHERE {
            ?statiya a kk:Statiya ;
                     kk:jinayat_turi ?jinayat_turi .
        }
        GROUP BY ?jinayat_turi
        ORDER BY ?jinayat_turi
        """
        type_results = graph.query(query_types)
        print(f"   └─ Jinayat túri boyınsha / By crime type:")
        for row in type_results:
            crime_type = str(row.jinayat_turi)
            count = int(row['count'])
            print(f"      ├─ {crime_type}: {count}")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def option_show_ontology_info(graph):
    """Show ontology information"""
    try:
        print("\n🏛️  ONTOLOGIYA MA'LIMATLARI / ONTOLOGY INFORMATION")
        print("=" * 70)

        print("\n📊 Negizgi ma'limatlar / Basic Information:")
        print(f"   ├─ Triple-lar sani / Triple count: {len(graph)}")

        # Count classes
        query_classes = """
        SELECT (COUNT(DISTINCT ?class) as ?count)
        WHERE {
            ?class a <http://www.w3.org/2002/07/owl#Class> .
        }
        """
        result = list(graph.query(query_classes))
        class_count = int(result[0][0]) if result and result[0][0] else 0
        print(f"   ├─ Klasslar sani / Class count: {class_count}")

        # Count properties
        query_props = """
        SELECT (COUNT(DISTINCT ?prop) as ?count)
        WHERE {
            { ?prop a <http://www.w3.org/2002/07/owl#ObjectProperty> }
            UNION
            { ?prop a <http://www.w3.org/2002/07/owl#DatatypeProperty> }
        }
        """
        result = list(graph.query(query_props))
        prop_count = int(result[0][0]) if result and result[0][0] else 0
        print(f"   └─ Xassalar / Properties: {prop_count}")

        # Get class instances counts
        print("\n📂 Klasslar / Classes:")

        query_statiya = """
        PREFIX kk: <http://karakalpak.law/ontology#>
        SELECT (COUNT(?s) as ?count)
        WHERE { ?s a kk:Statiya }
        """
        result = list(graph.query(query_statiya))
        statiya_count = int(result[0][0]) if result and result[0][0] else 0
        print(f"   ├─ 📜 Statiya: {statiya_count} misal")

        # Namespaces
        print("\n🔗 Namespace-lar / Namespaces:")
        namespaces = list(graph.namespaces())
        for prefix, uri in namespaces:
            if prefix:  # Skip empty prefix
                print(f"   ├─ {prefix}: {uri}")

        print("\n📄 Ontologiya strukturası / Ontology Structure:")
        print("   ├─ Format: RDF/OWL")
        print("   ├─ Til / Language: Qaraqalpaq (kaa)")
        print("   └─ Domain: Huquqıy bilimler / Legal knowledge")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"❌ Qátelik: {e}")


def main():
    """Main function"""
    try:
        show_welcome()

        # Load knowledge base
        graph = load_knowledge_base()

        if len(graph) == 0:
            print("❌ Ma'limler júklenmedi! Programmadı toxtatiw...")
            return

        print("✅ Sistema tayar! / System ready!\n")

        # Main loop
        while True:
            try:
                show_menu()
                choice = input("\n👉 Tańlawıńızdı kirgiziń: ").strip()

                if choice == '0':
                    print("\n👋 Sag bolıń! / Goodbye!")
                    break
                elif choice == '1':
                    option_show_all(graph)
                elif choice == '2':
                    option_search_keyword(graph)
                elif choice == '3':
                    option_punishment_range(graph)
                elif choice == '4':
                    option_search_by_article(graph)
                elif choice == '5':
                    option_search_by_crime_type(graph)
                elif choice == '6':
                    option_show_statistics(graph)
                elif choice == '7':
                    option_show_ontology_info(graph)
                else:
                    print("⚠️  Nádurıs tańlaw! 0-7 aralıǵında tańlań.")

            except KeyboardInterrupt:
                print("\n\n👋 Sag bolıń!")
                break
            except Exception as e:
                print(f"\n❌ Qátelik: {e}")

    except Exception as e:
        print(f"\n❌ Sistemalıq qátelik: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
