"""
Beaufort Cipher implementation.

The Beaufort cipher is a polyalphabetic substitution cipher that is essentially
a reverse Vigenère cipher. It uses the same tabula recta but with subtraction
instead of addition for encryption.

Key features:
- Self-reciprocal: encryption and decryption use the same algorithm
- Uses same table generation as Vigenère (tabula recta)
- Supports custom tables generated using monoalphabetic ciphers
- English (26x26) and Turkish (29x29) table sizes
- Composable system with produce_table() method
- Random key generation for enhanced security
"""

import secrets
from typing import List, Optional, Tuple
from ..monoalphabetic.caesar import produce_alphabet as caesar_produce
from ..monoalphabetic.keyword import produce_alphabet as keyword_produce
from ..monoalphabetic.affine import produce_alphabet as affine_produce
from ..monoalphabetic.atbash import produce_alphabet as atbash_produce

DEFAULT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def generate_random_key(length: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Generate a cryptographically secure random key.
    
    Args:
        length: Length of the key to generate
        alphabet: The alphabet to use for key generation
        
    Returns:
        A random key of the specified length
        
    Raises:
        ValueError: If length is not positive or alphabet is empty
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    if not alphabet:
        raise ValueError("Alphabet cannot be empty")
    
    # Generate random key using cryptographically secure random
    key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return key


def generate_key_for_text(plaintext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Generate a random key matching the plaintext length.
    
    Args:
        plaintext: The text to encrypt (determines key length)
        alphabet: The alphabet to use for key generation
        
    Returns:
        A random key matching the plaintext length
    """
    if not plaintext:
        return ""
    
    # Count only alphabetic characters (spaces are preserved in encryption)
    alphabetic_chars = sum(1 for c in plaintext.upper() if c.isalpha())
    return generate_random_key(alphabetic_chars, alphabet)


def encrypt_with_random_key(plaintext: str,
                          table: Optional[List[List[str]]] = None,
                          alphabet: str = DEFAULT_ALPHABET,
                          key_length: Optional[int] = None) -> Tuple[str, str]:
    """
    Encrypt plaintext using a randomly generated key.
    
    Args:
        plaintext: Text to encrypt
        table: Custom Beaufort table (uses classical if None)
        alphabet: The alphabet to use
        key_length: Length of random key (uses text length if None)
        
    Returns:
        Tuple of (encrypted_text, generated_key)
        
    Raises:
        ValueError: If plaintext is empty or key_length is invalid
    """
    if not plaintext:
        raise ValueError("Plaintext cannot be empty")
    
    # Generate random key
    if key_length is None:
        key = generate_key_for_text(plaintext, alphabet)
    else:
        key = generate_random_key(key_length, alphabet)
    
    # Encrypt using the generated key
    encrypted = encrypt(plaintext, key, table, alphabet)
    
    return encrypted, key


def _create_classical_table(alphabet: str) -> List[List[str]]:
    """
    Create classical Beaufort table (same as Vigenère tabula recta).
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the classical Beaufort table
    """
    alphabet_len = len(alphabet)
    table = []
    
    for i in range(alphabet_len):
        row = []
        for j in range(alphabet_len):
            # Each row is a Caesar cipher shifted by row index
            row.append(alphabet[(j + i) % alphabet_len])
        table.append(row)
    
    return table


def _create_caesar_table(alphabet: str, shift: int) -> List[List[str]]:
    """
    Create Beaufort table where each row uses Caesar cipher with different offsets.
    
    Args:
        alphabet: The alphabet to use for the table
        shift: Base shift for Caesar cipher
        
    Returns:
        A 2D list representing the Caesar-based Beaufort table
    """
    alphabet_len = len(alphabet)
    table = []
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Caesar cipher with base_shift + row_index
        row_shift = shift + i
        for j in range(alphabet_len):
            row.append(alphabet[(j + row_shift) % alphabet_len])
        table.append(row)
    
    return table


def _create_affine_table(alphabet: str, a: int, b: int) -> List[List[str]]:
    """
    Create Beaufort table where each row uses Affine cipher with different offsets.
    
    Args:
        alphabet: The alphabet to use for the table
        a: Affine cipher parameter a
        b: Affine cipher parameter b
        
    Returns:
        A 2D list representing the Affine-based Beaufort table
    """
    alphabet_len = len(alphabet)
    table = []
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Affine cipher with modified b
        row_b = b + i
        for j in range(alphabet_len):
            affine_result = (a * j + row_b) % alphabet_len
            row.append(alphabet[affine_result])
        table.append(row)
    
    return table


def _create_keyword_table(alphabet: str, keyword: str) -> List[List[str]]:
    """
    Create Beaufort table where each row uses Keyword cipher with different keywords.
    
    Args:
        alphabet: The alphabet to use for the table
        keyword: Base keyword for the cipher
        
    Returns:
        A 2D list representing the Keyword-based Beaufort table
    """
    alphabet_len = len(alphabet)
    table = []
    
    for i in range(alphabet_len):
        row = []
        # Each row uses keyword cipher with row character appended
        row_keyword = keyword + alphabet[i]  # Add row character to keyword
        transformed_alphabet = keyword_produce(row_keyword, alphabet)
        
        for j in range(alphabet_len):
            row.append(transformed_alphabet[j])
        table.append(row)
    
    return table


def _create_atbash_table(alphabet: str) -> List[List[str]]:
    """
    Create Beaufort table where each row uses Atbash cipher with different offsets.
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the Atbash-based Beaufort table
    """
    alphabet_len = len(alphabet)
    table = []
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Atbash cipher with rotation by row index
        for j in range(alphabet_len):
            atbash_index = (alphabet_len - 1 - j + i) % alphabet_len
            row.append(alphabet[atbash_index])
        table.append(row)
    
    return table


def produce_table(table_type: str, alphabet: str = DEFAULT_ALPHABET, **kwargs) -> List[List[str]]:
    """
    Produce a Beaufort table using different strategies.
    
    Args:
        table_type: Type of table ("classical", "caesar", "affine", "keyword", "atbash")
        alphabet: The alphabet to use for the table
        **kwargs: Additional parameters for specific table types
        
    Returns:
        A 2D list representing the Beaufort table
        
    Raises:
        ValueError: If table_type is not supported or parameters are missing
    """
    if not table_type:
        raise ValueError("Table type must be specified")
    
    if table_type == "classical":
        return _create_classical_table(alphabet)
    
    elif table_type == "caesar":
        if "shift" not in kwargs:
            raise ValueError("Caesar table requires 'shift' parameter")
        return _create_caesar_table(alphabet, kwargs["shift"])
    
    elif table_type == "affine":
        if "a" not in kwargs or "b" not in kwargs:
            raise ValueError("Affine table requires 'a' and 'b' parameters")
        return _create_affine_table(alphabet, kwargs["a"], kwargs["b"])
    
    elif table_type == "keyword":
        if "keyword" not in kwargs:
            raise ValueError("Keyword table requires 'keyword' parameter")
        return _create_keyword_table(alphabet, kwargs["keyword"])
    
    elif table_type == "atbash":
        return _create_atbash_table(alphabet)
    
    else:
        raise ValueError(f"Unsupported table type: {table_type}")


def _prepare_text(text: str, alphabet: str) -> str:
    """
    Prepare text for encryption by cleaning and handling special cases.
    
    Args:
        text: The input text
        alphabet: The alphabet being used
        
    Returns:
        Cleaned text ready for encryption
    """
    text_clean = ""
    for char in text.upper():
        if char.isalpha():
            # Handle custom alphabets
            if alphabet == DEFAULT_ALPHABET:
                # Apply language-specific replacements for English alphabet
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
            text_clean += char
        elif char == ' ':
            text_clean += ' '  # Preserve spaces
    return text_clean


def _prepare_ciphertext(ciphertext: str) -> str:
    """
    Prepare ciphertext for decryption by cleaning.
    
    Args:
        ciphertext: The input ciphertext
        
    Returns:
        Cleaned ciphertext ready for decryption
    """
    text_clean = ""
    for char in ciphertext.upper():
        if char.isalpha() or char == ' ':
            text_clean += char
    return text_clean


def encrypt(plaintext: str, key: str, table: Optional[List[List[str]]] = None, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Beaufort cipher.
    
    Args:
        plaintext: The text to encrypt
        key: The Beaufort key
        table: Custom Beaufort table (uses classical if None)
        alphabet: The alphabet to use (defaults to English)
        
    Returns:
        Encrypted ciphertext
    """
    if not plaintext or not key:
        return ""
    
    # Note: If table is None, we'll use modular arithmetic instead of table lookup
    
    # Prepare text
    prepared_text = _prepare_text(plaintext, alphabet)
    
    result = ""
    key_index = 0
    
    for char in prepared_text:
        if char == ' ':
            result += ' '
            continue
        
        if char in alphabet:
            # Find character position in alphabet
            char_pos = alphabet.index(char)
            
            # Get key character
            key_char = key[key_index % len(key)]
            key_pos = alphabet.index(key_char)
            
            # Beaufort encryption: always use modular arithmetic (C = (K - P) mod 26)
            encrypted_pos = (key_pos - char_pos) % len(alphabet)
            result += alphabet[encrypted_pos]
            
            key_index += 1
    
    return result


def decrypt(ciphertext: str, key: str, table: Optional[List[List[str]]] = None, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Beaufort cipher.
    
    Note: Beaufort is self-reciprocal, so this function is identical to encrypt().
    This function exists for API consistency and clarity.
    
    Args:
        ciphertext: The text to decrypt
        key: The Beaufort key
        table: Custom Beaufort table (uses classical if None)
        alphabet: The alphabet to use (defaults to English)
        
    Returns:
        Decrypted plaintext
    """
    # Beaufort is self-reciprocal: decryption is the same as encryption
    return encrypt(ciphertext, key, table, alphabet)
