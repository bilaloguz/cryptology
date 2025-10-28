"""
Straddling Checkerboard Cipher Implementation

A composite cipher that combines substitution and fractionation techniques.
Uses a 10×3 grid to convert letters to digits, then applies numeric key addition.

Features:
- Custom checkerboard generation
- Multiple checkerboard types: standard, keyword-based, custom
- Numeric key support with random generation
- Turkish alphabet support (29 letters → 3×10 grid)
- Composite encryption: substitution + fractionation + key addition
"""

import random
import string
from typing import Dict, List, Optional, Tuple


def straddling_checkerboard_encrypt(
    plaintext: str,
    key: str,
    checkerboard: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Encrypt text using the Straddling Checkerboard cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Encryption key (numeric string for numeric keys)
        checkerboard: Custom checkerboard (default: standard)
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Encrypted text
    """
    if not plaintext or not key:
        return ""
    
    if checkerboard is None:
        checkerboard = _create_standard_checkerboard()
    
    # Prepare text
    text = plaintext.lower().replace(" ", "")
    
    # Step 1: Convert letters to digits using checkerboard
    digits = _letters_to_digits(text, checkerboard)
    if not digits:
        return ""
    
    # Step 2: Apply key addition
    if key_type == "numeric":
        encrypted_digits = _apply_numeric_key(digits, key)
    else:
        encrypted_digits = _apply_alphabetic_key(digits, key, checkerboard)
    
    # Step 3: Convert digits back to letters
    result = _digits_to_letters(encrypted_digits, checkerboard)
    
    return result


def straddling_checkerboard_decrypt(
    ciphertext: str,
    key: str,
    checkerboard: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Decrypt text using the Straddling Checkerboard cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Decryption key (numeric string for numeric keys)
        checkerboard: Custom checkerboard (default: standard)
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Decrypted text
    """
    if not ciphertext or not key:
        return ""
    
    if checkerboard is None:
        checkerboard = _create_standard_checkerboard()
    
    # Prepare text
    text = ciphertext.lower().replace(" ", "")
    
    # Step 1: Convert letters to digits using checkerboard
    digits = _letters_to_digits(text, checkerboard)
    if not digits:
        return ""
    
    # Step 2: Apply key subtraction (reverse of addition)
    if key_type == "numeric":
        decrypted_digits = _apply_numeric_key(digits, key, reverse=True)
    else:
        decrypted_digits = _apply_alphabetic_key(digits, key, checkerboard, reverse=True)
    
    # Step 3: Convert digits back to letters
    result = _digits_to_letters(decrypted_digits, checkerboard)
    
    return result


def straddling_checkerboard_produce_checkerboard(
    checkerboard_type: str = "standard",
    keyword: Optional[str] = None,
    alphabet: Optional[str] = None
) -> str:
    """
    Produce a checkerboard for Straddling Checkerboard cipher.
    
    Args:
        checkerboard_type: Type of checkerboard ("standard", "frequency", "vowel_consonant", "keyword", "custom")
        keyword: Keyword for keyword-based checkerboard
        alphabet: Custom alphabet (default: English)
    
    Returns:
        Checkerboard string representation
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase
    
    if checkerboard_type == "standard":
        return _create_standard_checkerboard()
    elif checkerboard_type == "frequency":
        return _create_frequency_checkerboard(alphabet)
    elif checkerboard_type == "vowel_consonant":
        return _create_vowel_consonant_checkerboard(alphabet)
    elif checkerboard_type == "keyword":
        if not keyword:
            raise ValueError("Keyword required for keyword-based checkerboard")
        return _create_keyword_checkerboard(keyword, alphabet)
    elif checkerboard_type == "custom":
        return _create_custom_checkerboard(alphabet)
    else:
        raise ValueError(f"Invalid checkerboard_type: {checkerboard_type}")


def straddling_checkerboard_generate_random_key(
    length: int,
    key_type: str = "numeric"
) -> str:
    """
    Generate a random key for Straddling Checkerboard cipher.
    
    Args:
        length: Length of the key to generate
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Random key string
    """
    if length <= 0:
        raise ValueError("Key length must be positive")
    
    if key_type == "numeric":
        return ''.join(random.choices(string.digits, k=length))
    elif key_type == "alphabetic":
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    else:
        raise ValueError(f"Invalid key_type: {key_type}")


def straddling_checkerboard_generate_key_for_text(
    text_length: int,
    key_type: str = "numeric"
) -> str:
    """
    Generate a key of appropriate length for the given text.
    
    Args:
        text_length: Length of the text to encrypt
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Random key string
    """
    if text_length <= 0:
        raise ValueError("Text length must be positive")
    
    # Generate key length between 3 and min(text_length, 10)
    key_length = random.randint(3, min(text_length, 10))
    return straddling_checkerboard_generate_random_key(key_length, key_type)


def straddling_checkerboard_encrypt_with_random_key(
    plaintext: str,
    key_length: Optional[int] = None,
    key_type: str = "numeric"
) -> Tuple[str, str]:
    """
    Encrypt text with a randomly generated key.
    
    Args:
        plaintext: Text to encrypt
        key_length: Length of key to generate (default: auto)
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Tuple of (encrypted_text, generated_key)
    """
    if not plaintext:
        return "", ""
    
    if key_length is None:
        key_length = random.randint(3, min(len(plaintext), 10))
    
    generated_key = straddling_checkerboard_generate_random_key(key_length, key_type)
    encrypted = straddling_checkerboard_encrypt(plaintext, generated_key, key_type=key_type)
    
    return encrypted, generated_key


# Helper functions

def _create_standard_checkerboard() -> str:
    """Create a standard 10×3 checkerboard."""
    # Standard checkerboard with letters A-Z and digits 0-9
    # Row 0: 0 1 2 3 4 5 6 7 8 9
    # Row 1: A B C D E F G H I J
    # Row 2: K L M N O P Q R S T
    # Row 3: U V W X Y Z (straddling positions)
    
    checkerboard = {}
    
    # Row 0: digits
    for i in range(10):
        checkerboard[str(i)] = str(i)
    
    # Row 1: A-J
    for i, letter in enumerate("ABCDEFGHIJ"):
        checkerboard[letter] = str(i)
    
    # Row 2: K-T
    for i, letter in enumerate("KLMNOPQRST"):
        checkerboard[letter] = "1" + str(i)
    
    # Row 3: U-Z (straddling)
    for i, letter in enumerate("UVWXYZ"):
        checkerboard[letter] = "2" + str(i)
    
    return _checkerboard_to_string(checkerboard)


def _create_keyword_checkerboard(keyword: str, alphabet: str) -> str:
    """Create a keyword-based checkerboard."""
    keyword_upper = keyword.lower()
    alphabet_upper = alphabet.lower()
    
    # Remove duplicates from keyword while preserving order
    keyword_chars = []
    seen = set()
    for char in keyword_upper:
        if char in alphabet_upper and char not in seen:
            keyword_chars.append(char)
            seen.add(char)
    
    # Add remaining alphabet characters
    remaining_chars = [char for char in alphabet_upper if char not in seen]
    all_chars = keyword_chars + remaining_chars
    
    checkerboard = {}
    
    # Row 0: digits
    for i in range(10):
        checkerboard[str(i)] = str(i)
    
    # Distribute letters across rows
    row1_chars = all_chars[:10]  # First 10 letters
    row2_chars = all_chars[10:20]  # Next 10 letters
    row3_chars = all_chars[20:]  # Remaining letters
    
    # Row 1
    for i, letter in enumerate(row1_chars):
        checkerboard[letter] = str(i)
    
    # Row 2
    for i, letter in enumerate(row2_chars):
        checkerboard[letter] = "1" + str(i)
    
    # Row 3 (straddling)
    for i, letter in enumerate(row3_chars):
        checkerboard[letter] = "2" + str(i)
    
    return _checkerboard_to_string(checkerboard)


def _create_custom_checkerboard(alphabet: str) -> str:
    """Create a custom checkerboard for the given alphabet."""
    alphabet_upper = alphabet.lower()
    
    checkerboard = {}
    
    # Row 0: digits
    for i in range(10):
        checkerboard[str(i)] = str(i)
    
    # Distribute letters across rows
    row1_chars = alphabet_upper[:10]  # First 10 letters
    row2_chars = alphabet_upper[10:20]  # Next 10 letters
    row3_chars = alphabet_upper[20:]  # Remaining letters
    
    # Row 1
    for i, letter in enumerate(row1_chars):
        checkerboard[letter] = str(i)
    
    # Row 2
    for i, letter in enumerate(row2_chars):
        checkerboard[letter] = "1" + str(i)
    
    # Row 3 (straddling)
    for i, letter in enumerate(row3_chars):
        checkerboard[letter] = "2" + str(i)
    
    return _checkerboard_to_string(checkerboard)


def _create_frequency_checkerboard(alphabet: str) -> str:
    """Create a frequency-based checkerboard for the given alphabet."""
    alphabet_upper = alphabet.lower()
    
    # Define frequency-based letter orders for English and Turkish
    if alphabet_upper == "abcdefghijklmnopqrstuvwxyz":
        # English frequency order (most to least frequent)
        frequency_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    elif alphabet_upper == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        # Turkish frequency order (most to least frequent)
        frequency_order = "AENRLDKMSUTOYBGHCÇPFVZŞĞÖÜJ"
    else:
        # For other alphabets, use alphabetical order
        frequency_order = alphabet_upper
    
    checkerboard = {}
    
    # Row 0: digits
    for i in range(10):
        checkerboard[str(i)] = str(i)
    
    # Distribute letters across rows based on frequency
    row1_chars = frequency_order[:10]  # Most frequent 10 letters
    row2_chars = frequency_order[10:20]  # Next 10 letters
    row3_chars = frequency_order[20:]  # Remaining letters
    
    # Row 1 (most frequent - single digit)
    for i, letter in enumerate(row1_chars):
        checkerboard[letter] = str(i)
    
    # Row 2 (medium frequency - two digits starting with 1)
    for i, letter in enumerate(row2_chars):
        checkerboard[letter] = "1" + str(i)
    
    # Row 3 (least frequent - two digits starting with 2)
    for i, letter in enumerate(row3_chars):
        checkerboard[letter] = "2" + str(i)
    
    return _checkerboard_to_string(checkerboard)


def _create_vowel_consonant_checkerboard(alphabet: str) -> str:
    """Create a vowel-consonant separation checkerboard."""
    alphabet_upper = alphabet.lower()
    
    # Define vowels and consonants
    if alphabet_upper == "abcdefghijklmnopqrstuvwxyz":
        vowels = "AEIOU"
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    elif alphabet_upper == "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ":
        vowels = "AEIOUÖÜ"
        consonants = "BCÇDFGĞHJKLMNPRSŞTVYZ"
    else:
        # For other alphabets, separate vowels and consonants
        vowels = "AEIOU"
        consonants = "".join(c for c in alphabet_upper if c not in vowels)
    
    checkerboard = {}
    
    # Row 0: digits
    for i in range(10):
        checkerboard[str(i)] = str(i)
    
    # Distribute vowels and consonants across rows
    row1_chars = vowels[:10]  # Vowels first
    remaining_vowels = vowels[10:] if len(vowels) > 10 else ""
    consonants_start = consonants[:10-len(remaining_vowels)]
    row1_chars += consonants_start
    
    row2_chars = consonants[len(consonants_start):20]  # Next consonants
    row3_chars = consonants[20:]  # Remaining consonants
    
    # Row 1
    for i, letter in enumerate(row1_chars):
        checkerboard[letter] = str(i)
    
    # Row 2
    for i, letter in enumerate(row2_chars):
        checkerboard[letter] = "1" + str(i)
    
    # Row 3
    for i, letter in enumerate(row3_chars):
        checkerboard[letter] = "2" + str(i)
    
    return _checkerboard_to_string(checkerboard)


def _checkerboard_to_string(checkerboard: Dict[str, str]) -> str:
    """Convert checkerboard dictionary to string representation."""
    # Format: "char1:digit1,char2:digit2,..."
    return ",".join([f"{char}:{digit}" for char, digit in sorted(checkerboard.items())])


def _string_to_checkerboard(checkerboard_str: str) -> Dict[str, str]:
    """Convert string representation to checkerboard dictionary."""
    checkerboard = {}
    for pair in checkerboard_str.split(","):
        if ":" in pair:
            char, digit = pair.split(":", 1)
            checkerboard[char] = digit
    return checkerboard


def _letters_to_digits(text: str, checkerboard: str) -> str:
    """Convert letters to digits using checkerboard."""
    checkerboard_dict = _string_to_checkerboard(checkerboard)
    digits = []
    
    for char in text:
        if char in checkerboard_dict:
            digits.append(checkerboard_dict[char])
        else:
            # Skip unknown characters
            continue
    
    return "".join(digits)


def _digits_to_letters(digits: str, checkerboard: str) -> str:
    """Convert digits to letters using checkerboard."""
    checkerboard_dict = _string_to_checkerboard(checkerboard)
    
    # Create reverse mapping
    reverse_checkerboard = {digit: char for char, digit in checkerboard_dict.items()}
    
    letters = []
    i = 0
    while i < len(digits):
        # Try 2-digit first (for straddling positions)
        if i + 1 < len(digits):
            two_digit = digits[i:i+2]
            if two_digit in reverse_checkerboard:
                letters.append(reverse_checkerboard[two_digit])
                i += 2
                continue
        
        # Try 1-digit
        one_digit = digits[i]
        if one_digit in reverse_checkerboard:
            letters.append(reverse_checkerboard[one_digit])
        
        i += 1
    
    return "".join(letters)


def _apply_numeric_key(digits: str, key: str, reverse: bool = False) -> str:
    """Apply numeric key addition/subtraction to digits."""
    key_digits = key.replace(" ", "")
    result_digits = []
    
    for i, digit in enumerate(digits):
        key_digit = int(key_digits[i % len(key_digits)])
        digit_value = int(digit)
        
        if reverse:
            # Subtraction for decryption
            result_value = (digit_value - key_digit) % 10
        else:
            # Addition for encryption
            result_value = (digit_value + key_digit) % 10
        
        result_digits.append(str(result_value))
    
    return "".join(result_digits)


def _apply_alphabetic_key(digits: str, key: str, checkerboard: str, reverse: bool = False) -> str:
    """Apply alphabetic key to digits."""
    checkerboard_dict = _string_to_checkerboard(checkerboard)
    key_upper = key.lower()
    
    result_digits = []
    
    for i, digit in enumerate(digits):
        key_char = key_upper[i % len(key_upper)]
        
        if key_char in checkerboard_dict:
            key_digit = int(checkerboard_dict[key_char])
            digit_value = int(digit)
            
            if reverse:
                # Subtraction for decryption
                result_value = (digit_value - key_digit) % 10
            else:
                # Addition for encryption
                result_value = (digit_value + key_digit) % 10
            
            result_digits.append(str(result_value))
        else:
            # Skip if key character not in checkerboard
            result_digits.append(digit)
    
    return "".join(result_digits)


# Turkish alphabet support
TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def straddling_checkerboard_encrypt_turkish(
    plaintext: str,
    key: str,
    checkerboard: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Encrypt Turkish text using Straddling Checkerboard cipher.
    
    Args:
        plaintext: Turkish text to encrypt
        key: Encryption key
        checkerboard: Custom checkerboard (default: Turkish)
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Encrypted Turkish text
    """
    if checkerboard is None:
        checkerboard = _create_custom_checkerboard(TURKISH_ALPHABET)
    
    return straddling_checkerboard_encrypt(plaintext, key, checkerboard, key_type)


def straddling_checkerboard_decrypt_turkish(
    ciphertext: str,
    key: str,
    checkerboard: Optional[str] = None,
    key_type: str = "numeric"
) -> str:
    """
    Decrypt Turkish text using Straddling Checkerboard cipher.
    
    Args:
        ciphertext: Turkish text to decrypt
        key: Decryption key
        checkerboard: Custom checkerboard (default: Turkish)
        key_type: Type of key ("numeric" or "alphabetic")
    
    Returns:
        Decrypted Turkish text
    """
    if checkerboard is None:
        checkerboard = _create_custom_checkerboard(TURKISH_ALPHABET)
    
    return straddling_checkerboard_decrypt(ciphertext, key, checkerboard, key_type)
