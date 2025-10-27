"""
Nihilist Cipher Implementation

The Nihilist cipher is a composite cipher that combines:
1. Polybius square substitution
2. Numeric key addition with modular arithmetic

It converts letters to coordinates, adds a numeric key, and converts back to letters.
"""

import string
import random
from typing import Optional, Tuple, Dict

from ..polygraphic.monoalphabetic_squares import create_monoalphabetic_square


def nihilist_encrypt(
    plaintext: str,
    key: str,
    square: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Encrypt text using the Nihilist cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Numeric or alphabetic key
        square: Polybius square (default: standard 5x5)
        key_type: "numeric" or "alphabetic"
    
    Returns:
        Encrypted text
    """
    if not plaintext or not key:
        raise ValueError("Plaintext and key cannot be empty")
    
    if square is None:
        square = nihilist_produce_square()
    
    # Prepare text and key
    processed_text = _prepare_text(plaintext)
    processed_key = _prepare_key(key, key_type)
    
    # Convert letters to coordinates
    coordinates = _letters_to_coordinates(processed_text, square)
    
    # Convert key to numeric values
    key_values = _key_to_values(processed_key, key_type)
    
    # Add coordinates and key with modular arithmetic
    encrypted_coordinates = _add_coordinates_and_key(coordinates, key_values, square)
    
    # Convert back to letters
    result = _coordinates_to_letters(encrypted_coordinates, square)
    
    return result


def nihilist_decrypt(
    ciphertext: str,
    key: str,
    square: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Decrypt text using the Nihilist cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Numeric or alphabetic key
        square: Polybius square (default: standard 5x5)
        key_type: "numeric" or "alphabetic"
    
    Returns:
        Decrypted text
    """
    if not ciphertext or not key:
        raise ValueError("Ciphertext and key cannot be empty")
    
    if square is None:
        square = nihilist_produce_square()
    
    # Prepare text and key
    processed_text = _prepare_text(ciphertext)
    processed_key = _prepare_key(key, key_type)
    
    # Convert letters to coordinates
    coordinates = _letters_to_coordinates(processed_text, square)
    
    # Convert key to numeric values
    key_values = _key_to_values(processed_key, key_type)
    
    # Subtract key from coordinates with modular arithmetic
    decrypted_coordinates = _subtract_key_from_coordinates(coordinates, key_values, square)
    
    # Convert back to letters
    result = _coordinates_to_letters(decrypted_coordinates, square)
    
    return result


def nihilist_produce_square(
    square_type: str = "standard",
    keyword: Optional[str] = None,
    alphabet: Optional[str] = None,
    mono_params: Optional[dict] = None
) -> str:
    """
    Produce a Polybius square for Nihilist cipher.
    
    Args:
        square_type: Type of square ("standard", "frequency", "keyword", "custom", 
                    "caesar", "atbash", "affine")
        keyword: Keyword for keyword-based square
        alphabet: Custom alphabet (default: English)
        mono_params: Parameters for monoalphabetic-based squares
                    - For "caesar": {"shift": int}
                    - For "affine": {"a": int, "b": int}
                    - For "keyword": {"keyword": str}
    
    Returns:
        Square string representation
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase
    
    if square_type == "standard":
        return _create_standard_square(alphabet)
    elif square_type == "frequency":
        return _create_frequency_square(alphabet)
    elif square_type == "keyword":
        if not keyword:
            raise ValueError("Keyword required for keyword-based square")
        return _create_keyword_square(keyword, alphabet)
    elif square_type == "custom":
        return _create_custom_square(alphabet)
    elif square_type in ["caesar", "atbash", "affine", "keyword"]:
        return create_monoalphabetic_square(square_type, alphabet, mono_params)
    else:
        raise ValueError(f"Invalid square_type: {square_type}")


def nihilist_generate_random_key(
    length: int,
    key_type: str = "numeric"
) -> str:
    """
    Generate a random key for Nihilist cipher.
    
    Args:
        length: Length of key to generate
        key_type: "numeric" or "alphabetic"
    
    Returns:
        Random key
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    if key_type == "numeric":
        return ''.join(str(random.randint(0, 9)) for _ in range(length))
    elif key_type == "alphabetic":
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
    else:
        raise ValueError(f"Invalid key_type: {key_type}")

def nihilist_generate_key_for_text(
    text: str,
    key_type: str = "numeric"
) -> str:
    """
    Generate a key matching the length of the text.
    
    Args:
        text: Text to match key length
        key_type: "numeric" or "alphabetic"
    
    Returns:
        Generated key
    """
    processed_text = _prepare_text(text)
    return nihilist_generate_random_key(len(processed_text), key_type)

def nihilist_encrypt_with_random_key(
    plaintext: str,
    key_length: int,
    key_type: str = "numeric",
    square: Optional[str] = None
) -> Tuple[str, str]:
    """
    Encrypt text with a randomly generated key.
    
    Args:
        plaintext: Text to encrypt
        key_length: Length of key to generate
        key_type: "numeric" or "alphabetic"
        square: Polybius square (default: standard)
    
    Returns:
        Tuple of (encrypted_text, generated_key)
    """
    generated_key = nihilist_generate_random_key(key_length, key_type)
    encrypted_text = nihilist_encrypt(plaintext, generated_key, square, key_type)
    return encrypted_text, generated_key


# Helper functions

def _prepare_text(text: str) -> str:
    """Prepare text for processing."""
    return ''.join(c.upper() for c in text if c.isalpha())


def _prepare_key(key: str, key_type: str) -> str:
    """Prepare key for processing."""
    if key_type == "numeric":
        return ''.join(c for c in key if c.isdigit())
    elif key_type == "alphabetic":
        return ''.join(c.upper() for c in key if c.isalpha())
    else:
        raise ValueError(f"Invalid key_type: {key_type}")


def _letters_to_coordinates(text: str, square: str) -> list:
    """Convert letters to coordinates using the square."""
    square_dict = _parse_square(square)
    coordinates = []
    
    for letter in text:
        if letter in square_dict:
            coordinates.append(square_dict[letter])
        else:
            raise ValueError(f"Letter '{letter}' not found in square")
    
    return coordinates


def _key_to_values(key: str, key_type: str) -> list:
    """Convert key to numeric values."""
    values = []
    
    if key_type == "numeric":
        for digit in key:
            values.append(int(digit))
    elif key_type == "alphabetic":
        for letter in key:
            values.append(ord(letter) - ord('A') + 1)
    else:
        raise ValueError(f"Invalid key_type: {key_type}")
    
    return values


def _add_coordinates_and_key(coordinates: list, key_values: list, square: str) -> list:
    """Add key values to coordinates with modular arithmetic."""
    square_size = _get_square_size(square)
    result = []
    
    for i, coord in enumerate(coordinates):
        key_val = key_values[i % len(key_values)]
        
        # Add key value to both row and column (modular arithmetic)
        new_row = ((coord[0] - 1 + key_val) % square_size) + 1
        new_col = ((coord[1] - 1 + key_val) % square_size) + 1
        
        result.append((new_row, new_col))
    
    return result


def _subtract_key_from_coordinates(coordinates: list, key_values: list, square: str) -> list:
    """Subtract key values from coordinates with modular arithmetic."""
    square_size = _get_square_size(square)
    result = []
    
    for i, coord in enumerate(coordinates):
        key_val = key_values[i % len(key_values)]
        
        # Subtract key value from both row and column (modular arithmetic)
        new_row = ((coord[0] - 1 - key_val) % square_size) + 1
        new_col = ((coord[1] - 1 - key_val) % square_size) + 1
        
        result.append((new_row, new_col))
    
    return result


def _coordinates_to_letters(coordinates: list, square: str) -> str:
    """Convert coordinates back to letters using the square."""
    square_dict = _parse_square(square)
    reverse_dict = {v: k for k, v in square_dict.items()}
    
    result = []
    for coord in coordinates:
        if coord in reverse_dict:
            result.append(reverse_dict[coord])
        else:
            raise ValueError(f"Coordinate {coord} not found in square")
    
    return ''.join(result)


def _parse_square(square: str) -> Dict[str, Tuple[int, int]]:
    """Parse square string into coordinate dictionary."""
    square_dict = {}
    lines = square.strip().split('\n')
    
    for row_idx, line in enumerate(lines):
        line = line.strip()
        for col_idx, char in enumerate(line):
            if char.isalpha():
                square_dict[char] = (row_idx + 1, col_idx + 1)
    
    return square_dict


def _get_square_size(square: str) -> int:
    """Get the size of the square (5x5 or 6x6)."""
    lines = square.strip().split('\n')
    return len(lines)


def _create_standard_square(alphabet: str) -> str:
    """Create a standard alphabetical square."""
    alphabet_upper = alphabet.upper()
    
    # Handle I=J combination for English
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Remove J, use I for both I and J
        alphabet_upper = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    # Determine square size
    if len(alphabet_upper) <= 25:
        size = 5
    else:
        size = 6
    
    # Pad alphabet if needed
    while len(alphabet_upper) < size * size:
        alphabet_upper += alphabet_upper[0]  # Pad with first letter
    
    # Create square
    square_lines = []
    for i in range(size):
        start_idx = i * size
        end_idx = start_idx + size
        square_lines.append(alphabet_upper[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_frequency_square(alphabet: str) -> str:
    """Create a frequency-based square."""
    alphabet_upper = alphabet.upper()
    
    # Define frequency orders
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # English frequency order (25 letters for 5x5 square)
        frequency_order = "ETAOINSHRDLCUMWFGYPBVKXQZ"
    elif alphabet_upper == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        # Turkish frequency order (29 letters for 6x6 square)
        frequency_order = "AENRLDKMSUTOYBGHCÇPFVZŞĞÖÜJIİ"
    else:
        # For other alphabets, use alphabetical order
        frequency_order = alphabet_upper
    
    # Handle I=J combination for English
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        frequency_order = frequency_order.replace('J', 'I')
    
    # Determine square size based on alphabet
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        size = 5  # English uses 5x5 (25 letters with I=J)
    elif alphabet_upper == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        size = 6  # Turkish uses 6x6 (29 letters)
    else:
        # For other alphabets, determine size based on length
        if len(frequency_order) <= 25:
            size = 5
        else:
            size = 6
    
    # Pad if needed
    while len(frequency_order) < size * size:
        frequency_order += frequency_order[0]
    
    # Create square
    square_lines = []
    for i in range(size):
        start_idx = i * size
        end_idx = start_idx + size
        square_lines.append(frequency_order[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_keyword_square(keyword: str, alphabet: str) -> str:
    """Create a keyword-based square."""
    alphabet_upper = alphabet.upper()
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
    for char in alphabet_upper:
        if char not in seen:
            remaining += char
    
    # Combine keyword and remaining letters
    square_alphabet = keyword_unique + remaining
    
    # Handle I=J combination for English
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        square_alphabet = square_alphabet.replace('J', 'I')
    
    # Determine square size based on alphabet
    if alphabet_upper == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        size = 5  # English uses 5x5 (25 letters with I=J)
    elif alphabet_upper == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        size = 6  # Turkish uses 6x6 (29 letters)
    else:
        # For other alphabets, determine size based on length
        if len(square_alphabet) <= 25:
            size = 5
        else:
            size = 6
    
    # Pad if needed
    while len(square_alphabet) < size * size:
        square_alphabet += square_alphabet[0]
    
    # Create square
    square_lines = []
    for i in range(size):
        start_idx = i * size
        end_idx = start_idx + size
        square_lines.append(square_alphabet[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_custom_square(alphabet: str) -> str:
    """Create a custom square based on alphabet."""
    return _create_standard_square(alphabet)


