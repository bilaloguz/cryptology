"""
Trifid Cipher implementation.

The Trifid cipher is a fractionated substitution cipher that uses a 3x3x3 cube.
It works by:
1. Converting each letter to its layer, row, and column coordinates
2. Writing all layer coordinates, then all row coordinates, then all column coordinates
3. Reading triplets of coordinates to get new letters

This 3D fractionation technique provides even more security than Bifid.
"""

from typing import List, Tuple, Optional, Dict, Any
import cryptology.alphabets as ALPHABETS
from ..polygraphic.alphabet_utils import combine_similar_letters, get_square_size, create_square_alphabet
from ..polygraphic.monoalphabetic_squares import create_monoalphabetic_square

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET


def _create_trifid_cube(
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> List[List[List[str]]]:
    """
    Create a Trifid cube from the key and alphabet.
    
    Args:
        key: The keyword to use for the cube
        alphabet: The alphabet to use (default: English)
        square_type: Type of square ("standard", "caesar", "atbash", "affine", "keyword")
        mono_params: Parameters for monoalphabetic-based squares
        
    Returns:
        A cube as a list of lists of lists
    """
    # Determine target cube size (3x3x3 or 3x3x4) based on alphabet length
    def compute_dims(target_len: int) -> Tuple[int, int, int]:
        # Layers and rows fixed at 3; columns vary
        layers = 3
        rows = 3
        cols = (target_len + (layers * rows) - 1) // (layers * rows)
        # Clamp to at least 3
        if cols < 3:
            cols = 3
        return layers, rows, cols

    # Handle monoalphabetic-based square generation
    if square_type in ["caesar", "atbash", "affine", "keyword"]:
        # Use shared monoalphabetic square generation
        if mono_params is None:
            mono_params = {}
            if square_type == "caesar":
                mono_params["shift"] = 3  # Default Caesar shift
            elif square_type == "affine":
                mono_params = {"a": 5, "b": 8}  # Default Affine params
        
        # Create square string (can be 5x5 or 6x6)
        square_string = create_monoalphabetic_square(square_type, alphabet, mono_params)
        
        # Extract characters for Trifid cube
        # Convert multiline string to single line
        square_chars = "".join(square_string.split()).lower()
        # Decide target length: 27 or 36
        target_len = 27 if len(square_chars) <= 27 else 36
        square_chars = square_chars[:target_len].ljust(target_len, 'x')
        L, R, C = compute_dims(target_len)
        # Create cube from transformed alphabet
        cube = []
        index = 0
        for layer in range(L):
            cube_layer = []
            for row in range(R):
                cube_row = []
                for col in range(C):
                    if index < len(square_chars):
                        cube_row.append(square_chars[index])
                    else:
                        cube_row.append('x')
                    index += 1
                cube_layer.append(cube_row)
            cube.append(cube_layer)
        return cube
    
    # Handle custom alphabets (standard cube creation)
    if alphabet != DEFAULT_ALPHABET:
        # Preserve all characters for non-English alphabets
        processed_alphabet = alphabet
        # Choose 27 or 36 target size
        target_len = 27 if len(processed_alphabet) <= 27 else 36
        if len(processed_alphabet) > target_len:
            processed_alphabet = processed_alphabet[:target_len]
        elif len(processed_alphabet) < target_len:
            processed_alphabet = processed_alphabet.ljust(target_len, 'x')
    else:
        # Standard English alphabet (I and J combined, 26 letters + 1 padding)
        processed_alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 letters (no j)
        processed_alphabet = processed_alphabet.ljust(27, 'x')  # Pad to 27
    
    # Remove duplicates while preserving order, keep lowercase
    key_clean = ""
    seen = set()
    
    for char in key.lower():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters from processed alphabet
    for char in processed_alphabet.lower():
        if char not in seen:
            key_clean += char
            seen.add(char)
    
    # Ensure we have target characters (27/36)
    target_len = 27 if len(processed_alphabet) <= 27 else 36
    if len(key_clean) > target_len:
        key_clean = key_clean[:target_len]
    elif len(key_clean) < target_len:
        key_clean = key_clean.ljust(target_len, 'x')
    
    # Create cube with computed dims
    L, R, C = compute_dims(target_len)
    cube = []
    index = 0
    for layer in range(L):
        cube_layer = []
        for row in range(R):
            cube_row = []
            for col in range(C):
                if index < len(key_clean):
                    cube_row.append(key_clean[index])
                else:
                    cube_row.append('x')
                index += 1
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
    char = char.lower()
    
    L = len(cube)
    R = len(cube[0])
    C = len(cube[0][0])
    for layer in range(L):
        for row in range(R):
            for col in range(C):
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
    for char in text.lower():
        # Keep letters and digits for ciphertext robustness
        if char.isalpha() or char.isdigit():
            # English: replace j with i on letters only
            if alphabet == DEFAULT_ALPHABET and char == 'j':
                char = 'i'
            text_clean += char
    
    return text_clean


def encrypt(
    plaintext: str, 
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
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
    cube = _create_trifid_cube(key, alphabet, square_type, mono_params)
    
    # Prepare the text
    text_clean = _prepare_text(plaintext, alphabet)
    
    if not text_clean:
        return ""
    
    
    # Block-wise processing with period
    period = 5
    L = len(cube)
    R = len(cube[0])
    C = len(cube[0][0])
    
    result = ""
    for start in range(0, len(text_clean), period):
        block = text_clean[start:start + period]
        # Convert each letter to coordinates
        layers: List[int] = []
        rows: List[int] = []
        cols: List[int] = []
        for char in block:
            try:
                layer, row, col = _find_position(cube, char)
                layers.append(layer)
                rows.append(row)
                cols.append(col)
            except ValueError:
                continue
        if not layers:
            continue
        # Fractionation: write all layers, then rows, then cols (within block)
        # Produce ciphertext by pairing corresponding indices
        for i in range(len(layers)):
            layer = layers[i]
            row = rows[i]
            col = cols[i]
            if layer < L and row < R and col < C:
                result += cube[layer][row][col]
    return result


def decrypt(
    ciphertext: str, 
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
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
    cube = _create_trifid_cube(key, alphabet, square_type, mono_params)
    
    # Prepare the text
    text_clean = _prepare_text(ciphertext, alphabet)
    
    if not text_clean:
        return ""
    
    
    # Block-wise processing with period
    period = 5
    L = len(cube)
    R = len(cube[0])
    C = len(cube[0][0])
    
    result = ""
    for start in range(0, len(text_clean), period):
        block = text_clean[start:start + period]
        # Convert each letter to coordinates for the block
        coords: List[Tuple[int, int, int]] = []
        for char in block:
            try:
                layer, row, col = _find_position(cube, char)
                coords.append((layer, row, col))
            except ValueError:
                continue
        if not coords:
            continue
        # Defractionation for the block: rebuild original index-wise
        layers_digits = [c[0] for c in coords]
        rows_digits = [c[1] for c in coords]
        cols_digits = [c[2] for c in coords]
        for i in range(len(coords)):
            layer = layers_digits[i]
            row = rows_digits[i]
            col = cols_digits[i]
            if layer < L and row < R and col < C:
                result += cube[layer][row][col]
    return result
