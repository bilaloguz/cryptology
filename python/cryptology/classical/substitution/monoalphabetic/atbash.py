"""
Atbash Cipher implementation.

The Atbash cipher is a monoalphabetic substitution cipher where the alphabet is reversed.
The first letter is replaced with the last, the second with the second-to-last, and so on.
Like ROT13, it is symmetric - encrypting twice returns the original text.
"""

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encrypt(plaintext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Atbash cipher.
    
    Args:
        plaintext: The text to encrypt (will be converted to lowercase)
        alphabet: The alphabet to use for encryption (default: English lowercase)
    
    Returns:
        The encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO")
        'svool'
    """
    # Convert input to lowercase
    plaintext = plaintext.lower()
    result = []
    
    for char in plaintext:
        if char in alphabet:
            # Find position in alphabet
            pos = alphabet.index(char)
            # Reverse position: first <-> last, second <-> second-to-last, etc.
            reversed_pos = len(alphabet) - 1 - pos
            result.append(alphabet[reversed_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Atbash cipher.
    
    Since Atbash reverses the alphabet, encrypting twice returns
    the original text. Therefore, decrypt is the same as encrypt.
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Example:
        >>> decrypt("svool")
        'hello'
    """
    return encrypt(ciphertext, alphabet)


def produce_alphabet(alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Produce an Atbash-reversed alphabet.
    
    This method creates a custom alphabet by reversing the base alphabet.
    The produced alphabet can be used with polygraphic ciphers for enhanced security.
    
    Args:
        alphabet: The base alphabet to reverse (default: English lowercase)
    
    Returns:
        An Atbash-reversed alphabet
    
    Example:
        >>> produce_alphabet()
        'zyxwvutsrqponmlkjihgfedcba'
        >>> produce_alphabet("abc")
        'cba'
    """
    return alphabet[::-1]

