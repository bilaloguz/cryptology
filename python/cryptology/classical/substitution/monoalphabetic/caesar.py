"""
Caesar Cipher implementation.

The Caesar cipher is one of the simplest and most widely known encryption techniques.
It is a type of substitution cipher where each letter in the plaintext is shifted
a certain number of places down the alphabet.
"""

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encrypt(plaintext: str, shift: int = 3, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Caesar cipher.
    
    Args:
        plaintext: The text to encrypt (will be converted to lowercase)
        shift: The number of positions to shift (default: 3)
        alphabet: The alphabet to use for encryption (default: English lowercase)
    
    Returns:
        The encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO", 3)
        'khoor'
        >>> encrypt("abc", 1)
        'bcd'
    """
    # Convert input to lowercase
    plaintext = plaintext.lower()
    result = []
    
    for char in plaintext:
        if char in alphabet:
            # Find position in alphabet
            pos = alphabet.index(char)
            # Shift the character
            new_pos = (pos + shift) % len(alphabet)
            result.append(alphabet[new_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, shift: int = 3, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Caesar cipher.
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        shift: The number of positions that were shifted (default: 3)
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Example:
        >>> decrypt("KHOOR", 3)
        'hello'
    """
    return encrypt(ciphertext, -shift, alphabet)

