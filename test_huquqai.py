#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HuquqAI - Qaraqalpaq Huquqıy Bilim Bazası Sisteması
Interactive Command-Line Test Script

This script demonstrates the working Karakalpak legal knowledge base system.
"""

import sys
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.core.ontology_manager import OntologyManager
    from src.core.sparql_engine import SPARQLEngine
    from rdflib import Graph
except ImportError as e:
    print(f"❌ Import qáteligi / Import error: {e}")
    print("Iltimas, requirements.txt-ten kerekli paketlerdi ornatıń!")
    print("Please install required packages from requirements.txt!")
    sys.exit(1)


class HuquqAIDemo:
    """Interactive demo for HuquqAI system"""

    def __init__(self):
        self.ontology_manager: Optional[OntologyManager] = None
        self.sparql_engine: Optional[SPARQLEngine] = None
        self.graph: Optional[Graph] = None

    def initialize(self) -> bool:
        """
        Initialize the HuquqAI system
        Returns True if successful, False otherwise
        """
        try:
            print("\n⏳ Sistema júkleniw / System loading...")

            # Load ontology
            ontology_path = Path("data/ontologies/legal_ontology.owl")
            if not ontology_path.exists():
                print(f"❌ Qátelik: {ontology_path} tabılmadı!")
                print(f"❌ Error: {ontology_path} not found!")
                return False

            print(f"📂 Ontologiya júkleniw: {ontology_path}")
            self.ontology_manager = OntologyManager()
            self.ontology_manager.load_ontology(str(ontology_path))

            # Load RDF data
            data_path = Path("data/knowledge/criminal_code.ttl")
            if not data_path.exists():
                print(f"❌ Qátelik: {data_path} tabılmadı!")
                print(f"❌ Error: {data_path} not found!")
                return False

            print(f"📂 Ma'limleri júklew: {data_path}")
            self.graph = Graph()
            self.graph.parse(str(data_path), format='turtle')

            # Merge with ontology graph
            if self.ontology_manager.graph:
                for triple in self.graph:
                    self.ontology_manager.graph.add(triple)
                self.graph = self.ontology_manager.graph

            # Initialize SPARQL engine
            self.sparql_engine = SPARQLEngine(graph=self.graph)

            print("✅ Sistema tayar!\n")
            return True

        except Exception as e:
            print(f"❌ Qátelik júklewde / Error loading: {e}")
            import traceback
            traceback.print_exc()
            return False

    def show_welcome(self):
        """Display welcome message"""
        print("=" * 70)
        print("🏛️  HuquqAI - Qaraqalpaq Huquqıy Bilim Bazası Sisteması")
        print("    Karakalpak Legal Knowledge Base System")
        print("=" * 70)
        print()

    def show_menu(self):
        """Display interactive menu in Karakalpak"""
        print("\n" + "─" * 70)
        print("📋 MENYU / MENU:")
        print("─" * 70)
        print("  1️⃣  Barlıq jinayatlardı kórsetiw (Show all crimes)")
        print("  2️⃣  Kalit sóz boyınsha izlew (Search by keyword)")
        print("  3️⃣  Statiya nómiri boyınsha (Search by article number)")
        print("  4️⃣  Awır jinayatlar (Heavy crimes > 10 years)")
        print("  5️⃣  Jinayat túri boyınsha (Search by crime type)")
        print("  0️⃣  Shıǵıw (Exit)")
        print("─" * 70)

    def display_article(self, binding: dict, detailed: bool = False):
        """Display a single article in formatted way"""
        try:
            nomiri = binding.get('nómiri', {}).get('value', 'N/A')
            sarelaw = binding.get('sárelaw', {}).get('value', 'N/A')
            jaza_min = binding.get('jaza_min', {}).get('value', 'N/A')
            jaza_max = binding.get('jaza_max', {}).get('value', 'N/A')
            jinayat_turi = binding.get('jinayat_turi', {}).get('value', 'N/A')
            awirliq = binding.get('awırlıq_dárejesi', {}).get('value', 'N/A')

            print(f"\n📜 Statiya {nomiri}: {sarelaw}")
            print(f"   ├─ Jinayat túri: {jinayat_turi}")
            print(f"   ├─ Awırlıq dárejesi: {awirliq}")
            print(f"   └─ Jaza: {jaza_min}-{jaza_max} jıl")

            if detailed and 'tekstı' in binding:
                teksti = binding['tekstı'].get('value', '')
                if teksti:
                    print(f"\n   📄 Teksti:")
                    print(f"   {teksti}")

        except Exception as e:
            print(f"   ⚠️  Qátelik ma'liwmatni kórsetiwde: {e}")

    def option_show_all(self):
        """Option 1: Show all crimes"""
        print("\n🔍 Barlıq jinayatlardı júklew...")

        query = """
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nómiri ?sárelaw ?jinayat_turi ?awırlıq_dárejesi ?jaza_min ?jaza_max
        WHERE {
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .
        }
        ORDER BY ?nómiri
        """

        try:
            results = self.sparql_engine.execute_cached(query)
            if results and len(results.get('results', {}).get('bindings', [])) > 0:
                bindings = results['results']['bindings']
                print(f"\n✅ Tabılǵan statiyalar sanı: {len(bindings)}")
                for binding in bindings:
                    self.display_article(binding)
            else:
                print("⚠️  Statiyalar tabılmadı / No articles found")

        except Exception as e:
            print(f"❌ Qátelik sorawdı orınlawda: {e}")

    def option_search_keyword(self):
        """Option 2: Search by keyword"""
        keyword = input("\n🔎 Kalit sózdi kirgiziń (Enter keyword): ").strip()
        if not keyword:
            print("⚠️  Kalit sóz kirigilmedi!")
            return

        print(f"\n🔍 '{keyword}' kalit sóz boyınsha izlew...")

        query = f"""
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nómiri ?sárelaw ?tekstı ?jinayat_turi ?awırlıq_dárejesi ?jaza_min ?jaza_max
        WHERE {{
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:tekstı ?tekstı ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            FILTER (
                CONTAINS(LCASE(?tekstı), LCASE("{keyword}")) ||
                CONTAINS(LCASE(?sárelaw), LCASE("{keyword}"))
            )
        }}
        ORDER BY ?nómiri
        """

        try:
            results = self.sparql_engine.execute_cached(query)
            if results and len(results.get('results', {}).get('bindings', [])) > 0:
                bindings = results['results']['bindings']
                print(f"\n✅ Tabılǵan statiyalar: {len(bindings)}")
                for binding in bindings:
                    self.display_article(binding, detailed=True)
            else:
                print(f"⚠️  '{keyword}' ushın hesh nárse tabılmadı")

        except Exception as e:
            print(f"❌ Qátelik: {e}")

    def option_search_by_number(self):
        """Option 3: Search by article number"""
        try:
            nomiri = input("\n🔢 Statiya nómirin kirgiziń (Enter article number): ").strip()
            if not nomiri.isdigit():
                print("⚠️  Nómirdi durus kirgiziń!")
                return

            nomiri = int(nomiri)
            print(f"\n🔍 Statiya {nomiri} izlenip atır...")

            query = f"""
            PREFIX kk: <http://karakalpak.law/ontology#>

            SELECT ?nómiri ?sárelaw ?tekstı ?jinayat_turi ?awırlıq_dárejesi
                   ?jaza_min ?jaza_max ?jaza_turi
            WHERE {{
                ?statiya a kk:Statiya ;
                         kk:nómiri ?nómiri ;
                         kk:sárelaw ?sárelaw ;
                         kk:tekstı ?tekstı ;
                         kk:jinayat_turi ?jinayat_turi ;
                         kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                         kk:jaza_min ?jaza_min ;
                         kk:jaza_max ?jaza_max ;
                         kk:jaza_turi ?jaza_turi .

                FILTER (?nómiri = {nomiri})
            }}
            """

            results = self.sparql_engine.execute_cached(query)
            if results and len(results.get('results', {}).get('bindings', [])) > 0:
                binding = results['results']['bindings'][0]
                print("\n" + "=" * 70)
                self.display_article(binding, detailed=True)

                jaza_turi = binding.get('jaza_turi', {}).get('value', 'N/A')
                print(f"   ├─ Jaza túri: {jaza_turi}")
                print("=" * 70)
            else:
                print(f"⚠️  Statiya {nomiri} tabılmadı")

        except ValueError:
            print("❌ Nómirdi durus kirgiziń!")
        except Exception as e:
            print(f"❌ Qátelik: {e}")

    def option_heavy_crimes(self):
        """Option 4: Show heavy crimes (> 10 years)"""
        print("\n🔍 Awır jinayatlar (10 jıldan artıq jaza)...")

        query = """
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nómiri ?sárelaw ?jinayat_turi ?awırlıq_dárejesi ?jaza_min ?jaza_max
        WHERE {
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            FILTER (?jaza_max > 10)
        }
        ORDER BY DESC(?jaza_max)
        """

        try:
            results = self.sparql_engine.execute_cached(query)
            if results and len(results.get('results', {}).get('bindings', [])) > 0:
                bindings = results['results']['bindings']
                print(f"\n✅ Tabılǵan awır jinayatlar: {len(bindings)}")
                for binding in bindings:
                    self.display_article(binding)
            else:
                print("⚠️  Awır jinayatlar tabılmadı")

        except Exception as e:
            print(f"❌ Qátelik: {e}")

    def option_search_by_type(self):
        """Option 5: Search by crime type"""
        print("\n📋 Jinayat túrleri:")
        print("  1. Adamǵa qarsi")
        print("  2. Múlikke qarsi")
        print("  3. Dawlat hákim-basqarıwına qarsi")
        print("  4. Jámiyet densawlıǵına qarsi")

        turi = input("\n🔎 Jinayat túrin kirgiziń (Enter crime type): ").strip()
        if not turi:
            print("⚠️  Túr kirigilmedi!")
            return

        print(f"\n🔍 '{turi}' túri boyınsha izlew...")

        query = f"""
        PREFIX kk: <http://karakalpak.law/ontology#>

        SELECT ?nómiri ?sárelaw ?jinayat_turi ?awırlıq_dárejesi ?jaza_min ?jaza_max
        WHERE {{
            ?statiya a kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            FILTER (CONTAINS(LCASE(?jinayat_turi), LCASE("{turi}")))
        }}
        ORDER BY ?nómiri
        """

        try:
            results = self.sparql_engine.execute_cached(query)
            if results and len(results.get('results', {}).get('bindings', [])) > 0:
                bindings = results['results']['bindings']
                print(f"\n✅ Tabılǵan statiyalar: {len(bindings)}")
                for binding in bindings:
                    self.display_article(binding)
            else:
                print(f"⚠️  '{turi}' ushın hesh nárse tabılmadı")

        except Exception as e:
            print(f"❌ Qátelik: {e}")

    def run(self):
        """Main interactive loop"""
        self.show_welcome()

        if not self.initialize():
            print("\n❌ Sistemanı júklew muwapıqiyetsiz boldi!")
            print("❌ System initialization failed!")
            return

        while True:
            try:
                self.show_menu()
                choice = input("\n👉 Tańlawıńızdı kirgiziń (Enter your choice): ").strip()

                if choice == '0':
                    print("\n👋 Sag bolıń! / Goodbye!")
                    break
                elif choice == '1':
                    self.option_show_all()
                elif choice == '2':
                    self.option_search_keyword()
                elif choice == '3':
                    self.option_search_by_number()
                elif choice == '4':
                    self.option_heavy_crimes()
                elif choice == '5':
                    self.option_search_by_type()
                else:
                    print("⚠️  Nádurıs tańlaw! Qaytadan kirgizin.")
                    print("⚠️  Invalid choice! Please try again.")

            except KeyboardInterrupt:
                print("\n\n👋 Sag bolıń! / Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Qátelik ornaldi: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Main entry point"""
    demo = HuquqAIDemo()
    demo.run()


if __name__ == "__main__":
    main()
