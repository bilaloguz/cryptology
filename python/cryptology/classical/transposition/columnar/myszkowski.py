"""
Myszkowski Transposition Cipher implementation.

The Myszkowski variant is a columnar transposition where repeated letters in
the keyword are treated together (grouped), rather than given sequential positions.

Key difference from standard columnar:
- Standard: "CIPHER" → positions: C=0, I=1, P=2, P=3, H=4, E=5, R=6
- Myszkowski: "CIPHER" → positions: C=0, I=1, P=2,2 (repeated), H=3, E=4, R=5
  After sorting: E=4, H=3, P=2,2, C=0, I=1, R=5
  Column order determined by handling ties carefully

When decrypting, letters are read from columns with same letter positions
in alphabetical order of the keyword letters.

Args:
    text: Plaintext or ciphertext
    keyword: The column arrangement keyword
    encrypt: True for encryption, False for decryption
"""


def _get_myszkowski_order(keyword: str) -> list:
    """
    Get column order using Myszkowski method.
    
    In Myszkowski, repeated letters are handled specially.
    The order is the same as alphabetical, but repeated letters
    have the same position value.
    
    Args:
        keyword: The keyword (converted to lowercase)
    
    Returns:
        List of (char, order_value) tuples sorted by char
    """
    keyword_lower = keyword.lower()
    
    # Count occurrences of each letter
    from collections import Counter
    counts = Counter()
    
    # Build tuples: (char, original_position)
    char_positions = [(c, i) for i, c in enumerate(keyword_lower)]
    
    # Assign positions, handling repeated letters
    result = []
    char_to_position = {}
    
    # First pass: get unique chars in sorted order
    unique_chars = sorted(set(keyword_lower))
    
    # Assign position based on sorted order of unique chars
    for pos, char in enumerate(unique_chars):
        char_to_position[char] = pos
    
    # Apply to all characters
    for char, orig_pos in char_positions:
        result.append((char, char_to_position[char], orig_pos))
    
    # Sort by (char, orig_pos) to handle ties
    result.sort(key=lambda x: (x[0], x[2]))
    
    return result


def encrypt(plaintext: str, keyword: str) -> str:
    """
    Encrypt plaintext using Myszkowski Transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        keyword: The column arrangement keyword
    
    Returns:
        Encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO WORLD", "CIPHER")
        'encrypted text'
    """
    if not plaintext or not keyword:
        return ""
    
    # Clean and normalize to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    keyword_lower = keyword.lower()
    
    if not text:
        return ""
    
    # Get Myszkowski column order
    order_info = _get_myszkowski_order(keyword_lower)
    
    # Extract position groups
    # Myszkowski groups columns by their order value
    groups = {}
    for char, order_val, orig_pos in order_info:
        if order_val not in groups:
            groups[order_val] = []
        groups[order_val].append(orig_pos)
    
    # Write text in rows
    key_len = len(keyword_lower)
    num_rows = (len(text) + key_len - 1) // key_len
    padded_text = text.ljust(num_rows * key_len, 'x')
    
    grid = []
    text_pos = 0
    for row in range(num_rows):
        grid_row = []
        for col in range(key_len):
            if text_pos < len(padded_text):
                grid_row.append(padded_text[text_pos])
                text_pos += 1
            else:
                grid_row.append('x')
        grid.append(grid_row)
    
    # Read columns in Myszkowski order
    result = []
    sorted_groups = sorted(groups.items())
    
    for order_val, col_indices in sorted_groups:
        # Read all columns with same order value (if there are multiples)
        for col_idx in col_indices:
            for row in grid:
                if col_idx < len(row):
                    char = row[col_idx]
                    if char and char != 'x':
                        result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, keyword: str) -> str:
    """
    Decrypt ciphertext using Myszkowski Transposition.
    
    Args:
        ciphertext: Encrypted text
        keyword: The column arrangement keyword
    
    Returns:
        Decrypted plaintext
    
    Example:
        >>> decrypt("encrypted text", "CIPHER")
        'helloworld'
    """
    if not ciphertext or not keyword:
        return ""
    
    # Clean and normalize
    text = ''.join([c.lower() for c in ciphertext if c.isalpha()])
    keyword_lower = keyword.lower()
    
    if not text:
        return ""
    
    # Get Myszkowski column order
    order_info = _get_myszkowski_order(keyword_lower)
    
    # Extract position groups
    groups = {}
    for char, order_val, orig_pos in order_info:
        if order_val not in groups:
            groups[order_val] = []
        groups[order_val].append(orig_pos)
    
    # Calculate grid dimensions
    key_len = len(keyword_lower)
    text_len = len(text)
    num_rows = (text_len + key_len - 1) // key_len
    
    # Create empty grid
    grid = [['' for _ in range(key_len)] for _ in range(num_rows)]
    
    # Fill grid column by column in Myszkowski order
    # Need to distribute text evenly across columns
    sorted_groups = sorted(groups.items())
    text_pos = 0
    
    for order_val, col_indices in sorted_groups:
        # Each column in this group gets the same number of chars
        total_rows_to_fill = num_rows * len(col_indices)
        chars_per_col = len(text) // key_len if key_len > 0 else 0
        extra_chars = len(text) % key_len
        
        for col_idx in col_indices:
            # Determine how many characters this column should get
            col_chars = chars_per_col
            if col_idx < extra_chars:
                col_chars += 1
                
            for row in range(min(col_chars, num_rows)):
                if text_pos < text_len and row < len(grid):
                    grid[row][col_idx] = text[text_pos]
                    text_pos += 1
    
    # Read by rows
    result = []
    for row in grid:
        for col in range(key_len):
            if col < len(row) and row[col]:
                char = row[col]
                if char and char != 'x':
                    result.append(char)
    
    return ''.join(result)


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("MYSZKOWSKI TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    keyword = "KEY"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Keyword:    {keyword}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, keyword)
    decrypted = decrypt(encrypted, keyword)
    
    print(f"\nEncrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    # Test with keyword that has repeated letters
    print("\n" + "=" * 60)
    plaintext2 = "ATTACK AT DAWN"
    keyword2 = "SECRET"
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Keyword:    {keyword2}")
    
    encrypted2 = encrypt(plaintext2, keyword2)
    decrypted2 = decrypt(encrypted2, keyword2)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == ''.join([c.lower() for c in plaintext2 if c.isalpha()])}")
    
    # Test with keyword specifically designed for Myszkowski
    print("\n" + "=" * 60)
    plaintext3 = "CRYPTOGRAPHY"
    keyword3 = "MASS"  # Has repeated 'S'
    
    print(f"\nPlaintext:  {plaintext3}")
    print(f"Keyword:    {keyword3}")
    
    encrypted3 = encrypt(plaintext3, keyword3)
    decrypted3 = decrypt(encrypted3, keyword3)
    
    print(f"Encrypted:  {encrypted3}")
    print(f"Decrypted:  {decrypted3}")
    print(f"Success:    {decrypted3 == plaintext3.lower()}")

