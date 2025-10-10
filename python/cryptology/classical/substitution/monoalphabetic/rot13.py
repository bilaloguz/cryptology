"""
ROT13 Cipher implementation.

ROT13 is a special case of the Caesar cipher where the shift is always 13.
Since there are 26 letters in the alphabet, applying ROT13 twice returns the original text.
This makes it useful for obscuring text (like spoilers) while being easily reversible.

Note: ROT13 only makes sense for alphabets with an even number of characters,
where the shift is half the alphabet size.
"""

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encrypt(plaintext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using ROT13.
    
    Args:
        plaintext: The text to encrypt (will be converted to lowercase)
        alphabet: The alphabet to use for encryption (default: English lowercase)
    
    Returns:
        The encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO")
        'uryyb'
    """
    # Convert input to lowercase
    plaintext = plaintext.lower()
    result = []
    shift = len(alphabet) // 2  # Half of the alphabet
    
    for char in plaintext:
        if char in alphabet:
            # Find position in alphabet
            pos = alphabet.index(char)
            # Shift by half the alphabet
            new_pos = (pos + shift) % len(alphabet)
            result.append(alphabet[new_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using ROT13.
    
    Since ROT13 shifts by half the alphabet, encrypting twice returns
    the original text. Therefore, decrypt is the same as encrypt.
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Example:
        >>> decrypt("URYYB")
        'hello'
    """
    return encrypt(ciphertext, alphabet)

