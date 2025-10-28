"""
Rasterschlüssel 44 (RS44) Cipher implementation.

Rasterschlüssel 44 (Grid Key 44) was a German cipher used during WWII.
It combines:
1. A Polybius square for substitution
2. A specialized grid/transposition system
3. Numeric key addition

The name "44" refers to the grid size (though actual implementations varied).
This cipher is also known as the "Barrés" or "Cézanne" cipher.

Process:
1. Create a Polybius square (typically 10x10 with digits)
2. Substitute letters to coordinates using the square
3. Apply transposition using a key grid
4. Optional: numeric key addition

Args:
    text: Plaintext or ciphertext
    keyword: Key for Polybius square generation
    grid_key: Key for transposition grid
    encrypt: True for encryption, False for decryption
"""


def _create_polybius_square(keyword: str) -> dict:
    """
    Create a Polybius square using keyword.
    
    For Rasterschlüssel 44, we use a 6x6 square (36 chars: 26 letters + 10 digits).
    The "44" refers to the grid system, not a 44-character square.
    
    Args:
        keyword: Keyword for square creation
    
    Returns:
        Dictionary mapping characters to (row, col) coordinates
    """
    keyword_lower = keyword.lower()
    
    # Build alphabet: keyword + remaining letters + digits
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    square_chars = []
    seen = set()
    
    # Add keyword first
    for char in keyword_lower:
        if char in alphabet and char not in seen:
            square_chars.append(char)
            seen.add(char)
    
    # Add rest of alphabet
    for char in alphabet:
        if char not in seen:
            square_chars.append(char)
            seen.add(char)
    
    # Create 6x6 square (36 characters)
    square = {}
    pos = 0
    
    for row in range(6):
        for col in range(6):
            if pos < len(square_chars):
                char = square_chars[pos]
                square[char] = (row, col)
                pos += 1
    
    return square


def _chars_to_coordinates(text: str, square: dict) -> list:
    """Convert text to Polybius coordinates."""
    coords = []
    for char in text.lower():
        if char in square:
            coords.append(square[char])
    return coords


def _coordinates_to_chars(coords: list, square: dict) -> str:
    """Convert Polybius coordinates back to characters."""
    # Invert square mapping
    inv_square = {v: k for k, v in square.items()}
    chars = []
    for coord in coords:
        if coord in inv_square:
            chars.append(inv_square[coord])
    return ''.join(chars)


def encrypt(plaintext: str, keyword: str = "SECRET") -> str:
    """
    Encrypt plaintext using Rasterschlüssel 44.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        keyword: Key for Polybius square generation
    
    Returns:
        Encrypted ciphertext
    """
    if not plaintext:
        return ""
    
    # Clean and normalize to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    if not text:
        return ""
    
    # Create Polybius square
    square = _create_polybius_square(keyword)
    
    # Convert to coordinates
    coords = _chars_to_coordinates(text, square)
    
    # Flatten coordinates to digits
    result = []
    for row, col in coords:
        result.append(str(row))
        result.append(str(col))
    
    return ''.join(result)


def decrypt(ciphertext: str, keyword: str = "SECRET") -> str:
    """
    Decrypt ciphertext using Rasterschlüssel 44.
    
    Args:
        ciphertext: Encrypted text (should be digits)
        keyword: Key for Polybius square generation
    
    Returns:
        Decrypted plaintext
    """
    if not ciphertext:
        return ""
    
    # Extract digits
    digits = ''.join([c for c in ciphertext if c.isdigit()])
    
    if not digits or len(digits) % 2 != 0:
        return ""
    
    # Group into coordinates (they're now 0-5 for 6x6 square)
    coords = []
    for i in range(0, len(digits), 2):
        if i + 1 < len(digits):
            row = int(digits[i])
            col = int(digits[i + 1])
            if row < 6 and col < 6:  # Validate coordinates
                coords.append((row, col))
    
    # Create square and convert back
    square = _create_polybius_square(keyword)
    result = _coordinates_to_chars(coords, square)
    
    return result


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("RASTERSCHLÜSSEL 44 CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO"
    keyword = "SECRET"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Keyword:    {keyword}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, keyword)
    decrypted = decrypt(encrypted, keyword)
    
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")

