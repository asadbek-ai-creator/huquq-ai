"""
OWL Ontology Manager for huquqAI Legal Knowledge Base
Huquqıy bilimler bazası ushın OWL Ontologiya Menedžeri

This module provides a professional ontology management system for Karakalpak legal data
using RDFLib and Owlready2 libraries.

Bu modul Qaraqalpaq huquqıy ma'limleri ushın RDFLib ha'm Owlready2 kitapxanalarını
qollanıp professional ontologiya basqarıw sistemasın beredi.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union
from threading import Lock
from datetime import datetime

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL
from rdflib.namespace import XSD
from rdflib.plugins.sparql import prepareQuery
from owlready2 import get_ontology, World, Thing
from loguru import logger

from src.core.config import get_config


class OntologyManagerError(Exception):
    """
    Base exception for ontology manager errors.
    Ontologiya menedžeri qátelikleri ushın bazalıq istisna.
    """
    def __init__(self, message: str, message_kaa: Optional[str] = None):
        """
        Initialize exception with bilingual messages.
        Istisnanı eki tilli xabarlar menen inizializaciyalaw.

        Args:
            message: Error message in English / Inglizше qátelik xabarı
            message_kaa: Error message in Karakalpak / Qaraqalpaqsha qátelik xabarı
        """
        self.message = message
        self.message_kaa = message_kaa or message
        super().__init__(self.message)


class OntologyNotLoadedError(OntologyManagerError):
    """
    Exception raised when ontology is not loaded.
    Ontologiya júklenmegen waqtında qaldırılatuǵın istisna.
    """
    pass


class OntologyManager:
    """
    Singleton OWL Ontology Manager for Karakalpak Legal Knowledge Base.
    Qaraqalpaq Huquqıy Bilimler Bazası ushın Singleton OWL Ontologiya Menedžeri.

    This class manages OWL ontologies containing Karakalpak legal terminology
    including Nızam (Law), Statiya (Article), Jinayat (Crime), and Jaza (Punishment).

    Bu klass Qaraqalpaq huquqıy terminologiyasın qamtıytuǵın OWL ontologiyalarni
    basqaradı, solay etip Nızam, Statiya, Jinayat ha'm Jaza túsiniklerin óz ishinde aladi.

    Examples / Misallar:
        >>> manager = OntologyManager()
        >>> manager.load_ontology("data/ontologies/legal_ontology.owl")
        >>> # Query for a crime / Jinayat haqqında soraw
        >>> results = manager.query_class("Jinayat")
        >>> # Get all articles / Barlıq statiyalardı alıw
        >>> articles = manager.get_instances("Statiya")
    """

    _instance: Optional['OntologyManager'] = None
    _lock: Lock = Lock()

    def __new__(cls) -> 'OntologyManager':
        """
        Implement singleton pattern.
        Singleton patterndi implements etiw.

        Returns:
            The single instance / Jálg'iz misal
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the Ontology Manager.
        Ontologiya Menedžerin inizializaciyalaw.

        This method is called only once due to singleton pattern.
        Bu metod singleton pattern sebepli tek bir ret shaqırıladi.
        """
        # Prevent re-initialization / Qayta inizializaciyadan saqlaw
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.config = get_config()

        # RDFLib graph for RDF/SPARQL operations
        # RDF/SPARQL ámeliyatlar ushın RDFLib grafı
        self.graph: Optional[Graph] = None

        # Owlready2 world for OWL reasoning
        # OWL sebep-saldar shıǵarıw ushın Owlready2 world
        self.world: Optional[World] = None
        self.ontology: Optional[Any] = None

        # Namespaces / Namespace-lar
        self.namespaces: Dict[str, Namespace] = {}
        self._setup_namespaces()

        # Statistics / Statistika
        self.stats = {
            'loaded': False,
            'load_time': None,
            'triple_count': 0,
            'class_count': 0,
            'individual_count': 0,
        }

        logger.info("OntologyManager initialized / Ontologiya Menedžer inizializaciya etildi")

    def _setup_namespaces(self) -> None:
        """
        Setup ontology namespaces from configuration.
        Konfiguraciyadan ontologiya namespace-larin ornatiw.
        """
        ns_config = self.config.ontology.namespaces

        # Create namespace objects / Namespace obyektlerin jasawiш
        for prefix, uri in ns_config.items():
            self.namespaces[prefix] = Namespace(uri)

        logger.debug(f"Namespaces configured: {len(self.namespaces)} / "
                    f"Namespace-lar sazlandı: {len(self.namespaces)}")

    def load_ontology(
        self,
        file_path: Union[str, Path],
        format: str = "auto"
    ) -> bool:
        """
        Load ontology file containing Karakalpak legal data.
        Qaraqalpaq huquqıy ma'limlerin qamtıytuǵın ontologiya faylın júklew.

        Supports .owl (RDF/XML), .ttl (Turtle), and .rdf formats.
        .owl (RDF/XML), .ttl (Turtle), ha'm .rdf formatların qollap-quwatlaydı.

        Args:
            file_path: Path to .owl or .ttl file / .owl yamasa .ttl fayl jolı
            format: File format (auto, xml, turtle, n3) / Fayl formatı

        Returns:
            True if successful / Tabıslı bolsa True

        Raises:
            OntologyManagerError: If loading fails / Júklew sátsiz bolsa
            FileNotFoundError: If file doesn't exist / Fayl joq bolsa

        Examples / Misallar:
            >>> manager = OntologyManager()
            >>> # Load Criminal Code ontology / Jinayat Kodeksi ontologiyasın júklew
            >>> manager.load_ontology("data/ontologies/criminal_code.owl")
            True
            >>> # Load knowledge base / Bilimler bazasın júklew
            >>> manager.load_ontology("data/knowledge/legal_kb.ttl", format="turtle")
            True
        """
        start_time = datetime.now()
        file_path = Path(file_path)

        # Check file existence / Fayldıń bar ekenin tekseriv
        if not file_path.exists():
            error_msg = f"Ontology file not found: {file_path}"
            error_msg_kaa = f"Ontologiya faylı tabılmadı: {file_path}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise FileNotFoundError(error_msg)

        try:
            logger.info(f"Loading ontology / Ontologiyani júklew: {file_path}")

            # Initialize RDFLib graph / RDFLib grafın inizializaciyalaw
            self.graph = Graph()

            # Bind namespaces / Namespace-lardı baylaw
            for prefix, namespace in self.namespaces.items():
                self.graph.bind(prefix, namespace)

            # Determine format / Formatı anıqlaw
            if format == "auto":
                format = self._detect_format(file_path)

            # Parse ontology / Ontologiyani parse etiw
            logger.debug(f"Parsing file with format: {format} / "
                        f"Fayldi formatlaw: {format}")
            self.graph.parse(file_path, format=format)

            # Load with Owlready2 for reasoning / Sebep-saldar ushın Owlready2 menen júklew
            self._load_owlready2(file_path)

            # Update statistics / Statistikani jańalaw
            self._update_statistics()

            load_duration = (datetime.now() - start_time).total_seconds()
            self.stats['loaded'] = True
            self.stats['load_time'] = load_duration

            logger.info(
                f"Ontology loaded successfully in {load_duration:.2f}s / "
                f"Ontologiya tabıslı júklendi {load_duration:.2f}s ishinde"
            )
            logger.info(
                f"Triples: {self.stats['triple_count']}, "
                f"Classes: {self.stats['class_count']}, "
                f"Individuals: {self.stats['individual_count']}"
            )

            return True

        except Exception as e:
            error_msg = f"Failed to load ontology: {str(e)}"
            error_msg_kaa = f"Ontologiyani júklew sátsiz: {str(e)}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise OntologyManagerError(error_msg, error_msg_kaa) from e

    def _detect_format(self, file_path: Path) -> str:
        """
        Auto-detect file format based on extension.
        Fayl formatın kengeytiw boyınsha avtomatik anıqlaw.

        Args:
            file_path: Path to file / Fayl jolı

        Returns:
            Format string / Format júrgen shıǵı
        """
        extension = file_path.suffix.lower()
        format_map = {
            '.owl': 'xml',
            '.rdf': 'xml',
            '.ttl': 'turtle',
            '.n3': 'n3',
            '.nt': 'nt',
            '.jsonld': 'json-ld',
        }
        return format_map.get(extension, 'xml')

    def _load_owlready2(self, file_path: Path) -> None:
        """
        Load ontology with Owlready2 for reasoning capabilities.
        Sebep-saldar imkaniyatları ushın Owlready2 menen ontologiyani júklew.

        Args:
            file_path: Path to ontology file / Ontologiya fayl jolı
        """
        try:
            self.world = World()
            self.ontology = self.world.get_ontology(f"file://{file_path}").load()
            logger.debug("Owlready2 ontology loaded / Owlready2 ontologiya júklendi")
        except Exception as e:
            logger.warning(f"Owlready2 loading failed (reasoning disabled): {e} / "
                          f"Owlready2 júklew sátsiz (sebep-saldar óshirildi): {e}")

    def _update_statistics(self) -> None:
        """
        Update ontology statistics.
        Ontologiya statistikasın jańalaw.
        """
        if self.graph is None:
            return

        # Count triples / Triple-lardı sanaw
        self.stats['triple_count'] = len(self.graph)

        # Count classes / Klasslardı sanaw
        classes = list(self.graph.subjects(RDF.type, OWL.Class))
        self.stats['class_count'] = len(classes)

        # Count individuals / Individuallarni sanaw
        individuals = set()
        for s, p, o in self.graph.triples((None, RDF.type, None)):
            if o != OWL.Class and o != OWL.ObjectProperty and o != OWL.DatatypeProperty:
                individuals.add(s)
        self.stats['individual_count'] = len(individuals)

    def query_sparql(
        self,
        query: str,
        lang: str = "kaa"
    ) -> List[Dict[str, Any]]:
        """
        Execute SPARQL query on the ontology.
        Ontologiyada SPARQL sorawdı orınlaw.

        Args:
            query: SPARQL query string / SPARQL soraw júrgen shıǵı
            lang: Language filter (kaa, uz, ru, en) / Til filtri

        Returns:
            Query results / Soraw nátiyјeleri

        Raises:
            OntologyNotLoadedError: If ontology not loaded / Ontologiya júklenmegen bolsa

        Examples / Misallar:
            >>> # Query all crimes / Barlıq jinayatlardı soraw
            >>> query = '''
            ... PREFIX huquq: <http://huquqai.org/ontology#>
            ... SELECT ?jinayat ?name
            ... WHERE {
            ...     ?jinayat a huquq:Jinayat ;
            ...              rdfs:label ?name .
            ...     FILTER(LANG(?name) = "kaa")
            ... }
            ... '''
            >>> results = manager.query_sparql(query)
        """
        self._check_loaded()

        try:
            logger.debug(f"Executing SPARQL query / SPARQL sorawdı orınlaw")

            # Prepare and execute query / Sorawdı tayyarlaw ha'm orınlaw
            prepared = prepareQuery(query, initNs=self.namespaces)
            results = self.graph.query(prepared)

            # Convert to list of dicts / Dict listi kórinisine aylantiriw
            result_list = []
            for row in results:
                result_dict = {}
                for var in results.vars:
                    value = row[var]
                    if isinstance(value, Literal):
                        result_dict[str(var)] = str(value)
                    elif isinstance(value, URIRef):
                        result_dict[str(var)] = str(value)
                    else:
                        result_dict[str(var)] = value
                result_list.append(result_dict)

            logger.debug(f"Query returned {len(result_list)} results / "
                        f"Soraw {len(result_list)} nátiyјe qaytardı")

            return result_list

        except Exception as e:
            error_msg = f"SPARQL query failed: {str(e)}"
            error_msg_kaa = f"SPARQL soraw sátsiz: {str(e)}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise OntologyManagerError(error_msg, error_msg_kaa) from e

    def get_class(self, class_name: str) -> Optional[URIRef]:
        """
        Get OWL class URI by name.
        OWL klass URI-in atı boyınsha alıw.

        Args:
            class_name: Class name (e.g., "Nızam", "Statiya", "Jinayat", "Jaza")
                       Klass atı (mısalı, "Nızam", "Statiya", "Jinayat", "Jaza")

        Returns:
            Class URI or None / Klass URI yamasa None

        Examples / Misallar:
            >>> # Get Crime class / Jinayat klassın alıw
            >>> crime_class = manager.get_class("Jinayat")
            >>> print(crime_class)
            http://huquqai.org/ontology#Jinayat
        """
        self._check_loaded()

        # Try with huquq namespace / huquq namespace menen urınıw
        huquq = self.namespaces.get('huquq')
        if huquq:
            class_uri = huquq[class_name]
            if (class_uri, RDF.type, OWL.Class) in self.graph:
                return class_uri

        # Search in all classes / Barlıq klasslarda izlew
        for s in self.graph.subjects(RDF.type, OWL.Class):
            if str(s).endswith(class_name) or str(s).endswith(f"#{class_name}"):
                return s

        logger.warning(f"Class not found: {class_name} / Klass tabılmadı: {class_name}")
        return None

    def get_instances(
        self,
        class_name: str,
        lang: Optional[str] = "kaa",
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all instances of a given class.
        Berilgen klasstıń barlıq misalların alıw.

        Args:
            class_name: Class name (Nızam, Statiya, Jinayat, Jaza) / Klass atı
            lang: Language filter / Til filtri
            limit: Maximum results / Eń kóp nátiyјe

        Returns:
            List of instances with properties / Xassalari bar misallar listı

        Examples / Misallar:
            >>> # Get all articles / Barlıq statiyalardı alıw
            >>> articles = manager.get_instances("Statiya", lang="kaa", limit=10)
            >>> for article in articles:
            ...     print(article['uri'], article['label'])
        """
        self._check_loaded()

        class_uri = self.get_class(class_name)
        if not class_uri:
            return []

        instances = []
        count = 0

        # Find all instances / Barlıq misallardı tabıw
        for instance in self.graph.subjects(RDF.type, class_uri):
            if limit and count >= limit:
                break

            instance_data = {
                'uri': str(instance),
                'type': class_name,
            }

            # Get properties / Xassalardı alıw
            for p, o in self.graph.predicate_objects(instance):
                pred_name = str(p).split('#')[-1].split('/')[-1]

                if isinstance(o, Literal):
                    # Filter by language / Til boyınsha filtirlaw
                    if lang and o.language and o.language != lang:
                        continue
                    instance_data[pred_name] = str(o)
                elif isinstance(o, URIRef):
                    instance_data[pred_name] = str(o)

            instances.append(instance_data)
            count += 1

        logger.debug(f"Found {len(instances)} instances of {class_name} / "
                    f"{class_name} klassinıń {len(instances)} misalı tabıldı")

        return instances

    def search_by_label(
        self,
        search_term: str,
        lang: str = "kaa",
        fuzzy: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search resources by label.
        Label boyınsha resurslarni izlew.

        Args:
            search_term: Search term / Izlew termini
            lang: Language / Til
            fuzzy: Enable fuzzy matching / Anıq emes sáykeslikti qosıw

        Returns:
            Matching resources / Sáykes resurslar

        Examples / Misallar:
            >>> # Search for "jinayat" / "jinayat" sózin izlew
            >>> results = manager.search_by_label("jinayat", lang="kaa")
            >>> # Fuzzy search / Anıq emes izlew
            >>> results = manager.search_by_label("jınayat", fuzzy=True)
        """
        self._check_loaded()

        results = []
        search_lower = search_term.lower()

        # Search in rdfs:label / rdfs:label ishinde izlew
        for s, p, o in self.graph.triples((None, RDFS.label, None)):
            if not isinstance(o, Literal):
                continue

            # Check language / Tildi tekseriv
            if o.language and o.language != lang:
                continue

            label = str(o).lower()

            # Match / Sáykeslik
            if fuzzy:
                # Simple fuzzy matching / Qарапайım anıq emes sáykeslik
                if search_lower in label or label in search_lower:
                    match = True
                else:
                    # Levenshtein-like simple check
                    match = self._simple_fuzzy_match(search_lower, label)
            else:
                match = search_lower in label

            if match:
                results.append({
                    'uri': str(s),
                    'label': str(o),
                    'language': o.language or 'unknown'
                })

        logger.debug(f"Search '{search_term}' found {len(results)} results / "
                    f"'{search_term}' izlewi {len(results)} nátiyјe tapdı")

        return results

    def _simple_fuzzy_match(self, term1: str, term2: str, threshold: float = 0.7) -> bool:
        """
        Simple fuzzy string matching.
        Qарапайım anıq emes júrgen shıǵı sáykesligi.

        Args:
            term1: First term / Birinshi termin
            term2: Second term / Ekinshi termin
            threshold: Similarity threshold / Uyqaslıq shegi

        Returns:
            True if similar / Uyqas bolsa True
        """
        # Simple character overlap ratio / Qарапайım hárip qabat qawısıw koefficienti
        set1 = set(term1)
        set2 = set(term2)

        if not set1 or not set2:
            return False

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold

    def get_related(
        self,
        resource_uri: str,
        relation: Optional[str] = None
    ) -> List[Tuple[str, str, str]]:
        """
        Get related resources.
        Baylanıslı resurslarni alıw.

        Args:
            resource_uri: Resource URI / Resurs URI
            relation: Specific relation or None for all / Belgili baylanıs yamasa barlığı ushın None

        Returns:
            List of (subject, predicate, object) tuples / (subyekt, predikat, obyekt) tuple-lar listı

        Examples / Misallar:
            >>> # Get all relations / Barlıq baylanıslarni alıw
            >>> relations = manager.get_related("http://huquqai.org/article/123")
            >>> # Get specific relation / Belgili baylanısnı alıw
            >>> punishments = manager.get_related(
            ...     "http://huquqai.org/crime/456",
            ...     "hasPunishment"
            ... )
        """
        self._check_loaded()

        uri = URIRef(resource_uri)
        relations = []

        if relation:
            # Specific relation / Belgili baylanıs
            pred_uri = self.namespaces.get('huquq', Namespace(''))[relation]
            for o in self.graph.objects(uri, pred_uri):
                relations.append((str(uri), relation, str(o)))
        else:
            # All relations / Barlıq baylanıslar
            for p, o in self.graph.predicate_objects(uri):
                pred_name = str(p).split('#')[-1].split('/')[-1]
                relations.append((str(uri), pred_name, str(o)))

        return relations

    def add_individual(
        self,
        class_name: str,
        individual_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> URIRef:
        """
        Add new individual to ontology.
        Ontologiyaga jańa individual qosıw.

        Args:
            class_name: Class name (Nızam, Statiya, Jinayat, Jaza) / Klass atı
            individual_name: Individual name / Individual atı
            properties: Properties dict / Xassalar dict

        Returns:
            Individual URI / Individual URI

        Raises:
            OntologyNotLoadedError: If ontology not loaded / Ontologiya júklenmegen bolsa

        Examples / Misallar:
            >>> # Add new article / Jańa statiya qosıw
            >>> article_uri = manager.add_individual(
            ...     "Statiya",
            ...     "Article_123",
            ...     {
            ...         "articleNumber": "123",
            ...         "title": "Jinayattıń awır túri",
            ...         "language": "kaa"
            ...     }
            ... )
        """
        self._check_loaded()

        class_uri = self.get_class(class_name)
        if not class_uri:
            raise OntologyManagerError(
                f"Class not found: {class_name}",
                f"Klass tabılmadı: {class_name}"
            )

        # Create individual URI / Individual URI jasawiш
        huquq = self.namespaces.get('huquq')
        individual_uri = huquq[individual_name]

        # Add type / Tipti qosıw
        self.graph.add((individual_uri, RDF.type, class_uri))

        # Add properties / Xassalarni qosıw
        if properties:
            for prop_name, value in properties.items():
                prop_uri = huquq[prop_name]

                if isinstance(value, str):
                    # Check if it's a language-tagged string
                    if prop_name in ['title', 'description', 'label']:
                        lang = properties.get('language', 'kaa')
                        literal = Literal(value, lang=lang)
                    else:
                        literal = Literal(value)
                    self.graph.add((individual_uri, prop_uri, literal))
                elif isinstance(value, (int, float)):
                    literal = Literal(value)
                    self.graph.add((individual_uri, prop_uri, literal))
                else:
                    # Assume URI reference
                    obj_uri = URIRef(value) if isinstance(value, str) else value
                    self.graph.add((individual_uri, prop_uri, obj_uri))

        logger.info(f"Added individual: {individual_name} of type {class_name} / "
                   f"Individual qosıldı: {class_name} tipindegi {individual_name}")

        return individual_uri

    def save_ontology(
        self,
        file_path: Union[str, Path],
        format: str = "turtle"
    ) -> bool:
        """
        Save ontology to file.
        Ontologiyani faylǵa saqlawish.

        Args:
            file_path: Output file path / Shıǵıs fayl jolı
            format: Output format (turtle, xml, n3) / Shıǵıs formatı

        Returns:
            True if successful / Tabıslı bolsa True

        Examples / Misallar:
            >>> # Save as Turtle / Turtle formatında saqlawish
            >>> manager.save_ontology("output/updated_ontology.ttl", "turtle")
            >>> # Save as RDF/XML / RDF/XML formatında saqlawish
            >>> manager.save_ontology("output/ontology.owl", "xml")
        """
        self._check_loaded()

        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Saving ontology to {file_path} / "
                       f"Ontologiyani {file_path}-ке saqlawish")

            self.graph.serialize(destination=str(file_path), format=format)

            logger.info("Ontology saved successfully / Ontologiya tabıslı saqlandi")
            return True

        except Exception as e:
            error_msg = f"Failed to save ontology: {str(e)}"
            error_msg_kaa = f"Ontologiyani saqlawish sátsiz: {str(e)}"
            logger.error(f"{error_msg} / {error_msg_kaa}")
            raise OntologyManagerError(error_msg, error_msg_kaa) from e

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get ontology statistics.
        Ontologiya statistikasın alıw.

        Returns:
            Statistics dictionary / Statistika dictionary

        Examples / Misallar:
            >>> stats = manager.get_statistics()
            >>> print(f"Classes: {stats['class_count']}")
            >>> print(f"Klasslar: {stats['class_count']}")
        """
        return self.stats.copy()

    def is_loaded(self) -> bool:
        """
        Check if ontology is loaded.
        Ontologiya júklengenin tekseriv.

        Returns:
            True if loaded / Júklengen bolsa True
        """
        return self.stats['loaded'] and self.graph is not None

    def _check_loaded(self) -> None:
        """
        Check if ontology is loaded and raise error if not.
        Ontologiya júklengenin tekseriv ha'm júklenmegen bolsa qátelik qaldırıw.

        Raises:
            OntologyNotLoadedError: If not loaded / Júklenmegen bolsa
        """
        if not self.is_loaded():
            raise OntologyNotLoadedError(
                "Ontology is not loaded. Call load_ontology() first.",
                "Ontologiya júklenmegen. Aldı bılan load_ontology() shaqırıń."
            )

    def clear(self) -> None:
        """
        Clear loaded ontology.
        Júklengen ontologiyani tazalaw.

        This method removes all loaded data and resets the manager.
        Bu metod barlıq júklengen ma'lumotlardı óshiredi ha'm menedžerdi qaytadan ornataydı.
        """
        if self.graph:
            self.graph.close()
            self.graph = None

        if self.world:
            self.world = None

        self.ontology = None

        self.stats = {
            'loaded': False,
            'load_time': None,
            'triple_count': 0,
            'class_count': 0,
            'individual_count': 0,
        }

        logger.info("Ontology cleared / Ontologiya tazalandı")

    def __repr__(self) -> str:
        """String representation."""
        status = "loaded" if self.is_loaded() else "not loaded"
        status_kaa = "júklendi" if self.is_loaded() else "júklenmedi"
        return (f"<OntologyManager status={status}/{status_kaa} "
                f"triples={self.stats['triple_count']}>")


# Convenience function to get singleton instance
# Singleton misalı alıw ushın qolaylı funktsiya
def get_ontology_manager() -> OntologyManager:
    """
    Get the singleton OntologyManager instance.
    Singleton OntologyManager misalın alıw.

    Returns:
        OntologyManager instance / OntologyManager misalı

    Examples / Misallar:
        >>> from src.core.ontology_manager import get_ontology_manager
        >>> manager = get_ontology_manager()
        >>> manager.load_ontology("data/ontologies/legal_ontology.owl")
    """
    return OntologyManager()
