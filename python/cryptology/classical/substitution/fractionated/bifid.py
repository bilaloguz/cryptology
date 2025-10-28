"""
Bifid Cipher implementation.

The Bifid cipher is a fractionated substitution cipher that uses a 5x5 Polybius square.
It works by:
1. Converting each letter to its row and column coordinates
2. Writing all row coordinates, then all column coordinates
3. Reading pairs of coordinates to get new letters

This fractionation technique makes frequency analysis much more difficult.
"""

from typing import List, Tuple, Optional, Dict, Any
import cryptology.alphabets as ALPHABETS
from ..polygraphic.alphabet_utils import combine_similar_letters, get_square_size, create_square_alphabet
from ..polygraphic.monoalphabetic_squares import create_monoalphabetic_square

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET


def _create_polybius_square(
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> List[List[str]]:
    """
    Create a 5x5 Polybius square from the key and alphabet.
    
    Args:
        key: The keyword to use for the square
        alphabet: The alphabet to use (default: English)
        square_type: Type of square ("standard", "caesar", "atbash", "affine", "keyword")
        mono_params: Parameters for monoalphabetic-based squares
        
    Returns:
        A 5x5 square as a list of lists
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
        
        square_string = create_monoalphabetic_square(square_type, alphabet, mono_params)
        square_size = get_square_size(len(alphabet))
        
        # Convert string to 2D list
        square = []
        for i in range(square_size):
            row = []
            for j in range(square_size):
                index = i * square_size + j
                if index < len(square_string):
                    row.append(square_string[index])
                else:
                    row.append('x')
            square.append(row)
        return square
    
    # Handle custom alphabets (standard square creation)
    if alphabet != DEFAULT_ALPHABET:
        # For Turkish alphabets, use 6x6 square to keep Turkish characters
        if len(alphabet) >= 29:
            # Turkish Standard (29 chars) or Extended (32+ chars) - use 6x6
            square_size = 6
            # Add digits to fill 36 positions (29 letters + 7 digits)
            if len(alphabet) == 29:
                processed_alphabet = alphabet + "0123456"  # 29 + 7 = 36
            elif len(alphabet) >= 32:
                processed_alphabet = alphabet + "0123"  # 32 + 4 = 36
            else:
                processed_alphabet = alphabet + 'X' * (36 - len(alphabet))
        else:
            # Combine similar letters for other alphabets
            processed_alphabet = combine_similar_letters(alphabet)
            # Determine square size
            square_size = get_square_size(len(processed_alphabet))
        
        # Create square-sized alphabet
        square_alphabet = create_square_alphabet(processed_alphabet, square_size)
    else:
        # Standard English alphabet (I and J combined)
        square_size = 5
        square_alphabet = "abcdefghiklmnopqrstuvwxyz"  # No j, j and i are combined (25 letters)
    
    # Remove duplicates while preserving order, keep lowercase
    key_clean = ""
    seen = set()
    
    for char in key.lower():
        if char.isalpha() and char not in seen:
            key_clean += char
            seen.add(char)
    
    # Add remaining letters from square alphabet
    for char in square_alphabet.lower():
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
                row.append('x')  # Padding
        square.append(row)
    
    return square


def _find_position(square: List[List[str]], char: str, alphabet: str = DEFAULT_ALPHABET) -> Tuple[int, int]:
    """
    Find the row and column position of a character in the square.
    
    Args:
        square: The Polybius square
        char: The character to find
        alphabet: The alphabet being used (for j/i handling)
        
    Returns:
        A tuple of (row, column) coordinates
    """
    char = char.lower()
    
    # Handle j/i combination ONLY for English
    if alphabet == DEFAULT_ALPHABET and char == 'j':
        char = 'i'
    
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
    # Clean the text - DON'T replace Turkish characters
    text_clean = ""
    for char in text.lower():
        if char.isalpha() or char.isdigit():
            # For English, replace J with I
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
    square = _create_polybius_square(key, alphabet, square_type, mono_params)
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
            row, col = _find_position(square, char, alphabet)
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


def decrypt(
    ciphertext: str, 
    key: str, 
    alphabet: str = DEFAULT_ALPHABET,
    square_type: str = "standard",
    mono_params: Optional[Dict[str, Any]] = None
) -> str:
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
    square = _create_polybius_square(key, alphabet, square_type, mono_params)
    square_size = len(square)
    
    # Prepare the text
    text_clean = _prepare_text(ciphertext, alphabet)
    
    if not text_clean:
        return ""
    
    # Convert each letter to coordinates
    coords = []
    for char in text_clean:
        try:
            row, col = _find_position(square, char, alphabet)
            coords.append((row, col))
        except ValueError:
            # Skip characters not in the square
            continue
    
    if not coords:
        return ""
    
    # Defractionation: Extract all coordinate digits
    all_digits = []
    for coord in coords:
        all_digits.append(coord[0])  # row
        all_digits.append(coord[1])  # col
    
    # Split the digit stream in half
    digit_count = len(all_digits)
    half = digit_count // 2
    
    rows_digits = all_digits[:half]
    cols_digits = all_digits[half:]
    
    # Interleave rows and cols to get original coordinates
    result = ""
    for i in range(min(len(rows_digits), len(cols_digits))):
        row = rows_digits[i]
        col = cols_digits[i]
        if row < square_size and col < square_size:
            result += square[row][col]
    
    return result
