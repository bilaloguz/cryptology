"""
Centralized Alphabet Definitions

This module provides standardized alphabet definitions for all ciphers.
All alphabets are lowercase and support UTF-8 for Turkish characters.

Alphabet Standards:
1. All alphabets use lowercase letters
2. All input is converted to lowercase before encryption
3. Turkish uses 29 letters + 7 digits (0-6) for 6x6 squares
4. English uses 26 letters + 10 digits (0-9) for 6x6 squares
5. All alphabets support UTF-8 encoding
"""

# Standard Alphabets (lowercase)

# English Alphabets
ENGLISH_ALPHABET = "abcdefghijklmnopqrstuvwxyz"  # 26 letters
ENGLISH_WITH_DIGITS = "abcdefghijklmnopqrstuvwxyz0123456789"  # 36 chars (for 6x6 squares)
ENGLISH_7X7_SQUARE = "abcdefghijklmnopqrstuvwxyz0123456789.,;:?!\'\"-[]{}"  # 49 chars (perfect 7x7, no duplicates)

# Turkish Alphabets (Two Variants)
TURKISH_STANDARD = "abcçdefgğhıijklmnoöprsştuüvyz"  # 29 letters (original)
TURKISH_EXTENDED = "abcçdefgğhıijklmnoöpqrsştuüvwxyz"  # 32 letters (includes Q,W,X)

# Turkish with digits for different square sizes
TURKISH_STANDARD_WITH_DIGITS = "abcçdefgğhıijklmnoöprsştuüvyz0123456"  # 36 chars (6x6)
TURKISH_EXTENDED_WITH_DIGITS = "abcçdefgğhıijklmnoöpqrsştuüvwxyz0123456789"  # 42 chars (7x7)
TURKISH_EXTENDED_FULL_SQUARE = "abcçdefgğhıijklmnoöpqrsştuüvwxyz0123456789.,;:?!\""  # 49 chars (perfect 7x7, no duplicates)

# Backward compatibility
TURKISH_ALPHABET = TURKISH_STANDARD  # 29 letters
TURKISH_WITH_DIGITS = TURKISH_STANDARD_WITH_DIGITS  # 36 chars

# Default Alphabets for Different Cipher Types
DEFAULT_MONOALPHABETIC_ALPHABET = ENGLISH_ALPHABET
DEFAULT_POLYALPHABETIC_ALPHABET = ENGLISH_ALPHABET
DEFAULT_POLYGRAPHIC_ALPHABET = ENGLISH_ALPHABET
DEFAULT_FRACTIONATED_ALPHABET = ENGLISH_ALPHABET

# Square-based alphabets (for 6x6 and 5x5 squares)
DEFAULT_SQUARE_ALPHABET = ENGLISH_WITH_DIGITS  # For ADFGVX, VIC (6x6)
DEFAULT_TURKISH_SQUARE_ALPHABET = TURKISH_WITH_DIGITS  # For Turkish squares

# Digits only
DIGITS = "0123456789"  # 10 digits

def get_alphabet(language: str = "english", include_digits: bool = False) -> str:
    """
    Get alphabet by language and digit inclusion.
    
    Args:
        language: "english" or "turkish"
        include_digits: Whether to include digits in alphabet
        
    Returns:
        Alphabet string
    """
    if language.lower() == "turkish":
        if include_digits:
            return TURKISH_WITH_DIGITS
        else:
            return TURKISH_ALPHABET
    else:  # english
        if include_digits:
            return ENGLISH_WITH_DIGITS
        else:
            return ENGLISH_ALPHABET

def get_turkish_alphabet(variant: str = "standard", include_digits: bool = False, square_size: str = "6x6") -> str:
    """
    Get Turkish alphabet variant for specific cipher families.
    
    Args:
        variant: "standard" (29 letters) or "extended" (32 letters)
        include_digits: Whether to include digits
        square_size: "6x6" or "7x7" for composite ciphers
        
    Returns:
        Turkish alphabet string
    """
    if variant.lower() == "extended":
        if include_digits:
            if square_size == "7x7":
                return TURKISH_EXTENDED_FULL_SQUARE  # 49 chars
            else:
                return TURKISH_EXTENDED_WITH_DIGITS  # 42 chars
        else:
            return TURKISH_EXTENDED
    else:  # standard
        if include_digits:
            return TURKISH_STANDARD_WITH_DIGITS
        else:
            return TURKISH_STANDARD

def get_alphabet_for_cipher_family(cipher_family: str, language: str = "english", square_size: str = "6x6") -> str:
    """
    Get appropriate alphabet for cipher family.
    
    Args:
        cipher_family: "monoalphabetic", "polyalphabetic", "polygraphic", "fractionated", "composite"
        language: "english" or "turkish"
        square_size: "6x6" or "7x7" for composite ciphers
        
    Returns:
        Alphabet string
    """
    if language.lower() == "turkish":
        if cipher_family.lower() == "composite":
            # Composite ciphers can use extended Turkish with 7x7 squares
            if square_size == "7x7":
                return TURKISH_EXTENDED_FULL_SQUARE  # 49 chars
            else:
                return TURKISH_EXTENDED_WITH_DIGITS  # 42 chars
        else:
            # All other cipher families use standard Turkish
            return TURKISH_STANDARD
    else:  # english
        if cipher_family.lower() == "composite":
            if square_size == "7x7":
                return ENGLISH_7X7_SQUARE  # 49 chars
            else:
                return ENGLISH_WITH_DIGITS  # 36 chars for 6x6
        else:
            return ENGLISH_ALPHABET

def normalize_text(text: str) -> str:
    """
    Normalize text to lowercase for consistent processing.
    
    Args:
        text: Text to normalize
        
    Returns:
        Lowercase text
    """
    return text.lower()

def validate_alphabet(alphabet: str) -> bool:
    """
    Validate alphabet has no duplicate characters.
    
    Args:
        alphabet: Alphabet to validate
        
    Returns:
        True if valid, False otherwise
    """
    return len(alphabet) == len(set(alphabet))

def get_alphabet_length(alphabet: str) -> int:
    """
    Get alphabet length in UTF-8 characters (not bytes).
    
    Args:
        alphabet: Alphabet string
        
    Returns:
        Number of UTF-8 characters
    """
    # For now, return string length
    # TODO: Implement proper UTF-8 character counting
    return len(alphabet)

# Convenience constants for common use cases
LANGUAGE_ALPHABETS = {
    "english": ENGLISH_ALPHABET,
    "turkish": TURKISH_ALPHABET,
}

LANGUAGE_SQUARE_ALPHABETS = {
    "english": ENGLISH_WITH_DIGITS,
    "turkish": TURKISH_WITH_DIGITS,
}
