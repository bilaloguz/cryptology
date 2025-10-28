"""
Rail Fence Cipher implementation.

The Rail Fence cipher is a transposition cipher that writes the message
in a zigzag pattern along multiple "rails" (rows), then reads it off
in a linear fashion.

The pattern looks like a fence when viewed from the side, hence the name.

Example with 3 rails:
  H . . . O . . . R . .
  . E . L . W . O . L .
  . . L . . . D . . . .

Encryption: Write diagonally, read horizontally
Decryption: Write horizontally, read diagonally

Args:
    text: Plaintext or ciphertext
    rails: Number of rails (rows in the zigzag pattern)
    encrypt: True for encryption, False for decryption
"""


def encrypt(plaintext: str, rails: int) -> str:
    """
    Encrypt plaintext using Rail Fence cipher.
    
    Args:
        plaintext: Text to encrypt (case-insensitive, removes non-alphabetic)
        rails: Number of rails (rows)
    
    Returns:
        Encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO WORLD", 3)
        'HLRLELODLLOW'
        >>> encrypt("ATTACK AT DAWN", 4)
        'AKTDCAATTW AN'
    """
    if rails <= 0:
        raise ValueError("Number of rails must be positive")
    
    if rails == 1:
        # Single rail = no encryption
        return ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    # Clean and normalize text to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    if not text:
        return ""
    
    # Build zigzag pattern
    # Each rail stores characters at positions following the zigzag
    pattern = [[] for _ in range(rails)]
    direction = 1  # 1 for down, -1 for up
    rail = 0
    
    for char in text:
        pattern[rail].append(char)
        
        # Change direction at the edges
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    # Concatenate all rails
    result = ''.join([''.join(rail) for rail in pattern])
    
    return result


def decrypt(ciphertext: str, rails: int) -> str:
    """
    Decrypt ciphertext using Rail Fence cipher.
    
    Args:
        ciphertext: Encrypted text
        rails: Number of rails (rows)
    
    Returns:
        Decrypted plaintext
    
    Example:
        >>> decrypt("HLRLELODLLOW", 3)
        'HELLOWORLD'
    """
    if rails <= 0:
        raise ValueError("Number of rails must be positive")
    
    if rails == 1:
        return ''.join([c.lower() for c in ciphertext if c.isalpha()])
    
    # Clean the ciphertext to lowercase
    text = ''.join([c.lower() for c in ciphertext if c.isalpha()])
    
    if not text:
        return ""
    
    # Calculate how many characters are in each rail
    # Simulate the pattern to count characters per rail
    pattern_lengths = [0] * rails
    direction = 1
    rail = 0
    
    for i in range(len(text)):
        pattern_lengths[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    # Distribute ciphertext across rails
    pattern = [[] for _ in range(rails)]
    text_pos = 0
    
    for rail_num in range(rails):
        for _ in range(pattern_lengths[rail_num]):
            if text_pos < len(text):
                pattern[rail_num].append(text[text_pos])
                text_pos += 1
    
    # Read off in zigzag order
    result = []
    direction = 1
    rail = 0
    rail_positions = [0] * rails
    
    for _ in range(len(text)):
        if rail_positions[rail] < len(pattern[rail]):
            result.append(pattern[rail][rail_positions[rail]])
            rail_positions[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    return ''.join(result)


def _visualize_pattern(text: str, rails: int) -> str:
    """
    Visualize the rail fence pattern (for debugging).
    
    Args:
        text: Text to visualize
        rails: Number of rails
    
    Returns:
        String representation of the pattern
    """
    # Clean text to lowercase
    clean_text = ''.join([c.lower() for c in text if c.isalpha()])
    
    # Create grid
    rows = len(clean_text)
    grid = [[' ' for _ in range(rows)] for _ in range(rails)]
    
    direction = 1
    rail = 0
    
    for col, char in enumerate(clean_text):
        grid[rail][col] = char
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    # Convert to string
    result = []
    for row in grid:
        result.append(' '.join(row))
    
    return '\n'.join(result)


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
    return (1, min(text_length, 10))  # Practical limit


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("RAIL FENCE CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    rails = 3
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Rails:      {rails}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, rails)
    decrypted = decrypt(encrypted, rails)
    
    print(f"\nEncrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    print("\nVisualization:")
    print(_visualize_pattern(plaintext, rails))
    
    # Test with different number of rails
    print("\n" + "=" * 60)
    plaintext2 = "ATTACK AT DAWN"
    rails2 = 4
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Rails:      {rails2}")
    
    encrypted2 = encrypt(plaintext2, rails2)
    decrypted2 = decrypt(encrypted2, rails2)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == ''.join([c.lower() for c in plaintext2 if c.isalpha()])}")

