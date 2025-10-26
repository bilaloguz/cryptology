"""
Porta Cipher implementation.

The Porta cipher is a polyalphabetic substitution cipher that uses a keyword to determine
which alphabet pairs to use for encryption. It divides the alphabet into 13 pairs and
uses the keyword to select between them.

This implementation supports:
- Fixed 13-pair alphabet system (A↔N, B↔O, C↔P, etc.)
- Self-reciprocal encryption/decryption
- Keyword-based encryption (alphabetic keys)
- Custom alphabet support with adapted pairs
- Random key generation for enhanced security
- Case preservation and non-alphabetic character handling
"""

import secrets
import re
from typing import List, Optional, Tuple

DEFAULT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def generate_random_key(length: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Generate a cryptographically secure random alphabetic key.
    
    Args:
        length: Length of the key to generate
        alphabet: The alphabet to use for key generation
        
    Returns:
        A random alphabetic key of the specified length
        
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
    Generate a random alphabetic key matching the plaintext length.
    
    Args:
        plaintext: The text to encrypt (determines key length)
        alphabet: The alphabet to use for key generation
        
    Returns:
        A random alphabetic key matching the plaintext length
    """
    if not plaintext:
        return ""
    
    # Count only alphabetic characters (spaces are preserved in encryption)
    alphabetic_chars = sum(1 for c in plaintext.upper() if c.isalpha())
    return generate_random_key(alphabetic_chars, alphabet)


def encrypt_with_random_key(plaintext: str,
                          alphabet: str = DEFAULT_ALPHABET,
                          key_length: Optional[int] = None) -> Tuple[str, str]:
    """
    Encrypt plaintext using a randomly generated alphabetic key.
    
    Args:
        plaintext: Text to encrypt
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
    encrypted = encrypt(plaintext, key, alphabet)
    
    return encrypted, key


def produce_pairs(pair_type: str = "default", 
                 alphabet: str = DEFAULT_ALPHABET,
                 custom_pairs: Optional[List[Tuple[str, str]]] = None) -> List[Tuple[str, str]]:
    """
    Produce alphabet pairs for the Porta cipher using different strategies.
    
    Args:
        pair_type: Type of pairs to generate ("default", "custom", "turkish", "balanced")
        alphabet: The alphabet to create pairs from
        custom_pairs: User-defined pairs (required for "custom" type)
        
    Returns:
        List of tuples representing alphabet pairs
        
    Raises:
        ValueError: If pair_type is invalid or required parameters are missing
    """
    pair_type = pair_type.lower()
    
    if pair_type == "default":
        return _create_default_pairs(alphabet)
    
    elif pair_type == "custom":
        if not custom_pairs:
            raise ValueError("Custom pairs require 'custom_pairs' parameter")
        return _validate_custom_pairs(custom_pairs, alphabet)
    
    elif pair_type == "turkish":
        return _create_turkish_pairs(alphabet)
    
    elif pair_type == "balanced":
        return _create_balanced_pairs(alphabet)
    
    else:
        raise ValueError(f"Unknown pair type: {pair_type}")


def _create_default_pairs(alphabet: str) -> List[Tuple[str, str]]:
    """
    Create default alphabet pairs for the Porta cipher.
    
    For English (26 letters): Creates 13 pairs (A↔N, B↔O, etc.)
    For other alphabets: Creates pairs based on alphabet length
    
    Args:
        alphabet: The alphabet to create pairs from
        
    Returns:
        List of tuples representing alphabet pairs
    """
    alphabet_len = len(alphabet)
    pairs = []
    
    # For English alphabet (26 letters), create 13 pairs
    if alphabet_len == 26:
        for i in range(13):
            pairs.append((alphabet[i], alphabet[i + 13]))
    else:
        # For other alphabets, create pairs based on length
        pair_count = alphabet_len // 2
        for i in range(pair_count):
            pairs.append((alphabet[i], alphabet[i + pair_count]))
    
    return pairs


def _create_turkish_pairs(alphabet: str) -> List[Tuple[str, str]]:
    """
    Create Turkish-specific alphabet pairs.
    
    Turkish alphabet: ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ (29 letters)
    Creates 14 pairs + 1 unpaired letter (V)
    
    Args:
        alphabet: The alphabet to create pairs from
        
    Returns:
        List of tuples representing Turkish alphabet pairs
    """
    if len(alphabet) != 29:
        # Fall back to default if not Turkish alphabet
        return _create_default_pairs(alphabet)
    
    # Turkish-specific pairs (14 pairs) - proper Turkish alphabet pairs
    # Turkish alphabet: ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ (29 letters)
    # Create 14 pairs, leaving Z unpaired
    turkish_pairs = [
        ("A", "L"), ("B", "M"), ("C", "N"), ("Ç", "O"), ("D", "Ö"),
        ("E", "P"), ("F", "R"), ("G", "S"), ("Ğ", "Ş"), ("H", "T"),
        ("I", "U"), ("İ", "Ü"), ("J", "V"), ("K", "Y")
    ]
    
    # Validate that all pairs exist in the alphabet
    valid_pairs = []
    for pair in turkish_pairs:
        if pair[0] in alphabet and pair[1] in alphabet:
            valid_pairs.append(pair)
    
    return valid_pairs


def _create_balanced_pairs(alphabet: str) -> List[Tuple[str, str]]:
    """
    Create balanced alphabet pairs that distribute letters evenly.
    
    Args:
        alphabet: The alphabet to create pairs from
        
    Returns:
        List of tuples representing balanced alphabet pairs
    """
    alphabet_len = len(alphabet)
    pairs = []
    
    # Create pairs by splitting alphabet in half
    half_len = alphabet_len // 2
    
    for i in range(half_len):
        pairs.append((alphabet[i], alphabet[i + half_len]))
    
    return pairs


def _validate_custom_pairs(custom_pairs: List[Tuple[str, str]], alphabet: str) -> List[Tuple[str, str]]:
    """
    Validate custom pairs and ensure they're valid for the given alphabet.
    
    Args:
        custom_pairs: User-defined pairs
        alphabet: The alphabet to validate against
        
    Returns:
        Validated list of pairs
        
    Raises:
        ValueError: If pairs are invalid
    """
    if not custom_pairs:
        raise ValueError("Custom pairs cannot be empty")
    
    validated_pairs = []
    used_letters = set()
    
    for pair in custom_pairs:
        if len(pair) != 2:
            raise ValueError(f"Each pair must have exactly 2 letters: {pair}")
        
        letter1, letter2 = pair
        
        # Check if letters are in alphabet
        if letter1 not in alphabet:
            raise ValueError(f"Letter '{letter1}' not found in alphabet")
        if letter2 not in alphabet:
            raise ValueError(f"Letter '{letter2}' not found in alphabet")
        
        # Check for duplicates
        if letter1 in used_letters:
            raise ValueError(f"Letter '{letter1}' appears in multiple pairs")
        if letter2 in used_letters:
            raise ValueError(f"Letter '{letter2}' appears in multiple pairs")
        
        used_letters.add(letter1)
        used_letters.add(letter2)
        
        validated_pairs.append((letter1, letter2))
    
    return validated_pairs


def _find_letter_pair(letter: str, pairs: List[Tuple[str, str]]) -> Optional[Tuple[str, str]]:
    """
    Find which pair contains the given letter.
    
    Args:
        letter: The letter to find
        pairs: List of alphabet pairs
        
    Returns:
        The pair containing the letter, or None if not found
    """
    letter_upper = letter.upper()
    for pair in pairs:
        if letter_upper in pair:
            return pair
    return None


def _validate_alphabetic_key(key: str) -> None:
    """
    Validate that the key contains only alphabetic characters.
    
    Args:
        key: The key to validate
        
    Raises:
        ValueError: If key is invalid
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    if not re.match(r'^[A-Za-z]+$', key):
        raise ValueError("Porta key must contain only alphabetic characters")


def _get_pair_index(key_letter: str, alphabet: str) -> int:
    """
    Get the pair index based on the key letter.
    
    For English alphabet: A,B -> 0, C,D -> 1, E,F -> 2, etc.
    
    Args:
        key_letter: The key letter
        alphabet: The alphabet being used
        
    Returns:
        The index of the pair to use
    """
    alphabet_len = len(alphabet)
    letter_pos = alphabet.find(key_letter.upper())
    
    if alphabet_len == 26:
        # English alphabet: pairs are every 2 letters
        return letter_pos // 2
    else:
        # Other alphabets: pairs are every (alphabet_len // 2) letters
        pair_size = alphabet_len // 2
        return letter_pos // pair_size


def encrypt(plaintext: str, 
           key: str, 
           alphabet: str = DEFAULT_ALPHABET,
           pairs: Optional[List[Tuple[str, str]]] = None) -> str:
    """
    Encrypt plaintext using Porta cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Alphabetic key
        alphabet: The alphabet to use
        pairs: Custom alphabet pairs (uses default if None)
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If key is invalid or plaintext is empty
    """
    if not plaintext:
        return ""
    
    _validate_alphabetic_key(key)
    
    # Create alphabet pairs
    if pairs is None:
        pairs = _create_default_pairs(alphabet)
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.upper() in alphabet:
            # Get the pair index from the key
            pair_index = _get_pair_index(key[key_index % len(key)], alphabet)
            
            # Find which pair contains this letter
            letter_pair = _find_letter_pair(char, pairs)
            
            if letter_pair:
                # Determine which letter in the pair to use based on key
                key_letter = key[key_index % len(key)].upper()
                key_pos = alphabet.find(key_letter)
                
                # Use the pair based on key letter position
                if key_pos % 2 == 0:  # Even position (A, C, E, etc.)
                    encrypted_char = letter_pair[1] if char.upper() == letter_pair[0] else letter_pair[0]
                else:  # Odd position (B, D, F, etc.)
                    encrypted_char = letter_pair[0] if char.upper() == letter_pair[0] else letter_pair[1]
                
                # Preserve case
                if char.islower():
                    encrypted_char = encrypted_char.lower()
                
                result.append(encrypted_char)
                key_index += 1
            else:
                # Letter not in any pair, keep as is
                result.append(char)
        else:
            # Preserve non-alphabetic characters
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, 
           key: str, 
           alphabet: str = DEFAULT_ALPHABET,
           pairs: Optional[List[Tuple[str, str]]] = None) -> str:
    """
    Decrypt ciphertext using Porta cipher.
    
    Note: Porta cipher is self-reciprocal, so decryption uses the same algorithm as encryption.
    
    Args:
        ciphertext: Text to decrypt
        key: Alphabetic key
        alphabet: The alphabet to use
        pairs: Custom alphabet pairs (uses default if None)
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If key is invalid or ciphertext is empty
    """
    # Porta cipher is self-reciprocal, so decryption is identical to encryption
    return encrypt(ciphertext, key, alphabet, pairs)
