# Ontologies Directory

This directory contains OWL ontology files for the huquqAI legal knowledge base system.

## Files

- `legal_ontology.owl` - Main legal ontology file
- `criminal_code.owl` - Criminal code ontology
- `civil_code.owl` - Civil code ontology

## Usage

To initialize the legal ontology:

```python
from src.models.ontology import LegalOntology

ontology = LegalOntology()
ontology.initialize_legal_ontology()
ontology.save_ontology("data/ontologies/legal_ontology.owl")
```

## Ontology Structure

### Classes
- `Nızam` (Law)
- `Statiya` (Article)
- `Jinayat` (Crime)
- `Jaza` (Punishment)
- `Kodeks` (Legal Code)

### Object Properties
- `hasArticle` - Links code to articles
- `hasPunishment` - Links crime to punishment
- `relatedToCrime` - Links article to crime
- `belongsToCode` - Links article to code

### Datatype Properties
- `articleNumber` - Article number
- `crimeType` - Type of crime
- `severity` - Severity level
- `description` - Text description
