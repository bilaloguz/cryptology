"""
Playfair Cipher implementation.

The Playfair cipher is a digraphic substitution cipher that uses a key square.
It encrypts pairs of letters (digrams) using special rules for positioning.
Supports custom alphabets with automatic letter combination for non-25-letter alphabets.
"""

import re
from typing import Optional, Dict, Any
import cryptology.alphabets as ALPHABETS
from .alphabet_utils import (
    get_square_size, combine_similar_letters, create_square_alphabet,
    create_caesared_alphabet, detect_language
)
from .monoalphabetic_squares import create_monoalphabetic_square

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET  # Already lowercase
TURKISH_STANDARD = ALPHABETS.TURKISH_STANDARD  # Already lowercase
TURKISH_EXTENDED = ALPHABETS.TURKISH_EXTENDED  # Already lowercase
# For 5x5 squares, we use TURKISH_EXTENDED (32 letters)
# After combination and I=J, we get 25 letters
TURKISH_ALPHABET = TURKISH_EXTENDED


def _create_key_square(
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> list[list[str]]:
    """
    Create a key square from the given keyword and alphabet.
    
    Args:
        key: The keyword to generate the key square
        alphabet: The alphabet to use (default: English)
        square_type: Type of square ("standard", "caesar", "atbash", "affine", "keyword")
        mono_params: Parameters for monoalphabetic-based squares
        
    Returns:
        A square matrix representing the key square
    """
    # Handle monoalphabetic-based square generation
    if square_type in ["caesar", "atbash", "affine", "keyword"]:
        # Use shared monoalphabetic square generation
        if mono_params is None:
            mono_params = {}
            if square_type == "caesar":
                mono_params["shift"] = 3  # Default Caesar shift
            elif square_type == "affine":
                mono_params = {"a": 5, "b": 8}  # Default Affine params
        
        # Create the transformed alphabet using monoalphabetic square generation
        if square_type == "caesar":
            from .monoalphabetic_squares import _create_caesar_alphabet
            transformed_alphabet = _create_caesar_alphabet(alphabet.lower(), mono_params.get("shift", 3))
        elif square_type == "atbash":
            from .monoalphabetic_squares import _create_atbash_alphabet
            transformed_alphabet = _create_atbash_alphabet(alphabet.lower())
        elif square_type == "affine":
            from .monoalphabetic_squares import _create_affine_alphabet
            transformed_alphabet = _create_affine_alphabet(alphabet.lower(), mono_params.get("a", 5), mono_params.get("b", 8))
        elif square_type == "keyword":
            from .monoalphabetic_squares import _create_keyword_alphabet
            transformed_alphabet = _create_keyword_alphabet(alphabet.lower(), mono_params.get("keyword", ""))
        else:
            transformed_alphabet = alphabet.lower()
        
        # Handle I=J for English, automatic sizing for Turkish
        is_english = (alphabet.lower() == DEFAULT_ALPHABET)
        is_turkish = (alphabet.lower() == TURKISH_ALPHABET)
        
        if is_english:
            transformed_alphabet = transformed_alphabet.replace('J', 'I')
            square_size = 5
        elif is_turkish:
            # Turkish EXTENDED (32 letters) needs to be combined to fit 25 letters for 5x5
            # Combine: Ç→C, Ğ→G, İ→I, I→I (lowercase), Ö→O, Ş→S, Ü→U, plus I=J
            transformed_alphabet = transformed_alphabet.replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('i', 'i')
            transformed_alphabet = transformed_alphabet.replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
            transformed_alphabet = transformed_alphabet.replace('j', 'i')  # j→i combination like English
            square_size = 5
        else:
            # Generic alphabet - combine letters to fit square
            square_size = get_square_size(len(transformed_alphabet))
        
        # Build Playfair square: key + remaining transformed alphabet
        key_clean = ""
        seen = set()
        for char in key.lower():
            if char.isalpha() and char not in seen:
                key_clean += char
                seen.add(char)
        
        # Add remaining letters from transformed alphabet
        for char in transformed_alphabet:
            if char not in seen and char in transformed_alphabet:
                key_clean += char
                seen.add(char)
        
        # Ensure we have enough characters
        if len(key_clean) < square_size * square_size:
            # Pad with remaining transformed alphabet
            for char in transformed_alphabet:
                if char not in seen:
                    key_clean += char
                    seen.add(char)
                    if len(key_clean) >= square_size * square_size:
                        break
        
        # Create square
        square = []
        for i in range(square_size):
            row = []
            for j in range(square_size):
                index = i * square_size + j
                if index < len(key_clean):
                    row.append(key_clean[index])
                else:
                    row.append('x')
            square.append(row)
        
        return square
    
    # Handle custom alphabets (standard square creation)
    if alphabet.lower() not in [DEFAULT_ALPHABET, TURKISH_ALPHABET, TURKISH_STANDARD]:
        # Combine similar letters for non-English alphabets
        alphabet = combine_similar_letters(alphabet)
        
        # Determine square size
        square_size = get_square_size(len(alphabet))
        
        # Create square-sized alphabet
        square_alphabet = create_square_alphabet(alphabet, square_size)
    elif alphabet.lower() == TURKISH_STANDARD:
        # Turkish STANDARD alphabet (29 letters) - needs 6x6 square (36 positions)
        # Add digits to make 36 characters
        square_size = 6
        square_alphabet = alphabet + "01234567"  # 29 letters + 7 digits = 36 chars
    elif alphabet.lower() == DEFAULT_ALPHABET:
        # Standard English alphabet (I and J combined)
        square_size = 5
        square_alphabet = "abcdefghiklmnopqrstuvwxyz"  # lowercase, 25 letters (j→i)
    elif alphabet.lower() == TURKISH_EXTENDED:
        # Turkish EXTENDED alphabet (32 letters) - needs 6x6 square (36 positions)
        # Add digits to make 36 characters
        square_size = 6
        square_alphabet = alphabet + "0123"  # 32 letters + 4 digits = 36 chars
    
    # Remove duplicates while preserving order, keep lowercase
    key_clean = ""
    seen = set()
    for char in key.lower():
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


def _prepare_text(text: str, alphabet: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """
    Prepare text for Playfair encryption/decryption.
    
    Args:
        text: Input text
        alphabet: The alphabet to use
        
    Returns:
        Prepared text (uppercase, letters only, X padding for odd length)
    """
    # Remove non-alphabetic characters and convert to lowercase
    # For Turkish alphabets with 6x6 squares, include digits
    if 'ç' in alphabet or 'ğ' in alphabet:
        # Turkish alphabet - keep letters AND digits
        text_clean = re.sub(r'[^a-zçğıöşü0-9]', '', text.lower())
    else:
        # English - only letters
        text_clean = re.sub(r'[^a-z]', '', text.lower())
    
    # Handle custom alphabets
    if alphabet != "abcdefghijklmnopqrstuvwxyz":
        # Don't replace Turkish characters - keep them as-is
        # Only handle Russian if needed
        if detect_language(alphabet) == "russian":
            text_clean = text_clean.replace('Ё', 'Е').replace('Й', 'И').replace('Ъ', '').replace('Ь', '')
    else:
        # Standard English: Replace J with I
        text_clean = text_clean.replace('j', 'i')
    
    # Add padding for odd length
    if len(text_clean) % 2 == 1:
        # For Turkish alphabets, use the last digit in the square as padding
        # For English, use 'x'
        if 'ç' in alphabet or 'ğ' in alphabet:
            # Use last digit in Turkish squares ('3' for EXTENDED, '6' for STANDARD)
            text_clean += '3'
        else:
            text_clean += 'x'
    
    return text_clean


def _find_position(square: list[list[str]], char: str) -> tuple[int, int]:
    """
    Find the position of a character in the key square.
    
    Args:
        square: The key square (5x5 or 6x6)
        char: Character to find
        
    Returns:
        Tuple of (row, column) position
    """
    size = len(square)  # Dynamic square size (5 or 6)
    for i in range(size):
        for j in range(size):
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
    
    square_size = len(square)  # Dynamic square size
    
    # Same row: shift right (wrap around)
    if row1 == row2:
        new_col1 = (col1 + 1) % square_size
        new_col2 = (col2 + 1) % square_size
        return square[row1][new_col1] + square[row2][new_col2]
    
    # Same column: shift down (wrap around)
    elif col1 == col2:
        new_row1 = (row1 + 1) % square_size
        new_row2 = (row2 + 1) % square_size
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
    
    square_size = len(square)  # Dynamic square size
    
    # Same row: shift left (wrap around)
    if row1 == row2:
        new_col1 = (col1 - 1) % square_size
        new_col2 = (col2 - 1) % square_size
        return square[row1][new_col1] + square[row2][new_col2]
    
    # Same column: shift up (wrap around)
    elif col1 == col2:
        new_row1 = (row1 - 1) % square_size
        new_row2 = (row2 - 1) % square_size
        return square[new_row1][col1] + square[new_row2][col2]
    
    # Rectangle: use opposite corners
    else:
        return square[row1][col2] + square[row2][col1]


def encrypt(
    plaintext: str, 
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
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
    square = _create_key_square(key, alphabet, square_type, mono_params)
    
    # Prepare text
    text = _prepare_text(plaintext, alphabet)
    
    # Encrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _encrypt_digram(square, digram)
    
    return result


def decrypt(
    ciphertext: str, 
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
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
    square = _create_key_square(key, alphabet, square_type, mono_params)
    
    # Prepare text
    text = _prepare_text(ciphertext, alphabet)
    
    # Decrypt digrams
    result = ""
    for i in range(0, len(text), 2):
        digram = text[i:i+2]
        result += _decrypt_digram(square, digram)
    
    return result
