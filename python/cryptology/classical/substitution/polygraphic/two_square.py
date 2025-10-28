"""
Two Square Cipher implementation.

The Two Square cipher uses two 5x5 key squares to encrypt digrams.
It is more secure than Playfair as it uses two different key squares.
"""

import re
from typing import Optional, Dict, Any
import cryptology.alphabets as ALPHABETS
from .monoalphabetic_squares import _create_caesar_alphabet, _create_atbash_alphabet, _create_affine_alphabet, _create_keyword_alphabet

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET  # Already lowercase
TURKISH_EXTENDED = ALPHABETS.TURKISH_EXTENDED  # Already lowercase


def _create_key_square(
    key: str, 
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> list[list[str]]:
    """
    Create a 5x5 key square from the given keyword.
    
    Args:
        key: The keyword to generate the key square
        square_type: Type of square ("standard", "caesar", "atbash", "affine", "keyword")
        mono_params: Parameters for monoalphabetic-based squares
        
    Returns:
        A 5x5 matrix representing the key square
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Handle monoalphabetic-based square generation
    if square_type in ["caesar", "atbash", "affine", "keyword"]:
        # Create the transformed alphabet
        if square_type == "caesar":
            transformed_alphabet = _create_caesar_alphabet(alphabet.lower(), mono_params.get("shift", 3) if mono_params else 3)
        elif square_type == "atbash":
            transformed_alphabet = _create_atbash_alphabet(alphabet.lower())
        elif square_type == "affine":
            transformed_alphabet = _create_affine_alphabet(alphabet.lower(), mono_params.get("a", 5) if mono_params else 5, mono_params.get("b", 8) if mono_params else 8)
        elif square_type == "keyword":
            transformed_alphabet = _create_keyword_alphabet(alphabet.lower(), mono_params.get("keyword", "") if mono_params else "")
        
        # Handle j=i for Playfair-style ciphers
        transformed_alphabet = transformed_alphabet.replace('j', 'i')
        
        # Build square: key + remaining transformed alphabet
        key_clean = ""
        seen = set()
        for char in key.lower():
            if char.isalpha() and char not in seen:
                key_clean += char
                seen.add(char)
        
        # Add remaining letters from transformed alphabet
        for char in transformed_alphabet:
            if char not in seen:
                key_clean += char
                seen.add(char)
                if len(key_clean) >= 25:
                    break
        
        # Ensure we have exactly 25 characters
        if len(key_clean) < 25:
            for char in alphabet.replace('J', 'I'):
                if char not in seen:
                    key_clean += char
                    seen.add(char)
                    if len(key_clean) >= 25:
                        break
        
        # Create 5x5 square
        square = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(key_clean[i * 5 + j])
            square.append(row)
        
        return square
    
    # Standard square creation
    # Remove duplicates while preserving order, keep lowercase
    key_clean = ""
    seen = set()
    for char in key.lower():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters (j and i are combined)
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # No j, j and i are combined (25 letters)
    for char in alphabet:
        if char not in seen:
            key_clean += char
    
    # Create 5x5 square
    square = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append(key_clean[i * 5 + j])
        square.append(row)
    
    return square


def _prepare_text(text: str) -> str:
    """
    Prepare text for Two Square encryption/decryption.
    
    Args:
        text: Input text
        
    Returns:
        Prepared text (uppercase, letters only, X padding for odd length)
    """
    # Remove non-alphabetic characters and convert to uppercase
    text_clean = re.sub(r'[^a-zçğıöşü]', '', text.lower())
    
    # Replace j with i
    text_clean = text_clean.replace('j', 'i')
    
    # Add x padding for odd length
    if len(text_clean) % 2 == 1:
        text_clean += 'x'
    
    return text_clean


def _find_position(square: list[list[str]], char: str) -> tuple[int, int]:
    """
    Find the position of a character in the key square.
    
    Args:
        square: The 5x5 key square
        char: Character to find
        
    Returns:
        Tuple of (row, column) position
    """
    for i in range(5):
        for j in range(5):
            if square[i][j] == char:
                return (i, j)
    raise ValueError(f"Character {char} not found in key square")


def _encrypt_digram(square1: list[list[str]], square2: list[list[str]], digram: str) -> str:
    """
    Encrypt a digram using Two Square rules.
    
    Args:
        square1: The first 5x5 key square
        square2: The second 5x5 key square
        digram: Two-character string to encrypt
        
    Returns:
        Encrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    row1, col1 = _find_position(square1, char1)
    row2, col2 = _find_position(square2, char2)
    
    # Use opposite corners of the rectangle formed by the two positions
    return square1[row1][col2] + square2[row2][col1]


def _decrypt_digram(square1: list[list[str]], square2: list[list[str]], digram: str) -> str:
    """
    Decrypt a digram using Two Square rules.
    
    Args:
        square1: The first 5x5 key square
        square2: The second 5x5 key square
        digram: Two-character string to decrypt
        
    Returns:
        Decrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    row1, col1 = _find_position(square1, char1)
    row2, col2 = _find_position(square2, char2)
    
    # Use opposite corners of the rectangle formed by the two positions
    return square1[row1][col2] + square2[row2][col1]


def encrypt(
    plaintext: str, 
    key1: str, 
    key2: str,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Encrypt plaintext using Two Square cipher.
    
    Args:
        plaintext: Text to encrypt
        key1: First keyword for generating the first key square
        key2: Second keyword for generating the second key square
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If keys are empty or contain no letters
    """
    if not key1 or not re.search(r'[A-Za-z]', key1):
        raise ValueError("Key1 must contain at least one letter")
    if not key2 or not re.search(r'[A-Za-z]', key2):
        raise ValueError("Key2 must contain at least one letter")
    
    # Create key squares
    square1 = _create_key_square(key1, square_type, mono_params)
    square2 = _create_key_square(key2, square_type, mono_params)
    
    # Prepare text
    text = _prepare_text(plaintext)
    
    # Encrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _encrypt_digram(square1, square2, digram)
    
    return result


def decrypt(
    ciphertext: str, 
    key1: str, 
    key2: str,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Decrypt ciphertext using Two Square cipher.
    
    Args:
        ciphertext: Text to decrypt
        key1: First keyword for generating the first key square
        key2: Second keyword for generating the second key square
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If keys are empty or contain no letters
    """
    if not key1 or not re.search(r'[A-Za-z]', key1):
        raise ValueError("Key1 must contain at least one letter")
    if not key2 or not re.search(r'[A-Za-z]', key2):
        raise ValueError("Key2 must contain at least one letter")
    
    # Create key squares
    square1 = _create_key_square(key1, square_type, mono_params)
    square2 = _create_key_square(key2, square_type, mono_params)
    
    # Prepare text
    text = _prepare_text(ciphertext)
    
    # Decrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _decrypt_digram(square1, square2, digram)
    
    return result
