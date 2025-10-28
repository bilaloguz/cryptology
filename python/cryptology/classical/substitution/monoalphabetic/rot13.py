"""
ROT13 Cipher implementation.

ROT13 is a special case of the Caesar cipher where the shift is always 13.
Since there are 26 letters in the alphabet, applying ROT13 twice returns the original text.
This makes it useful for obscuring text (like spoilers) while being easily reversible.

Note: ROT13 only makes sense for alphabets with an even number of characters,
where the shift is half the alphabet size.
"""

from cryptology import alphabets as ALPHABETS

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET


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
    shift = 13  # Fixed shift value (ROT13)
    
    for char in plaintext:
        if char in alphabet:
            # Find position in alphabet
            pos = alphabet.index(char)
            # Shift by 13 positions
            new_pos = (pos + shift) % len(alphabet)
            result.append(alphabet[new_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using ROT13.
    
    Since ROT13 shifts by 13, decryption shifts by -13.
    For English alphabet with 26 letters, ROT13 is self-reciprocal (encrypt twice).
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Example:
        >>> decrypt("URYYB")
        'hello'
    """
    # Convert input to lowercase
    ciphertext = ciphertext.lower()
    result = []
    shift = 13  # Fixed shift value (ROT13)
    
    for char in ciphertext:
        if char in alphabet:
            # Find position in alphabet
            pos = alphabet.index(char)
            # Shift back by 13 positions (decryption)
            new_pos = (pos - shift) % len(alphabet)
            result.append(alphabet[new_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)

