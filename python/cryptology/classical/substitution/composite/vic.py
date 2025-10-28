"""
VIC Cipher Implementation

The VIC cipher is a complex multi-stage encryption system that combines:
1. Polybius square substitution (6x6)
2. Fractionation (letters to digits)
3. Straddling checkerboard (digits to letters)
4. Columnar transposition (multiple passes)
5. Numeric key addition (modular arithmetic)
6. Chain addition (progressive key modification)

This implementation supports both English and Turkish alphabets with UTF-8 handling.
"""

import random
import string
from typing import Optional, Dict, Any, List, Tuple
from ..polygraphic.monoalphabetic_squares import create_monoalphabetic_square

# Default alphabets
import cryptology.alphabets as ALPHABETS

DEFAULT_VIC_ALPHABET = ALPHABETS.ENGLISH_WITH_DIGITS
TURKISH_VIC_ALPHABET = ALPHABETS.TURKISH_WITH_DIGITS

# VIC characters for substitution
VIC_LETTERS = "ADFGVX"

def vic_encrypt(
    plaintext: str,
    polybius_key: str,
    checkerboard_key: str,
    transposition_key: str,
    numeric_key: str,
    square_type: str = "standard",
    alphabet: Optional[str] = None,
    language: Optional[str] = "english",
    mono_params: Optional[Dict[str, Any]] = None,
    transposition_passes: int = 1,
    use_chain_addition: bool = False
) -> str:
    """
    Encrypt text using the VIC cipher.
    
    Args:
        plaintext: Text to encrypt
        polybius_key: Keyword for Polybius square generation
        checkerboard_key: Keyword for straddling checkerboard
        transposition_key: Keyword for columnar transposition
        numeric_key: Numeric key for addition operations
        square_type: Type of Polybius square ("standard", "caesar", "atbash", "affine", "keyword")
        alphabet: Custom alphabet (None for default)
        language: Language ("english" or "turkish")
        mono_params: Parameters for monoalphabetic transformations
        transposition_passes: Number of transposition passes (1-3)
        use_chain_addition: Whether to use chain addition
        
    Returns:
        Encrypted text
    """
    if not plaintext or not all([polybius_key, checkerboard_key, transposition_key, numeric_key]):
        raise ValueError("Plaintext and all keys must be provided")
    
    # Determine alphabet to use
    use_alphabet = alphabet
    if use_alphabet is None:
        use_alphabet = DEFAULT_VIC_ALPHABET if language == "english" else TURKISH_VIC_ALPHABET
    
    # Step 1: Generate Polybius square
    polybius_square = vic_produce_polybius_square(
        square_type, polybius_key, use_alphabet, mono_params
    )
    
    # Step 2: Substitute to Polybius pairs
    polybius_pairs = _substitute_to_polybius(plaintext.lower(), polybius_square)
    
    # Step 3: Convert pairs to digits
    digits = _pairs_to_digits(polybius_pairs)
    
    # Step 4: Generate straddling checkerboard
    checkerboard = vic_produce_checkerboard(checkerboard_key, use_alphabet)
    
    # Step 5: Convert digits to letters using checkerboard
    letters = _digits_to_letters(digits, checkerboard)
    
    # Step 6: Apply columnar transposition (multiple passes)
    transposed = letters
    for _ in range(transposition_passes):
        transposed = _columnar_transposition(transposed, transposition_key, encrypt=True)
    
    # Step 7: Apply numeric key addition
    if use_chain_addition:
        result = _chain_addition_encrypt(transposed, numeric_key, use_alphabet)
    else:
        result = _numeric_addition(transposed, numeric_key, use_alphabet, encrypt=True)
    
    return result

def vic_decrypt(
    ciphertext: str,
    polybius_key: str,
    checkerboard_key: str,
    transposition_key: str,
    numeric_key: str,
    square_type: str = "standard",
    alphabet: Optional[str] = None,
    language: Optional[str] = "english",
    mono_params: Optional[Dict[str, Any]] = None,
    transposition_passes: int = 1,
    use_chain_addition: bool = False
) -> str:
    """
    Decrypt text using the VIC cipher.
    
    Args:
        ciphertext: Text to decrypt
        polybius_key: Keyword for Polybius square generation
        checkerboard_key: Keyword for straddling checkerboard
        transposition_key: Keyword for columnar transposition
        numeric_key: Numeric key for addition operations
        square_type: Type of Polybius square ("standard", "caesar", "atbash", "affine", "keyword")
        alphabet: Custom alphabet (None for default)
        language: Language ("english" or "turkish")
        mono_params: Parameters for monoalphabetic transformations
        transposition_passes: Number of transposition passes (1-3)
        use_chain_addition: Whether to use chain addition
        
    Returns:
        Decrypted text
    """
    if not ciphertext or not all([polybius_key, checkerboard_key, transposition_key, numeric_key]):
        raise ValueError("Ciphertext and all keys must be provided")
    
    # Determine alphabet to use
    use_alphabet = alphabet
    if use_alphabet is None:
        use_alphabet = DEFAULT_VIC_ALPHABET if language == "english" else TURKISH_VIC_ALPHABET
    
    # Step 1: Reverse numeric key addition
    if use_chain_addition:
        letters = _chain_addition_decrypt(ciphertext, numeric_key, use_alphabet)
    else:
        letters = _numeric_addition(ciphertext, numeric_key, use_alphabet, encrypt=False)
    
    # Step 2: Reverse columnar transposition (multiple passes)
    transposed = letters
    for _ in range(transposition_passes):
        transposed = _columnar_transposition(transposed, transposition_key, encrypt=False)
    
    # Step 3: Generate straddling checkerboard
    checkerboard = vic_produce_checkerboard(checkerboard_key, use_alphabet)
    
    # Step 4: Convert letters to digits using checkerboard
    digits = _letters_to_digits(transposed, checkerboard)
    
    # Step 5: Convert digits to Polybius pairs
    polybius_pairs = _digits_to_pairs(digits)
    
    # Step 6: Generate Polybius square
    polybius_square = vic_produce_polybius_square(
        square_type, polybius_key, use_alphabet, mono_params
    )
    
    # Step 7: Substitute from Polybius pairs
    result = _substitute_from_polybius(polybius_pairs, polybius_square)
    
    return result

def vic_produce_polybius_square(
    square_type: str,
    keyword: Optional[str] = None,
    alphabet: Optional[str] = None,
    mono_params: Optional[Dict[str, Any]] = None,
    language: Optional[str] = "english"
) -> str:
    """
    Produce a Polybius square for VIC cipher.
    
    Args:
        square_type: Type of square ("standard", "caesar", "atbash", "affine", "keyword")
        keyword: Keyword for keyword-based squares
        alphabet: Custom alphabet (None for default)
        mono_params: Parameters for monoalphabetic transformations
        language: Language ("english" or "turkish")
        
    Returns:
        Polybius square as formatted string
    """
    if alphabet is None:
        alphabet = DEFAULT_VIC_ALPHABET if language == "english" else TURKISH_VIC_ALPHABET
    
    if square_type == "standard":
        return _create_standard_polybius_square(alphabet)
    elif square_type in ["caesar", "atbash", "affine"]:
        # Use shared monoalphabetic square generation
        return create_monoalphabetic_square(square_type, alphabet, mono_params)
    elif square_type == "keyword":
        return _create_keyword_polybius_square(keyword or "SECRET", alphabet)
    else:
        raise ValueError(f"Unsupported square type: {square_type}")

def vic_produce_checkerboard(
    keyword: str,
    alphabet: Optional[str] = None,
    language: Optional[str] = "english"
) -> str:
    """
    Produce a straddling checkerboard for VIC cipher.
    
    Args:
        keyword: Keyword for checkerboard generation
        alphabet: Custom alphabet (None for default)
        language: Language ("english" or "turkish")
        
    Returns:
        Straddling checkerboard as formatted string
    """
    if alphabet is None:
        alphabet = DEFAULT_VIC_ALPHABET if language == "english" else TURKISH_VIC_ALPHABET
    
    return _create_straddling_checkerboard(keyword, alphabet)

def vic_generate_random_key(length: int) -> str:
    """
    Generate a random alphabetic key for VIC cipher.
    
    Args:
        length: Length of key to generate
        
    Returns:
        Random alphabetic key
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def vic_generate_random_numeric_key(length: int) -> str:
    """
    Generate a random numeric key for VIC cipher.
    
    Args:
        length: Length of numeric key to generate
        
    Returns:
        Random numeric key
    """
    return ''.join(random.choices(string.digits, k=length))

def vic_generate_keys_for_text(
    plaintext: str,
    polybius_key_length: int = 6,
    checkerboard_key_length: int = 6,
    transposition_key_length: int = 6,
    numeric_key_length: int = 6
) -> Dict[str, str]:
    """
    Generate all required keys for VIC cipher.
    
    Args:
        plaintext: Text to encrypt (used for key length determination)
        polybius_key_length: Length of Polybius key
        checkerboard_key_length: Length of checkerboard key
        transposition_key_length: Length of transposition key
        numeric_key_length: Length of numeric key
        
    Returns:
        Dictionary containing all generated keys
    """
    return {
        'polybius_key': vic_generate_random_key(polybius_key_length),
        'checkerboard_key': vic_generate_random_key(checkerboard_key_length),
        'transposition_key': vic_generate_random_key(transposition_key_length),
        'numeric_key': vic_generate_random_numeric_key(numeric_key_length)
    }

def vic_encrypt_with_random_keys(
    plaintext: str,
    square_type: str = "standard",
    alphabet: Optional[str] = None,
    language: Optional[str] = "english",
    mono_params: Optional[Dict[str, Any]] = None,
    transposition_passes: int = 1,
    use_chain_addition: bool = False
) -> Tuple[str, Dict[str, str]]:
    """
    Encrypt text using VIC cipher with randomly generated keys.
    
    Args:
        plaintext: Text to encrypt
        square_type: Type of Polybius square
        alphabet: Custom alphabet (None for default)
        language: Language ("english" or "turkish")
        mono_params: Parameters for monoalphabetic transformations
        transposition_passes: Number of transposition passes
        use_chain_addition: Whether to use chain addition
        
    Returns:
        Tuple of (encrypted_text, generated_keys)
    """
    keys = vic_generate_keys_for_text(plaintext)
    
    encrypted = vic_encrypt(
        plaintext,
        keys['polybius_key'],
        keys['checkerboard_key'],
        keys['transposition_key'],
        keys['numeric_key'],
        square_type,
        alphabet,
        language,
        mono_params,
        transposition_passes,
        use_chain_addition
    )
    
    return encrypted, keys

# Helper functions

def _create_standard_polybius_square(alphabet: str) -> str:
    """Create a standard Polybius square."""
    if len(alphabet) < 36:
        raise ValueError("Alphabet must have at least 36 characters for 6x6 square")
    
    # Take first 36 characters and arrange in 6x6 grid
    square_chars = alphabet[:36]
    
    result = []
    for row in range(6):
        row_chars = []
        for col in range(6):
            char_index = row * 6 + col
            if char_index < len(square_chars):
                row_chars.append(square_chars[char_index])
        result.append(''.join(row_chars))
    
    return '\n'.join(result)

def _create_keyword_polybius_square(keyword: str, alphabet: str) -> str:
    """Create a keyword-based Polybius square."""
    if len(alphabet) < 36:
        raise ValueError("Alphabet must have at least 36 characters for 6x6 square")
    
    # Remove duplicates from keyword while preserving order
    keyword_unique = []
    seen = set()
    for char in keyword.lower():
        if char in alphabet and char not in seen:
            keyword_unique.append(char)
            seen.add(char)
    
    # Add remaining alphabet characters
    remaining_chars = []
    for char in alphabet:
        if char not in seen:
            remaining_chars.append(char)
    
    # Combine keyword and remaining characters
    square_chars = keyword_unique + remaining_chars
    
    # Take first 36 characters
    square_chars = square_chars[:36]
    
    result = []
    for row in range(6):
        row_chars = []
        for col in range(6):
            char_index = row * 6 + col
            if char_index < len(square_chars):
                row_chars.append(square_chars[char_index])
        result.append(''.join(row_chars))
    
    return '\n'.join(result)

def _create_straddling_checkerboard(keyword: str, alphabet: str) -> str:
    """Create a straddling checkerboard."""
    if len(alphabet) < 30:
        raise ValueError("Alphabet must have at least 30 characters for checkerboard")
    
    # Remove duplicates from keyword while preserving order
    keyword_unique = []
    seen = set()
    for char in keyword.lower():
        if char in alphabet and char not in seen:
            keyword_unique.append(char)
            seen.add(char)
    
    # Add remaining alphabet characters
    remaining_chars = []
    for char in alphabet:
        if char not in seen:
            remaining_chars.append(char)
    
    # Combine keyword and remaining characters
    checkerboard_chars = keyword_unique + remaining_chars
    
    # Take first 30 characters for 10x3 checkerboard
    checkerboard_chars = checkerboard_chars[:30]
    
    result = []
    for row in range(3):
        row_chars = []
        for col in range(10):
            char_index = row * 10 + col
            if char_index < len(checkerboard_chars):
                row_chars.append(checkerboard_chars[char_index])
        result.append(''.join(row_chars))
    
    return '\n'.join(result)

def _substitute_to_polybius(text: str, square: str) -> str:
    """Substitute text to Polybius pairs."""
    vic_chars = VIC_LETTERS
    pairs = []
    
    for char in text:
        if char in square:
            # Find character position in square
            row, col = _find_char_in_square(square, char)
            if row >= 0 and col >= 0:
                pairs.append(vic_chars[row] + vic_chars[col])
    
    return ''.join(pairs)

def _substitute_from_polybius(pairs: str, square: str) -> str:
    """Substitute Polybius pairs back to text."""
    vic_chars = VIC_LETTERS
    result = []
    
    for i in range(0, len(pairs), 2):
        if i + 1 < len(pairs):
            row_char = pairs[i]
            col_char = pairs[i + 1]
            
            row = vic_chars.find(row_char)
            col = vic_chars.find(col_char)
            
            if row >= 0 and col >= 0:
                char = _get_char_from_square(square, row, col)
                if char:
                    result.append(char)
    
    return ''.join(result)

def _find_char_in_square(square: str, char: str) -> Tuple[int, int]:
    """Find character position in Polybius square."""
    lines = square.split('\n')
    for row, line in enumerate(lines):
        for col, square_char in enumerate(line):
            if square_char == char:
                return row, col
    return -1, -1

def _get_char_from_square(square: str, row: int, col: int) -> Optional[str]:
    """Get character from Polybius square at given position."""
    lines = square.split('\n')
    if 0 <= row < len(lines) and 0 <= col < len(lines[row]):
        return lines[row][col]
    return None

def _pairs_to_digits(pairs: str) -> str:
    """Convert Polybius pairs to digits."""
    vic_chars = VIC_LETTERS
    digits = []
    
    for char in pairs:
        if char in vic_chars:
            digits.append(str(vic_chars.find(char)))
    
    return ''.join(digits)

def _digits_to_pairs(digits: str) -> str:
    """Convert digits to Polybius pairs."""
    vic_chars = VIC_LETTERS
    pairs = []
    
    for digit in digits:
        if digit.isdigit():
            index = int(digit)
            if 0 <= index < len(vic_chars):
                pairs.append(vic_chars[index])
    
    return ''.join(pairs)

def _digits_to_letters(digits: str, checkerboard: str) -> str:
    """Convert digits to letters using straddling checkerboard."""
    lines = checkerboard.split('\n')
    letters = []
    
    i = 0
    while i < len(digits):
        # Try two-digit lookup first (rows 1-2)
        if i + 1 < len(digits):
            row = int(digits[i])
            col = int(digits[i + 1])
            if 1 <= row < len(lines) and 0 <= col < len(lines[row]):
                letters.append(lines[row][col])
                i += 2
                continue
        
        # Single digit lookup (row 0)
        digit = int(digits[i])
        if 0 <= digit < len(lines[0]):
            letters.append(lines[0][digit])
        i += 1
    
    return ''.join(letters)

def _letters_to_digits(letters: str, checkerboard: str) -> str:
    """Convert letters to digits using straddling checkerboard."""
    lines = checkerboard.split('\n')
    digits = []
    
    for letter in letters:
        found = False
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == letter:
                    if row == 0:
                        # Single digit (first row)
                        digits.append(str(col))
                    else:
                        # Two digits (other rows)
                        digits.append(str(row) + str(col))
                    found = True
                    break
            if found:
                break
        
        if not found:
            # Character not found in checkerboard, skip it
            continue
    
    return ''.join(digits)

def _columnar_transposition(text: str, key: str, encrypt: bool = True) -> str:
    """
    Perform columnar transposition.
    
    Args:
        text: Text to transpose
        key: Keyword for columnar arrangement
        encrypt: True for encryption, False for decryption
    """
    if not text or not key:
        raise ValueError("Text and key cannot be empty")
    
    key_upper = key.lower()
    text_len = len(text)
    
    # Get key order (indices sorted by key letters)
    key_indices = sorted(range(len(key_upper)), key=lambda k: key_upper[k])
    
    if encrypt:
        # Encrypt: write by rows, read by columns
        cols = len(key_upper)
        rows = (text_len + cols - 1) // cols  # Ceiling division
        
        # Create grid
        grid = [''] * cols
        for i, char in enumerate(text):
            grid[i % cols] += char
        
        # Read columns in key order
        result = ''.join([grid[i] for i in key_indices])
    else:
        # Decrypt: write by columns, read by rows
        cols = len(key_upper)
        rows = (text_len + cols - 1) // cols
        
        # Distribute text to columns in key order
        grid = [''] * cols
        col_lens = [0] * cols
        pos = 0
        
        for idx in key_indices:
            # Calculate column length based on position in key order
            if text_len % cols == 0:
                # All columns have equal length
                col_len = rows
            else:
                # First (text_len % cols) columns get (rows) chars, rest get (rows-1) chars
                col_len = rows if idx < text_len % cols else rows - 1
            grid[idx] = text[pos:pos + col_len]
            pos += col_len
        
        # Read by rows
        result = ''.join([''.join([grid[j][i] for j in range(cols) if i < len(grid[j])]) 
                         for i in range(rows)])
    
    return result

def _numeric_addition(text: str, numeric_key: str, alphabet: str, encrypt: bool = True) -> str:
    """Apply numeric key addition."""
    if not text or not numeric_key:
        raise ValueError("Text and numeric key cannot be empty")
    
    result = []
    key_len = len(numeric_key)
    
    for i, char in enumerate(text):
        if char in alphabet:
            char_index = alphabet.find(char)
            key_digit = int(numeric_key[i % key_len])
            
            if encrypt:
                new_index = (char_index + key_digit) % len(alphabet)
            else:
                new_index = (char_index - key_digit) % len(alphabet)
            
            result.append(alphabet[new_index])
        else:
            result.append(char)
    
    return ''.join(result)

def _chain_addition_encrypt(text: str, numeric_key: str, alphabet: str) -> str:
    """Apply chain addition encryption."""
    if not text or not numeric_key:
        raise ValueError("Text and numeric key cannot be empty")
    
    result = []
    key_len = len(numeric_key)
    current_key = numeric_key
    
    for i, char in enumerate(text):
        if char in alphabet:
            char_index = alphabet.find(char)
            key_digit = int(current_key[i % key_len])
            
            new_index = (char_index + key_digit) % len(alphabet)
            result.append(alphabet[new_index])
            
            # Update key for next character
            current_key = current_key[1:] + str(new_index)
        else:
            result.append(char)
    
    return ''.join(result)

def _chain_addition_decrypt(text: str, numeric_key: str, alphabet: str) -> str:
    """Apply chain addition decryption."""
    if not text or not numeric_key:
        raise ValueError("Text and numeric key cannot be empty")
    
    result = []
    key_len = len(numeric_key)
    current_key = numeric_key
    
    for i, char in enumerate(text):
        if char in alphabet:
            char_index = alphabet.find(char)
            key_digit = int(current_key[i % key_len])
            
            new_index = (char_index - key_digit) % len(alphabet)
            result.append(alphabet[new_index])
            
            # Update key for next character
            current_key = current_key[1:] + str(new_index)
        else:
            result.append(char)
    
    return ''.join(result)
