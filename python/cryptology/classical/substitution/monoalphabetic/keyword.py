"""
Keyword Cipher implementation.

The keyword cipher is a monoalphabetic substitution cipher where a keyword is used
to create the cipher alphabet. The keyword (with duplicates removed) is written first,
followed by the remaining letters of the alphabet in order.
"""

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _create_cipher_alphabet(keyword: str, alphabet: str) -> str:
    """
    Create cipher alphabet from keyword.
    
    Args:
        keyword: The keyword to use (will be converted to lowercase)
        alphabet: The base alphabet
    
    Returns:
        The cipher alphabet with keyword first, then remaining letters
    """
    keyword = keyword.lower()
    seen = set()
    cipher_alphabet = []
    
    # Add keyword letters (removing duplicates)
    for char in keyword:
        if char in alphabet and char not in seen:
            cipher_alphabet.append(char)
            seen.add(char)
    
    # Add remaining alphabet letters
    for char in alphabet:
        if char not in seen:
            cipher_alphabet.append(char)
    
    return ''.join(cipher_alphabet)


def encrypt(plaintext: str, keyword: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Keyword cipher.
    
    Args:
        plaintext: The text to encrypt (will be converted to lowercase)
        keyword: The keyword to use for creating cipher alphabet
        alphabet: The alphabet to use for encryption (default: English lowercase)
    
    Returns:
        The encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO", "zebra")
        'dclla'
    """
    # Convert input to lowercase
    plaintext = plaintext.lower()
    
    # Create cipher alphabet from keyword
    cipher_alphabet = _create_cipher_alphabet(keyword, alphabet)
    
    result = []
    for char in plaintext:
        if char in alphabet:
            # Find position in plain alphabet
            pos = alphabet.index(char)
            # Replace with character from cipher alphabet
            result.append(cipher_alphabet[pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, keyword: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Keyword cipher.
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        keyword: The keyword that was used for encryption
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Example:
        >>> decrypt("dclla", "zebra")
        'hello'
    """
    # Convert input to lowercase
    ciphertext = ciphertext.lower()
    
    # Create cipher alphabet from keyword
    cipher_alphabet = _create_cipher_alphabet(keyword, alphabet)
    
    result = []
    for char in ciphertext:
        if char in cipher_alphabet:
            # Find position in cipher alphabet
            pos = cipher_alphabet.index(char)
            # Replace with character from plain alphabet
            result.append(alphabet[pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)

