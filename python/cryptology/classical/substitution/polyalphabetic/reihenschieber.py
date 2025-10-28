"""
Reihenschieber Cipher Implementation

A mechanical polyalphabetic substitution cipher that uses shifting strips.
Essentially a mechanical Vigenère cipher with progressive shifting capabilities.

Features:
- Multiple shift modes: fixed, progressive, custom
- Shift directions: forward (default), backward
- Custom alphabets support (English, Turkish, etc.)
- Random key generation
- Self-reciprocal encryption/decryption
"""

import random
import string
from typing import List, Optional, Union


def reihenschieber_encrypt(
    plaintext: str,
    key: str,
    alphabet: Optional[str] = None,
    shift_mode: str = "fixed",
    shift_direction: str = "forward",
    shift_amount: int = 1,
    custom_shifts: Optional[List[int]] = None
) -> str:
    """
    Encrypt text using the Reihenschieber cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Encryption key (repeats as needed)
        alphabet: Custom alphabet (default: English)
        shift_mode: "fixed", "progressive", or "custom"
        shift_direction: "forward" or "backward"
        shift_amount: Amount to shift (for fixed/progressive modes)
        custom_shifts: List of custom shift values (for custom mode)
    
    Returns:
        Encrypted text
    """
    if not plaintext or not key:
        return ""
    
    if alphabet is None:
        alphabet = string.ascii_uppercase
    
    # Prepare text and key
    text = plaintext.lower()
    key_upper = key.lower()
    alphabet_upper = alphabet.lower()
    
    # Validate inputs
    if not all(c in alphabet_upper for c in text):
        raise ValueError("Plaintext contains characters not in alphabet")
    if not all(c in alphabet_upper for c in key_upper):
        raise ValueError("Key contains characters not in alphabet")
    
    result = []
    key_index = 0
    cumulative_shift = 0
    
    for i, char in enumerate(text):
        if char not in alphabet_upper:
            result.append(char)
            continue
        
        # Get current key character
        current_key = key_upper[key_index % len(key_upper)]
        key_index += 1
        
        # Calculate shift based on mode
        if shift_mode == "fixed":
            current_shift = shift_amount
        elif shift_mode == "progressive":
            current_shift = shift_amount
            cumulative_shift += current_shift
        elif shift_mode == "custom":
            if custom_shifts is None or i >= len(custom_shifts):
                current_shift = 0
            else:
                current_shift = custom_shifts[i]
        else:
            raise ValueError(f"Invalid shift_mode: {shift_mode}")
        
        # Apply shift direction
        if shift_direction == "backward":
            current_shift = -current_shift
        
        # Calculate final shift
        if shift_mode == "progressive":
            final_shift = cumulative_shift
        else:
            final_shift = current_shift
        
        # Encrypt character
        char_index = alphabet_upper.index(char)
        key_index_pos = alphabet_upper.index(current_key)
        
        # Apply Vigenère-like encryption with additional shift
        encrypted_index = (char_index + key_index_pos + final_shift) % len(alphabet_upper)
        encrypted_char = alphabet_upper[encrypted_index]
        
        result.append(encrypted_char)
    
    return ''.join(result)


def reihenschieber_decrypt(
    ciphertext: str,
    key: str,
    alphabet: Optional[str] = None,
    shift_mode: str = "fixed",
    shift_direction: str = "forward",
    shift_amount: int = 1,
    custom_shifts: Optional[List[int]] = None
) -> str:
    """
    Decrypt text using the Reihenschieber cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Decryption key (repeats as needed)
        alphabet: Custom alphabet (default: English)
        shift_mode: "fixed", "progressive", or "custom"
        shift_direction: "forward" or "backward"
        shift_amount: Amount to shift (for fixed/progressive modes)
        custom_shifts: List of custom shift values (for custom mode)
    
    Returns:
        Decrypted text
    """
    if not ciphertext or not key:
        return ""
    
    if alphabet is None:
        alphabet = string.ascii_uppercase
    
    # Prepare text and key
    text = ciphertext.lower()
    key_upper = key.lower()
    alphabet_upper = alphabet.lower()
    
    # Validate inputs
    if not all(c in alphabet_upper for c in text):
        raise ValueError("Ciphertext contains characters not in alphabet")
    if not all(c in alphabet_upper for c in key_upper):
        raise ValueError("Key contains characters not in alphabet")
    
    result = []
    key_index = 0
    cumulative_shift = 0
    
    for i, char in enumerate(text):
        if char not in alphabet_upper:
            result.append(char)
            continue
        
        # Get current key character
        current_key = key_upper[key_index % len(key_upper)]
        key_index += 1
        
        # Calculate shift based on mode
        if shift_mode == "fixed":
            current_shift = shift_amount
        elif shift_mode == "progressive":
            current_shift = shift_amount
            cumulative_shift += current_shift
        elif shift_mode == "custom":
            if custom_shifts is None or i >= len(custom_shifts):
                current_shift = 0
            else:
                current_shift = custom_shifts[i]
        else:
            raise ValueError(f"Invalid shift_mode: {shift_mode}")
        
        # Apply shift direction
        if shift_direction == "backward":
            current_shift = -current_shift
        
        # Calculate final shift
        if shift_mode == "progressive":
            final_shift = cumulative_shift
        else:
            final_shift = current_shift
        
        # Decrypt character
        char_index = alphabet_upper.index(char)
        key_index_pos = alphabet_upper.index(current_key)
        
        # Apply Vigenère-like decryption with additional shift
        decrypted_index = (char_index - key_index_pos - final_shift) % len(alphabet_upper)
        decrypted_char = alphabet_upper[decrypted_index]
        
        result.append(decrypted_char)
    
    return ''.join(result)


def reihenschieber_generate_random_key(length: int) -> str:
    """
    Generate a random key for Reihenschieber cipher.
    
    Args:
        length: Length of the key to generate
    
    Returns:
        Random key string
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def reihenschieber_generate_key_for_text(text_length: int) -> str:
    """
    Generate a key of appropriate length for the given text.
    
    Args:
        text_length: Length of the text to encrypt
    
    Returns:
        Random key string
    """
    if text_length <= 0:
        raise ValueError("Text length must be positive")
    
    # Generate key length between 3 and min(text_length, 10)
    key_length = random.randint(3, min(text_length, 10))
    return reihenschieber_generate_random_key(key_length)


def reihenschieber_encrypt_with_random_key(
    plaintext: str,
    key_length: Optional[int] = None
) -> tuple[str, str]:
    """
    Encrypt text with a randomly generated key.
    
    Args:
        plaintext: Text to encrypt
        key_length: Length of key to generate (default: auto)
    
    Returns:
        Tuple of (encrypted_text, generated_key)
    """
    if not plaintext:
        return "", ""
    
    if key_length is None:
        key_length = random.randint(3, min(len(plaintext), 10))
    
    generated_key = reihenschieber_generate_random_key(key_length)
    encrypted = reihenschieber_encrypt(plaintext, generated_key)
    
    return encrypted, generated_key


def reihenschieber_produce_custom_shifts(
    pattern_type: str = "alternating",
    pattern_length: int = 10,
    **kwargs
) -> List[int]:
    """
    Produce custom shift patterns for Reihenschieber cipher.
    
    Args:
        pattern_type: Type of pattern ("alternating", "fibonacci", "prime", "random")
        pattern_length: Length of the pattern
        **kwargs: Additional parameters for specific patterns
    
    Returns:
        List of shift values
    """
    if pattern_length <= 0:
        raise ValueError("Pattern length must be positive")
    
    if pattern_type == "alternating":
        # Alternating positive and negative shifts
        return [1 if i % 2 == 0 else -1 for i in range(pattern_length)]
    
    elif pattern_type == "fibonacci":
        # Fibonacci-like pattern
        shifts = [1, 1]
        for i in range(2, pattern_length):
            shifts.append(shifts[i-1] + shifts[i-2])
        return shifts[:pattern_length]
    
    elif pattern_type == "prime":
        # Prime number pattern
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        return [primes[i % len(primes)] for i in range(pattern_length)]
    
    elif pattern_type == "random":
        # Random shifts between -5 and 5
        return [random.randint(-5, 5) for _ in range(pattern_length)]
    
    else:
        raise ValueError(f"Invalid pattern_type: {pattern_type}")


# Turkish alphabet support
TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def reihenschieber_encrypt_turkish(
    plaintext: str,
    key: str,
    shift_mode: str = "fixed",
    shift_direction: str = "forward",
    shift_amount: int = 1,
    custom_shifts: Optional[List[int]] = None
) -> str:
    """
    Encrypt Turkish text using Reihenschieber cipher.
    
    Args:
        plaintext: Turkish text to encrypt
        key: Encryption key
        shift_mode: "fixed", "progressive", or "custom"
        shift_direction: "forward" or "backward"
        shift_amount: Amount to shift
        custom_shifts: List of custom shift values
    
    Returns:
        Encrypted Turkish text
    """
    return reihenschieber_encrypt(
        plaintext, key, TURKISH_ALPHABET, shift_mode, 
        shift_direction, shift_amount, custom_shifts
    )


def reihenschieber_decrypt_turkish(
    ciphertext: str,
    key: str,
    shift_mode: str = "fixed",
    shift_direction: str = "forward",
    shift_amount: int = 1,
    custom_shifts: Optional[List[int]] = None
) -> str:
    """
    Decrypt Turkish text using Reihenschieber cipher.
    
    Args:
        ciphertext: Turkish text to decrypt
        key: Decryption key
        shift_mode: "fixed", "progressive", or "custom"
        shift_direction: "forward" or "backward"
        shift_amount: Amount to shift
        custom_shifts: List of custom shift values
    
    Returns:
        Decrypted Turkish text
    """
    return reihenschieber_decrypt(
        ciphertext, key, TURKISH_ALPHABET, shift_mode, 
        shift_direction, shift_amount, custom_shifts
    )
