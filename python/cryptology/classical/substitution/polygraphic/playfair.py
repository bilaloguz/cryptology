"""
Playfair Cipher implementation.

The Playfair cipher is a digraphic substitution cipher that uses a key square.
It encrypts pairs of letters (digrams) using special rules for positioning.
Supports custom alphabets with automatic letter combination for non-25-letter alphabets.
"""

import re
from typing import Optional
from .alphabet_utils import (
    get_square_size, combine_similar_letters, create_square_alphabet,
    create_caesared_alphabet, detect_language
)


def _create_key_square(key: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> list[list[str]]:
    """
    Create a key square from the given keyword and alphabet.
    
    Args:
        key: The keyword to generate the key square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        A square matrix representing the key square
    """
    # Handle custom alphabets
    if alphabet != "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Combine similar letters for non-English alphabets
        alphabet = combine_similar_letters(alphabet)
        
        # Determine square size
        square_size = get_square_size(len(alphabet))
        
        # Create square-sized alphabet
        square_alphabet = create_square_alphabet(alphabet, square_size)
    else:
        # Standard English alphabet (I and J combined)
        square_size = 5
        square_alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J, I and J are combined
    
    # Remove duplicates while preserving order, convert to uppercase
    key_clean = ""
    seen = set()
    for char in key.upper():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters from square alphabet
    for char in square_alphabet:
        if char not in seen:
            key_clean += char
    
    # Create square
    square = []
    for i in range(square_size):
        row = []
        for j in range(square_size):
            row.append(key_clean[i * square_size + j])
        square.append(row)
    
    return square


def _prepare_text(text: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    Prepare text for Playfair encryption/decryption.
    
    Args:
        text: Input text
        alphabet: The alphabet to use
        
    Returns:
        Prepared text (uppercase, letters only, X padding for odd length)
    """
    # Remove non-alphabetic characters and convert to uppercase
    text_clean = re.sub(r'[^A-Za-z]', '', text.upper())
    
    # Handle custom alphabets
    if alphabet != "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Combine similar letters for non-English alphabets
        alphabet = combine_similar_letters(alphabet)
        
        # Replace letters according to combination rules
        if detect_language(alphabet) == "turkish":
            text_clean = text_clean.replace('Ç', 'C').replace('Ğ', 'G').replace('I', 'I')
            text_clean = text_clean.replace('Ö', 'O').replace('Ş', 'S').replace('Ü', 'U')
        elif detect_language(alphabet) == "russian":
            text_clean = text_clean.replace('Ё', 'Е').replace('Й', 'И').replace('Ъ', '').replace('Ь', '')
    else:
        # Standard English: Replace J with I
        text_clean = text_clean.replace('J', 'I')
    
    # Add X padding for odd length
    if len(text_clean) % 2 == 1:
        text_clean += 'X'
    
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


def _encrypt_digram(square: list[list[str]], digram: str) -> str:
    """
    Encrypt a digram using Playfair rules.
    
    Args:
        square: The 5x5 key square
        digram: Two-character string to encrypt
        
    Returns:
        Encrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    row1, col1 = _find_position(square, char1)
    row2, col2 = _find_position(square, char2)
    
    # Same row: shift right (wrap around)
    if row1 == row2:
        new_col1 = (col1 + 1) % 5
        new_col2 = (col2 + 1) % 5
        return square[row1][new_col1] + square[row2][new_col2]
    
    # Same column: shift down (wrap around)
    elif col1 == col2:
        new_row1 = (row1 + 1) % 5
        new_row2 = (row2 + 1) % 5
        return square[new_row1][col1] + square[new_row2][col2]
    
    # Rectangle: use opposite corners
    else:
        return square[row1][col2] + square[row2][col1]


def _decrypt_digram(square: list[list[str]], digram: str) -> str:
    """
    Decrypt a digram using Playfair rules.
    
    Args:
        square: The 5x5 key square
        digram: Two-character string to decrypt
        
    Returns:
        Decrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    row1, col1 = _find_position(square, char1)
    row2, col2 = _find_position(square, char2)
    
    # Same row: shift left (wrap around)
    if row1 == row2:
        new_col1 = (col1 - 1) % 5
        new_col2 = (col2 - 1) % 5
        return square[row1][new_col1] + square[row2][new_col2]
    
    # Same column: shift up (wrap around)
    elif col1 == col2:
        new_row1 = (row1 - 1) % 5
        new_row2 = (row2 - 1) % 5
        return square[new_row1][col1] + square[new_row2][col2]
    
    # Rectangle: use opposite corners
    else:
        return square[row1][col2] + square[row2][col1]


def encrypt(plaintext: str, key: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    Encrypt plaintext using Playfair cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Keyword for generating the key square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If key is empty or contains no letters
    """
    if not key or not re.search(r'[A-Za-z]', key):
        raise ValueError("Key must contain at least one letter")
    
    # Create key square
    square = _create_key_square(key, alphabet)
    
    # Prepare text
    text = _prepare_text(plaintext, alphabet)
    
    # Encrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _encrypt_digram(square, digram)
    
    return result


def decrypt(ciphertext: str, key: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    Decrypt ciphertext using Playfair cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Keyword for generating the key square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If key is empty or contains no letters
    """
    if not key or not re.search(r'[A-Za-z]', key):
        raise ValueError("Key must contain at least one letter")
    
    # Create key square
    square = _create_key_square(key, alphabet)
    
    # Prepare text
    text = _prepare_text(ciphertext, alphabet)
    
    # Decrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _decrypt_digram(square, digram)
    
    return result
