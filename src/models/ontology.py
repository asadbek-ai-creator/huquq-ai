"""
OWL Ontology models for huquqAI system
"""

from typing import Optional, List, Dict
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from src.core.config import get_config


class LegalOntology:
    """Legal ontology manager using OWL"""

    def __init__(self):
        self.config = get_config()
        self.graph = Graph()
        self._setup_namespaces()

    def _setup_namespaces(self):
        """Setup ontology namespaces"""
        # Define namespaces
        self.huquq = Namespace(self.config.ontology.base_uri)
        self.legal = Namespace("http://legal-ontology.org#")

        # Bind namespaces
        self.graph.bind("huquq", self.huquq)
        self.graph.bind("legal", self.legal)
        self.graph.bind("owl", OWL)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)

    def create_class(self, class_name: str, label: Optional[str] = None,
                     comment: Optional[str] = None) -> URIRef:
        """Create an OWL class"""
        class_uri = self.huquq[class_name]
        self.graph.add((class_uri, RDF.type, OWL.Class))

        if label:
            self.graph.add((class_uri, RDFS.label, Literal(label, lang="kaa")))
        if comment:
            self.graph.add((class_uri, RDFS.comment, Literal(comment, lang="kaa")))

        return class_uri

    def create_object_property(self, property_name: str,
                                domain: Optional[URIRef] = None,
                                range_class: Optional[URIRef] = None) -> URIRef:
        """Create an OWL object property"""
        prop_uri = self.huquq[property_name]
        self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))

        if domain:
            self.graph.add((prop_uri, RDFS.domain, domain))
        if range_class:
            self.graph.add((prop_uri, RDFS.range, range_class))

        return prop_uri

    def create_datatype_property(self, property_name: str,
                                  domain: Optional[URIRef] = None,
                                  range_type: Optional[URIRef] = None) -> URIRef:
        """Create an OWL datatype property"""
        prop_uri = self.huquq[property_name]
        self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))

        if domain:
            self.graph.add((prop_uri, RDFS.domain, domain))
        if range_type:
            self.graph.add((prop_uri, RDFS.range, range_type))

        return prop_uri

    def create_individual(self, individual_name: str,
                          class_uri: URIRef,
                          properties: Optional[Dict] = None) -> URIRef:
        """Create an individual instance"""
        ind_uri = self.huquq[individual_name]
        self.graph.add((ind_uri, RDF.type, class_uri))

        if properties:
            for prop_name, value in properties.items():
                prop_uri = self.huquq[prop_name]
                if isinstance(value, str):
                    self.graph.add((ind_uri, prop_uri, Literal(value)))
                else:
                    self.graph.add((ind_uri, prop_uri, value))

        return ind_uri

    def initialize_legal_ontology(self):
        """Initialize the legal ontology with core classes"""
        # Create core classes
        nizam = self.create_class("Nizam", "Nızam", "Huqıqlıq nızam")
        statiya = self.create_class("Statiya", "Statiya", "Huqıqlıq statiya")
        jinayat = self.create_class("Jinayat", "Jinayat", "Jinayat")
        jaza = self.create_class("Jaza", "Jaza", "Jaza")
        kodeks = self.create_class("Kodeks", "Kodeks", "Huqıqlıq kodeks")

        # Create object properties
        self.create_object_property("hasArticle", kodeks, statiya)
        self.create_object_property("hasPunishment", jinayat, jaza)
        self.create_object_property("relatedToCrime", statiya, jinayat)
        self.create_object_property("belongsToCode", statiya, kodeks)

        # Create datatype properties
        self.create_datatype_property("articleNumber", statiya, XSD.string)
        self.create_datatype_property("crimeType", jinayat, XSD.string)
        self.create_datatype_property("severity", jinayat, XSD.string)
        self.create_datatype_property("description", None, XSD.string)

    def save_ontology(self, filename: str, format: str = "turtle"):
        """Save ontology to file"""
        self.graph.serialize(destination=filename, format=format)

    def load_ontology(self, filename: str, format: str = "turtle"):
        """Load ontology from file"""
        self.graph.parse(filename, format=format)

    def query(self, sparql_query: str) -> List:
        """Execute SPARQL query on the ontology"""
        return list(self.graph.query(sparql_query))
