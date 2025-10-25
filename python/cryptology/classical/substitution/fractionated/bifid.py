"""
Bifid Cipher implementation.

The Bifid cipher is a fractionated substitution cipher that uses a 5x5 Polybius square.
It works by:
1. Converting each letter to its row and column coordinates
2. Writing all row coordinates, then all column coordinates
3. Reading pairs of coordinates to get new letters

This fractionation technique makes frequency analysis much more difficult.
"""

from typing import List, Tuple
from ..polygraphic.alphabet_utils import combine_similar_letters, get_square_size, create_square_alphabet

DEFAULT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _create_polybius_square(key: str, alphabet: str = DEFAULT_ALPHABET) -> List[List[str]]:
    """
    Create a 5x5 Polybius square from the key and alphabet.
    
    Args:
        key: The keyword to use for the square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        A 5x5 square as a list of lists
    """
    # Handle custom alphabets
    if alphabet != DEFAULT_ALPHABET:
        # Combine similar letters for non-English alphabets
        processed_alphabet = combine_similar_letters(alphabet)
        
        # Determine square size
        square_size = get_square_size(len(processed_alphabet))
        
        # Create square-sized alphabet
        square_alphabet = create_square_alphabet(processed_alphabet, square_size)
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
    for char in square_alphabet.upper():
        if char not in seen:
            key_clean += char
            seen.add(char)
    
    # Create square
    square = []
    for i in range(square_size):
        row = []
        for j in range(square_size):
            index = i * square_size + j
            if index < len(key_clean):
                row.append(key_clean[index])
            else:
                row.append('X')  # Padding
        square.append(row)
    
    return square


def _find_position(square: List[List[str]], char: str) -> Tuple[int, int]:
    """
    Find the row and column position of a character in the square.
    
    Args:
        square: The Polybius square
        char: The character to find
        
    Returns:
        A tuple of (row, column) coordinates
    """
    char = char.upper()
    
    # Handle I/J combination for English
    if char == 'J':
        char = 'I'
    
    for i, row in enumerate(square):
        for j, cell in enumerate(row):
            if cell == char:
                return i, j
    
    raise ValueError(f"Character '{char}' not found in square")


def _prepare_text(text: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Prepare text for encryption by cleaning and handling special cases.
    
    Args:
        text: The input text
        alphabet: The alphabet being used
        
    Returns:
        Cleaned text ready for encryption
    """
    # Clean the text
    text_clean = ""
    for char in text.upper():
        if char.isalpha():
            # Handle custom alphabets
            if alphabet != DEFAULT_ALPHABET:
                # Apply language-specific replacements
                if 'ç' in alphabet.lower() or 'Ç' in alphabet:
                    # Turkish character replacements
                    if char == 'Ç':
                        char = 'C'
                    elif char == 'Ğ':
                        char = 'G'
                    elif char == 'I':
                        char = 'I'
                    elif char == 'Ö':
                        char = 'O'
                    elif char == 'Ş':
                        char = 'S'
                    elif char == 'Ü':
                        char = 'U'
            else:
                # Standard English: Replace J with I
                if char == 'J':
                    char = 'I'
            
            text_clean += char
    
    return text_clean


def encrypt(plaintext: str, key: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using the Bifid cipher.
    
    Args:
        plaintext: The text to encrypt
        key: The keyword for the Polybius square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        The encrypted text
    """
    if not plaintext or not key:
        return ""
    
    # Create the Polybius square
    square = _create_polybius_square(key, alphabet)
    square_size = len(square)
    
    # Prepare the text
    text_clean = _prepare_text(plaintext, alphabet)
    
    if not text_clean:
        return ""
    
    # Convert each letter to coordinates
    rows = []
    cols = []
    
    for char in text_clean:
        try:
            row, col = _find_position(square, char)
            rows.append(row)
            cols.append(col)
        except ValueError:
            # Skip characters not in the square
            continue
    
    if not rows:
        return ""
    
    # Fractionation: write all rows, then all columns
    fractionated = rows + cols
    
    # Read pairs of coordinates to get new letters
    result = ""
    for i in range(0, len(fractionated), 2):
        if i + 1 < len(fractionated):
            row = fractionated[i]
            col = fractionated[i + 1]
            if row < square_size and col < square_size:
                result += square[row][col]
    
    return result


def decrypt(ciphertext: str, key: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using the Bifid cipher.
    
    Args:
        ciphertext: The text to decrypt
        key: The keyword for the Polybius square
        alphabet: The alphabet to use (default: English)
        
    Returns:
        The decrypted text
    """
    if not ciphertext or not key:
        return ""
    
    # Create the Polybius square
    square = _create_polybius_square(key, alphabet)
    square_size = len(square)
    
    # Prepare the text
    text_clean = _prepare_text(ciphertext, alphabet)
    
    if not text_clean:
        return ""
    
    # Convert each letter to coordinates
    coords = []
    for char in text_clean:
        try:
            row, col = _find_position(square, char)
            coords.append((row, col))
        except ValueError:
            # Skip characters not in the square
            continue
    
    if not coords:
        return ""
    
    # Defractionation: separate rows and columns
    rows = [coord[0] for coord in coords]
    cols = [coord[1] for coord in coords]
    
    # Interleave rows and columns
    result = ""
    for i in range(len(rows)):
        if i < len(rows) and i < len(cols):
            row = rows[i]
            col = cols[i]
            if row < square_size and col < square_size:
                result += square[row][col]
    
    return result
