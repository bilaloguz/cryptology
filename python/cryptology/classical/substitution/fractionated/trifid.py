"""
Trifid Cipher implementation.

The Trifid cipher is a fractionated substitution cipher that uses a 3x3x3 cube.
It works by:
1. Converting each letter to its layer, row, and column coordinates
2. Writing all layer coordinates, then all row coordinates, then all column coordinates
3. Reading triplets of coordinates to get new letters

This 3D fractionation technique provides even more security than Bifid.
"""

from typing import List, Tuple
from ..polygraphic.alphabet_utils import combine_similar_letters, get_square_size, create_square_alphabet

DEFAULT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _create_trifid_cube(key: str, alphabet: str = DEFAULT_ALPHABET) -> List[List[List[str]]]:
    """
    Create a 3x3x3 Trifid cube from the key and alphabet.
    
    Args:
        key: The keyword to use for the cube
        alphabet: The alphabet to use (default: English)
        
    Returns:
        A 3x3x3 cube as a list of lists of lists
    """
    # Handle custom alphabets
    if alphabet != DEFAULT_ALPHABET:
        # Combine similar letters for non-English alphabets
        processed_alphabet = combine_similar_letters(alphabet)
        
        # For Trifid, we need exactly 27 characters (3x3x3)
        if len(processed_alphabet) > 27:
            # Take first 27 characters
            processed_alphabet = processed_alphabet[:27]
        elif len(processed_alphabet) < 27:
            # Pad with X
            processed_alphabet = processed_alphabet.ljust(27, 'X')
    else:
        # Standard English alphabet (I and J combined, 26 letters + 1 padding)
        processed_alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 25 letters
        processed_alphabet = processed_alphabet.ljust(27, 'X')  # Pad to 27
    
    # Remove duplicates while preserving order, convert to uppercase
    key_clean = ""
    seen = set()
    
    for char in key.upper():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters from processed alphabet
    for char in processed_alphabet.upper():
        if char not in seen:
            key_clean += char
            seen.add(char)
    
    # Ensure we have exactly 27 characters
    if len(key_clean) > 27:
        key_clean = key_clean[:27]
    elif len(key_clean) < 27:
        key_clean = key_clean.ljust(27, 'X')
    
    # Create 3x3x3 cube
    cube = []
    for layer in range(3):
        cube_layer = []
        for row in range(3):
            cube_row = []
            for col in range(3):
                index = layer * 9 + row * 3 + col
                if index < len(key_clean):
                    cube_row.append(key_clean[index])
                else:
                    cube_row.append('X')  # Padding
            cube_layer.append(cube_row)
        cube.append(cube_layer)
    
    return cube


def _find_position(cube: List[List[List[str]]], char: str) -> Tuple[int, int, int]:
    """
    Find the layer, row, and column position of a character in the cube.
    
    Args:
        cube: The Trifid cube
        char: The character to find
        
    Returns:
        A tuple of (layer, row, column) coordinates
    """
    char = char.upper()
    
    # Handle I/J combination for English
    if char == 'J':
        char = 'I'
    
    for layer in range(3):
        for row in range(3):
            for col in range(3):
                if cube[layer][row][col] == char:
                    return layer, row, col
    
    raise ValueError(f"Character '{char}' not found in cube")


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
    Encrypt plaintext using the Trifid cipher.
    
    Args:
        plaintext: The text to encrypt
        key: The keyword for the Trifid cube
        alphabet: The alphabet to use (default: English)
        
    Returns:
        The encrypted text
    """
    if not plaintext or not key:
        return ""
    
    # Create the Trifid cube
    cube = _create_trifid_cube(key, alphabet)
    
    # Prepare the text
    text_clean = _prepare_text(plaintext, alphabet)
    
    if not text_clean:
        return ""
    
    # Convert each letter to coordinates
    layers = []
    rows = []
    cols = []
    
    for char in text_clean:
        try:
            layer, row, col = _find_position(cube, char)
            layers.append(layer)
            rows.append(row)
            cols.append(col)
        except ValueError:
            # Skip characters not in the cube
            continue
    
    if not layers:
        return ""
    
    # Fractionation: write all layers, then all rows, then all columns
    fractionated = layers + rows + cols
    
    # Read triplets of coordinates to get new letters
    result = ""
    for i in range(0, len(fractionated), 3):
        if i + 2 < len(fractionated):
            layer = fractionated[i]
            row = fractionated[i + 1]
            col = fractionated[i + 2]
            if layer < 3 and row < 3 and col < 3:
                result += cube[layer][row][col]
    
    return result


def decrypt(ciphertext: str, key: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using the Trifid cipher.
    
    Args:
        ciphertext: The text to decrypt
        key: The keyword for the Trifid cube
        alphabet: The alphabet to use (default: English)
        
    Returns:
        The decrypted text
    """
    if not ciphertext or not key:
        return ""
    
    # Create the Trifid cube
    cube = _create_trifid_cube(key, alphabet)
    
    # Prepare the text
    text_clean = _prepare_text(ciphertext, alphabet)
    
    if not text_clean:
        return ""
    
    # Convert each letter to coordinates
    coords = []
    for char in text_clean:
        try:
            layer, row, col = _find_position(cube, char)
            coords.append((layer, row, col))
        except ValueError:
            # Skip characters not in the cube
            continue
    
    if not coords:
        return ""
    
    # Defractionation: separate layers, rows, and columns
    layers = [coord[0] for coord in coords]
    rows = [coord[1] for coord in coords]
    cols = [coord[2] for coord in coords]
    
    # Interleave layers, rows, and columns
    result = ""
    for i in range(len(layers)):
        if i < len(layers) and i < len(rows) and i < len(cols):
            layer = layers[i]
            row = rows[i]
            col = cols[i]
            if layer < 3 and row < 3 and col < 3:
                result += cube[layer][row][col]
    
    return result
