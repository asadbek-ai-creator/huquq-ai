# OntologyManager Documentation
# OntologyManager Dokumentatsiyası

## Table of Contents / Mazmunı

1. [Overview / Umumiy túsinik](#overview)
2. [Installation / Ornatiw](#installation)
3. [Quick Start / Tez baslaw](#quick-start)
4. [API Reference / API anıqlama](#api-reference)
5. [Examples / Misallar](#examples)
6. [Error Handling / Qáteliklerdi islew](#error-handling)
7. [Best Practices / Eń jaqsı tácriyбeler](#best-practices)

---

## Overview / Umumiy túsinik

The `OntologyManager` is a professional singleton class for managing OWL ontologies containing Karakalpak legal data. It provides comprehensive support for:

`OntologyManager` - Qaraqalpaq huquqıy ma'limlerin qamtıytuǵın OWL ontologiyalardı basqarıw ushın professional singleton klass. Ol tómendegi funkciyalardı qollap-quwatlaydı:

- Loading OWL/RDF ontologies / OWL/RDF ontologiyalarni júklew
- SPARQL query execution / SPARQL sorawlarni orınlaw
- OWL reasoning with Owlready2 / Owlready2 menen OWL sebep-saldar shıǵarıw
- Karakalpak language support / Qaraqalpaq tiliniń qollap-quwatlaw
- UTF-8 encoding / UTF-8 kodlaw
- Bilingual error messages / Eki tilli qátelik xabarları

### Key Features / Negizgi imkaniyatlar

✅ **Singleton Pattern** - Single instance across application / Qollanba boyınsha jálg'iz misal
✅ **Bilingual Support** - English and Karakalpak / Inglizше ha'm Qaraqalpaqsha
✅ **Type Hints** - Full type annotation / Tóliq tip annotaciya
✅ **Error Handling** - Comprehensive error handling / Kólemli qátelik basqarıw
✅ **Logging** - Detailed logging with loguru / Loguru menen eǵjeyli loglaw
✅ **Thread-Safe** - Thread-safe singleton implementation / Potokqa qáwipsiz singleton implements

---

## Installation / Ornatiw

### Prerequisites / Aldınǵı talablar

```bash
# Required packages / Kerekli paketler
pip install rdflib==7.0.0
pip install owlready2==0.46
pip install loguru==0.7.2
```

### Import / Import

```python
# Import the manager / Menedžerdi import etiw
from src.core.ontology_manager import OntologyManager, get_ontology_manager

# Or import exceptions / Yamasa istisnalardı import etiw
from src.core.ontology_manager import (
    OntologyManagerError,
    OntologyNotLoadedError
)
```

---

## Quick Start / Tez baslaw

### Basic Usage / Negizgi qollanıw

```python
from src.core.ontology_manager import get_ontology_manager

# Get manager instance / Menedžer misalın alıw
manager = get_ontology_manager()

# Load ontology / Ontologiyani júklew
manager.load_ontology("data/ontologies/legal_ontology.owl")

# Check if loaded / Júklengenin tekseriv
if manager.is_loaded():
    print("Ontology loaded / Ontologiya júklendi")

# Get statistics / Statistikani alıw
stats = manager.get_statistics()
print(f"Triples: {stats['triple_count']}")
```

### Working with Legal Classes / Huquqıy klasslar menen islewi

```python
# Get legal classes / Huquqıy klasslardı alıw
nizam = manager.get_class("Nızam")      # Law / Huqıqlıq nızam
statiya = manager.get_class("Statiya")  # Article / Statiya
jinayat = manager.get_class("Jinayat")  # Crime / Jinayat
jaza = manager.get_class("Jaza")        # Punishment / Jaza

print(f"Law class URI: {nizam}")
```

---

## API Reference / API anıqlama

### Class: `OntologyManager`

#### Constructor / Konstruktor

```python
manager = OntologyManager()
# Or use singleton getter / Yamasa singleton getter-di qollanıw
manager = get_ontology_manager()
```

**Note:** The constructor implements singleton pattern. Multiple calls return the same instance.
**Eskertiw:** Konstruktor singleton pattern implements etedi. Kóp shaqırıwlar bir xıl misaldı qaytaradı.

---

### Methods / Metodlar

#### `load_ontology(file_path, format="auto")`

Load ontology file containing Karakalpak legal data.
Qaraqalpaq huquqıy ma'limlerin qamtıytuǵın ontologiya faylın júklew.

**Parameters / Parametrler:**
- `file_path` (str | Path): Path to .owl or .ttl file / .owl yamasa .ttl fayl jolı
- `format` (str): File format - "auto", "xml", "turtle", "n3" / Fayl formatı

**Returns / Qaytaradi:** `bool` - True if successful / Tabıslı bolsa True

**Raises / Qaldıradı:**
- `FileNotFoundError`: If file doesn't exist / Fayl joq bolsa
- `OntologyManagerError`: If loading fails / Júklew sátsiz bolsa

**Example / Misal:**
```python
# Load Criminal Code / Jinayat Kodeksin júklew
manager.load_ontology("data/ontologies/criminal_code.owl")

# Load Turtle format / Turtle formatında júklew
manager.load_ontology("data/knowledge/legal_kb.ttl", format="turtle")
```

---

#### `query_sparql(query, lang="kaa")`

Execute SPARQL query on the ontology.
Ontologiyada SPARQL sorawdı orınlaw.

**Parameters / Parametrler:**
- `query` (str): SPARQL query string / SPARQL soraw júrgen shıǵı
- `lang` (str): Language filter (kaa, uz, ru, en) / Til filtri

**Returns / Qaytaradi:** `List[Dict[str, Any]]` - Query results / Soraw nátiyјeleri

**Raises / Qaldıradı:**
- `OntologyNotLoadedError`: If ontology not loaded / Ontologiya júklenmegen bolsa
- `OntologyManagerError`: If query fails / Soraw sátsiz bolsa

**Example / Misal:**
```python
# Query all crimes / Barlıq jinayatlardı soraw
query = """
PREFIX huquq: <http://huquqai.org/ontology#>
SELECT ?jinayat ?name
WHERE {
    ?jinayat a huquq:Jinayat ;
             rdfs:label ?name .
    FILTER(LANG(?name) = "kaa")
}
"""
results = manager.query_sparql(query)
```

---

#### `get_class(class_name)`

Get OWL class URI by name.
OWL klass URI-in atı boyınsha alıw.

**Parameters / Parametrler:**
- `class_name` (str): Class name - "Nızam", "Statiya", "Jinayat", "Jaza"

**Returns / Qaytaradi:** `Optional[URIRef]` - Class URI or None

**Example / Misal:**
```python
# Get Crime class / Jinayat klassın alıw
crime_class = manager.get_class("Jinayat")
if crime_class:
    print(f"Crime class URI: {crime_class}")
```

---

#### `get_instances(class_name, lang="kaa", limit=None)`

Get all instances of a given class.
Berilgen klasstıń barlıq misallarin alıw.

**Parameters / Parametrler:**
- `class_name` (str): Class name / Klass atı
- `lang` (str): Language filter / Til filtri
- `limit` (int): Maximum results / Eń kóp nátiyјe

**Returns / Qaytaradi:** `List[Dict[str, Any]]` - List of instances / Misallar listı

**Example / Misal:**
```python
# Get all articles in Karakalpak / Qaraqalpaqshadaǵı barlıq statiyalardı alıw
articles = manager.get_instances("Statiya", lang="kaa", limit=10)

for article in articles:
    print(f"Article: {article.get('label')}")
    print(f"  Number: {article.get('articleNumber')}")
    print(f"  URI: {article.get('uri')}")
```

---

#### `search_by_label(search_term, lang="kaa", fuzzy=False)`

Search resources by label.
Label boyınsha resurslarni izlew.

**Parameters / Parametrler:**
- `search_term` (str): Search term / Izlew termini
- `lang` (str): Language / Til
- `fuzzy` (bool): Enable fuzzy matching / Anıq emes sáykeslikti qosıw

**Returns / Qaytaradi:** `List[Dict[str, Any]]` - Matching resources / Sáykes resurslar

**Example / Misal:**
```python
# Exact search / Anıq izlew
results = manager.search_by_label("jinayat", lang="kaa")

# Fuzzy search (tolerates typos) / Anıq emes izlew (typo-lardı qabıl etedi)
results = manager.search_by_label("jınayat", lang="kaa", fuzzy=True)

for result in results:
    print(f"Found: {result['label']} ({result['language']})")
```

---

#### `add_individual(class_name, individual_name, properties=None)`

Add new individual to ontology.
Ontologiyaga jańa individual qosıw.

**Parameters / Parametrler:**
- `class_name` (str): Class name / Klass atı
- `individual_name` (str): Individual name / Individual atı
- `properties` (Dict): Properties dictionary / Xassalar dictionary

**Returns / Qaytaradi:** `URIRef` - Individual URI

**Example / Misal:**
```python
# Add new article / Jańa statiya qosıw
article_uri = manager.add_individual(
    "Statiya",
    "Statiya_456",
    {
        "articleNumber": "456",
        "title": "Jańa huquqıy nızam",
        "description": "Bu jańa statiya",
        "language": "kaa"
    }
)

print(f"Added article: {article_uri}")
```

---

#### `get_related(resource_uri, relation=None)`

Get related resources.
Baylanıslı resurslarni alıw.

**Parameters / Parametrler:**
- `resource_uri` (str): Resource URI / Resurs URI
- `relation` (str): Specific relation or None for all / Belgili baylanıs yamasa barlığı ushın None

**Returns / Qaytaradi:** `List[Tuple[str, str, str]]` - (subject, predicate, object) tuples

**Example / Misal:**
```python
# Get all relations / Barlıq baylanıslarni alıw
crime_uri = "http://huquqai.org/crime/123"
all_relations = manager.get_related(crime_uri)

# Get specific relation / Belgili baylanısnı alıw
punishments = manager.get_related(crime_uri, "hasPunishment")

for subj, pred, obj in punishments:
    print(f"{pred}: {obj}")
```

---

#### `save_ontology(file_path, format="turtle")`

Save ontology to file.
Ontologiyani faylǵa saqlawish.

**Parameters / Parametrler:**
- `file_path` (str | Path): Output file path / Shıǵıs fayl jolı
- `format` (str): Output format - "turtle", "xml", "n3" / Shıǵıs formatı

**Returns / Qaytaradi:** `bool` - True if successful / Tabıslı bolsa True

**Example / Misal:**
```python
# Save as Turtle / Turtle formatında saqlawish
manager.save_ontology("output/updated.ttl", format="turtle")

# Save as RDF/XML / RDF/XML formatında saqlawish
manager.save_ontology("output/ontology.owl", format="xml")
```

---

#### `get_statistics()`

Get ontology statistics.
Ontologiya statistikasın alıw.

**Returns / Qaytaradi:** `Dict[str, Any]` - Statistics dictionary

**Example / Misal:**
```python
stats = manager.get_statistics()

print(f"Loaded: {stats['loaded']}")
print(f"Triples: {stats['triple_count']}")
print(f"Classes: {stats['class_count']}")
print(f"Individuals: {stats['individual_count']}")
print(f"Load time: {stats['load_time']:.2f}s")
```

---

#### `is_loaded()`

Check if ontology is loaded.
Ontologiya júklengenin tekseriv.

**Returns / Qaytaradi:** `bool` - True if loaded / Júklengen bolsa True

---

#### `clear()`

Clear loaded ontology.
Júklengen ontologiyani tazalaw.

**Example / Misal:**
```python
manager.clear()
print(f"Is loaded: {manager.is_loaded()}")  # False
```

---

## Examples / Misallar

### Example 1: Complete Workflow / Tóliq iş joli

```python
from src.core.ontology_manager import get_ontology_manager

# Get manager / Menedžerdi alıw
manager = get_ontology_manager()

# Load ontology / Ontologiyani júklew
manager.load_ontology("data/ontologies/criminal_code.owl")

# Query crimes / Jinayatlardı soraw
crimes = manager.get_instances("Jinayat", lang="kaa")

# Add new crime / Jańa jinayat qosıw
new_crime = manager.add_individual(
    "Jinayat",
    "Jinayat_NewCrime",
    {
        "label": "Jańa jinayat",
        "crimeType": "medium",
        "description": "Bu jańa jinayat túsindirmesi"
    }
)

# Save updated ontology / Jańalanǵan ontologiyani saqlawish
manager.save_ontology("output/updated_criminal_code.ttl")
```

### Example 2: SPARQL Query / SPARQL soraw

```python
# Complex SPARQL query / Kúrdelі SPARQL soraw
query = """
PREFIX huquq: <http://huquqai.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?jinayat ?label ?type ?jaza
WHERE {
    ?jinayat a huquq:Jinayat ;
             rdfs:label ?label ;
             huquq:crimeType ?type .

    OPTIONAL {
        ?jinayat huquq:hasPunishment ?jaza .
    }

    FILTER(LANG(?label) = "kaa")
    FILTER(?type = "heavy")
}
ORDER BY ?label
LIMIT 10
"""

results = manager.query_sparql(query)

for result in results:
    print(f"Crime: {result['label']}")
    print(f"  Type: {result['type']}")
    if 'jaza' in result:
        print(f"  Punishment: {result['jaza']}")
```

### Example 3: Multilingual Search / Kóp tilli izlew

```python
# Search in different languages / Túrli tillerde izlew
languages = ["kaa", "uz", "ru", "en"]

for lang in languages:
    results = manager.search_by_label("law", lang=lang)
    print(f"\n{lang}: {len(results)} results")
    for r in results[:2]:
        print(f"  - {r['label']}")
```

---

## Error Handling / Qáteliklerdi islew

### Exception Hierarchy / Istisna iyerarchiyası

```
OntologyManagerError (base)
    ├── OntologyNotLoadedError
    └── (other errors inherit from base)
```

### Handling Errors / Qáteliklерdi basqarıw

```python
from src.core.ontology_manager import (
    get_ontology_manager,
    OntologyManagerError,
    OntologyNotLoadedError
)

manager = get_ontology_manager()

try:
    # Try to load ontology / Ontologiyani júklew urınısı
    manager.load_ontology("data/ontologies/legal.owl")

except FileNotFoundError as e:
    print(f"File not found: {e}")
    print("Fayl tabılmadı")

except OntologyManagerError as e:
    # Bilingual error messages / Eki tilli qátelik xabarları
    print(f"Error (EN): {e.message}")
    print(f"Qátelik (KAA): {e.message_kaa}")

try:
    # Try to query before loading / Júklewden aldın soraw urınısı
    results = manager.query_sparql("SELECT * WHERE { ?s ?p ?o }")

except OntologyNotLoadedError as e:
    print("Please load ontology first!")
    print("Aldı bılan ontologiyani júkleń!")
```

---

## Best Practices / Eń jaqsı tácriyбeler

### 1. Use Singleton Getter / Singleton getter-di qollanıw

✅ **Good / Jaqsı:**
```python
from src.core.ontology_manager import get_ontology_manager

manager = get_ontology_manager()
```

❌ **Avoid / Qollanbaý:**
```python
from src.core.ontology_manager import OntologyManager

manager = OntologyManager()  # Still works but less clear
```

### 2. Check Loading Status / Júklew statusın tekseriv

✅ **Good / Jaqsı:**
```python
if not manager.is_loaded():
    manager.load_ontology("path/to/ontology.owl")

# Now safe to query / Endi soraw qáwipsiz
results = manager.query_sparql(query)
```

### 3. Handle UTF-8 Properly / UTF-8-di tuwrı islew

✅ **Good / Jaqsı:**
```python
# Always use UTF-8 for Karakalpak text
# Qaraqalpaq tekst ushın árbir waqıt UTF-8 qollanıw

properties = {
    "title": "Jinayattıń awır túri",  # UTF-8 characters
    "language": "kaa"
}

manager.add_individual("Statiya", "Article_1", properties)
```

### 4. Use Try-Except / Try-Except qollanıw

✅ **Good / Jaqsı:**
```python
try:
    manager.load_ontology("ontology.owl")
    results = manager.query_sparql(query)
except OntologyManagerError as e:
    logger.error(f"Error: {e.message_kaa}")
    # Handle error / Qátelikti islew
```

### 5. Clear When Done / Bitkende tazalaw

✅ **Good / Jaqsı:**
```python
# When switching ontologies / Ontologiyalardı almaslırıwda
manager.clear()
manager.load_ontology("new_ontology.owl")
```

### 6. Use Language Filters / Til filtrlerin qollanıw

✅ **Good / Jaqsı:**
```python
# Always specify language for consistent results
# Uyǵın nátiyјeler ushın til-di árbir waqıt kórsetiw

articles_kaa = manager.get_instances("Statiya", lang="kaa")
articles_uz = manager.get_instances("Statiya", lang="uz")
```

---

## Performance Tips / Ónimdarlıq keńesleri

### 1. Cache Results / Nátiyјelerdi keshlaw

```python
# Cache frequently used data / Kóp qollanılatuǵın ma'lumotlardı keshlaw
class LegalDataCache:
    def __init__(self):
        self.manager = get_ontology_manager()
        self._crimes_cache = None

    def get_crimes(self, force_reload=False):
        if self._crimes_cache is None or force_reload:
            self._crimes_cache = self.manager.get_instances("Jinayat")
        return self._crimes_cache
```

### 2. Use Limits / Limitlerdi qollanıw

```python
# Don't load everything at once / Hámmeni bir waqıtta júklemew
crimes = manager.get_instances("Jinayat", limit=100)
```

### 3. Efficient SPARQL / Efektiv SPARQL

```python
# Use LIMIT and OFFSET / LIMIT ha'm OFFSET qollanıw
query = """
SELECT ?s ?p ?o
WHERE { ?s ?p ?o }
LIMIT 100
OFFSET 0
"""
```

---

## Troubleshooting / Qáteliklерdi sheshiv

### Problem: Encoding Errors / Kodlaw qátelikleri

```python
# Solution: Ensure UTF-8 / Sheshim: UTF-8-di tastıqlaw
import sys
print(sys.getdefaultencoding())  # Should be 'utf-8'

# On Windows / Windows-ta
# set PYTHONIOENCODING=utf-8
```

### Problem: Ontology Not Loading / Ontologiya júklenmeydi

```python
# Check file path / Fayl jolın tekseriv
from pathlib import Path

ontology_path = Path("data/ontologies/legal.owl")
if not ontology_path.exists():
    print(f"File not found: {ontology_path}")

# Check file format / Fayl formatın tekseriv
manager.load_ontology(ontology_path, format="xml")  # Try specific format
```

### Problem: SPARQL Query Fails / SPARQL soraw sátsiz

```python
# Debug query / Sorawdı debug etiw
import logging
logging.basicConfig(level=logging.DEBUG)

# Check query syntax / Soraw sintaksisı tekseriv
# Use SPARQL validator online
```

---

## Changelog / Ózgerister tарıхı

### Version 0.1.0
- Initial release / Birinshi shıǵarılıs
- Singleton pattern implementation / Singleton pattern implements
- Bilingual support (English, Karakalpak) / Eki tilli qollap-quwatlawish
- SPARQL query support / SPARQL soraw qollap-quwatlawish
- Owlready2 integration / Owlready2 integratsiya

---

## References / Anıqlamalar

- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [Owlready2 Documentation](https://owlready2.readthedocs.io/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [OWL 2 Web Ontology Language](https://www.w3.org/TR/owl2-overview/)

---

**Last Updated / Soń jańalanǵan:** 2024
**Version / Versiya:** 0.1.0
**Maintained by / Qollap-quwatlaýjı:** huquqAI Team
