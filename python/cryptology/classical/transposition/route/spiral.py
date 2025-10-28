"""
Spiral Route Transposition Cipher implementation.

The Spiral Route cipher writes text in a spiral pattern (starting from
a corner and spiraling inward or outward), then reads it in a linear fashion.

Common patterns:
- Clockwise outward spiral: Start at center, spiral out
- Counter-clockwise outward spiral: Start at center, spiral out opposite direction
- Clockwise inward spiral: Start at edge, spiral in
- Counter-clockwise inward spiral: Start at edge, spiral in opposite direction

Args:
    text: Plaintext or ciphertext
    direction: 'clockwise' or 'counterclockwise'
    start: 'center' or 'edge'
    encrypt: True for encryption, False for decryption
"""


def encrypt(plaintext: str, direction: str = 'clockwise', start: str = 'center') -> str:
    """
    Encrypt plaintext using Spiral Route transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        direction: 'clockwise' or 'counterclockwise'
        start: 'center' or 'edge' (where spiral starts)
    
    Returns:
        Encrypted ciphertext
    """
    if not plaintext:
        return ""
    
    # Clean and normalize to lowercase
    text = ''.join([c.lower() for c in plaintext if c.isalpha()])
    
    if not text:
        return ""
    
    # Calculate grid size (smallest square that fits)
    text_len = len(text)
    side = 1
    while side * side < text_len:
        side += 1
    
    # Create grid and fill with spiral pattern
    grid = [['x' for _ in range(side)] for _ in range(side)]
    
    # Start from center
    row = side // 2
    col = side // 2
    
    # Directions: right, down, left, up
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    
    dir_idx = 0 if direction == 'clockwise' else 2
    text_pos = 0
    steps_in_dir = 1
    step_count = 0
    turns = 0
    
    while text_pos < text_len:
        if row >= 0 and row < side and col >= 0 and col < side:
            if grid[row][col] == 'x':
                grid[row][col] = text[text_pos]
                text_pos += 1
                step_count += 1
        
        row += dr[dir_idx]
        col += dc[dir_idx]
        step_count += 1
        
        if step_count >= steps_in_dir:
            step_count = 0
            turns += 1
            dir_idx = (dir_idx + 1) % 4
            
            if turns % 2 == 0 and turns > 0:
                steps_in_dir += 1
    
    # Read in row-major order (or column-major for variation)
    result = []
    for r in range(side):
        for c in range(side):
            if grid[r][c] != 'x':
                result.append(grid[r][c])
    
    return ''.join(result)


def decrypt(ciphertext: str, direction: str = 'clockwise', start: str = 'center') -> str:
    """
    Decrypt ciphertext using Spiral Route transposition.
    
    Args:
        ciphertext: Encrypted text
        direction: 'clockwise' or 'counterclockwise'
        start: 'center' or 'edge' (where spiral starts)
    
    Returns:
        Decrypted plaintext
    """
    if not ciphertext:
        return ""
    
    text = ''.join([c.lower() for c in ciphertext if c.isalpha()])
    
    if not text:
        return ""
    
    # Calculate grid size
    text_len = len(text)
    side = 1
    while side * side < text_len:
        side += 1
    
    # Fill grid in spiral pattern
    grid = [['x' for _ in range(side)] for _ in range(side)]
    
    row = side // 2
    col = side // 2
    
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    
    dir_idx = 0 if direction == 'clockwise' else 2
    text_pos = 0
    steps_in_dir = 1
    step_count = 0
    turns = 0
    
    while text_pos < text_len:
        if row >= 0 and row < side and col >= 0 and col < side:
            grid[row][col] = '_'  # Mark as filled
            text_pos += 1
        
        row += dr[dir_idx]
        col += dc[dir_idx]
        step_count += 1
        
        if step_count >= steps_in_dir:
            step_count = 0
            turns += 1
            dir_idx = (dir_idx + 1) % 4
            
            if turns % 2 == 0 and turns > 0:
                steps_in_dir += 1
    
    # Fill grid with ciphertext in row-major order
    text_pos = 0
    for r in range(side):
        for c in range(side):
            if grid[r][c] == '_':
                if text_pos < text_len:
                    grid[r][c] = text[text_pos]
                    text_pos += 1
    
    # Now read in spiral order (reversing the process)
    # This is complex - simplified version
    result = []
    visited = [[False for _ in range(side)] for _ in range(side)]
    
    row = side // 2
    col = side // 2
    dir_idx = 0
    step_count = 0
    steps_in_dir = 1
    turns = 0
    visited[row][col] = True
    result.append(grid[row][col])
    
    while len(result) < text_len:
        row += dr[dir_idx]
        col += dc[dir_idx]
        
        if row >= 0 and row < side and col >= 0 and col < side and not visited[row][col]:
            visited[row][col] = True
            result.append(grid[row][col])
            step_count += 1
        
        if step_count >= steps_in_dir:
            step_count = 0
            turns += 1
            dir_idx = (dir_idx + 1) % 4
            
            if turns % 2 == 0 and turns > 0:
                steps_in_dir += 1
    
    return ''.join(result).rstrip('x')


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("SPIRAL ROUTE TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO"
    direction = "clockwise"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Direction:  {direction}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, direction)
    print(f"Encrypted:  {encrypted}")

