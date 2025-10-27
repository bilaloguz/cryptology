"""
Monoalphabetic-based Polybius Square Generation

This module provides shared utilities for generating Polybius squares using
monoalphabetic cipher transformations. This can be used by any cipher that
employs Polybius squares: Playfair, Two Square, Four Square, Bifid, Trifid, Nihilist.
"""

import string
from typing import Optional, Dict, Any


def create_monoalphabetic_square(
    square_type: str,
    alphabet: Optional[str] = None,
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a Polybius square using monoalphabetic cipher transformations.
    
    Args:
        square_type: Type of monoalphabetic transformation ("caesar", "atbash", "affine", "keyword")
        alphabet: Base alphabet (default: English)
        mono_params: Parameters for the monoalphabetic transformation
                    - For "caesar": {"shift": int}
                    - For "affine": {"a": int, "b": int}
                    - For "keyword": {"keyword": str}
    
    Returns:
        Square string representation
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase
    
    alphabet_upper = alphabet.upper()
    
    # Generate transformed alphabet based on square type
    if square_type == "caesar":
        if not mono_params or "shift" not in mono_params:
            raise ValueError("Caesar square requires mono_params with 'shift' key")
        transformed_alphabet = _create_caesar_alphabet(alphabet_upper, mono_params["shift"])
    
    elif square_type == "atbash":
        transformed_alphabet = _create_atbash_alphabet(alphabet_upper)
    
    elif square_type == "affine":
        if not mono_params or "a" not in mono_params or "b" not in mono_params:
            raise ValueError("Affine square requires mono_params with 'a' and 'b' keys")
        transformed_alphabet = _create_affine_alphabet(alphabet_upper, mono_params["a"], mono_params["b"])
    
    elif square_type == "keyword":
        if not mono_params or "keyword" not in mono_params:
            raise ValueError("Keyword square requires mono_params with 'keyword' key")
        transformed_alphabet = _create_keyword_alphabet(alphabet_upper, mono_params["keyword"])
    
    else:
        raise ValueError(f"Invalid square_type: {square_type}")
    
    # Convert transformed alphabet to Polybius square
    return _alphabet_to_square(transformed_alphabet, alphabet_upper)


def _create_caesar_alphabet(alphabet: str, shift: int) -> str:
    """Create a Caesar-shifted alphabet."""
    shifted_alphabet = ""
    for char in alphabet:
        if char.isalpha():
            # Apply Caesar shift
            shifted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            shifted_alphabet += shifted_char
    return shifted_alphabet


def _create_atbash_alphabet(alphabet: str) -> str:
    """Create an Atbash-reversed alphabet."""
    reversed_alphabet = ""
    for char in alphabet:
        if char.isalpha():
            # Apply Atbash reversal
            reversed_char = chr(ord('Z') - (ord(char) - ord('A')))
            reversed_alphabet += reversed_char
    return reversed_alphabet


def _create_affine_alphabet(alphabet: str, a: int, b: int) -> str:
    """Create an Affine-transformed alphabet."""
    # Check that a is coprime with alphabet length
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    if gcd(a, len(alphabet)) != 1:
        raise ValueError(f"Parameter 'a' ({a}) must be coprime with alphabet length ({len(alphabet)})")
    
    # Create Affine-transformed alphabet
    affine_alphabet = ""
    for char in alphabet:
        if char.isalpha():
            # Apply Affine transformation: E(x) = (ax + b) mod m
            x = ord(char) - ord('A')
            encrypted_pos = (a * x + b) % len(alphabet)
            affine_char = alphabet[encrypted_pos]
            affine_alphabet += affine_char
    return affine_alphabet


def _create_keyword_alphabet(alphabet: str, keyword: str) -> str:
    """Create a keyword-based alphabet."""
    keyword_upper = keyword.upper()
    
    # Remove duplicates from keyword while preserving order
    seen = set()
    keyword_unique = ""
    for char in keyword_upper:
        if char.isalpha() and char not in seen:
            keyword_unique += char
            seen.add(char)
    
    # Add remaining alphabet letters
    remaining = ""
    for char in alphabet:
        if char not in seen:
            remaining += char
    
    return keyword_unique + remaining


def _alphabet_to_square(transformed_alphabet: str, original_alphabet: str) -> str:
    """Convert a transformed alphabet to a Polybius square."""
    # Handle I=J combination for English
    if original_alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        transformed_alphabet = transformed_alphabet.replace('J', 'I')
    
    # Determine square size based on original alphabet
    if original_alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        size = 5  # English uses 5x5 (25 letters with I=J)
    elif original_alphabet == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        size = 6  # Turkish uses 6x6 (29 letters)
    else:
        size = 5 if len(transformed_alphabet) <= 25 else 6
    
    # Pad if needed
    while len(transformed_alphabet) < size * size:
        transformed_alphabet += transformed_alphabet[0]
    
    # Create square
    square_lines = []
    for i in range(size):
        start_idx = i * size
        end_idx = start_idx + size
        square_lines.append(transformed_alphabet[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def get_available_monoalphabetic_types() -> list:
    """
    Get list of available monoalphabetic square types.
    
    Returns:
        List of available square types
    """
    return ["caesar", "atbash", "affine", "keyword"]


def validate_mono_params(square_type: str, mono_params: Optional[Dict[str, Any]]) -> bool:
    """
    Validate monoalphabetic parameters for a given square type.
    
    Args:
        square_type: Type of monoalphabetic transformation
        mono_params: Parameters to validate
    
    Returns:
        True if parameters are valid, False otherwise
    """
    if square_type == "caesar":
        return mono_params is not None and "shift" in mono_params and isinstance(mono_params["shift"], int)
    
    elif square_type == "atbash":
        return True  # No parameters needed
    
    elif square_type == "affine":
        return (mono_params is not None and 
                "a" in mono_params and "b" in mono_params and
                isinstance(mono_params["a"], int) and isinstance(mono_params["b"], int))
    
    elif square_type == "keyword":
        return (mono_params is not None and 
                "keyword" in mono_params and 
                isinstance(mono_params["keyword"], str) and 
                len(mono_params["keyword"]) > 0)
    
    return False
