"""
Vigenère Cipher implementation.

The Vigenère cipher is a polyalphabetic substitution cipher that uses a table
where each row is a different Caesar cipher. This implementation supports:

- Classical Vigenère table (tabula recta) as default
- Custom tables generated using monoalphabetic ciphers
- English (26x26) and Turkish (29x29) table sizes
- Composable system with produce_table() method
- On-the-fly table generation for efficiency
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
        table: Custom Vigenère table (uses classical if None)
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
    Create classical Vigenère table (tabula recta).
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the Vigenère table
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
    Create Vigenère table where each row uses Caesar cipher with different shifts.
    
    Args:
        alphabet: The alphabet to use for the table
        shift: The base shift amount
        
    Returns:
        A 2D list representing the Caesar-based Vigenère table
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
    Create Vigenère table where each row uses Affine cipher with different parameters.
    
    Args:
        alphabet: The alphabet to use for the table
        a: The multiplicative parameter
        b: The additive parameter
        
    Returns:
        A 2D list representing the Affine-based Vigenère table
    """
    table = []
    alphabet_len = len(alphabet)
    
    for i in range(alphabet_len):
        row = []
        # Each row uses Affine with b = (base_b + row_index) % alphabet_len
        row_b = (b + i) % alphabet_len
        transformed_alphabet = affine_produce(a, row_b, alphabet)
        
        for j in range(alphabet_len):
            row.append(transformed_alphabet[j])
        table.append(row)
    
    return table


def _create_keyword_table(alphabet: str, keyword: str) -> List[List[str]]:
    """
    Create Vigenère table where each row uses Keyword cipher with different keywords.
    
    Args:
        alphabet: The alphabet to use for the table
        keyword: The base keyword
        
    Returns:
        A 2D list representing the Keyword-based Vigenère table
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
    Create Vigenère table where each row uses Atbash cipher with different offsets.
    
    Args:
        alphabet: The alphabet to use for the table
        
    Returns:
        A 2D list representing the Atbash-based Vigenère table
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
    Produce a Vigenère table using different strategies.
    
    Args:
        table_type: Type of table to generate ("classical", "caesar", "affine", "keyword", "atbash")
        alphabet: The alphabet to use for the table
        **kwargs: Additional parameters for specific table types
        
    Returns:
        A 2D list representing the Vigenère table
        
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
    char_upper = char.upper()
    for i, c in enumerate(alphabet):
        if c.upper() == char_upper:
            return i
    raise ValueError(f"Character '{char}' not found in alphabet")


def _prepare_ciphertext(text: str, alphabet: str) -> str:
    """
    Prepare ciphertext for decryption by cleaning and handling special cases.
    
    Args:
        text: The input text
        alphabet: The alphabet being used
        
    Returns:
        Cleaned text ready for decryption
    """
    text_clean = ""
    for char in text.upper():
        if char.isalpha():
            text_clean += char
        elif char == ' ':
            # Preserve spaces
            text_clean += char
    
    return text_clean


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
        elif char == ' ':
            # Preserve spaces
            text_clean += char
    
    return text_clean


def encrypt(plaintext: str, 
           key: str,
           table: Optional[List[List[str]]] = None,
           alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Vigenère cipher.
    
    Args:
        plaintext: Text to encrypt
        key: The Vigenère key
        table: Custom Vigenère table (uses classical if None)
        alphabet: The alphabet to use
        
    Returns:
        Encrypted text
    """
    if not plaintext or not key:
        return ""
    
    # Generate table if not provided
    if table is None:
        table = produce_table("classical", alphabet)
    
    # Prepare text and key
    plaintext_clean = _prepare_text(plaintext, alphabet)
    key_clean = _prepare_text(key, alphabet)
    
    if not plaintext_clean or not key_clean:
        return ""
    
    # Encrypt using Vigenère method
    result = ""
    key_index = 0
    
    for char in plaintext_clean:
        if char == ' ':
            # Preserve spaces
            result += char
        else:
            try:
                # Find character positions
                plain_pos = _find_char_position(alphabet, char)
                key_pos = _find_char_position(alphabet, key_clean[key_index % len(key_clean)])
                
                # Get cipher character from table
                cipher_char = table[key_pos][plain_pos]
                result += cipher_char
                
                # Move to next key character
                key_index += 1
                
            except ValueError:
                # Skip characters not in alphabet
                continue
    
    return result


def decrypt(ciphertext: str,
           key: str,
           table: Optional[List[List[str]]] = None,
           alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Vigenère cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: The Vigenère key
        table: Custom Vigenère table (uses classical if None)
        alphabet: The alphabet to use
        
    Returns:
        Decrypted text
    """
    if not ciphertext or not key:
        return ""
    
    # Generate table if not provided
    if table is None:
        table = produce_table("classical", alphabet)
    
    # Prepare text and key
    ciphertext_clean = _prepare_ciphertext(ciphertext, alphabet)
    key_clean = _prepare_text(key, alphabet)
    
    if not ciphertext_clean or not key_clean:
        return ""
    
    # Decrypt using Vigenère method
    result = ""
    key_index = 0
    
    for char in ciphertext_clean:
        if char == ' ':
            # Preserve spaces
            result += char
        else:
            try:
                # Find key position
                key_pos = _find_char_position(alphabet, key_clean[key_index % len(key_clean)])
                
                # Find cipher character in table row
                cipher_pos = _find_char_position(table[key_pos], char)
                
                # Get plain character from alphabet
                plain_char = alphabet[cipher_pos]
                result += plain_char
                
                # Move to next key character
                key_index += 1
                
            except ValueError:
                # Skip characters not in alphabet
                continue
    
    return result
