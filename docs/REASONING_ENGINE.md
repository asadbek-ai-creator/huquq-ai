# ReasoningEngine Documentation
# ReasoningEngine Dokumentaciyası

**Comprehensive guide to the OWL Reasoning Engine for Karakalpak legal data**
**Qaraqalpaq huquqıy ma'limleri ushın OWL Mántıqlı Juwmaq Mexanizmi boyınsha tóliq qollanba**

---

## Table of Contents / Mazmunı

1. [Overview / Kórinisi](#overview)
2. [Installation / Ornatıw](#installation)
3. [Quick Start / Tez baslaw](#quick-start)
4. [Core Concepts / Basqı túsiniler](#core-concepts)
5. [API Reference / API anıqlaması](#api-reference)
6. [Reasoning Methods / Mántıqlı juwmaq metodları](#reasoning-methods)
7. [Karakalpak Legal Reasoning / Qaraqalpaq huquqıy mántıq juwmaǵı](#karakalpak-legal-reasoning)
8. [Supported Reasoners / Qollaw kórsetilgen mántıq juwmaqshılar](#supported-reasoners)
9. [Inference Explanations / Qorıtındı túsindirmeleri](#inference-explanations)
10. [Error Handling / Qáteliklerdi basqarıw](#error-handling)
11. [Examples / Misallar](#examples)
12. [Best Practices / Eń jaqsı táјiribeler](#best-practices)

---

## Overview / Kórinisi

The **ReasoningEngine** provides automated reasoning capabilities for OWL ontologies containing Karakalpak legal data. It uses state-of-the-art reasoners (Pellet, HermiT) to infer new facts, check consistency, and validate legal knowledge.

**ReasoningEngine** - Qaraqalpaq huquqıy ma'limlerin qamtıǵan OWL ontologiyalar ushın avtomatik mántıqlı juwmaq imkaniyatlarin beredi. Ol jańa faktlardı qorıtındılaw, úyelislikti tastıqlaw ha'm huquqıy bilimlerdi tastıqlaw ushın zaman talabına sáykes mántıq juwmaqshılarni (Pellet, HermiT) qollanadı.

### Key Features / Basqı imkaniyatlar

- ✅ **Consistency Checking** - Detect logical contradictions in legal ontologies
- ✅ **Classification Reasoning** - Automatically classify individuals into classes
- ✅ **Fact Inference** - Derive new facts from existing knowledge
- ✅ **Property Validation** - Validate data properties and constraints
- ✅ **Karakalpak Legal Rules** - Specialized reasoning for Karakalpak law
- ✅ **Crime Severity Classification** - Classify crimes by punishment duration
- ✅ **Punishment Type Inference** - Infer punishment types from properties
- ✅ **Law Consistency Validation** - Check legal document integrity
- ✅ **Inference Explanations** - Explain why facts were inferred
- ✅ **Multiple Reasoners** - Support for Pellet and HermiT

---

## Installation / Ornatıw

### Prerequisites / Aldın-ala talablar

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

### Required Dependencies / Kerekli baylanıslar

```python
owlready2>=0.46        # OWL ontology and reasoning
rdflib>=7.0.0          # RDF graph manipulation
```

### Java Requirement / Java talabı

The reasoners (Pellet, HermiT) require Java to be installed:

Mántıq juwmaqshılar (Pellet, HermiT) Java-nıń ornalıwın talap etedi:

```bash
# Check Java installation
java -version

# Java 8 or higher is required
# Java 8 yaki joqarı versiya kerek
```

---

## Quick Start / Tez baslaw

### Basic Usage / Baslanǵısh qollanıw

```python
from src.core.reasoning_engine import create_reasoning_engine, ReasonerType

# Create reasoning engine / Mántıqlı juwmaq mexanizmin jasawıш
engine = create_reasoning_engine(
    "data/ontologies/criminal_code.owl",
    reasoner=ReasonerType.PELLET
)

# Check consistency / Úyelislikti tastıqlaw
is_consistent = engine.check_consistency()
print(f"Ontology is consistent: {is_consistent}")

# Classify crimes by severity / Jinayatlardı awırlıǵı boyınsha klassifikaciyalaw
crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
severity = engine.classify_jinayat_awırlıǵı(crime_uri)
print(f"Crime severity: {severity.value}")

# Infer punishment type / Jaza túrin qorıtındılaw
punishment_uri = "http://huquqai.org/ontology#Jaza_Urılıq"
pun_type = engine.infer_jaza_turi(punishment_uri)
print(f"Punishment type: {pun_type.value}")
```

---

## Core Concepts / Basqı túsiniler

### 1. Consistency Checking / Úyelislik Tastıqlaw

Consistency checking ensures that the ontology contains no logical contradictions.

Úyelislik tastıqlaw ontologiyada logikalıq qarama-qarsılıqlar joqlıǵın qámlep beredi.

**What is checked / Ne tastıqlanadı:**
- No individual belongs to disjoint classes
- All property restrictions are satisfied
- No conflicting data type assertions
- All cardinality constraints are met

**Example inconsistency / Úyelisliksizlik misalı:**
```turtle
# This is inconsistent / Bu úyelislikke sáykes kelmeydi:
:Crime1 a :Jinayat, :Jaza .  # Crime and Punishment are disjoint
```

### 2. Classification Reasoning / Klassifikaciya Mántıq Juwmaǵı

Classification infers class membership based on properties and restrictions.

Klassifikaciya xassalar ha'm shekler negizinde klass agzalıǵın qorıtındılaydı.

**How it works / Qanday isleydi:**
1. Reasoner examines all property values
2. Checks which class restrictions are satisfied
3. Automatically assigns individuals to classes
4. Infers subclass relationships

**Example / Misal:**
```turtle
# If a crime has punishment > 10 years
# Eger jinayattıń jazası 10 jıldan kóp bolsa

:Jinayat_X :hasPunishment :Jaza_X .
:Jaza_X :maxYears 12 .

# Reasoner infers / Mántıq juwmaqshı qorıtındılaydı:
:Jinayat_X a :AwırJinayat .  # Severe crime
```

### 3. Fact Inference / Fakt Qorıtındılawı

Inference derives new facts from existing knowledge using rules.

Qorıtındılaw bar bilimlerd qáǵıydalar arqalı jańa faktlardı shıǵarıdı.

**Inference types / Qorıtındılaw túrleri:**
- Property value inference
- Class membership inference
- Relationship inference
- Transitive property inference

---

## API Reference / API anıqlaması

### ReasoningEngine Class

```python
class ReasoningEngine:
    """
    OWL Reasoning Engine for Karakalpak Legal Knowledge Base.
    Qaraqalpaq Huquqıy Bilimler Bazası ushın OWL Mántıqlı Juwmaq Mexanizmi.
    """
```

#### Constructor / Konstruktor

```python
def __init__(
    self,
    graph: Optional[Graph] = None,
    ontology_path: Optional[Union[str, Path]] = None,
    reasoner: ReasonerType = ReasonerType.PELLET
)
```

**Parameters:**
- `graph` (Graph, optional): RDFLib Graph object
- `ontology_path` (str|Path, optional): Path to OWL ontology file
- `reasoner` (ReasonerType): Reasoner type (PELLET or HERMIT)

**Example:**
```python
# With ontology file / Ontologiya faylı menen
engine = ReasoningEngine(
    ontology_path="data/ontologies/criminal_code.owl",
    reasoner=ReasonerType.PELLET
)

# With RDF graph / RDF graf menen
from src.core.ontology_manager import get_ontology_manager
manager = get_ontology_manager()
manager.load_ontology("data/ontologies/criminal_code.owl")
engine = ReasoningEngine(graph=manager.graph)
```

---

## Reasoning Methods / Mántıqlı Juwmaq Metodları

### check_consistency()

Check if the ontology is logically consistent.

Ontologiyadan logikalıq úyelisli ekenin tastıqlaw.

```python
def check_consistency(self) -> bool
```

**Returns:** `True` if consistent, `False` if inconsistencies found

**Raises:**
- `ConsistencyError`: If consistency check fails

**Example:**
```python
try:
    is_consistent = engine.check_consistency()

    if is_consistent:
        print("✓ No contradictions found / Qarama-qarsılıqlar joq")
    else:
        print("✗ Ontology is inconsistent / Ontologiya úyelislikke sáykes kelmeydi")

except ConsistencyError as e:
    print(f"Check failed: {e.message_kaa}")
```

**Performance Note:**
Consistency checking can be computationally expensive for large ontologies. Use caching strategies for production systems.

### classify()

Perform classification reasoning to infer class memberships.

Klass agzalıǵın qorıtındılaw ushın klassifikaciya mántıq juwmaǵın orınlaw.

```python
def classify(self, explain: bool = False) -> ReasoningResult
```

**Parameters:**
- `explain` (bool): Include explanations for inferences

**Returns:** `ReasoningResult` with inferred class memberships

**Example:**
```python
result = engine.classify(explain=True)

print(f"Success: {result.success}")
print(f"Inferences: {len(result.inferences)}")
print(f"Time: {result.execution_time:.4f}s")

for inference in result.inferences:
    print(f"{inference['individual']} → {inference['class']}")

for explanation in result.explanations:
    print(f"Explanation: {explanation}")
```

**ReasoningResult Structure:**
```python
@dataclass
class ReasoningResult:
    success: bool                  # Operation succeeded
    inferences: List[Dict]         # Inferred facts
    inconsistencies: List[str]     # Found inconsistencies
    explanations: List[str]        # Inference explanations
    execution_time: float          # Time taken (seconds)
    reasoner_type: str            # Reasoner used
```

### infer_facts()

Infer new facts based on ontology axioms.

Ontologiya aksiomalar negizinde jańa faktlardı qorıtındılaw.

```python
def infer_facts(self, rules: Optional[List[str]] = None) -> ReasoningResult
```

**Parameters:**
- `rules` (List[str], optional): SWRL rules to apply (future feature)

**Returns:** `ReasoningResult` with inferred facts

**Example:**
```python
result = engine.infer_facts()

print(f"Inferred {len(result.inferences)} new facts")

for inf in result.inferences:
    print(f"New fact: {inf}")
```

---

## Karakalpak Legal Reasoning / Qaraqalpaq Huquqıy Mántıq Juwmaǵı

### classify_jinayat_awırlıǵı()

Classify crime severity based on punishment duration.

Jaza uzaqlıǵı negizinde jinayat awırlıǵın klassifikaciyalaw.

```python
def classify_jinayat_awırlıǵı(
    self,
    jinayat_uri: str
) -> Optional[JinayatAwırlıǵı]
```

**Parameters:**
- `jinayat_uri` (str): URI of the crime to classify

**Returns:** `JinayatAwırlıǵı` enum value or `None`

**Classification Rules / Klassifikaciya Qáǵıydaları:**

| Duration | Severity | Karakalpak |
|----------|----------|------------|
| 0-2 years | Light | jeńil |
| 2-5 years | Medium | orta |
| 5-15 years | Severe | awır |
| 15+ years | Very Severe | óte awır |

**Example:**
```python
crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
severity = engine.classify_jinayat_awırlıǵı(crime_uri)

if severity:
    print(f"Crime severity: {severity.value}")

    # Map to description
    descriptions = {
        JinayatAwırlıǵı.JENIL: "Light crime (0-2 years) / Jeńil jinayat (0-2 jıl)",
        JinayatAwırlıǵı.ORTA: "Medium crime (2-5 years) / Orta jinayat (2-5 jıl)",
        JinayatAwırlıǵı.AWIR: "Severe crime (5-15 years) / Awır jinayat (5-15 jıl)",
        JinayatAwırlıǵı.OTE_AWIR: "Very severe (15+ years) / Óte awır (15+ jıl)",
    }

    print(descriptions[severity])
else:
    print("Cannot classify / Klassifikaciyalaw múmkin emes")
```

**JinayatAwırlıǵı Enum:**
```python
class JinayatAwırlıǵı(Enum):
    JENIL = "jeńil"        # Light crime
    ORTA = "orta"          # Medium crime
    AWIR = "awır"          # Severe crime
    OTE_AWIR = "óte awır"  # Very severe crime
```

### infer_jaza_turi()

Infer punishment type from properties.

Xassalardan jaza túrin qorıtındılaw.

```python
def infer_jaza_turi(
    self,
    jaza_uri: str
) -> Optional[JazaTuri]
```

**Parameters:**
- `jaza_uri` (str): URI of the punishment

**Returns:** `JazaTuri` enum value or `None`

**Inference Rules / Qorıtındılaw Qáǵıydaları:**

```python
# Rule 1: Zero duration → Fine / Qáǵıyda 1: Nol uzaqlıq → Jarıma
if minYears == 0 and maxYears == 0:
    → JazaTuri.JARIMA

# Rule 2: Conditional flag → Conditional sentence / Qáǵıyda 2: Shartı belgisi → Shartı jaza
if conditional == True:
    → JazaTuri.SHARTI_JAZA

# Rule 3: Labor flag → Compulsory labor / Qáǵıyda 3: Jumıs belgisi → Shimeli jumıs
if compulsoryLabor == True:
    → JazaTuri.SHIMELI_JUMIS

# Rule 4: Has duration → Imprisonment / Qáǵıyda 4: Uzaqlıq bar → Azatlıqtan ayırıw
if minYears > 0:
    → JazaTuri.AZATLIQTAN_AYIRIW
```

**Example:**
```python
jaza_uri = "http://huquqai.org/ontology#Jaza_Shartı"
pun_type = engine.infer_jaza_turi(jaza_uri)

if pun_type:
    # Map to bilingual description
    descriptions = {
        JazaTuri.JARIMA: "Fine / Jarıma - Puldı tólaw",
        JazaTuri.SHARTI_JAZA: "Conditional / Shartı jaza - Erkin, biraq qadaǵalawda",
        JazaTuri.SHIMELI_JUMIS: "Compulsory Labor / Shimeli jumıs - Májburiy jumıs",
        JazaTuri.AZATLIQTAN_AYIRIW: "Imprisonment / Azatlıqtan ayırıw - Apsanada",
    }

    print(descriptions[pun_type])
```

**JazaTuri Enum:**
```python
class JazaTuri(Enum):
    JARIMA = "jarıma"                    # Fine
    AZATLIQTAN_AYIRIW = "azatlıqtan ayırıw"  # Imprisonment
    SHIMELI_JUMIS = "shimeli jumıs"      # Compulsory labor
    ERTE_JIBERILIW = "erte jiberiliw"    # Early release
    SHARTI_JAZA = "shartı jaza"          # Conditional sentence
```

### check_nızam_consistency()

Check consistency of a law (nızam) document.

Nızam dokumentiniń úyelisligin tastıqlaw.

```python
def check_nızam_consistency(
    self,
    nızam_uri: str
) -> Tuple[bool, List[str]]
```

**Parameters:**
- `nızam_uri` (str): URI of the law to check

**Returns:** Tuple of (is_consistent, list_of_issues)

**Validation Checks / Tastıqlaw Tekseriwleri:**

1. **Label Check** - Law must have `rdfs:label`
2. **Language Check** - Must have Karakalpak (kaa) label
3. **Date Check** - Must have effective date
4. **Article Check** - Referenced articles must exist
5. **Uniqueness Check** - Article numbers must be unique

**Example:**
```python
nızam_uri = "http://huquqai.org/ontology#Nızam_JinayatKodeksi"
is_consistent, issues = engine.check_nızam_consistency(nızam_uri)

if is_consistent:
    print("✓ Law is valid / Nızam járamlı")
else:
    print(f"✗ Found {len(issues)} issues:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
```

**Common Issues / Kóp ushıramaytın máseler:**
```python
# Missing label
"Law missing rdfs:label / Nızamda rdfs:label joq"

# Missing Karakalpak label
"Law missing Karakalpak (kaa) label / Nızamda Qaraqalpaq (kaa) label joq"

# Missing effective date
"Law missing effective date / Nızamda kúsh kirisiw sánesi joq"

# Invalid article reference
"Referenced article not found: <URI> / Siltelme jasalǵan statiya tabılmadı: <URI>"

# Duplicate article numbers
"Duplicate article numbers found: {123, 456} / Qaytalanıwshı statiya nomerleri: {123, 456}"
```

---

## Supported Reasoners / Qollaw Kórsetilgen Mántıq Juwmaqshılar

### Pellet Reasoner

**Advantages / Artıqshılıqları:**
- Complete OWL 2 DL support
- Fast for most queries
- Good error messages
- Stable and well-tested

**Use when / Qashanda qollanıw:**
- Standard legal ontologies
- Need complete OWL 2 DL reasoning
- Production systems

**Example:**
```python
engine = create_reasoning_engine(
    "data/ontologies/criminal_code.owl",
    reasoner=ReasonerType.PELLET
)
```

### HermiT Reasoner

**Advantages / Artıqshılıqları:**
- Very accurate reasoning
- Handles complex ontologies
- Good for debugging

**Use when / Qashanda qollanıw:**
- Complex class hierarchies
- Need high accuracy
- Debugging ontology issues

**Example:**
```python
engine = create_reasoning_engine(
    "data/ontologies/criminal_code.owl",
    reasoner=ReasonerType.HERMIT
)
```

### Comparison / Salıstırıw

```python
# Compare reasoner performance
import time

reasoners = [ReasonerType.PELLET, ReasonerType.HERMIT]

for reasoner in reasoners:
    engine = create_reasoning_engine(ontology_path, reasoner)

    start = time.time()
    engine.check_consistency()
    duration = time.time() - start

    print(f"{reasoner.value}: {duration:.4f}s")
```

---

## Inference Explanations / Qorıtındı Túsindirmeleri

### explain_inference()

Get explanation for an inferred fact.

Qorıtındılanǵan fakt ushın túsindirme alıw.

```python
def explain_inference(
    self,
    subject: str,
    predicate: str,
    obj: str
) -> Optional[InferenceExplanation]
```

**Returns:** `InferenceExplanation` object with bilingual explanations

**InferenceExplanation Structure:**
```python
@dataclass
class InferenceExplanation:
    subject: str           # Subject URI
    predicate: str         # Predicate URI
    object: str           # Object value
    rule: str             # Rule name
    explanation_en: str   # English explanation
    explanation_kaa: str  # Karakalpak explanation
    confidence: float     # Confidence (0.0-1.0)
```

**Example:**
```python
# Make an inference
crime_uri = "http://huquqai.org/ontology#Jinayat_Urılıq"
severity = engine.classify_jinayat_awırlıǵı(crime_uri)

# Explain it
explanation = engine.explain_inference(
    crime_uri,
    "http://huquqai.org/ontology#crimeType",
    severity.value
)

if explanation:
    print(f"Rule: {explanation.rule}")
    print(f"\nEnglish: {explanation.explanation_en}")
    print(f"\nQaraqalpaqsha: {explanation.explanation_kaa}")
    print(f"\nConfidence: {explanation.confidence * 100:.0f}%")
```

### get_all_inferences()

Get all inferred facts.

Barlıq qorıtındılanǵan faktlardı alıw.

```python
def get_all_inferences(self) -> List[Tuple[str, str, str]]
```

**Returns:** List of (subject, predicate, object) triples

**Example:**
```python
inferences = engine.get_all_inferences()

print(f"Total inferences: {len(inferences)}")

for subj, pred, obj in inferences:
    print(f"{subj} → {pred} → {obj}")
```

---

## Error Handling / Qáteliklerdi Basqarıw

### Exception Hierarchy / Istisna İerarxiyası

```python
ReasoningEngineError          # Base exception / Baslanǵısh istisna
├── ConsistencyError          # Consistency check failed
├── ClassificationError       # Classification failed
└── InferenceError           # Inference failed
```

### Exception Handling / İstisna Basqarıw

```python
from src.core.reasoning_engine import (
    ReasoningEngineError,
    ConsistencyError,
    ClassificationError,
    InferenceError
)

try:
    engine = create_reasoning_engine("data/ontologies/criminal_code.owl")
    is_consistent = engine.check_consistency()
    result = engine.classify()

except ConsistencyError as e:
    print(f"Consistency error: {e.message}")
    print(f"Qaraqalpaqsha: {e.message_kaa}")

except ClassificationError as e:
    print(f"Classification error: {e.message}")

except InferenceError as e:
    print(f"Inference error: {e.message}")

except ReasoningEngineError as e:
    print(f"General reasoning error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Examples / Misallar

### Example 1: Full Reasoning Workflow

```python
from src.core.reasoning_engine import create_reasoning_engine, ReasonerType

# Create engine / Mexanizm yasawıш
engine = create_reasoning_engine(
    "data/ontologies/criminal_code.owl",
    reasoner=ReasonerType.PELLET
)

# Step 1: Check consistency / 1-qádem: Úyelislikti tastıqlaw
print("Checking consistency...")
is_consistent = engine.check_consistency()
print(f"Consistent: {is_consistent}\n")

# Step 2: Classify ontology / 2-qádem: Ontologiyani klassifikaciyalaw
print("Classifying ontology...")
result = engine.classify(explain=True)
print(f"Made {len(result.inferences)} inferences\n")

# Step 3: Classify crimes / 3-qádem: Jinayatlardı klassifikaciyalaw
print("Classifying crimes by severity...")
crimes = [
    "http://huquqai.org/ontology#Jinayat_Urılıq",
    "http://huquqai.org/ontology#Jinayat_Awır",
]

for crime_uri in crimes:
    severity = engine.classify_jinayat_awırlıǵı(crime_uri)
    print(f"  {crime_uri.split('#')[1]}: {severity.value}")

# Step 4: Get statistics / 4-qádem: Statistikani alıw
print("\nStatistics:")
stats = engine.get_statistics()
print(f"  Reasoning runs: {stats['reasoning_runs']}")
print(f"  Inferences made: {stats['inferences_made']}")
print(f"  Total time: {stats['total_reasoning_time']:.4f}s")
```

### Example 2: Batch Crime Classification

```python
# Classify all crimes in ontology
from rdflib import Namespace

huquq = Namespace("http://huquqai.org/ontology#")

# Get all crimes
crimes = list(engine.graph.subjects(
    predicate=RDF.type,
    object=huquq.Jinayat
))

# Classify each
results = {}
for crime_uri in crimes:
    severity = engine.classify_jinayat_awırlıǵı(str(crime_uri))
    if severity:
        results[crime_uri] = severity

# Group by severity
from collections import defaultdict
grouped = defaultdict(list)

for uri, severity in results.items():
    grouped[severity].append(uri)

# Print summary
for severity in [JinayatAwırlıǵı.JENIL, JinayatAwırlıǵı.ORTA,
                 JinayatAwırlıǵı.AWIR, JinayatAwırlıǵı.OTE_AWIR]:
    count = len(grouped[severity])
    print(f"{severity.value}: {count} crimes")
```

---

## Best Practices / Eń Jaqsı Táјiribeler

### 1. Always Check Consistency First

```python
# Good / Jaqsı
engine = create_reasoning_engine(ontology_path)
if engine.check_consistency():
    result = engine.classify()
else:
    print("Fix inconsistencies before reasoning")

# Bad / Naqıs - Don't classify inconsistent ontology
result = engine.classify()  # May give incorrect results
```

### 2. Use Appropriate Reasoner

```python
# For production systems / Produkce sistemalar ushın
engine = create_reasoning_engine(path, ReasonerType.PELLET)

# For debugging / Debug etiw ushın
engine = create_reasoning_engine(path, ReasonerType.HERMIT)
```

### 3. Monitor Performance

```python
import time

start = time.time()
result = engine.classify()
duration = time.time() - start

if duration > 10.0:
    print(f"Warning: Reasoning took {duration:.2f}s")
    print("Consider optimizing ontology or using caching")
```

### 4. Clear Inferences Periodically

```python
# After major changes to ontology
engine.clear_inferences()

# Reclassify
result = engine.classify()
```

### 5. Handle Errors Gracefully

```python
def safe_classify(engine, crime_uri):
    """Safely classify with error handling"""
    try:
        severity = engine.classify_jinayat_awırlıǵı(crime_uri)
        return severity
    except Exception as e:
        logger.error(f"Failed to classify {crime_uri}: {e}")
        return None
```

### 6. Use Explanations for Debugging

```python
# When debugging inference issues
severity = engine.classify_jinayat_awırlıǵı(crime_uri)

explanation = engine.explain_inference(
    crime_uri,
    "http://huquqai.org/ontology#crimeType",
    severity.value
)

if explanation:
    print(f"Why: {explanation.explanation_en}")
    print(f"Rule: {explanation.rule}")
```

---

## Troubleshooting / Máselelerni Sheshiw

### Issue 1: Java Not Found

**Error:**
```
Java not found. Please install Java 8 or higher.
```

**Solution:**
```bash
# Install Java
sudo apt-get install openjdk-11-jdk  # Ubuntu/Debian
brew install openjdk@11               # macOS

# Verify
java -version
```

### Issue 2: Slow Reasoning

**Problem:** Reasoning takes too long

**Solutions:**
1. Use Pellet instead of HermiT
2. Simplify ontology (fewer axioms)
3. Use profile restrictions (OWL 2 EL, QL, RL)
4. Implement caching

```python
# Cache reasoning results
@lru_cache(maxsize=100)
def cached_classify(crime_uri):
    return engine.classify_jinayat_awırlıǵı(crime_uri)
```

### Issue 3: Out of Memory

**Problem:** Reasoner runs out of memory

**Solution:**
```python
# Increase Java heap size
import os
os.environ['JAVA_OPTS'] = '-Xmx4g'  # 4GB heap

# Or split ontology into smaller modules
```

### Issue 4: Inconsistent Ontology

**Problem:** Ontology contains contradictions

**Solution:**
```python
# Find inconsistent classes
is_consistent = engine.check_consistency()

if not is_consistent:
    # Check world for details
    inconsistent = list(engine.world.inconsistent_classes())
    for cls in inconsistent:
        print(f"Inconsistent: {cls}")
```

---

## Performance Tips / Tabıslılıq Keńesleri

1. **Use Caching** - Cache reasoning results for repeated queries
2. **Optimize Ontology** - Remove unnecessary axioms
3. **Choose Right Reasoner** - Pellet for speed, HermiT for accuracy
4. **Limit Scope** - Reason on subsets when possible
5. **Monitor Memory** - Increase heap size for large ontologies

---

## Additional Resources / Qosımsha Resurslar

- **OWL 2 Primer**: https://www.w3.org/TR/owl2-primer/
- **Pellet Reasoner**: https://github.com/stardog-union/pellet
- **HermiT Reasoner**: http://www.hermit-reasoner.com/
- **Owlready2 Docs**: https://owlready2.readthedocs.io/

---

## Support / Qollawıw

For issues and questions:

- GitHub Issues: https://github.com/yourusername/huquqAI/issues
- Documentation: `docs/`
- Examples: `examples/reasoning_usage.py`

---

**Version:** 1.0.0
**Last Updated:** 2024
**License:** MIT
