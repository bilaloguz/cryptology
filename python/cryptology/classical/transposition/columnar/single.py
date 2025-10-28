"""
Single Columnar Transposition Cipher implementation.

The columnar transposition cipher is a method of encryption where the plaintext
is written in rows of a fixed length, then read out again column by column,
but in the order specified by a keyword.

Process:
1. Write plaintext in rows (row length determined by keyword length)
2. Label columns with keyword letters
3. Rearrange columns in alphabetical order of keyword
4. Read text column by column in new order

Example with keyword "KEY":
  Plaintext: "HELLO WORLD"
  Keyword: "KEY" (length 3)
  
  Write in rows:
  H E L
  L O W
  O R L
  D
  
  Label columns: K E Y (alphabetic order: E K Y)
  After rearrangement: E K Y
  Read: LOW DHO ELR

Args:
    text: Plaintext or ciphertext
    keyword: The column arrangement keyword
    encrypt: True for encryption, False for decryption
"""


def encrypt(plaintext: str, keyword: str) -> str:
    """
    Encrypt plaintext using Single Columnar Transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        keyword: The column arrangement keyword
    
    Returns:
        Encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO WORLD", "KEY")
        'owldlo elrh'
    """
    if not plaintext or not keyword:
        return ""
    
    # Clean and normalize to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    keyword_lower = keyword.lower()
    
    if not text:
        return ""
    
    # Get keyword length and column order
    key_len = len(keyword_lower)
    
    # Create sorted key with original positions (stable sort for ties)
    key_chars = list(keyword_lower)
    sorted_indices = sorted(range(key_len), key=lambda i: key_chars[i])
    
    # Calculate grid dimensions
    num_rows = (len(text) + key_len - 1) // key_len
    
    # Write in rows (don't pad, leave empty cells)
    grid = [['' for _ in range(key_len)] for _ in range(num_rows)]
    text_pos = 0
    
    for row in range(num_rows):
        for col in range(key_len):
            if text_pos < len(text):
                grid[row][col] = text[text_pos]
                text_pos += 1
    
    # Read by columns in sorted order
    result = []
    for col_idx in sorted_indices:
        for row in range(num_rows):
            char = grid[row][col_idx]
            if char:  # Only append non-empty cells
                result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, keyword: str) -> str:
    """
    Decrypt ciphertext using Single Columnar Transposition.
    
    Args:
        ciphertext: Encrypted text
        keyword: The column arrangement keyword
    
    Returns:
        Decrypted plaintext
    
    Example:
        >>> decrypt("owldlo elrh", "KEY")
        'helloworld'
    """
    if not ciphertext or not keyword:
        return ""
    
    # Clean and normalize
    text = ''.join([c.lower() for c in ciphertext if c.isalpha()])
    keyword_lower = keyword.lower()
    
    if not text:
        return ""
    
    # Get keyword length and column order
    key_len = len(keyword_lower)
    
    # Create sorted key with original positions
    key_chars = list(keyword_lower)
    sorted_indices = sorted(range(key_len), key=lambda i: key_chars[i])
    
    # Calculate dimensions
    text_len = len(text)
    num_rows = (text_len + key_len - 1) // key_len
    
    # Determine how many full columns and partial columns
    full_cols = text_len % key_len  # Columns with full rows
    partial_col = 1 if text_len % key_len > 0 else 0
    
    # Total cells that were filled
    total_cells = text_len
    
    # Calculate number of full rows
    full_rows = total_cells // key_len
    chars_in_last_row = total_cells % key_len
    
    # Create empty grid
    grid = [['' for _ in range(key_len)] for _ in range(num_rows)]
    
    # Fill in ciphertext by columns (in sorted order)
    # We need to distribute the chars among columns
    # First determine how many chars each column in SORTED order has
    
    text_pos = 0
    for i, col_idx in enumerate(sorted_indices):
        # The original grid had:
        # - full_rows complete rows filled by all columns
        # - Last row has chars_in_last_row chars
        
        # Determine how many chars this column has
        # If this is one of the first chars_in_last_row columns (in original order),
        # it has full_rows + 1 chars, otherwise full_rows chars
        
        # Map from sorted position to original column
        # sorted_indices[i] is the original column idx
        # We need to know if this original column was in the first chars_in_last_row columns
        
        # Wait, we need to figure this out differently
        # The encryption wrote by rows, then read by sorted columns
        # When written by rows:
        # - All columns get full_rows chars from the first full_rows rows
        # - The first chars_in_last_row columns get 1 more char from the last row
        
        # When read by sorted columns, we need to know how many each sorted column has
        # This depends on the position of each column in the original grid
        
        # Determine number of chars for this column in sorted order
        if sorted_indices[i] < chars_in_last_row:
            chars_in_col = full_rows + 1
        else:
            chars_in_col = full_rows
        
        for row in range(chars_in_col):
            if text_pos < len(text):
                grid[row][col_idx] = text[text_pos]
                text_pos += 1
    
    # Read by rows (original order)
    result = []
    for row in grid:
        for col in range(key_len):
            char = row[col]
            if char:  # Only append non-empty cells
                result.append(char)
    
    return ''.join(result)


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("SINGLE COLUMNAR TRANSPOSITION CIPHER")
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
    
    # Test with different keyword
    print("\n" + "=" * 60)
    plaintext2 = "ATTACK AT DAWN"
    keyword2 = "CIPHER"
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Keyword:    {keyword2}")
    
    encrypted2 = encrypt(plaintext2, keyword2)
    decrypted2 = decrypt(encrypted2, keyword2)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == ''.join([c.lower() for c in plaintext2 if c.isalpha()])}")

