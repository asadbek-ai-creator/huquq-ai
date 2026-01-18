"""
Helper utilities for huquqAI system
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def extract_article_number(text: str) -> Optional[str]:
    """Extract article number from text"""
    # Look for patterns like "Statiya 123" or "123-statiya"
    patterns = [
        r'statiya\s+(\d+)',
        r'(\d+)-statiya',
        r'(?:^|\s)(\d+)(?:\s|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1)

    return None


def format_date(date: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return date.strftime(format)


def paginate(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Paginate list of items"""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": items[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size
    }


def normalize_karakalpak_text(text: str) -> str:
    """
    Normalize Karakalpak text
    Handle different character encodings
    """
    # Mapping of similar characters
    replacements = {
        'ń': 'n',
        'ǵ': 'g',
        'ı': 'i',
        'ú': 'u',
        'ó': 'o'
    }

    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return normalized


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two texts
    Returns value between 0 and 1
    """
    # Simple Jaccard similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)


def validate_crime_type(crime_type: str) -> bool:
    """Validate crime type"""
    valid_types = ["light", "medium", "heavy", "very_heavy"]
    return crime_type in valid_types


def validate_code_type(code_type: str) -> bool:
    """Validate legal code type"""
    valid_types = ["criminal", "civil", "administrative", "labor"]
    return code_type in valid_types


def generate_id(prefix: str = "") -> str:
    """Generate unique ID"""
    from uuid import uuid4
    unique_id = str(uuid4())[:8]
    return f"{prefix}{unique_id}" if prefix else unique_id
