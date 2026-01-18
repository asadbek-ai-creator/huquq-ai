"""
Karakalpak legal system SPARQL query templates
SPARQL sorıw úlgileri Qaraqalpaq hám-háreket basqarıw sisteması ushın
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class QueryResult:
    """
    Query result wrapper for SPARQL query results
    """
    bindings: List[Dict[str, Any]]
    count: int = 0

    def __post_init__(self):
        self.count = len(self.bindings)

    def get_values(self, field: str) -> List[Any]:
        """
        Extract all values for a specific field from results

        Args:
            field: field name to extract

        Returns:
            List of values
        """
        return [binding.get(field, {}).get('value') for binding in self.bindings if field in binding]

    def first(self) -> Optional[Dict[str, Any]]:
        """
        Get first result or None

        Returns:
            First binding or None if empty
        """
        return self.bindings[0] if self.bindings else None


class QueryTemplates:
    """
    SPARQL sorıw úlgileri - SPARQL query templates for Karakalpak legal queries
    """

    # Namespace prefixes for SPARQL queries
    PREFIXES = """
        PREFIX kk: <http://karakalpak.law/ontology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """

    @staticmethod
    def izlew_achqich_soz(achqich_soz: str) -> str:
        """
        Achqich sóz boyınsha statiyalardı izlew - Search articles by Karakalpak keyword

        Args:
            achqich_soz: keyword to search in Karakalpak

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?tekstı ?jinayat_turi ?awırlıq_dárejesi
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:tekstı ?tekstı ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi .

            # Tekstte yamasa sárelawda achqich sózdi izlew
            FILTER (
                CONTAINS(LCASE(?tekstı), LCASE("{achqich_soz}")) ||
                CONTAINS(LCASE(?sárelaw), LCASE("{achqich_soz}"))
            )
        }}
        ORDER BY ?nómiri
        """

    @staticmethod
    def awır_jinayatlardı_alıw() -> str:
        """
        Awır jinayatlardı alıw - Get heavy crimes with punishment > 10 years

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?jaza_min ?jaza_max ?jinayat_turi
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi .

            # 10 jıldan artıq jaza beriletuǵın jinayatlar
            FILTER (?jaza_max > 10)
        }}
        ORDER BY DESC(?jaza_max)
        """

    @staticmethod
    def izlew_kategoriya(kategoriya: str) -> str:
        """
        Kategoriya boyınsha izlew - Search by crime category in Karakalpak

        Args:
            kategoriya: crime category in Karakalpak

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?tekstı ?jaza_min ?jaza_max ?awırlıq_dárejesi
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:tekstı ?tekstı ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi .

            # Belgili kategoriya boyınsha filtrlew
            FILTER (CONTAINS(LCASE(?jinayat_turi), LCASE("{kategoriya}")))
        }}
        ORDER BY ?nómiri
        """

    @staticmethod
    def baylanıslı_statiyalardı_alıw(statiya_nómiri: int) -> str:
        """
        Baylanıslı statiyalardı alıw - Find related articles

        Args:
            statiya_nómiri: article number

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?baylanıslı_statiya ?nómiri ?sárelaw ?jinayat_turi
        WHERE {{
            # Negizgi statiya
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri {statiya_nómiri} ;
                     kk:jinayat_turi ?kategoriya .

            # Birday kategoriyalı basqa statiyalar
            ?baylanıslı_statiya rdf:type kk:Statiya ;
                                kk:nómiri ?nómiri ;
                                kk:sárelaw ?sárelaw ;
                                kk:jinayat_turi ?jinayat_turi .

            # Birday kategoriya, biraq basqa nómir
            FILTER (?jinayat_turi = ?kategoriya && ?nómiri != {statiya_nómiri})
        }}
        ORDER BY ?nómiri
        LIMIT 10
        """

    @staticmethod
    def jaza_diapazonı(min_jıl: int, max_jıl: int) -> str:
        """
        Jaza diapazonı boyınsha izlew - Get articles by punishment range

        Args:
            min_jıl: minimum years
            max_jıl: maximum years

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?jaza_min ?jaza_max ?jaza_turi ?awırlıq_dárejesi
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max ;
                     kk:jaza_turi ?jaza_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi .

            # Belgili jaza diapazonındaǵı statiyalar
            FILTER (?jaza_min >= {min_jıl} && ?jaza_max <= {max_jıl})
        }}
        ORDER BY ?jaza_max DESC
        """

    @staticmethod
    def izlew_nızam_turi(nızam_turi: str) -> str:
        """
        Nızam turi boyınsha izlew - Search by law type

        Args:
            nızam_turi: law type (e.g., "Jinayat Kodeksi", "Puqaralıq Kodeksi")

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?nızam ?nızam_atı
        WHERE {{
            ?nızam rdf:type kk:Nızam ;
                   kk:atı ?nızam_atı ;
                   kk:turi ?turi .

            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:nızam_id ?nızam .

            # Belgili nızam turi boyınsha filtrlew
            FILTER (CONTAINS(LCASE(?turi), LCASE("{nızam_turi}")))
        }}
        ORDER BY ?nómiri
        """

    @staticmethod
    def barlıq_statiyalardı_alıw() -> str:
        """
        Barlıq statiyalardı alıw - Get all articles with basic info

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?jinayat_turi ?awırlıq_dárejesi ?jaza_max
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:jaza_max ?jaza_max .
        }}
        ORDER BY ?nómiri
        """

    @staticmethod
    def statiya_nómiri_boyınsha(nómiri: int) -> str:
        """
        Nómir boyınsha statiya tabıw - Get article by number

        Args:
            nómiri: article number

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?tekstı ?jaza_min ?jaza_max
               ?jaza_turi ?jinayat_turi ?awırlıq_dárejesi ?nızam_id
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:tekstı ?tekstı ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max ;
                     kk:jaza_turi ?jaza_turi ;
                     kk:jinayat_turi ?jinayat_turi ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi ;
                     kk:nızam_id ?nızam_id .

            # Belgili nómirdegi statiya
            FILTER (?nómiri = {nómiri})
        }}
        """

    @staticmethod
    def statistika_alıw() -> str:
        """
        Nızamlardıń statistikasın alıw - Get law statistics

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?awırlıq_dárejesi (COUNT(?statiya) as ?san)
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:awırlıq_dárejesi ?awırlıq_dárejesi .
        }}
        GROUP BY ?awırlıq_dárejesi
        ORDER BY DESC(?san)
        """

    @staticmethod
    def jaza_turi_boyınsha(jaza_turi: str) -> str:
        """
        Jaza turi boyınsha statiyalardı alıw - Get articles by punishment type

        Args:
            jaza_turi: punishment type in Karakalpak

        Returns:
            SPARQL query string
        """
        return f"""{QueryTemplates.PREFIXES}

        SELECT ?statiya ?nómiri ?sárelaw ?jaza_turi ?jaza_min ?jaza_max
        WHERE {{
            ?statiya rdf:type kk:Statiya ;
                     kk:nómiri ?nómiri ;
                     kk:sárelaw ?sárelaw ;
                     kk:jaza_turi ?jaza_turi ;
                     kk:jaza_min ?jaza_min ;
                     kk:jaza_max ?jaza_max .

            # Belgili jaza turi boyınsha filtrlew
            FILTER (CONTAINS(LCASE(?jaza_turi), LCASE("{jaza_turi}")))
        }}
        ORDER BY ?nómiri
        """
