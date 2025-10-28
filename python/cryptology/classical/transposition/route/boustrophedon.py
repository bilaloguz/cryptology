"""
Boustrophedon Transposition Cipher implementation.

Boustrophedon ("ox-turning") is an ancient writing pattern where text
alternates direction line by line, like plowing a field.

Reading pattern:
Row 1: left to right →→→
Row 2: right to left ←←←
Row 3: left to right →→→
Row 4: right to left ←←←
...

This creates a zigzag reading pattern across the grid.

Args:
    text: Plaintext or ciphertext
    encrypt: True for encryption, False for decryption
"""


def encrypt(plaintext: str) -> str:
    """
    Encrypt plaintext using Boustrophedon transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
    
    Returns:
        Encrypted ciphertext
    """
    if not plaintext:
        return ""
    
    # Clean and normalize to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    if not text:
        return ""
    
    # Determine grid dimensions (approx square)
    text_len = len(text)
    side = int(text_len ** 0.5)
    if side * side < text_len:
        side += 1
    
    # Write text in boustrophedon pattern
    grid = [['x' for _ in range(side)] for _ in range(side)]
    text_pos = 0
    
    for row in range(side):
        if row % 2 == 0:
            # Left to right
            for col in range(side):
                if text_pos < text_len:
                    grid[row][col] = text[text_pos]
                    text_pos += 1
        else:
            # Right to left
            for col in range(side - 1, -1, -1):
                if text_pos < text_len:
                    grid[row][col] = text[text_pos]
                    text_pos += 1
    
    # Read in linear order (top to bottom, left to right)
    result = []
    for row in range(side):
        for col in range(side):
            if grid[row][col] != 'x':
                result.append(grid[row][col])
    
    return ''.join(result)


def decrypt(ciphertext: str) -> str:
    """
    Decrypt ciphertext using Boustrophedon transposition.
    
    Args:
        ciphertext: Encrypted text
    
    Returns:
        Decrypted plaintext
    """
    if not ciphertext:
        return ""
    
    text = ''.join([c.lower() for c in ciphertext if c.isalpha()])
    
    if not text:
        return ""
    
    # Determine grid dimensions
    text_len = len(text)
    side = int(text_len ** 0.5)
    if side * side < text_len:
        side += 1
    
    # Fill grid with ciphertext in linear order
    grid = [['x' for _ in range(side)] for _ in range(side)]
    text_pos = 0
    
    for row in range(side):
        for col in range(side):
            if text_pos < text_len:
                grid[row][col] = text[text_pos]
                text_pos += 1
    
    # Read in boustrophedon pattern (alternating directions)
    result = []
    for row in range(side):
        if row % 2 == 0:
            # Left to right
            for col in range(side):
                if grid[row][col] != 'x':
                    result.append(grid[row][col])
        else:
            # Right to left
            for col in range(side - 1, -1, -1):
                if grid[row][col] != 'x':
                    result.append(grid[row][col])
    
    return ''.join(result).rstrip('x')


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("BOUSTROPHEDON TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext)
    decrypted = decrypt(encrypted)
    
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")

