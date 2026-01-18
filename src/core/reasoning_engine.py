"""
OWL Reasoning Engine for Karakalpak Legal System
Qaraqalpaq Huquqıy Sisteması ushın OWL Mántıqlı Juwmaq Mexanizmi

This module provides OWL reasoning capabilities for the Karakalpak legal knowledge base.
Bu modul Qaraqalpaq huquqıy bilimler bazası ushın OWL mántıqlı juwmaq imkaniyatlarin beredi.

Features / Imkaniyatlar:
- Consistency checking / Úyelislik tastıqlaw
- Classification reasoning / Klassifikaciya mántıq juwmaǵı
- Fact inference / Fakt qorıtındılawı
- Property constraints validation / Xassa shekleriń tastıqlaw
- SWRL rules support / SWRL qáǵıydalar qollawı
- Karakalpak-specific legal reasoning / Qaraqalpaq-maxsus huquqıy mántıq juwmaǵı
"""

import logging
import time
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from owlready2 import (
    World,
    get_ontology,
    sync_reasoner_pellet,
    sync_reasoner_hermit,
    OwlReadyError,
    Thing,
    AllDisjoint,
    Or,
    Not
)
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL

# Configure logging / Jurnal yazıwdı konfiguraciyalaw
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exceptions / Maxsus istinalar
# ============================================================================

class ReasoningEngineError(Exception):
    """
    Base exception for reasoning engine errors.
    Mántıqlı juwmaq mexanizmi qáteleri ushın baslanǵısh istisna.
    """

    def __init__(self, message: str, message_kaa: str = ""):
        """
        Initialize reasoning engine error.

        Parameters:
            message (str): Error message in English
            message_kaa (str): Error message in Karakalpak
        """
        self.message = message
        self.message_kaa = message_kaa or message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} / {self.message_kaa}"


class ConsistencyError(ReasoningEngineError):
    """
    Raised when ontology is inconsistent.
    Ontologiya úyelislikke sáykes kelmegen waqtında kóteriledi.
    """
    pass


class ClassificationError(ReasoningEngineError):
    """
    Raised when classification reasoning fails.
    Klassifikaciya mántıq juwmaǵı sátsiz bolǵanda kóteriledi.
    """
    pass


class InferenceError(ReasoningEngineError):
    """
    Raised when fact inference fails.
    Fakt qorıtındılawı sátsiz bolǵanda kóteriledi.
    """
    pass


# ============================================================================
# Enumerations / Sanawlamalar
# ============================================================================

class ReasonerType(Enum):
    """Supported reasoner types / Qollaw kórsetilgen mántıq juwmaq túrleri"""
    PELLET = "pellet"
    HERMIT = "hermit"


class JinayatAwırlıǵı(Enum):
    """
    Crime severity levels in Karakalpak legal system.
    Qaraqalpaq huquqıy sistemasındaǵı jinayat awırlıq dereželeri.
    """
    JENIL = "jeńil"  # Light crime (0-2 years)
    ORTA = "orta"  # Medium crime (2-5 years)
    AWIR = "awır"  # Severe crime (5-15 years)
    OTE_AWIR = "óte awır"  # Very severe crime (15+ years)


class JazaTuri(Enum):
    """
    Punishment types in Karakalpak legal system.
    Qaraqalpaq huquqıy sistemasındaǵı jaza túrleri.
    """
    JARIMA = "jarıma"  # Fine
    AZATLIQTAN_AYIRIW = "azatlıqtan ayırıw"  # Imprisonment
    SHIMELI_JUMIS = "shimeli jumıs"  # Compulsory labor
    ERTE_JIBERILIW = "erte jiberiliw"  # Early release
    SHARTI_JAZA = "shartı jaza"  # Conditional sentence


# ============================================================================
# Data Classes / Ma'limat klassları
# ============================================================================

@dataclass
class ReasoningResult:
    """
    Result of a reasoning operation.
    Mántıqlı juwmaq operaciyasınıń nátiyјesi.
    """
    success: bool
    inferences: List[Dict[str, Any]]
    inconsistencies: List[str]
    explanations: List[str]
    execution_time: float
    reasoner_type: str

    def __str__(self) -> str:
        return (
            f"ReasoningResult(success={self.success}, "
            f"inferences={len(self.inferences)}, "
            f"inconsistencies={len(self.inconsistencies)}, "
            f"time={self.execution_time:.4f}s)"
        )


@dataclass
class InferenceExplanation:
    """
    Explanation for an inferred fact.
    Qorıtındılanǵan fakt ushın túsindirme.
    """
    subject: str
    predicate: str
    object: str
    rule: str
    explanation_en: str
    explanation_kaa: str
    confidence: float = 1.0


# ============================================================================
# Reasoning Engine / Mántıqlı Juwmaq Mexanizmi
# ============================================================================

class ReasoningEngine:
    """
    OWL Reasoning Engine for Karakalpak Legal Knowledge Base.
    Qaraqalpaq Huquqıy Bilimler Bazası ushın OWL Mántıqlı Juwmaq Mexanizmi.

    This engine performs automated reasoning on legal ontologies to infer new facts,
    check consistency, and validate Karakalpak legal data.

    Bu mexanizm huquqıy ontologiyalarda jańa faktlardı qorıtındılaw, úyelislikti
    tastıqlaw ha'm Qaraqalpaq huquqıy ma'limlerin tastıqlaw ushın avtomatik
    mántıqlı juwmaq orınlaydı.

    Example / Misal:
        >>> from src.core.ontology_manager import get_ontology_manager
        >>> from src.core.reasoning_engine import ReasoningEngine, ReasonerType
        >>>
        >>> # Load ontology / Ontologiyani júklew
        >>> manager = get_ontology_manager()
        >>> manager.load_ontology("data/ontologies/criminal_code.owl")
        >>>
        >>> # Create reasoning engine / Mántıqlı juwmaq mexanizmin jasawıш
        >>> engine = ReasoningEngine(manager.graph, reasoner=ReasonerType.PELLET)
        >>>
        >>> # Check consistency / Úyelislikti tastıqlaw
        >>> is_consistent = engine.check_consistency()
        >>> print(f"Ontology is consistent: {is_consistent}")
        >>>
        >>> # Classify crimes by severity / Jinayatlardı awırlıǵı boyınsha klassifikaciyalaw
        >>> severity = engine.classify_jinayat_awırlıǵı("http://huquqai.org/ontology#Jinayat_Urılıq")
        >>> print(f"Crime severity: {severity}")
        >>>
        >>> # Infer punishment type / Jaza túrin qorıtındılaw
        >>> punishment_type = engine.infer_jaza_turi("http://huquqai.org/ontology#Jaza_Urılıq")
        >>> print(f"Punishment type: {punishment_type}")
    """

    def __init__(
        self,
        graph: Optional[Graph] = None,
        ontology_path: Optional[Union[str, Path]] = None,
        reasoner: ReasonerType = ReasonerType.PELLET
    ):
        """
        Initialize the reasoning engine.
        Mántıqlı juwmaq mexanizmin inicializaciyalaw.

        Parameters:
            graph (Graph, optional): RDFLib Graph object
            ontology_path (str|Path, optional): Path to OWL ontology file
            reasoner (ReasonerType): Reasoner type to use (PELLET or HERMIT)

        Raises:
            ReasoningEngineError: If initialization fails
        """
        self.graph = graph
        self.ontology_path = ontology_path
        self.reasoner_type = reasoner

        # Owlready2 world and ontology / Owlready2 dúnya ha'm ontologiya
        self.world: Optional[World] = None
        self.onto = None

        # Namespaces / Isim keshikleri
        self.huquq = Namespace("http://huquqai.org/ontology#")
        self.namespaces = {
            "huquq": self.huquq,
            "rdf": RDF,
            "rdfs": RDFS,
            "owl": OWL
        }

        # Statistics / Statistika
        self.stats = {
            'reasoning_runs': 0,
            'inferences_made': 0,
            'inconsistencies_found': 0,
            'total_reasoning_time': 0.0,
            'last_reasoning_time': 0.0
        }

        # Inferred facts storage / Qorıtındılanǵan faktlar saqlanıwı
        self.inferred_facts: List[Tuple[str, str, str]] = []

        # Load ontology if path provided / Jol berilgen bolsa ontologiyani júklew
        if ontology_path:
            self._load_ontology(ontology_path)

        logger.info(
            f"ReasoningEngine initialized with {reasoner.value} reasoner / "
            f"Mántıqlı juwmaq mexanizmi {reasoner.value} juwmaqshı menen inicializaciyalandı"
        )

    def _load_ontology(self, ontology_path: Union[str, Path]) -> None:
        """
        Load OWL ontology using owlready2.
        OWL ontologiyani owlready2 arqalı júklew.

        Parameters:
            ontology_path: Path to ontology file

        Raises:
            ReasoningEngineError: If loading fails
        """
        try:
            ontology_path = Path(ontology_path)

            if not ontology_path.exists():
                raise FileNotFoundError(
                    f"Ontology file not found: {ontology_path} / "
                    f"Ontologiya faylı tabılmadı: {ontology_path}"
                )

            # Create owlready2 world / owlready2 dúnyani jasawıш
            self.world = World()

            # Load ontology / Ontologiyani júklew
            self.onto = self.world.get_ontology(f"file://{ontology_path}").load()

            logger.info(
                f"Ontology loaded successfully / Ontologiya tabıslı júklendi: {ontology_path}"
            )

        except Exception as e:
            raise ReasoningEngineError(
                f"Failed to load ontology: {e}",
                f"Ontologiyani júklew sátsiz: {e}"
            )

    def check_consistency(self) -> bool:
        """
        Check ontology consistency using the configured reasoner.
        Konfiguraciyalanǵan mántıq juwmaqshı arqalı ontologiya úyelisligin tastıqlaw.

        Returns:
            bool: True if consistent, False otherwise

        Raises:
            ConsistencyError: If consistency check fails

        Example / Misal:
            >>> engine = ReasoningEngine(reasoner=ReasonerType.PELLET)
            >>> is_consistent = engine.check_consistency()
            >>> if is_consistent:
            ...     print("Ontology is consistent / Ontologiya úyelisli")
            ... else:
            ...     print("Ontology has inconsistencies / Ontologiyada úyelisliksizlikler bar")
        """
        if not self.onto:
            raise ConsistencyError(
                "No ontology loaded. Load an ontology first.",
                "Ontologiya júklenmegen. Aldı bılan ontologiyani júkleń."
            )

        start_time = time.time()

        try:
            logger.info(
                f"Starting consistency check with {self.reasoner_type.value} / "
                f"{self.reasoner_type.value} menen úyelislik tastıqlaw baslandı"
            )

            # Run reasoner / Mántıq juwmaqshını júrgiziw
            with self.onto:
                if self.reasoner_type == ReasonerType.PELLET:
                    sync_reasoner_pellet(self.world, infer_property_values=True)
                elif self.reasoner_type == ReasonerType.HERMIT:
                    sync_reasoner_hermit(self.world, infer_property_values=True)

            # Check for inconsistent classes / Úyelislikke sáykes kelmegen klasslardı tastıqlaw
            inconsistent_classes = list(self.world.inconsistent_classes())

            execution_time = time.time() - start_time
            self.stats['last_reasoning_time'] = execution_time
            self.stats['total_reasoning_time'] += execution_time
            self.stats['reasoning_runs'] += 1

            if inconsistent_classes:
                self.stats['inconsistencies_found'] += len(inconsistent_classes)
                logger.warning(
                    f"Found {len(inconsistent_classes)} inconsistent classes / "
                    f"{len(inconsistent_classes)} úyelislikke sáykes kelmegen klass tabıldı"
                )
                for cls in inconsistent_classes:
                    logger.warning(f"  Inconsistent class / Úyelislikke sáykes kelmegen klass: {cls}")
                return False

            logger.info(
                f"Consistency check passed in {execution_time:.4f}s / "
                f"Úyelislik tastıqlaw {execution_time:.4f}s ishinde ótti"
            )
            return True

        except Exception as e:
            raise ConsistencyError(
                f"Consistency check failed: {e}",
                f"Úyelislik tastıqlaw sátsiz: {e}"
            )

    def classify(self, explain: bool = False) -> ReasoningResult:
        """
        Perform classification reasoning on the ontology.
        Ontologiyada klassifikaciya mántıq juwmaǵın orınlaw.

        Classification infers class membership based on property values and restrictions.
        Klassifikaciya xassa ma'nisleri ha'm sheklerge suyanıp klass agzalıǵın qorıtındılaydı.

        Parameters:
            explain (bool): Include explanations for inferences

        Returns:
            ReasoningResult: Result with inferred class memberships

        Example / Misal:
            >>> result = engine.classify(explain=True)
            >>> print(f"Made {len(result.inferences)} inferences")
            >>> for inf in result.inferences:
            ...     print(f"  {inf['individual']} is a {inf['class']}")
        """
        if not self.onto:
            raise ClassificationError(
                "No ontology loaded",
                "Ontologiya júklenmegen"
            )

        start_time = time.time()
        inferences = []
        explanations = []

        try:
            logger.info("Starting classification reasoning / Klassifikaciya mántıq juwmaǵı baslandı")

            # Store original classes / Baslanǵısh klasslardı saqlaw
            original_classes = {}
            for individual in self.onto.individuals():
                original_classes[individual] = set(individual.is_a)

            # Run reasoner / Mántıq juwmaqshını júrgiziw
            with self.onto:
                if self.reasoner_type == ReasonerType.PELLET:
                    sync_reasoner_pellet(self.world, infer_property_values=True)
                else:
                    sync_reasoner_hermit(self.world, infer_property_values=True)

            # Find new inferred classes / Jańa qorıtındılanǵan klasslardı tabıw
            for individual in self.onto.individuals():
                new_classes = set(individual.is_a) - original_classes[individual]

                for new_class in new_classes:
                    if new_class != Thing:  # Exclude trivial Thing class
                        inference = {
                            'individual': str(individual.name),
                            'class': str(new_class.name if hasattr(new_class, 'name') else new_class),
                            'type': 'classification'
                        }
                        inferences.append(inference)
                        self.inferred_facts.append((
                            str(individual.iri),
                            str(RDF.type),
                            str(new_class.iri if hasattr(new_class, 'iri') else new_class)
                        ))

                        if explain:
                            explanations.append(
                                f"Individual {individual.name} classified as {new_class} / "
                                f"Individual {individual.name} {new_class} dep klassifikaciyalandı"
                            )

            execution_time = time.time() - start_time
            self.stats['last_reasoning_time'] = execution_time
            self.stats['total_reasoning_time'] += execution_time
            self.stats['reasoning_runs'] += 1
            self.stats['inferences_made'] += len(inferences)

            logger.info(
                f"Classification completed: {len(inferences)} inferences in {execution_time:.4f}s / "
                f"Klassifikaciya tamamlandı: {len(inferences)} qorıtındı {execution_time:.4f}s ishinde"
            )

            return ReasoningResult(
                success=True,
                inferences=inferences,
                inconsistencies=[],
                explanations=explanations,
                execution_time=execution_time,
                reasoner_type=self.reasoner_type.value
            )

        except Exception as e:
            raise ClassificationError(
                f"Classification failed: {e}",
                f"Klassifikaciya sátsiz: {e}"
            )

    def infer_facts(self, rules: Optional[List[str]] = None) -> ReasoningResult:
        """
        Infer new facts based on ontology axioms and optional SWRL rules.
        Ontologiya aksiomalar ha'm opsional SWRL qáǵıydalar negizinde jańa faktlardı qorıtındılaw.

        Parameters:
            rules (List[str], optional): SWRL rules to apply

        Returns:
            ReasoningResult: Result with inferred facts

        Example / Misal:
            >>> # Infer facts using built-in rules
            >>> result = engine.infer_facts()
            >>>
            >>> # Apply custom SWRL rule
            >>> rules = ["Jinayat(?j) ^ minYears(?j, ?y) ^ greaterThan(?y, 10) -> AwırJinayat(?j)"]
            >>> result = engine.infer_facts(rules=rules)
        """
        if not self.onto:
            raise InferenceError(
                "No ontology loaded",
                "Ontologiya júklenmegen"
            )

        start_time = time.time()
        inferences = []

        try:
            logger.info("Starting fact inference / Fakt qorıtındılawı baslandı")

            # TODO: Implement SWRL rule parsing and application
            # SWRL rules require additional setup with Jess or similar
            if rules:
                logger.warning(
                    "SWRL rules provided but not yet implemented / "
                    "SWRL qáǵıydalar berildi biraq áli ámelge asırılmadı"
                )

            # Run reasoner / Mántıq juwmaqshını júrgiziw
            with self.onto:
                if self.reasoner_type == ReasonerType.PELLET:
                    sync_reasoner_pellet(self.world, infer_property_values=True)
                else:
                    sync_reasoner_hermit(self.world, infer_property_values=True)

            # Property value inferences are handled by reasoner
            # We can extract them from the world
            # Xassa ma'nis qorıtındıları mántıq juwmaqshı tárepinen basqarıladı

            execution_time = time.time() - start_time
            self.stats['last_reasoning_time'] = execution_time
            self.stats['total_reasoning_time'] += execution_time
            self.stats['reasoning_runs'] += 1
            self.stats['inferences_made'] += len(inferences)

            logger.info(
                f"Fact inference completed in {execution_time:.4f}s / "
                f"Fakt qorıtındılawı {execution_time:.4f}s ishinde tamamlandı"
            )

            return ReasoningResult(
                success=True,
                inferences=inferences,
                inconsistencies=[],
                explanations=[],
                execution_time=execution_time,
                reasoner_type=self.reasoner_type.value
            )

        except Exception as e:
            raise InferenceError(
                f"Fact inference failed: {e}",
                f"Fakt qorıtındılawı sátsiz: {e}"
            )

    # ========================================================================
    # Karakalpak-Specific Reasoning Methods
    # Qaraqalpaq-Maxsus Mántıqlı Juwmaq Metodları
    # ========================================================================

    def classify_jinayat_awırlıǵı(
        self,
        jinayat_uri: str
    ) -> Optional[JinayatAwırlıǵı]:
        """
        Classify crime severity based on punishment duration.
        Jaza uzaqlıǵı negizinde jinayat awırlıǵın klassifikaciyalaw.

        Karakalpak Legal Rules / Qaraqalpaq Huquqıy Qáǵıydaları:
        - Eger jaza 0-2 jıl bolsa → jeńil jinayat (light crime)
        - Eger jaza 2-5 jıl bolsa → orta jinayat (medium crime)
        - Eger jaza 5-15 jıl bolsa → awır jinayat (severe crime)
        - Eger jaza > 15 jıl bolsa → óte awır jinayat (very severe crime)

        Parameters:
            jinayat_uri (str): URI of the crime to classify

        Returns:
            JinayatAwırlıǵı: Classified severity level, or None if cannot classify

        Example / Misal:
            >>> uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
            >>> severity = engine.classify_jinayat_awırlıǵı(uri)
            >>> print(f"Crime severity: {severity.value}")
            >>> # Output: Crime severity: orta
        """
        try:
            logger.info(
                f"Classifying crime severity / Jinayat awırlıǵın klassifikaciyalaw: {jinayat_uri}"
            )

            # Get associated punishment / Baylanıslı jazani alıw
            punishment_years = self._get_punishment_years(jinayat_uri)

            if punishment_years is None:
                logger.warning(
                    f"Cannot determine punishment years for crime / "
                    f"Jinayat ushın jaza jılların anıqlaw múmkin emes: {jinayat_uri}"
                )
                return None

            # Apply classification rules / Klassifikaciya qáǵıydaların qollaw
            if punishment_years <= 2:
                severity = JinayatAwırlıǵı.JENIL
            elif punishment_years <= 5:
                severity = JinayatAwırlıǵı.ORTA
            elif punishment_years <= 15:
                severity = JinayatAwırlıǵı.AWIR
            else:
                severity = JinayatAwırlıǵı.OTE_AWIR

            logger.info(
                f"Crime classified as {severity.value} / "
                f"Jinayat {severity.value} dep klassifikaciyalandı"
            )

            # Store inference / Qorıtındını saqlaw
            self.inferred_facts.append((
                jinayat_uri,
                str(self.huquq.crimeType),
                severity.value
            ))
            self.stats['inferences_made'] += 1

            return severity

        except Exception as e:
            logger.error(
                f"Failed to classify crime severity: {e} / "
                f"Jinayat awırlıǵın klassifikaciyalaw sátsiz: {e}"
            )
            return None

    def infer_jaza_turi(
        self,
        jaza_uri: str
    ) -> Optional[JazaTuri]:
        """
        Infer punishment type based on duration and other properties.
        Uzaqlıq ha'm basqa xassalar negizinde jaza túrin qorıtındılaw.

        Karakalpak Legal Rules / Qaraqalpaq Huquqıy Qáǵıydaları:
        - Eger minYears = 0 ha'm maxYears = 0 → jarıma (fine)
        - Eger minYears > 0 ha'm conditional = true → shartı jaza (conditional)
        - Eger minYears > 0 ha'm labor = true → shimeli jumıs (compulsory labor)
        - Eger minYears > 0 → azatlıqtan ayırıw (imprisonment)

        Parameters:
            jaza_uri (str): URI of the punishment

        Returns:
            JazaTuri: Inferred punishment type, or None if cannot infer

        Example / Misal:
            >>> uri = "http://huquqai.org/ontology#Jaza_Urılıq"
            >>> pun_type = engine.infer_jaza_turi(uri)
            >>> print(f"Punishment type: {pun_type.value}")
        """
        try:
            logger.info(
                f"Inferring punishment type / Jaza túrin qorıtındılaw: {jaza_uri}"
            )

            if not self.graph:
                logger.warning("No RDF graph available / RDF graf joq")
                return None

            # Query punishment properties / Jaza xassalarin soraw
            min_years = self._get_property_value(jaza_uri, self.huquq.minYears)
            max_years = self._get_property_value(jaza_uri, self.huquq.maxYears)
            is_conditional = self._get_property_value(jaza_uri, self.huquq.conditional)
            is_labor = self._get_property_value(jaza_uri, self.huquq.compulsoryLabor)

            # Apply inference rules / Qorıtındılaw qáǵıydaların qollaw
            punishment_type = None

            if min_years == 0 and max_years == 0:
                punishment_type = JazaTuri.JARIMA
            elif is_conditional:
                punishment_type = JazaTuri.SHARTI_JAZA
            elif is_labor:
                punishment_type = JazaTuri.SHIMELI_JUMIS
            elif min_years and min_years > 0:
                punishment_type = JazaTuri.AZATLIQTAN_AYIRIW

            if punishment_type:
                logger.info(
                    f"Punishment type inferred as {punishment_type.value} / "
                    f"Jaza túri {punishment_type.value} dep qorıtındılandı"
                )

                # Store inference / Qorıtındını saqlaw
                self.inferred_facts.append((
                    jaza_uri,
                    str(self.huquq.punishmentType),
                    punishment_type.value
                ))
                self.stats['inferences_made'] += 1

            return punishment_type

        except Exception as e:
            logger.error(
                f"Failed to infer punishment type: {e} / "
                f"Jaza túrin qorıtındılaw sátsiz: {e}"
            )
            return None

    def check_nızam_consistency(
        self,
        nızam_uri: str
    ) -> Tuple[bool, List[str]]:
        """
        Check consistency of a specific law (nızam).
        Belgili nızamdıń úyelisligin tastıqlaw.

        Validates:
        - Law has required properties (label, effectiveDate)
        - Referenced articles exist
        - No conflicting provisions
        - Proper language tags for Karakalpak content

        Parameters:
            nızam_uri (str): URI of the law to check

        Returns:
            Tuple[bool, List[str]]: (is_consistent, list of issues)

        Example / Misal:
            >>> uri = "http://huquqai.org/ontology#Nızam_JinayatKodeksi"
            >>> is_valid, issues = engine.check_nızam_consistency(uri)
            >>> if is_valid:
            ...     print("Law is consistent / Nızam úyelisli")
            ... else:
            ...     print(f"Found {len(issues)} issues")
        """
        issues = []

        try:
            logger.info(
                f"Checking law consistency / Nızam úyelisligin tastıqlaw: {nızam_uri}"
            )

            if not self.graph:
                issues.append("No RDF graph available / RDF graf joq")
                return False, issues

            nızam_ref = URIRef(nızam_uri)

            # Check 1: Law must have label / Nızam label-ǵa iye bolıwı kerek
            labels = list(self.graph.objects(nızam_ref, RDFS.label))
            if not labels:
                issues.append(
                    "Law missing rdfs:label / Nızamda rdfs:label joq"
                )

            # Check 2: Must have Karakalpak label / Qaraqalpaq label-i bolıwı kerek
            kaa_labels = [l for l in labels if hasattr(l, 'language') and l.language == 'kaa']
            if not kaa_labels:
                issues.append(
                    "Law missing Karakalpak (kaa) label / Nızamda Qaraqalpaq (kaa) label joq"
                )

            # Check 3: Check effective date / Kúsh kirisiw sánesi tastıqlaw
            effective_date = self._get_property_value(nızam_uri, self.huquq.effectiveDate)
            if not effective_date:
                issues.append(
                    "Law missing effective date / Nızamda kúsh kirisiw sánesi joq"
                )

            # Check 4: Validate referenced articles / Siltelme jasalǵan statiyalardı tastıqlaw
            articles = list(self.graph.objects(nızam_ref, self.huquq.hasArticle))
            for article_uri in articles:
                if not (article_uri, RDF.type, self.huquq.Statiya) in self.graph:
                    issues.append(
                        f"Referenced article not found or invalid: {article_uri} / "
                        f"Siltelme jasalǵan statiya tabılmadı yaki notoǵrı: {article_uri}"
                    )

            # Check 5: No duplicate article numbers / Qaytalanıwshı statiya nomerleri joq
            article_numbers = [
                self._get_property_value(str(art), self.huquq.articleNumber)
                for art in articles
            ]
            duplicates = [n for n in article_numbers if article_numbers.count(n) > 1]
            if duplicates:
                issues.append(
                    f"Duplicate article numbers found: {set(duplicates)} / "
                    f"Qaytalanıwshı statiya nomerleri tabıldı: {set(duplicates)}"
                )

            is_consistent = len(issues) == 0

            if is_consistent:
                logger.info(
                    f"Law is consistent / Nızam úyelisli: {nızam_uri}"
                )
            else:
                logger.warning(
                    f"Law has {len(issues)} consistency issues / "
                    f"Nızamda {len(issues)} úyelislik máselesi bar: {nızam_uri}"
                )
                for issue in issues:
                    logger.warning(f"  - {issue}")

            return is_consistent, issues

        except Exception as e:
            issues.append(f"Error during consistency check: {e}")
            logger.error(
                f"Failed to check law consistency: {e} / "
                f"Nızam úyelisligin tastıqlaw sátsiz: {e}"
            )
            return False, issues

    # ========================================================================
    # Explanation Methods / Túsindiriw Metodları
    # ========================================================================

    def explain_inference(
        self,
        subject: str,
        predicate: str,
        obj: str
    ) -> Optional[InferenceExplanation]:
        """
        Explain why a fact was inferred.
        Fakt nege qorıtındılanǵanın túsindiriw.

        Parameters:
            subject (str): Subject URI
            predicate (str): Predicate URI
            obj (str): Object URI or literal

        Returns:
            InferenceExplanation: Detailed explanation, or None if not found

        Example / Misal:
            >>> explanation = engine.explain_inference(
            ...     "http://huquqai.org/ontology#Jinayat_Urılıq",
            ...     "http://huquqai.org/ontology#crimeType",
            ...     "orta"
            ... )
            >>> if explanation:
            ...     print(explanation.explanation_kaa)
        """
        # Check if this fact was inferred / Bu fakt qorıtındılanǵan ma tastıqlaw
        fact = (subject, predicate, obj)

        if fact not in self.inferred_facts:
            logger.warning(
                f"Fact not found in inferred facts / Fakt qorıtındılanǵan faktlarda joq"
            )
            return None

        # Generate explanation based on the predicate / Predikat negizinde túsindirme jasawıш
        if "crimeType" in predicate:
            return InferenceExplanation(
                subject=subject,
                predicate=predicate,
                object=obj,
                rule="Crime classification by punishment duration",
                explanation_en=(
                    f"Crime was classified as '{obj}' based on the duration of "
                    f"its associated punishment."
                ),
                explanation_kaa=(
                    f"Jinayat baylanıslı jazasınıń uzaqlıǵı negizinde '{obj}' dep "
                    f"klassifikaciyalandı."
                ),
                confidence=0.95
            )
        elif "punishmentType" in predicate:
            return InferenceExplanation(
                subject=subject,
                predicate=predicate,
                object=obj,
                rule="Punishment type inference",
                explanation_en=(
                    f"Punishment type was inferred as '{obj}' based on its properties "
                    f"such as duration and conditions."
                ),
                explanation_kaa=(
                    f"Jaza túri uzaqlıq ha'm shartlar sıyaqlı xassalar negizinde "
                    f"'{obj}' dep qorıtındılandı."
                ),
                confidence=0.90
            )
        else:
            return InferenceExplanation(
                subject=subject,
                predicate=predicate,
                object=obj,
                rule="General reasoning",
                explanation_en=f"Fact inferred through automated reasoning.",
                explanation_kaa=f"Fakt avtomatik mántıqlı juwmaq arqalı qorıtındılandı.",
                confidence=0.80
            )

    def get_all_inferences(self) -> List[Tuple[str, str, str]]:
        """
        Get all inferred facts.
        Barlıq qorıtındılanǵan faktlardı alıw.

        Returns:
            List of (subject, predicate, object) triples

        Example / Misal:
            >>> inferences = engine.get_all_inferences()
            >>> print(f"Total inferences: {len(inferences)}")
            >>> for subj, pred, obj in inferences[:5]:
            ...     print(f"{subj} {pred} {obj}")
        """
        return self.inferred_facts.copy()

    # ========================================================================
    # Helper Methods / Kómekshi Metodlar
    # ========================================================================

    def _get_punishment_years(self, jinayat_uri: str) -> Optional[float]:
        """
        Get punishment duration for a crime.
        Jinayat ushın jaza uzaqlıǵın alıw.

        Parameters:
            jinayat_uri: URI of the crime

        Returns:
            Average punishment years, or None if not found
        """
        if not self.graph:
            return None

        try:
            jinayat_ref = URIRef(jinayat_uri)

            # Get punishment URI / Jaza URI-in alıw
            punishment_uris = list(self.graph.objects(jinayat_ref, self.huquq.hasPunishment))

            if not punishment_uris:
                return None

            # Get min and max years / Minimal ha'm maksimal jıllardı alıw
            punishment_uri = punishment_uris[0]
            min_years = self._get_property_value(str(punishment_uri), self.huquq.minYears)
            max_years = self._get_property_value(str(punishment_uri), self.huquq.maxYears)

            if min_years is not None and max_years is not None:
                # Return average / Ortashasın qaytarıw
                return (float(min_years) + float(max_years)) / 2
            elif max_years is not None:
                return float(max_years)
            elif min_years is not None:
                return float(min_years)

            return None

        except Exception:
            return None

    def _get_property_value(self, subject_uri: str, predicate: URIRef) -> Optional[Any]:
        """
        Get property value from RDF graph.
        RDF graftan xassa ma'nisin alıw.

        Parameters:
            subject_uri: Subject URI
            predicate: Predicate URIRef

        Returns:
            Property value, or None if not found
        """
        if not self.graph:
            return None

        try:
            subject_ref = URIRef(subject_uri)
            values = list(self.graph.objects(subject_ref, predicate))

            if not values:
                return None

            value = values[0]

            # Convert literal to Python type / Literaldı Python túrine ózgertiriw
            if isinstance(value, Literal):
                return value.toPython()

            return str(value)

        except Exception:
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get reasoning engine statistics.
        Mántıqlı juwmaq mexanizmi statistikasın alıw.

        Returns:
            Dictionary with statistics

        Example / Misal:
            >>> stats = engine.get_statistics()
            >>> print(f"Total reasoning runs: {stats['reasoning_runs']}")
            >>> print(f"Inferences made: {stats['inferences_made']}")
            >>> print(f"Average time: {stats['average_reasoning_time']:.4f}s")
        """
        stats = self.stats.copy()
        stats['average_reasoning_time'] = (
            self.stats['total_reasoning_time'] / self.stats['reasoning_runs']
            if self.stats['reasoning_runs'] > 0
            else 0.0
        )
        stats['total_inferred_facts'] = len(self.inferred_facts)

        return stats

    def clear_inferences(self) -> None:
        """
        Clear all stored inferences.
        Barlıq saqlanǵan qorıtındılardı tazalaw.
        """
        self.inferred_facts.clear()
        logger.info(
            "Inferences cleared / Qorıtındılar tazalandı"
        )

    def __repr__(self) -> str:
        """String representation / Júrgen kórinisi"""
        onto_status = "loaded" if self.onto else "not loaded"
        onto_status_kaa = "júklendi" if self.onto else "júklenmedi"

        return (
            f"ReasoningEngine(reasoner={self.reasoner_type.value}, "
            f"ontology={onto_status}/{onto_status_kaa}, "
            f"inferences={len(self.inferred_facts)})"
        )


# ============================================================================
# Module-level convenience functions / Modul-derežedegi qulaylıq funkciyaları
# ============================================================================

def create_reasoning_engine(
    ontology_path: Union[str, Path],
    reasoner: ReasonerType = ReasonerType.PELLET
) -> ReasoningEngine:
    """
    Create and initialize a reasoning engine.
    Mántıqlı juwmaq mexanizmin jasawıш ha'm inicializaciyalaw.

    Parameters:
        ontology_path: Path to OWL ontology file
        reasoner: Reasoner type to use

    Returns:
        Initialized ReasoningEngine instance

    Example / Misal:
        >>> engine = create_reasoning_engine(
        ...     "data/ontologies/criminal_code.owl",
        ...     reasoner=ReasonerType.PELLET
        ... )
        >>> result = engine.check_consistency()
    """
    return ReasoningEngine(ontology_path=ontology_path, reasoner=reasoner)
