"""
Alphabet utilities for polygraphic substitution ciphers.

This module provides utilities for handling custom alphabets in polygraphic ciphers,
including letter combination strategies and square size calculations.
"""

import re
from typing import List, Tuple, Optional


def get_square_size(alphabet_length: int) -> int:
    """
    Calculate the appropriate square size for a given alphabet length.
    
    Args:
        alphabet_length: Number of letters in the alphabet
        
    Returns:
        Square size (e.g., 5 for 25 letters, 6 for 36 letters)
    """
    import math
    return math.ceil(math.sqrt(alphabet_length))


def combine_similar_letters(alphabet: str, language: str = "auto") -> str:
    """
    Combine similar letters in an alphabet to fit polygraphic cipher requirements.
    
    Args:
        alphabet: Input alphabet
        language: Language hint for combination rules
        
    Returns:
        Alphabet with similar letters combined
    """
    if language == "auto":
        language = detect_language(alphabet)
    
    if language == "turkish":
        return _combine_turkish_letters(alphabet)
    elif language == "russian":
        return _combine_russian_letters(alphabet)
    elif language == "german":
        return _combine_german_letters(alphabet)
    else:
        return _combine_generic_letters(alphabet)


def _combine_turkish_letters(alphabet: str) -> str:
    """Combine Turkish letters for polygraphic ciphers."""
    combinations = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    }
    
    result = alphabet
    for turkish, english in combinations.items():
        result = result.replace(turkish, english)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_chars = []
    for char in result:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    return ''.join(unique_chars)


def _combine_russian_letters(alphabet: str) -> str:
    """Combine Russian letters for polygraphic ciphers."""
    combinations = {
        'ё': 'е', 'й': 'и', 'ъ': '', 'ь': '',
        'Ё': 'Е', 'Й': 'И', 'Ъ': '', 'Ь': ''
    }
    
    result = alphabet
    for russian, replacement in combinations.items():
        result = result.replace(russian, replacement)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_chars = []
    for char in result:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    return ''.join(unique_chars)


def _combine_german_letters(alphabet: str) -> str:
    """Combine German letters for polygraphic ciphers."""
    combinations = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'AE', 'Ö': 'OE', 'Ü': 'UE'
    }
    
    result = alphabet
    for german, replacement in combinations.items():
        result = result.replace(german, replacement)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_chars = []
    for char in result:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    return ''.join(unique_chars)


def _combine_generic_letters(alphabet: str) -> str:
    """Generic letter combination for unknown languages."""
    # Remove duplicates while preserving order
    seen = set()
    unique_chars = []
    for char in alphabet:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    return ''.join(unique_chars)


def detect_language(alphabet: str) -> str:
    """
    Detect the language of an alphabet based on character patterns.
    
    Args:
        alphabet: Input alphabet
        
    Returns:
        Detected language ('turkish', 'russian', 'german', 'english', 'unknown')
    """
    alphabet_lower = alphabet.lower()
    
    # Turkish indicators
    if any(char in alphabet_lower for char in ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü']):
        return "turkish"
    
    # Russian indicators
    if any(char in alphabet_lower for char in ['ё', 'й', 'ъ', 'ь']):
        return "russian"
    
    # German indicators
    if any(char in alphabet_lower for char in ['ä', 'ö', 'ü', 'ß']):
        return "german"
    
    # English indicators
    if all(char in 'abcdefghijklmnopqrstuvwxyz' for char in alphabet_lower):
        return "english"
    
    return "unknown"


def create_square_alphabet(alphabet: str, square_size: int) -> str:
    """
    Create a square-sized alphabet by combining letters if necessary.
    
    Args:
        alphabet: Input alphabet
        square_size: Desired square size
        
    Returns:
        Alphabet of exactly square_size² length
    """
    target_length = square_size * square_size
    
    if len(alphabet) == target_length:
        return alphabet
    elif len(alphabet) < target_length:
        # Pad with X if too short
        return alphabet + 'X' * (target_length - len(alphabet))
    else:
        # Truncate if too long
        return alphabet[:target_length]


def create_caesared_alphabet(base_alphabet: str, shift: int) -> str:
    """
    Create a 'Caesared' alphabet by shifting the base alphabet.
    
    Args:
        base_alphabet: Base alphabet to shift
        shift: Number of positions to shift
        
    Returns:
        Shifted alphabet
    """
    shift = shift % len(base_alphabet)
    return base_alphabet[shift:] + base_alphabet[:shift]


def get_letter_combination_rules() -> dict:
    """
    Get the letter combination rules for different languages.
    
    Returns:
        Dictionary mapping languages to their combination rules
    """
    return {
        "turkish": {
            "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
            "Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"
        },
        "russian": {
            "ё": "е", "й": "и", "ъ": "", "ь": "",
            "Ё": "Е", "Й": "И", "Ъ": "", "Ь": ""
        },
        "german": {
            "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
            "Ä": "AE", "Ö": "OE", "Ü": "UE"
        }
    }
