"""
Four Square Cipher implementation.

The Four Square cipher uses four 5x5 key squares to encrypt digrams.
It provides even more security than Two Square by using four different key squares.
"""

import re
from typing import Optional


def _create_key_square(key: str) -> list[list[str]]:
    """
    Create a 5x5 key square from the given keyword.
    
    Args:
        key: The keyword to generate the key square
        
    Returns:
        A 5x5 matrix representing the key square
    """
    # Remove duplicates while preserving order, convert to uppercase
    key_clean = ""
    seen = set()
    for char in key.upper():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters (I and J are combined)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J, I and J are combined
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
    Prepare text for Four Square encryption/decryption.
    
    Args:
        text: Input text
        
    Returns:
        Prepared text (uppercase, letters only, X padding for odd length)
    """
    # Remove non-alphabetic characters and convert to uppercase
    text_clean = re.sub(r'[^A-Za-z]', '', text.upper())
    
    # Replace J with I
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


def _encrypt_digram(square1: list[list[str]], square2: list[list[str]], 
                   square3: list[list[str]], square4: list[list[str]], 
                   digram: str) -> str:
    """
    Encrypt a digram using Four Square rules.
    
    Args:
        square1: The first 5x5 key square (top-left)
        square2: The second 5x5 key square (top-right)
        square3: The third 5x5 key square (bottom-left)
        square4: The fourth 5x5 key square (bottom-right)
        digram: Two-character string to encrypt
        
    Returns:
        Encrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    
    # Find positions in squares 1 and 4
    row1, col1 = _find_position(square1, char1)
    row2, col2 = _find_position(square4, char2)
    
    # Use the intersection of the row from square1 and column from square4
    # in square2, and the intersection of the column from square1 and row from square4
    # in square3
    result_char1 = square2[row1][col2]
    result_char2 = square3[row2][col1]
    
    return result_char1 + result_char2


def _decrypt_digram(square1: list[list[str]], square2: list[list[str]], 
                   square3: list[list[str]], square4: list[list[str]], 
                   digram: str) -> str:
    """
    Decrypt a digram using Four Square rules.
    
    Args:
        square1: The first 5x5 key square (top-left)
        square2: The second 5x5 key square (top-right)
        square3: The third 5x5 key square (bottom-left)
        square4: The fourth 5x5 key square (bottom-right)
        digram: Two-character string to decrypt
        
    Returns:
        Decrypted digram
    """
    if len(digram) != 2:
        raise ValueError("Digram must be exactly 2 characters")
    
    char1, char2 = digram[0], digram[1]
    
    # Find positions in squares 2 and 3
    row1, col1 = _find_position(square2, char1)
    row2, col2 = _find_position(square3, char2)
    
    # Use the intersection of the row from square2 and column from square3
    # in square1, and the intersection of the column from square2 and row from square3
    # in square4
    result_char1 = square1[row1][col2]
    result_char2 = square4[row2][col1]
    
    return result_char1 + result_char2


def encrypt(plaintext: str, key1: str, key2: str, key3: str, key4: str) -> str:
    """
    Encrypt plaintext using Four Square cipher.
    
    Args:
        plaintext: Text to encrypt
        key1: First keyword for generating the first key square (top-left)
        key2: Second keyword for generating the second key square (top-right)
        key3: Third keyword for generating the third key square (bottom-left)
        key4: Fourth keyword for generating the fourth key square (bottom-right)
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If any key is empty or contains no letters
    """
    if not key1 or not re.search(r'[A-Za-z]', key1):
        raise ValueError("Key1 must contain at least one letter")
    if not key2 or not re.search(r'[A-Za-z]', key2):
        raise ValueError("Key2 must contain at least one letter")
    if not key3 or not re.search(r'[A-Za-z]', key3):
        raise ValueError("Key3 must contain at least one letter")
    if not key4 or not re.search(r'[A-Za-z]', key4):
        raise ValueError("Key4 must contain at least one letter")
    
    # Create key squares
    square1 = _create_key_square(key1)
    square2 = _create_key_square(key2)
    square3 = _create_key_square(key3)
    square4 = _create_key_square(key4)
    
    # Prepare text
    text = _prepare_text(plaintext)
    
    # Encrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _encrypt_digram(square1, square2, square3, square4, digram)
    
    return result


def decrypt(ciphertext: str, key1: str, key2: str, key3: str, key4: str) -> str:
    """
    Decrypt ciphertext using Four Square cipher.
    
    Args:
        ciphertext: Text to decrypt
        key1: First keyword for generating the first key square (top-left)
        key2: Second keyword for generating the second key square (top-right)
        key3: Third keyword for generating the third key square (bottom-left)
        key4: Fourth keyword for generating the fourth key square (bottom-right)
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If any key is empty or contains no letters
    """
    if not key1 or not re.search(r'[A-Za-z]', key1):
        raise ValueError("Key1 must contain at least one letter")
    if not key2 or not re.search(r'[A-Za-z]', key2):
        raise ValueError("Key2 must contain at least one letter")
    if not key3 or not re.search(r'[A-Za-z]', key3):
        raise ValueError("Key3 must contain at least one letter")
    if not key4 or not re.search(r'[A-Za-z]', key4):
        raise ValueError("Key4 must contain at least one letter")
    
    # Create key squares
    square1 = _create_key_square(key1)
    square2 = _create_key_square(key2)
    square3 = _create_key_square(key3)
    square4 = _create_key_square(key4)
    
    # Prepare text
    text = _prepare_text(ciphertext)
    
    # Decrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _decrypt_digram(square1, square2, square3, square4, digram)
    
    return result
