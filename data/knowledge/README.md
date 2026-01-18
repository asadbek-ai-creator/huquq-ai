# Knowledge Base Directory

This directory contains legal documents and knowledge base files.

## Structure

- `criminal_code/` - Criminal code articles
- `civil_code/` - Civil code articles
- `raw/` - Raw legal documents
- `processed/` - Processed and structured documents

## Data Format

Legal documents should be stored in JSON format:

```json
{
  "article_number": "123",
  "title": "Jinayattıń awır túri",
  "content": "Bu statiya jinayattıń awır túrin anıqlaydı...",
  "code_type": "criminal",
  "language": "kaa",
  "metadata": {
    "effective_date": "2020-01-01",
    "last_updated": "2023-06-15"
  }
}
```

## Adding Data

To add new legal documents:

1. Place raw documents in `raw/` directory
2. Process and convert to JSON format
3. Move to appropriate subdirectory
4. Load into ontology using import scripts
