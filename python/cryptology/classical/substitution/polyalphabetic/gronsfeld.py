"""
Gronsfeld Cipher implementation.

The Gronsfeld cipher is a polyalphabetic substitution cipher that uses numeric keys
instead of alphabetic keys like Vigenère. Each digit in the key specifies how many
positions to shift the corresponding character in the plaintext.

This implementation supports:
- Numeric key validation and handling
- Custom tables generated using monoalphabetic ciphers
- English (26x26) and Turkish (29x29) table sizes
- Composable system with produce_table() method
- On-the-fly table generation for efficiency
- Random numeric key generation for enhanced security
"""

import secrets
import re
from typing import List, Optional, Tuple
from ..monoalphabetic.caesar import produce_alphabet as caesar_produce
from ..monoalphabetic.keyword import produce_alphabet as keyword_produce
from ..monoalphabetic.affine import produce_alphabet as affine_produce
from ..monoalphabetic.atbash import produce_alphabet as atbash_produce

import cryptology.alphabets as ALPHABETS

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET
TURKISH_ALPHABET = ALPHABETS.TURKISH_STANDARD


def generate_random_numeric_key(length: int) -> str:
    """
    Generate a cryptographically secure random numeric key.
    
    Args:
        length: Length of the key to generate
        
    Returns:
        A random numeric key of the specified length
        
    Raises:
        ValueError: If length is not positive
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    # Generate random numeric key using cryptographically secure random
    key = ''.join(secrets.choice('0123456789') for _ in range(length))
    return key


def generate_numeric_key_for_text(plaintext: str) -> str:
    """
    Generate a random numeric key matching the plaintext length.
    
    Args:
        plaintext: The text to encrypt (determines key length)
        
    Returns:
        A random numeric key matching the plaintext length
    """
    if not plaintext:
        return ""
    
    # Count only alphabetic characters (spaces are preserved in encryption)
    alphabetic_chars = sum(1 for c in plaintext.lower() if c.isalpha())
    return generate_random_numeric_key(alphabetic_chars)


def encrypt_with_random_key(plaintext: str,
                          table: Optional[List[List[str]]] = None,
                          alphabet: str = DEFAULT_ALPHABET,
                          key_length: Optional[int] = None) -> Tuple[str, str]:
    """
    Encrypt plaintext using a randomly generated numeric key.
    
    Args:
        plaintext: Text to encrypt
        table: Custom Gronsfeld table (uses classical if None)
        alphabet: The alphabet to use
        key_length: Length of random key (uses text length if None)
        
    Returns:
        Tuple of (encrypted_text, generated_key)
        
    Raises:
        ValueError: If plaintext is empty or key_length is invalid
    """
    if not plaintext:
        raise ValueError("Plaintext cannot be empty")
    
    # Generate random numeric key
    if key_length is None:
        key = generate_numeric_key_for_text(plaintext)
    else:
        key = generate_random_numeric_key(key_length)
    
    # Encrypt using the generated key
    encrypted = encrypt(plaintext, key, table, alphabet)
    
    return encrypted, key


def _create_classical_table(alphabet: str) -> List[List[str]]:
    """
    Create classical Gronsfeld table (same as Vigenère tabula recta).
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the Gronsfeld table
    """
    table = []
    alphabet_len = len(alphabet)
    
    for i in range(alphabet_len):
        row = []
        # Each row is a Caesar shift of the alphabet by i positions
        shifted_alphabet = caesar_produce(i, alphabet)
        for j in range(alphabet_len):
            row.append(shifted_alphabet[j])
        table.append(row)
    
    return table


def _create_caesar_table(alphabet: str, shift: int) -> List[List[str]]:
    """
    Create Gronsfeld table where each row uses Caesar cipher with different shifts.
    
    Args:
        alphabet: The alphabet to use for the table
        shift: The base shift amount
        
    Returns:
        A 2D list representing the Caesar-based Gronsfeld table
    """
    table = []
    alphabet_len = len(alphabet)
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Caesar with shift = (base_shift + row_index) % alphabet_len
        row_shift = (shift + i) % alphabet_len
        shifted_alphabet = caesar_produce(row_shift, alphabet)
        
        for j in range(alphabet_len):
            row.append(shifted_alphabet[j])
        table.append(row)
    
    return table


def _create_affine_table(alphabet: str, a: int, b: int) -> List[List[str]]:
    """
    Create Gronsfeld table where each row uses Affine cipher with different parameters.
    
    Args:
        alphabet: The alphabet to use for the table
        a: The multiplicative key for Affine cipher
        b: The additive key for Affine cipher
        
    Returns:
        A 2D list representing the Affine-based Gronsfeld table
    """
    table = []
    alphabet_len = len(alphabet)
    
    # Ensure base 'a' is coprime with alphabet length
    if a == 0:
        a = 1
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Affine with modified parameters
        row_a = (a + i) % alphabet_len
        row_b = (b + i) % alphabet_len
        
        # Ensure row_a is coprime with alphabet length
        if row_a == 0:
            row_a = 1
        
        # Find next coprime number if needed
        while row_a < alphabet_len and _gcd(row_a, alphabet_len) != 1:
            row_a += 1
        
        # If we can't find a coprime, use 1
        if row_a >= alphabet_len:
            row_a = 1
        
        transformed_alphabet = affine_produce(row_a, row_b, alphabet)
        
        for j in range(alphabet_len):
            row.append(transformed_alphabet[j])
        table.append(row)
    
    return table


def _gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def _create_keyword_table(alphabet: str, keyword: str) -> List[List[str]]:
    """
    Create Gronsfeld table where each row uses Keyword cipher with different keywords.
    
    Args:
        alphabet: The alphabet to use for the table
        keyword: The base keyword for Keyword cipher
        
    Returns:
        A 2D list representing the Keyword-based Gronsfeld table
    """
    table = []
    alphabet_len = len(alphabet)
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Keyword with modified keyword
        row_keyword = keyword + alphabet[i]  # Add row character to keyword
        transformed_alphabet = keyword_produce(row_keyword, alphabet)
        
        for j in range(alphabet_len):
            row.append(transformed_alphabet[j])
        table.append(row)
    
    return table


def _create_atbash_table(alphabet: str) -> List[List[str]]:
    """
    Create Gronsfeld table where each row uses Atbash cipher with different offsets.
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the Atbash-based Gronsfeld table
    """
    table = []
    alphabet_len = len(alphabet)
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Atbash with offset
        reversed_alphabet = atbash_produce(alphabet)
        # Rotate the reversed alphabet by row index
        rotated_alphabet = reversed_alphabet[i:] + reversed_alphabet[:i]
        
        for j in range(alphabet_len):
            row.append(rotated_alphabet[j])
        table.append(row)
    
    return table


def produce_table(table_type: str = "classical", 
                 alphabet: str = DEFAULT_ALPHABET,
                 **kwargs) -> List[List[str]]:
    """
    Produce a Gronsfeld table using different strategies.
    
    Args:
        table_type: Type of table to generate ("classical", "caesar", "affine", "keyword", "atbash")
        alphabet: The alphabet to use for the table
        **kwargs: Additional parameters for specific table types
        
    Returns:
        A 2D list representing the Gronsfeld table
        
    Raises:
        ValueError: If table_type is invalid or required parameters are missing
    """
    table_type = table_type.lower()
    
    if table_type == "classical":
        return _create_classical_table(alphabet)
    
    elif table_type == "caesar":
        shift = kwargs.get('shift')
        if shift is None:
            raise ValueError("Caesar table requires 'shift' parameter")
        return _create_caesar_table(alphabet, shift)
    
    elif table_type == "affine":
        a = kwargs.get('a')
        b = kwargs.get('b')
        if a is None or b is None:
            raise ValueError("Affine table requires 'a' and 'b' parameters")
        return _create_affine_table(alphabet, a, b)
    
    elif table_type == "keyword":
        keyword = kwargs.get('keyword')
        if not keyword:
            raise ValueError("Keyword table requires 'keyword' parameter")
        return _create_keyword_table(alphabet, keyword)
    
    elif table_type == "atbash":
        return _create_atbash_table(alphabet)
    
    else:
        raise ValueError(f"Unknown table type: {table_type}")


def _find_char_position(alphabet: str, char: str) -> int:
    """
    Find position of character in alphabet.
    
    Args:
        alphabet: Alphabet to search in
        char: Character to find
        
    Returns:
        Position of character (0-based)
        
    Raises:
        ValueError: If character not found
    """
    char_upper = char.lower()
    try:
        return alphabet.index(char_upper)
    except ValueError:
        raise ValueError(f"Character '{char}' not found in alphabet")


def _validate_numeric_key(key: str) -> None:
    """
    Validate that the key contains only digits.
    
    Args:
        key: The key to validate
        
    Raises:
        ValueError: If key is invalid
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    if not re.match(r'^[0-9]+$', key):
        raise ValueError("Gronsfeld key must contain only digits (0-9)")


def encrypt(plaintext: str, 
           key: str, 
           table: Optional[List[List[str]]] = None,
           alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Gronsfeld cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Numeric key (digits only)
        table: Custom Gronsfeld table (uses classical if None)
        alphabet: The alphabet to use
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If key is invalid or plaintext is empty
    """
    if not plaintext:
        return ""
    
    _validate_numeric_key(key)
    
    # Use classical table if none provided
    if table is None:
        table = _create_classical_table(alphabet)
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.lower() in alphabet:
            # Get the shift value from the numeric key
            shift = int(key[key_index % len(key)])
            
            # Find character position in alphabet
            char_pos = _find_char_position(alphabet, char)
            
            # Apply shift using the table
            encrypted_char = table[shift][char_pos]
            
            # Preserve case
            if char.islower():
                encrypted_char = encrypted_char.lower()
            
            result.append(encrypted_char)
            key_index += 1
        else:
            # Preserve non-alphabetic characters
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, 
           key: str, 
           table: Optional[List[List[str]]] = None,
           alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Gronsfeld cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Numeric key (digits only)
        table: Custom Gronsfeld table (uses classical if None)
        alphabet: The alphabet to use
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If key is invalid or ciphertext is empty
    """
    if not ciphertext:
        return ""
    
    _validate_numeric_key(key)
    
    # Use classical table if none provided
    if table is None:
        table = _create_classical_table(alphabet)
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.lower() in alphabet:
            # Get the shift value from the numeric key
            shift = int(key[key_index % len(key)])
            
            # Find character position in the shifted alphabet (table row)
            char_pos = _find_char_position(table[shift], char)
            
            # Get original character from base alphabet
            decrypted_char = alphabet[char_pos]
            
            # Preserve case
            if char.islower():
                decrypted_char = decrypted_char.lower()
            
            result.append(decrypted_char)
            key_index += 1
        else:
            # Preserve non-alphabetic characters
            result.append(char)
    
    return ''.join(result)
