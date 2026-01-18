"""
Karakalpak legal domain model
Domain model for Karakalpak legal system using native terminology
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Statiya:
    """
    Statiya (Article) - represents a legal article in Karakalpak law
    """
    nómiri: int  # article number
    sárelaw: str  # title in Karakalpak
    tekstı: str  # full text in Karakalpak
    nızam_id: str  # reference to parent law
    jaza_min: int  # minimum punishment in years
    jaza_max: int  # maximum punishment in years
    jaza_turi: str  # punishment type in Karakalpak
    jinayat_turi: str  # crime category in Karakalpak
    awırlıq_dárejesi: str  # severity level: "Jeńil", "Orta", "Awır"

    def awır_jinayat_pa(self) -> bool:
        """
        Check if this is a heavy (serious) crime
        Returns True if awırlıq_dárejesi is "Awır"
        """
        return self.awırlıq_dárejesi == "Awır"

    def orta_jaza_alıw(self) -> float:
        """
        Get average punishment
        Returns the average of minimum and maximum punishment in years
        """
        return (self.jaza_min + self.jaza_max) / 2

    def jaza_aralıǵı_alıw(self) -> int:
        """
        Get punishment range
        Returns the difference between maximum and minimum punishment
        """
        return self.jaza_max - self.jaza_min


@dataclass
class Nızam:
    """
    Nızam (Law) - represents a legal code in Karakalpak legal system
    """
    id: str
    atı: str  # name in Karakalpak
    turi: str  # type: "Jinayat Kodeksi" or "Puqaralıq Kodeksi"
    qabıl_etilgen_jıl: int  # year adopted
    statiyalar: List[Statiya] = field(default_factory=list)

    def statiya_qosıw(self, statiya: Statiya) -> None:
        """
        Add an article to this law

        Args:
            statiya: Statiya object to add
        """
        if statiya.nızam_id != self.id:
            statiya.nızam_id = self.id
        self.statiyalar.append(statiya)

    def statiyalardı_alıw(self) -> List[Statiya]:
        """
        Get all articles in this law

        Returns:
            List of Statiya objects
        """
        return self.statiyalar

    def statiya_tabıw(self, nómiri: int) -> Optional[Statiya]:
        """
        Find an article by its number

        Args:
            nómiri: article number to find

        Returns:
            Statiya object if found, None otherwise
        """
        for statiya in self.statiyalar:
            if statiya.nómiri == nómiri:
                return statiya
        return None

    def awır_jinayatlar_sanı(self) -> int:
        """
        Count heavy crimes in this law

        Returns:
            Number of heavy crimes
        """
        return sum(1 for statiya in self.statiyalar if statiya.awır_jinayat_pa())

    def jinayat_turi_boyınsha_filtrlew(self, jinayat_turi: str) -> List[Statiya]:
        """
        Filter articles by crime category

        Args:
            jinayat_turi: crime category to filter by

        Returns:
            List of Statiya objects matching the category
        """
        return [s for s in self.statiyalar if s.jinayat_turi == jinayat_turi]
