"""
Scytale (Spartan Stick) Cipher implementation.

The Scytale cipher is one of the oldest known transposition ciphers,
used by the ancient Spartans around 400 BC. It involves wrapping a
leather strip around a cylindrical rod, writing the message along
the length of the rod, and then unwrapping it to reveal the cipher.

Modern implementation uses a matrix approach where we:
1. Write text in rows based on key (wrapping around rod)
2. Read it column by column (unwrapping from rod)

Args:
    text: Plaintext or ciphertext to encrypt/decrypt
    key: The diameter of the rod (number of columns)
    encrypt: True for encryption, False for decryption

The key determines how many columns to use, which corresponds
to the diameter of the cylindrical rod used in ancient times.
"""


def encrypt(plaintext: str, key: int) -> str:
    """
    Encrypt plaintext using Scytale cipher.
    
    Args:
        plaintext: Text to encrypt (case-insensitive, removes non-alphabetic)
        key: Number of columns (diameter of the rod)
    
    Returns:
        Encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO WORLD", 3)
        'HLWL OEOLRDL'
        >>> encrypt("CRYPTOGRAPHY", 4)
        'CYY ARG THPROG P'
    """
    if key <= 0:
        raise ValueError("Key must be positive")
    
    # Clean and normalize text to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    if not text:
        return ""
    
    # Calculate number of rows
    rows = (len(text) + key - 1) // key  # Ceiling division
    
    # Create matrix: write text row by row, filling with spaces if needed
    matrix = []
    text_index = 0
    
    for row in range(rows):
        row_text = []
        for col in range(key):
            if text_index < len(text):
                row_text.append(text[text_index])
                text_index += 1
            else:
                row_text.append(' ')  # Padding with space
        matrix.append(row_text)
    
    # Read column by column (unwrapping from rod)
    result = []
    for col in range(key):
        for row in range(rows):
            result.append(matrix[row][col])
    
    return ''.join(result).strip()


def decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypt ciphertext using Scytale cipher.
    
    Args:
        ciphertext: Encrypted text
        key: Number of columns (diameter of the rod)
    
    Returns:
        Decrypted plaintext
    
    Example:
        >>> decrypt("HLWL OEOLRDL", 3)
        'HELLOWORLD'
    """
    if key <= 0:
        raise ValueError("Key must be positive")
    
    # Clean the ciphertext to lowercase
    text = ciphertext.lower()
    
    if not text:
        return ""
    
    # Reverse the process: read column by column, write row by row
    rows = len(text) // key
    if len(text) % key != 0:
        rows += 1
    
    # Create matrix: write text column by column
    matrix = [[' ' for _ in range(key)] for _ in range(rows)]
    text_index = 0
    
    for col in range(key):
        for row in range(rows):
            if text_index < len(text):
                matrix[row][col] = text[text_index]
                text_index += 1
    
    # Read row by row
    result = []
    for row in range(rows):
        for col in range(key):
            result.append(matrix[row][col])
    
    return ''.join(result).strip()


def get_key_range(text_length: int) -> tuple:
    """
    Get the valid range of keys for a given text length.
    
    Args:
        text_length: Length of the text
    
    Returns:
        Tuple of (min_key, max_key)
    """
    if text_length <= 0:
        return (0, 0)
    return (1, text_length)


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("SCYTALE CIPHER - Spartan Stick Cipher")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    key = 3
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Key:        {key}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, key)
    decrypted = decrypt(encrypted, key)
    
    print(f"\nEncrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    # Test with different key
    print("\n" + "=" * 60)
    plaintext2 = "CRYPTOGRAPHY"
    key2 = 4
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Key:        {key2}")
    
    encrypted2 = encrypt(plaintext2, key2)
    decrypted2 = decrypt(encrypted2, key2)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == plaintext2}")

