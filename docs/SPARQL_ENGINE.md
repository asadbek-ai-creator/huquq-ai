# SPARQLEngine Documentation
# SPARQLEngine Dokumentaciyası

**Comprehensive guide to the SPARQL Query Engine for Karakalpak legal data**
**Qaraqalpaq huquqıy ma'limleri ushın SPARQL Soraw Mexanizmi boyınsha tóliq qollanba**

---

## Table of Contents / Mazmunı

1. [Overview / Kórinisi](#overview)
2. [Installation / Ornatıw](#installation)
3. [Quick Start / Tez baslaw](#quick-start)
4. [Core Features / Basqı funktsiyalar](#core-features)
5. [API Reference / API anıqlaması](#api-reference)
6. [Query Methods / Soraw metodları](#query-methods)
7. [Karakalpak-Specific Methods / Qaraqalpaq-maxsus metodlar](#karakalpak-specific-methods)
8. [Performance & Caching / Tabıslılıq ha'm keshlew](#performance-caching)
9. [Error Handling / Qáteliklerdi basqarıw](#error-handling)
10. [Examples / Misallar](#examples)
11. [Best Practices / Eń jaqsı táјiribeler](#best-practices)

---

## Overview / Kórinisi

The **SPARQLEngine** is a specialized query engine optimized for executing SPARQL queries on Karakalpak legal knowledge bases. It provides high-performance querying with built-in caching, validation, and Karakalpak language support.

**SPARQLEngine** - Qaraqalpaq huquqıy bilimler bazalarında SPARQL sorawların orınlaw ushın optimizaciyalanǵan maxsus soraw mexanizmi. Ol ichki keshlew, tastıqlaw ha'm Qaraqalpaq tili qollawı menen joqarı tabıslılıqtı soraw etiwdi úsinis etedi.

### Key Features / Basqı imkaniyatlar

- ✅ **SPARQL 1.1 Support** - Full support for SELECT, ASK, CONSTRUCT queries
- ✅ **Query Caching** - LRU cache for improved performance
- ✅ **Query Validation** - Syntax checking before execution
- ✅ **Karakalpak Optimized** - Special methods for legal queries
- ✅ **UTF-8 Support** - Full support for Karakalpak characters (ǵ, ń, ı, ú, ó)
- ✅ **Performance Monitoring** - Built-in statistics and timing
- ✅ **Type Conversion** - Automatic type conversion for query results
- ✅ **Fuzzy Search** - Tolerant search for typos

---

## Installation / Ornatıw

### Prerequisites / Aldın-ala talablar

```bash
# Python 3.8 or higher / Python 3.8 yaki joqarı
python --version

# Install dependencies / Baylanıslarni ornatıw
pip install -r requirements.txt
```

### Required Dependencies / Kerekli baylanıslar

```python
rdflib>=7.0.0          # RDF graph and SPARQL support
owlready2>=0.46        # OWL ontology support
```

---

## Quick Start / Tez baslaw

### Basic Usage / Baslanǵısh qollanıw

```python
from src.core.ontology_manager import get_ontology_manager
from src.core.sparql_engine import SPARQLEngine

# Load ontology / Ontologiyani júklew
manager = get_ontology_manager()
manager.load_ontology("data/ontologies/criminal_code.owl")

# Create SPARQL engine / SPARQL mexanizmin jasawiш
engine = SPARQLEngine(manager.graph)

# Execute a query / Sorawdı orınlaw
results = engine.select("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    SELECT ?jinayat ?label
    WHERE {
        ?jinayat a huquq:Jinayat .
        ?jinayat rdfs:label ?label .
        FILTER(LANG(?label) = "kaa")
    }
    LIMIT 10
""")

# Print results / Nátiyјelerin shıǵarıw
for result in results:
    print(f"{result['label']}: {result['jinayat']}")
```

---

## Core Features / Basqı funktsiyalar

### 1. Query Execution / Soraw orınlaw

The SPARQLEngine supports three types of SPARQL queries:

SPARQLEngine úsh túrli SPARQL sorawların qollaydı:

#### SELECT Queries

Returns tabular results as a list of dictionaries.

Tárepdegi nátiyјelerin lúǵatlardıń tizimi retinde qaytarıdı.

```python
results = engine.select("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10
""")
# Returns: [{'s': '...', 'p': '...', 'o': '...'}, ...]
```

#### ASK Queries

Returns a boolean indicating if the pattern exists.

Pattern bar ma joq ekenin kórsetiwshi boolean qaytarıdı.

```python
exists = engine.ask("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    ASK { ?s a huquq:Jinayat }
""")
# Returns: True or False
```

#### CONSTRUCT Queries

Builds a new RDF graph and returns it in the specified format.

Jańa RDF graf quriydı ha'm onı belgili formatda qaytarıdı.

```python
turtle_data = engine.construct("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    CONSTRUCT { ?s rdfs:label ?label }
    WHERE { ?s rdfs:label ?label }
""", format="turtle")
# Returns: RDF Turtle string
```

### 2. Query Validation / Soraw tastıqlaw

All queries are validated before execution to catch syntax errors early.

Sintaksis qátelerin irekte tabıw ushın barlıq sorawlar orınlawdan aldın tastıqlanıdı.

```python
# Invalid query will raise QueryValidationError
try:
    engine.select("INVALID SPARQL SYNTAX")
except QueryValidationError as e:
    print(f"Query error: {e.message}")
```

### 3. Language Support / Til qollawı

Automatic language filtering for multilingual content.

Kóp tilli mazmun ushın avtomatik til filtrlew.

```python
# Search in Karakalpak / Qaraqalpaqsha izlew
results = engine.select(query, lang="kaa")

# Search in English / Anglissha izlew
results = engine.select(query, lang="en")
```

### 4. Performance Monitoring / Tabıslılıq monitoriı

Built-in statistics tracking for optimization.

Optimizaciya ushın ichki statistika baqlaw.

```python
stats = engine.get_statistics()
print(f"Queries executed: {stats['queries_executed']}")
print(f"Average time: {stats['average_query_time']:.4f}s")
print(f"Cache hit rate: {stats['cache_hits']}/{stats['queries_executed']}")
```

---

## API Reference / API anıqlaması

### SPARQLEngine Class

```python
class SPARQLEngine:
    """
    SPARQL Query Engine optimized for Karakalpak legal content.
    Qaraqalpaq huquqıy mazmun ushın optimizaciyalanǵan SPARQL Soraw Mexanizmi.
    """
```

#### Constructor / Konstruktor

```python
def __init__(self, graph: Graph)
```

**Parameters / Parametrler:**
- `graph` (Graph): RDFLib Graph object containing the knowledge base

**Example / Misal:**
```python
from rdflib import Graph
from src.core.sparql_engine import SPARQLEngine

graph = Graph()
graph.parse("data/knowledge/legal_kb.ttl", format="turtle")
engine = SPARQLEngine(graph)
```

---

## Query Methods / Soraw metodları

### select()

Execute a SPARQL SELECT query and return results as dictionaries.

SPARQL SELECT sorawdı orınlaydı ha'm nátiyјelerin lúǵatlar retinde qaytarıdı.

```python
def select(
    self,
    query: str,
    lang: Optional[str] = "kaa"
) -> List[Dict[str, Any]]
```

**Parameters:**
- `query` (str): SPARQL SELECT query string
- `lang` (str, optional): Language code to replace %%LANG%% placeholder. Default: "kaa"

**Returns:** List of dictionaries with query results

**Raises:**
- `QueryValidationError`: If query syntax is invalid
- `SPARQLEngineError`: If execution fails

**Example:**
```python
query = """
    PREFIX huquq: <http://huquqai.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?jinayat ?label ?turi
    WHERE {
        ?jinayat a huquq:Jinayat .
        ?jinayat rdfs:label ?label .
        OPTIONAL { ?jinayat huquq:crimeType ?turi }
        FILTER(LANG(?label) = "%%LANG%%")
    }
    LIMIT 20
"""

results = engine.select(query, lang="kaa")

for result in results:
    print(f"Crime: {result['label']}")
    print(f"Type: {result.get('turi', 'N/A')}")
```

### ask()

Execute a SPARQL ASK query and return boolean result.

SPARQL ASK sorawdı orınlaydı ha'm boolean nátiyјeni qaytarıdı.

```python
def ask(self, query: str) -> bool
```

**Parameters:**
- `query` (str): SPARQL ASK query string

**Returns:** True if pattern exists, False otherwise

**Example:**
```python
# Check if theft crimes exist / Urılıq jinayatlardıń bar ekenin tastıqlaw
exists = engine.ask("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    ASK {
        ?crime a huquq:Jinayat .
        ?crime rdfs:label "Urılıq"@kaa .
    }
""")

if exists:
    print("Theft crimes found in knowledge base")
```

### construct()

Execute a SPARQL CONSTRUCT query and return RDF graph in specified format.

SPARQL CONSTRUCT sorawdı orınlaydı ha'm RDF grafti belgili formatda qaytarıdı.

```python
def construct(
    self,
    query: str,
    format: str = "turtle"
) -> str
```

**Parameters:**
- `query` (str): SPARQL CONSTRUCT query string
- `format` (str): Output format (turtle, xml, n3, nt). Default: "turtle"

**Returns:** Serialized RDF graph as string

**Example:**
```python
result = engine.construct("""
    PREFIX huquq: <http://huquqai.org/ontology#>
    CONSTRUCT {
        ?jinayat rdfs:label ?label .
        ?jinayat huquq:crimeType ?type .
    }
    WHERE {
        ?jinayat a huquq:Jinayat .
        ?jinayat rdfs:label ?label .
        OPTIONAL { ?jinayat huquq:crimeType ?type }
    }
""", format="turtle")

print(result)  # Turtle format RDF
```

---

## Karakalpak-Specific Methods / Qaraqalpaq-maxsus metodlar

These methods are optimized for common Karakalpak legal queries.

Bu metodlar kóp ushıramaytın Qaraqalpaq huquqıy sorawlar ushın optimizaciyalanǵan.

### search_by_term_kaa()

Search for resources by Karakalpak term with fuzzy matching support.

Anıq emes sáykeslik qollawı menen Qaraqalpaq termin boyınsha resurslarni izlew.

```python
def search_by_term_kaa(
    self,
    term: str,
    fuzzy: bool = False,
    limit: int = 10
) -> List[Dict[str, Any]]
```

**Parameters:**
- `term` (str): Karakalpak search term (e.g., "urılıq", "jinayat", "jaza")
- `fuzzy` (bool): Enable fuzzy matching for typos. Default: False
- `limit` (int): Maximum number of results. Default: 10

**Returns:** List of resources matching the term

**Example:**
```python
# Search for theft / Urılıq izlew
results = engine.search_by_term_kaa("urılıq", limit=5)

for result in results:
    print(f"Found: {result['label']}")
    print(f"URI: {result['resource']}")
    if result['comment']:
        print(f"Description: {result['comment']}")

# Fuzzy search with typo / Qáte menen anıq emes izlew
results = engine.search_by_term_kaa("uriliq", fuzzy=True)
```

### get_jaza_range()

Get punishments within a specified year range.

Belgili jıl diapazoni ishindegi jazalardı alıw.

```python
def get_jaza_range(
    self,
    min_jıl: Optional[int] = None,
    max_jıl: Optional[int] = None
) -> List[Dict[str, Any]]
```

**Parameters:**
- `min_jıl` (int, optional): Minimum years of punishment
- `max_jıl` (int, optional): Maximum years of punishment

**Returns:** List of punishments within the range

**Example:**
```python
# Light punishments (0-2 years) / Jeńil jazalar (0-2 jıl)
light = engine.get_jaza_range(min_jıl=0, max_jıl=2)

# Medium punishments (3-5 years) / Orta jazalar (3-5 jıl)
medium = engine.get_jaza_range(min_jıl=3, max_jıl=5)

# Severe punishments (5+ years) / Awır jazalar (5+ jıl)
severe = engine.get_jaza_range(min_jıl=5, max_jıl=None)

for punishment in severe:
    print(f"{punishment['label']}: {punishment['minYears']}-{punishment['maxYears']} years")
```

### search_jinayat_turi()

Search crimes by severity type (jeńil, orta, awır, óte awır).

Awırlıq túri boyınsha jinayatlardı izlew (jeńil, orta, awır, óte awır).

```python
def search_jinayat_turi(
    self,
    turi: str,
    limit: int = 20
) -> List[Dict[str, Any]]
```

**Parameters:**
- `turi` (str): Crime type - "jeńil", "orta", "awır", "óte awır"
- `limit` (int): Maximum results. Default: 20

**Returns:** List of crimes of specified type

**Example:**
```python
# Find all light crimes / Barlıq jeńil jinayatlardı tabıw
light_crimes = engine.search_jinayat_turi("jeńil")

# Find severe crimes / Awır jinayatlardı tabıw
severe_crimes = engine.search_jinayat_turi("awır", limit=10)

for crime in severe_crimes:
    print(f"Crime: {crime['label']}")
    print(f"Type: {crime['crimeType']}")
    print(f"URI: {crime['jinayat']}")
```

**Crime Types / Jinayat túrleri:**
- `"jeńil"` - Light crime (up to 2 years)
- `"orta"` - Medium crime (2-5 years)
- `"awır"` - Severe crime (5-15 years)
- `"óte awır"` - Very severe crime (15+ years)

### search_statiya()

Search legal articles by number or code type.

Nomer yaki kodeks túri boyınsha huquqıy statiyalardı izlew.

```python
def search_statiya(
    self,
    nomer: Optional[str] = None,
    kodeks: Optional[str] = None
) -> List[Dict[str, Any]]
```

**Parameters:**
- `nomer` (str, optional): Article number (e.g., "123", "456")
- `kodeks` (str, optional): Code type (e.g., "JK", "AK", "ShK")

**Returns:** List of matching articles

**Example:**
```python
# Find specific article / Belgili statiyani tabıw
article = engine.search_statiya(nomer="123")

# Find all Criminal Code articles / Barlıq Jinayat Kodeksi statiyalarin tabıw
jk_articles = engine.search_statiya(kodeks="JK")

# Find article 456 from Administrative Code
article_456 = engine.search_statiya(nomer="456", kodeks="AK")

for art in jk_articles:
    print(f"Article {art['articleNumber']}: {art['label']}")
    print(f"Code: {art['codeType']}")
```

**Code Types / Kodeks túrleri:**
- `"JK"` - Jinayat Kodeksi (Criminal Code)
- `"AK"` - Administrativlik Kodeksi (Administrative Code)
- `"ShK"` - Shıwıllıq Kodeksi (Civil Code)

### get_related_jinayat_jaza()

Get crime and its related punishments.

Jinayat ha'm oǵan baylanıslı jazalardı alıw.

```python
def get_related_jinayat_jaza(
    self,
    jinayat_uri: str
) -> List[Dict[str, Any]]
```

**Parameters:**
- `jinayat_uri` (str): URI of the crime

**Returns:** List with crime and punishment information

**Example:**
```python
crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
relations = engine.get_related_jinayat_jaza(crime_uri)

for rel in relations:
    print(f"Crime: {rel['jinayatLabel']}")
    print(f"Punishment: {rel['jazaLabel']}")
    print(f"Crime URI: {rel['jinayat']}")
    print(f"Punishment URI: {rel['jaza']}")
```

---

## Performance & Caching / Tabıslılıq ha'm keshlew

### Query Caching / Soraw keshlew

The SPARQLEngine uses LRU (Least Recently Used) caching to improve performance for repeated queries.

SPARQLEngine qayta-qayta orınlanıwshı sorawlar ushın tabıslılıqtı jaqsılawı ushın LRU (eń keyin qollanılǵan) keshlew qollanıdı.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def execute_cached(
    self,
    query: str,
    query_type: str = "select"
) -> Union[List[Dict], bool, str]
```

**Example:**
```python
# First execution - queries the graph / Birinshi orınlaw - graftan soraydı
result1 = engine.execute_cached(query, query_type="select")

# Second execution - returns from cache / Ekinshi orınlaw - keshten qaytarıdı
result2 = engine.execute_cached(query, query_type="select")

# Results are identical but second is much faster
# Nátiyјeler birday, biraq ekinshisi ansha tez
```

### Clearing Cache / Keshti tazalaw

```python
def clear_cache(self) -> None:
    """Clear the query cache / Soraw keshtin tazalaw"""

engine.clear_cache()
print("Cache cleared / Kesh tazalandı")
```

### Statistics / Statistika

Track query performance and cache effectiveness.

Soraw tabıslılıǵın ha'm kesh nátiyjeligin baqlaw.

```python
def get_statistics(self) -> Dict[str, Any]

stats = engine.get_statistics()

print(f"Total queries: {stats['queries_executed']}")
print(f"Cache hits: {stats['cache_hits']}")
print(f"Cache misses: {stats['cache_misses']}")
print(f"Total execution time: {stats['total_execution_time']:.4f}s")
print(f"Average query time: {stats['average_query_time']:.4f}s")

# Calculate cache hit rate / Kesh tabıslılıq kórsetkishin esaplaw
if stats['queries_executed'] > 0:
    hit_rate = (stats['cache_hits'] / stats['queries_executed']) * 100
    print(f"Cache hit rate: {hit_rate:.1f}%")
```

---

## Error Handling / Qáteliklerdi basqarıw

### Exception Classes / Istisna klassları

```python
class SPARQLEngineError(Exception):
    """Base exception for SPARQL engine errors"""

class QueryValidationError(SPARQLEngineError):
    """Raised when query validation fails"""
```

### Handling Errors / Qáteliklerdi basqarıw

```python
from src.core.sparql_engine import SPARQLEngine, SPARQLEngineError, QueryValidationError

try:
    results = engine.select(query)
except QueryValidationError as e:
    print(f"Invalid query syntax: {e.message}")
    print(f"Qaraqalpaqsha: {e.message_kaa}")
except SPARQLEngineError as e:
    print(f"Engine error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Examples / Misallar

### Example 1: Find All Crimes / Barlıq jinayatlardı tabıw

```python
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
ORDER BY ?label
"""

crimes = engine.select(query, lang="kaa")

print(f"Found {len(crimes)} crimes\n")
for crime in crimes:
    print(f"- {crime['label']} (Type: {crime.get('turi', 'N/A')})")
```

### Example 2: Search with Fuzzy Matching / Anıq emes sáykeslik menen izlew

```python
# User might have typos / Paydalanıwshıda qáteler bolıwı múmkin
search_term = "uriliq"  # Correct: "urılıq"

# Normal search may not find results / Qálegelik izlew nátiyјe bermewi múmkin
normal = engine.search_by_term_kaa(search_term, fuzzy=False)
print(f"Normal search: {len(normal)} results")

# Fuzzy search is more tolerant / Anıq emes izlew kóbirek tolerantlı
fuzzy = engine.search_by_term_kaa(search_term, fuzzy=True)
print(f"Fuzzy search: {len(fuzzy)} results")

for result in fuzzy:
    print(f"  - {result['label']}")
```

### Example 3: Filter by Punishment Duration / Jaza uzaqlıǵı boyınsha filtrlew

```python
# Short punishments (good for rehabilitation programs)
short = engine.get_jaza_range(min_jıl=0, max_jıl=2)

# Long punishments (serious crimes)
long = engine.get_jaza_range(min_jıl=10, max_jıl=None)

print(f"Short punishments: {len(short)}")
print(f"Long punishments: {len(long)}")
```

### Example 4: Complex Query with Relations / Baylanıslar menen múrekkeb soraw

```python
# Find crimes with their punishments and articles
query = """
PREFIX huquq: <http://huquqai.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?jinayat ?jinayatLabel ?jaza ?jazaLabel ?statiya
WHERE {
    ?jinayat a huquq:Jinayat ;
             rdfs:label ?jinayatLabel .
    OPTIONAL {
        ?jinayat huquq:hasPunishment ?jaza .
        ?jaza rdfs:label ?jazaLabel .
    }
    OPTIONAL {
        ?jinayat huquq:definedInArticle ?statiya .
    }
    FILTER(LANG(?jinayatLabel) = "kaa")
}
LIMIT 20
"""

results = engine.select(query)

for r in results:
    print(f"Crime: {r['jinayatLabel']}")
    if 'jazaLabel' in r:
        print(f"  Punishment: {r['jazaLabel']}")
    if 'statiya' in r:
        print(f"  Article: {r['statiya']}")
```

---

## Best Practices / Eń jaqsı táјiribeler

### 1. Use Language Placeholders / Til órnin alıwshılardı qollanıń

```python
# Good / Jaqsı
query = """
SELECT ?s ?label
WHERE {
    ?s rdfs:label ?label .
    FILTER(LANG(?label) = "%%LANG%%")
}
"""
results = engine.select(query, lang="kaa")

# Bad / Naqıs
query = """
SELECT ?s ?label
WHERE {
    ?s rdfs:label ?label .
    FILTER(LANG(?label) = "kaa")
}
"""
```

### 2. Use LIMIT for Large Datasets / Úlken ma'limatlar toplamları ushın LIMIT qollanıń

```python
# Good / Jaqsı
query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 100"

# Bad / Naqıs - may return millions of results
query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
```

### 3. Leverage Caching / Keshlewdi qollanıń

```python
# For repeated queries, use execute_cached
# Qayta-qayta sorawlar ushın execute_cached qollanıń
result = engine.execute_cached(query, query_type="select")
```

### 4. Handle Optional Fields / Opsional órislerdi basqarıń

```python
# Always use .get() for optional fields
# Opsional órisler ushın hámiyjese .get() qollanıń

for result in results:
    label = result.get('label', 'No label')  # Good
    # label = result['label']  # Bad - may raise KeyError
```

### 5. Use Specific Methods / Anıq metodlardı qollanıń

```python
# Good / Jaqsı - use specialized method
crimes = engine.search_jinayat_turi("awır")

# Less efficient / Nátiyjeli emes - manual query
crimes = engine.select("""
    SELECT ?j WHERE {
        ?j huquq:crimeType "awır"
    }
""")
```

### 6. Validate Input / Kirislewdi tastıqlan

```python
# Validate crime types before querying
valid_types = ["jeńil", "orta", "awır", "óte awır"]

turi = user_input.strip().lower()
if turi not in valid_types:
    print(f"Invalid crime type. Must be one of: {', '.join(valid_types)}")
else:
    results = engine.search_jinayat_turi(turi)
```

### 7. Monitor Performance / Tabıslılıqtı monitoriń

```python
import time

start = time.time()
results = engine.select(query)
duration = time.time() - start

print(f"Query returned {len(results)} results in {duration:.4f}s")

# Check statistics periodically
stats = engine.get_statistics()
if stats['average_query_time'] > 1.0:
    print("Warning: Queries are slow, consider optimization")
```

---

## Troubleshooting / Máselelerni sheshiw

### Common Issues / Kóp ushıramaytın máseler

#### Issue 1: QueryValidationError

**Problem:** Query syntax is invalid

**Solution:**
```python
# Check query syntax carefully
# Use PREFIX declarations for all namespaces
# Ensure proper SPARQL 1.1 syntax

query = """
PREFIX huquq: <http://huquqai.org/ontology#>  # Required
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?s WHERE {
    ?s a huquq:Jinayat .
}
"""
```

#### Issue 2: Empty Results

**Problem:** Query returns no results

**Solution:**
```python
# Check if data exists
exists = engine.ask("ASK { ?s ?p ?o }")
if not exists:
    print("Knowledge base is empty!")

# Verify namespace URIs match your ontology
# Use broader queries first to debug
```

#### Issue 3: UTF-8 Encoding Errors

**Problem:** Karakalpak characters not displaying correctly

**Solution:**
```python
# Ensure UTF-8 encoding in source files
# -*- coding: utf-8 -*-

# On Windows, set console encoding
import sys
if sys.platform == 'win32':
    import os
    os.system('chcp 65001')
```

#### Issue 4: Slow Queries

**Problem:** Queries take too long

**Solution:**
```python
# 1. Use LIMIT clause
query = query + " LIMIT 100"

# 2. Use caching for repeated queries
result = engine.execute_cached(query)

# 3. Add indices (RDFLib limitation)
# Consider using a triple store like Apache Jena for large datasets

# 4. Use specific properties instead of ?p
# Bad: ?s ?p ?o
# Good: ?s rdfs:label ?label
```

---

## Performance Tips / Tabıslılıq keńesleri

1. **Use Indexed Properties** - Query specific properties rather than `?p`
2. **Enable Caching** - Use `execute_cached()` for repeated queries
3. **Limit Results** - Always use `LIMIT` clause for large datasets
4. **Specific Filters** - Use FILTER early in the query
5. **Monitor Statistics** - Check `get_statistics()` regularly

---

## Additional Resources / Qosımsha resurslar

- **SPARQL 1.1 Specification**: https://www.w3.org/TR/sparql11-query/
- **RDFLib Documentation**: https://rdflib.readthedocs.io/
- **OWL 2 Primer**: https://www.w3.org/TR/owl2-primer/

---

## Support / Qollawıw

For issues and questions:
Máseler ha'm sorawlar ushın:

- GitHub Issues: https://github.com/yourusername/huquqAI/issues
- Documentation: `docs/`
- Examples: `examples/sparql_usage.py`

---

**Version / Versiya:** 1.0.0
**Last Updated / Sońǵı jańalawıw:** 2024
**License / Licenziya:** MIT
