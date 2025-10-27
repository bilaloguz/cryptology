"""
ADFGVX and ADFGVZX Cipher Implementations

The ADFGVX cipher was used by the German Army during World War I.
It combines substitution (via a Polybius square) with fractionation
through specific letters (A, D, F, G, V, X) and columnar transposition.

ADFGVZX is an extension that adds fractionation with an extra pair of letters.
"""

import random
import string
from typing import Optional, Tuple, Dict

from ..polygraphic.monoalphabetic_squares import create_monoalphabetic_square


# Default square characters for ADFGVX
ADFGVX_LETTERS = "ADFGVX"
ADFGVZX_LETTERS = "ADFGVZX"  # Extension with additional Z letter

# Standard 6x6 square for ADFGVX/ADFGVZX (A-Z + 0-9)
DEFAULT_ADFGVX_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Turkish alphabet for ADFGVX (29 letters + 7 digits = 36 characters for 6x6)
TURKISH_ADFGVX_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456"


def adfgvx_encrypt(
    plaintext: str,
    key: str,
    square: Optional[str] = None,
    alphabet: Optional[str] = None,
    mono_params: Optional[Dict] = None
) -> str:
    """
    Encrypt text using the ADFGVX cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Keyword for columnar transposition
        square: Optional 6×6 Polybius square (default: standard)
        alphabet: Alphabet to use ("english" or "turkish", default: "english")
        mono_params: Parameters for monoalphabetic square generation
    
    Returns:
        Encrypted ciphertext
    """
    if not plaintext or not key:
        raise ValueError("Plaintext and key cannot be empty")
    
    # Determine alphabet to use
    use_alphabet = DEFAULT_ADFGVX_ALPHABET
    if alphabet and alphabet.lower() == "turkish":
        use_alphabet = TURKISH_ADFGVX_ALPHABET
    
    # Clean plaintext
    plaintext = plaintext.upper().replace(' ', '')
    
    # Handle Turkish-specific letter combinations/reductions if needed
    if alphabet and alphabet.lower() == "turkish":
        # Turkish I and İ are distinct, but we might need I=İ combination
        plaintext = plaintext  # Keep as is for now
    
    # Generate or use provided square
    if square is None:
        # Determine language for square generation
        language = "turkish" if alphabet and alphabet.lower() == "turkish" else "english"
        if mono_params:
            mono_params["language"] = language
        else:
            mono_params = {"language": language}
        square = adfgvx_produce_square("standard", language=language)
    
    # Step 1: Substitution - convert letters to ADFGVX pairs
    substituted = _substitute_to_adfgvx(plaintext, square)
    
    # Step 2: Columnar transposition
    ciphertext = _columnar_transposition(substituted, key, encrypt=True)
    
    return ciphertext


def adfgvx_decrypt(
    ciphertext: str,
    key: str,
    square: Optional[str] = None,
    alphabet: Optional[str] = None,
    mono_params: Optional[Dict] = None
) -> str:
    """
    Decrypt text using the ADFGVX cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Keyword for columnar transposition
        square: Optional 6×6 Polybius square (default: standard)
        alphabet: Alphabet to use ("english" or "turkish", default: "english")
        mono_params: Parameters for monoalphabetic square generation
    
    Returns:
        Decrypted plaintext
    """
    if not ciphertext or not key:
        raise ValueError("Ciphertext and key cannot be empty")
    
    # Determine alphabet to use
    use_alphabet = DEFAULT_ADFGVX_ALPHABET
    if alphabet and alphabet.lower() == "turkish":
        use_alphabet = TURKISH_ADFGVX_ALPHABET
    
    # Generate or use provided square
    if square is None:
        # Determine language for square generation
        language = "turkish" if alphabet and alphabet.lower() == "turkish" else "english"
        square = adfgvx_produce_square("standard", language=language)
    
    # Step 1: Reverse columnar transposition
    substituted = _columnar_transposition(ciphertext, key, encrypt=False)
    
    # Step 2: Reverse substitution - convert ADFGVX pairs back to letters
    plaintext = _substitute_from_adfgvx(substituted, square)
    
    return plaintext


def adfgvx_produce_square(
    square_type: str = "standard",
    keyword: Optional[str] = None,
    alphabet: Optional[str] = None,
    language: Optional[str] = "english",
    mono_params: Optional[Dict] = None
) -> str:
    """
    Produce a 6×6 Polybius square for ADFGVX cipher.
    
    Args:
        square_type: Type of square ("standard", "frequency", "keyword", 
                    "custom", "caesar", "atbash", "affine")
        keyword: Keyword for keyword-based square
        alphabet: Custom alphabet (if provided, overrides language)
        language: Language to use ("english" or "turkish")
        mono_params: Parameters for monoalphabetic-based squares
    
    Returns:
        Square string representation
    """
    if alphabet is None:
        # Use language-based alphabet
        if language and language.lower() == "turkish":
            alphabet = TURKISH_ADFGVX_ALPHABET
        else:
            alphabet = DEFAULT_ADFGVX_ALPHABET
    
    alphabet_upper = alphabet.upper()
    
    if square_type == "standard":
        return _create_standard_adfgvx_square(alphabet_upper)
    elif square_type == "frequency":
        return _create_frequency_adfgvx_square(alphabet_upper)
    elif square_type == "keyword":
        if not keyword:
            raise ValueError("Keyword required for keyword-based square")
        return _create_keyword_adfgvx_square(keyword, alphabet_upper)
    elif square_type == "custom":
        return _create_custom_adfgvx_square(alphabet_upper)
    elif square_type in ["caesar", "atbash", "affine"]:
        # Use shared monoalphabetic square generation
        # Create proper mono_params from the square_type
        if square_type == "caesar":
            use_mono_params = mono_params or {"shift": 3}
        elif square_type == "affine":
            use_mono_params = mono_params or {"a": 5, "b": 7}  # 5 is coprime with 36
        else:
            use_mono_params = None
        
        return create_monoalphabetic_square(square_type, alphabet_upper, use_mono_params)
    else:
        raise ValueError(f"Invalid square_type: {square_type}")


def _create_standard_adfgvx_square(alphabet: str = DEFAULT_ADFGVX_ALPHABET) -> str:
    """Create a standard alphabetical 6×6 square."""
    alphabet_upper = alphabet.upper()
    
    # Take first 36 characters
    square_letters = alphabet_upper[:36]
    
    # Pad to 36 if needed
    while len(square_letters) < 36:
        square_letters += alphabet_upper[0]
    
    # Create 6×6 square
    square_lines = []
    for i in range(6):
        start_idx = i * 6
        end_idx = start_idx + 6
        square_lines.append(square_letters[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_frequency_adfgvx_square(alphabet: str = DEFAULT_ADFGVX_ALPHABET) -> str:
    """Create a frequency-based 6×6 square."""
    alphabet_upper = alphabet.upper()
    
    # English frequency order (A-Z, 0-9)
    frequency_order = "ETAOINSHRDLCUMWFGYPBVKXJQZ0123456789"
    
    # Take letters in frequency order
    square_letters = ""
    used = set()
    
    for char in frequency_order:
        if char in alphabet_upper and char not in used:
            square_letters += char
            used.add(char)
    
    # Add remaining characters
    for char in alphabet_upper:
        if char not in used:
            square_letters += char
            used.add(char)
    
    # Take first 36 characters
    square_letters = square_letters[:36]
    
    # Create 6×6 square
    square_lines = []
    for i in range(6):
        start_idx = i * 6
        end_idx = start_idx + 6
        square_lines.append(square_letters[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_keyword_adfgvx_square(keyword: str, alphabet: str = DEFAULT_ADFGVX_ALPHABET) -> str:
    """Create a keyword-based 6×6 square."""
    alphabet_upper = alphabet.upper()
    keyword_upper = keyword.upper()
    
    # Remove duplicates from keyword
    keyword_unique = ""
    for char in keyword_upper:
        if char.isalnum() and char not in keyword_unique:
            keyword_unique += char
    
    # Add remaining alphabet letters
    remaining = ""
    for char in alphabet_upper:
        if char not in keyword_unique:
            remaining += char
    
    square_letters = keyword_unique + remaining
    
    # Take first 36 characters
    square_letters = square_letters[:36]
    
    # Create 6×6 square
    square_lines = []
    for i in range(6):
        start_idx = i * 6
        end_idx = start_idx + 6
        square_lines.append(square_letters[start_idx:end_idx])
    
    return '\n'.join(square_lines)


def _create_custom_adfgvx_square(alphabet: str = DEFAULT_ADFGVX_ALPHABET) -> str:
    """Create a custom 6×6 square based on alphabet."""
    return _create_standard_adfgvx_square(alphabet)


def _substitute_to_adfgvx(text: str, square: str) -> str:
    """Convert text to ADFGVX pairs using the square."""
    # Parse square into dict
    square_dict = _parse_square(square)
    
    # Convert to ADFGVX pairs
    pairs = []
    for char in text:
        if char.upper() in square_dict:
            row_col = square_dict[char.upper()]
            row_char = ADFGVX_LETTERS[row_col[0]]
            col_char = ADFGVX_LETTERS[row_col[1]]
            pairs.append(row_char + col_char)
        else:
            raise ValueError(f"Character '{char}' not found in square")
    
    return ''.join(pairs)


def _substitute_from_adfgvx(pairs: str, square: str) -> str:
    """Convert ADFGVX pairs back to text using the square."""
    # Parse square into dict for reverse lookup
    reverse_dict = _parse_square_reverse(square)
    
    # Convert pairs back to letters
    text = ""
    for i in range(0, len(pairs), 2):
        if i + 1 < len(pairs):
            row_char = pairs[i]
            col_char = pairs[i + 1]
            
            row_idx = ADFGVX_LETTERS.index(row_char)
            col_idx = ADFGVX_LETTERS.index(col_char)
            
            if (row_idx, col_idx) in reverse_dict:
                text += reverse_dict[(row_idx, col_idx)]
            else:
                raise ValueError(f"Invalid pair: {row_char}{col_char}")
    
    return text


def _parse_square(square: str) -> Dict[str, Tuple[int, int]]:
    """Parse square string into character to (row, col) mapping."""
    lines = square.strip().split('\n')
    result = {}
    
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char.isalnum():
                result[char] = (row_idx, col_idx)
    
    return result


def _parse_square_reverse(square: str) -> Dict[Tuple[int, int], str]:
    """Parse square string into (row, col) to character mapping."""
    lines = square.strip().split('\n')
    result = {}
    
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char.isalnum():
                result[(row_idx, col_idx)] = char
    
    return result


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
    
    key_upper = key.upper()
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


def adfgvx_generate_random_key(length: int) -> str:
    """
    Generate a random keyword for ADFGVX cipher.
    
    Args:
        length: Desired key length
    
    Returns:
        Random alphabetic key
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    return ''.join(random.choices(string.ascii_uppercase, k=length))


if __name__ == "__main__":
    # Test
    plaintext = "HELLO"
    key = "SECRET"
    
    square = adfgvx_produce_square("standard")
    encrypted = adfgvx_encrypt(plaintext, key, square)
    decrypted = adfgvx_decrypt(encrypted, key, square)
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {decrypted == plaintext}")
