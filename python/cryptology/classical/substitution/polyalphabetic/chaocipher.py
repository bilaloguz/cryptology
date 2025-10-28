"""
Chaocipher Implementation

The Chaocipher is a polyalphabetic substitution cipher invented by John F. Byrne in 1918.
It uses two rotating alphabets (disks) that are permuted after each character is processed,
making it a dynamic, self-modifying cipher.

Key features:
- Two alphabets: left (ciphertext) and right (plaintext)
- Self-reciprocal: encryption and decryption use the same process
- Dynamic permutation after each character
- More secure than simple substitution ciphers

Algorithm:
1. Find plaintext character in right alphabet
2. Use corresponding position in left alphabet for ciphertext
3. Permute both alphabets:
   - Right alphabet: Move plaintext char to zenith (position 1), then permute
   - Left alphabet: Move ciphertext char to zenith (position 1), then permute
"""

import string
from typing import List, Tuple, Optional


def _create_default_alphabets() -> Tuple[List[str], List[str]]:
    """Create default left and right alphabets for Chaocipher."""
    alphabet = list(string.ascii_uppercase) + [' ']  # Include space
    
    # Default left alphabet (ciphertext alphabet) - standard order
    left_alphabet = alphabet.copy()
    
    # Default right alphabet (plaintext alphabet) - reversed order for variety
    right_alphabet = alphabet.copy()
    right_alphabet.reverse()
    
    return left_alphabet, right_alphabet


def _permute_right_alphabet(right_alphabet: List[str], plain_char: str) -> List[str]:
    """
    Permute the right alphabet after processing a character.
    
    Steps:
    1. Move the plaintext character to position 1 (zenith)
    2. Move the character at position 2 to position 14 (nadir)
    3. Move all characters from position 3 to position 13 one position to the left
    4. Move all characters from position 15 to position 26 one position to the right
    """
    new_alphabet = right_alphabet.copy()
    
    # Find the position of the plaintext character
    plain_pos = new_alphabet.index(plain_char)
    
    # Step 1: Move plaintext character to position 1 (zenith)
    new_alphabet.insert(0, new_alphabet.pop(plain_pos))
    
    # Step 2: Move character at position 2 to position 14 (nadir)
    if len(new_alphabet) > 1:
        char_at_pos_2 = new_alphabet.pop(1)  # Remove from position 2
        new_alphabet.insert(13, char_at_pos_2)  # Insert at position 14 (index 13)
    
    # Steps 3 & 4: Shift remaining characters
    # Characters 3-13 shift left (positions 2-12)
    # Characters 15-26 shift right (positions 14-25)
    if len(new_alphabet) > 14:
        # Move characters 15-26 (indices 14-25) to the right
        chars_15_26 = new_alphabet[14:]
        new_alphabet = new_alphabet[:14] + chars_15_26
    
    return new_alphabet


def _permute_left_alphabet(left_alphabet: List[str], cipher_char: str) -> List[str]:
    """
    Permute the left alphabet after processing a character.
    
    Steps:
    1. Move the ciphertext character to position 1 (zenith)
    2. Move the character at position 2 to position 14 (nadir)
    3. Move all characters from position 3 to position 13 one position to the left
    4. Move all characters from position 15 to position 26 one position to the right
    """
    new_alphabet = left_alphabet.copy()
    
    # Find the position of the ciphertext character
    cipher_pos = new_alphabet.index(cipher_char)
    
    # Step 1: Move ciphertext character to position 1 (zenith)
    new_alphabet.insert(0, new_alphabet.pop(cipher_pos))
    
    # Step 2: Move character at position 2 to position 14 (nadir)
    if len(new_alphabet) > 1:
        char_at_pos_2 = new_alphabet.pop(1)  # Remove from position 2
        new_alphabet.insert(13, char_at_pos_2)  # Insert at position 14 (index 13)
    
    # Steps 3 & 4: Shift remaining characters
    # Characters 3-13 shift left (positions 2-12)
    # Characters 15-26 shift right (positions 14-25)
    if len(new_alphabet) > 14:
        # Move characters 15-26 (indices 14-25) to the right
        chars_15_26 = new_alphabet[14:]
        new_alphabet = new_alphabet[:14] + chars_15_26
    
    return new_alphabet


def _prepare_text(text: str, alphabet: Optional[List[str]] = None) -> str:
    """Prepare text for Chaocipher processing."""
    if alphabet is None:
        alphabet = list(string.ascii_uppercase) + [' ']  # Include space by default
    
    prepared = ""
    for char in text.lower():
        if char in alphabet:
            prepared += char
        elif char == ' ' and ' ' in alphabet:
            prepared += ' '  # Only preserve spaces if they're in the alphabet
    
    return prepared


def encrypt(plaintext: str, 
           left_alphabet: Optional[List[str]] = None,
           right_alphabet: Optional[List[str]] = None) -> str:
    """
    Encrypt plaintext using Chaocipher.
    
    Args:
        plaintext: Text to encrypt
        left_alphabet: Left alphabet (ciphertext alphabet)
        right_alphabet: Right alphabet (plaintext alphabet)
    
    Returns:
        Encrypted text
    """
    if left_alphabet is None or right_alphabet is None:
        left_alphabet, right_alphabet = _create_default_alphabets()
    
    # Prepare text
    prepared_text = _prepare_text(plaintext, right_alphabet)
    
    encrypted = ""
    current_left = left_alphabet.copy()
    current_right = right_alphabet.copy()
    
    for char in prepared_text:
        if char not in current_right:
            continue
        
        # Find position in right alphabet
        right_pos = current_right.index(char)
        
        # Get corresponding character from left alphabet
        cipher_char = current_left[right_pos]
        encrypted += cipher_char
        
        # Permute both alphabets
        current_left = _permute_left_alphabet(current_left, cipher_char)
        current_right = _permute_right_alphabet(current_right, char)
    
    return encrypted


def decrypt(ciphertext: str,
           left_alphabet: Optional[List[str]] = None,
           right_alphabet: Optional[List[str]] = None) -> str:
    """
    Decrypt ciphertext using Chaocipher.
    
    Args:
        ciphertext: Text to decrypt
        left_alphabet: Left alphabet (ciphertext alphabet)
        right_alphabet: Right alphabet (plaintext alphabet)
    
    Returns:
        Decrypted text
    """
    if left_alphabet is None or right_alphabet is None:
        left_alphabet, right_alphabet = _create_default_alphabets()
    
    # Prepare text
    prepared_text = _prepare_text(ciphertext, left_alphabet)
    
    decrypted = ""
    current_left = left_alphabet.copy()
    current_right = right_alphabet.copy()
    
    for char in prepared_text:
        if char not in current_left:
            continue
        
        # Find position in left alphabet
        left_pos = current_left.index(char)
        
        # Get corresponding character from right alphabet
        plain_char = current_right[left_pos]
        decrypted += plain_char
        
        # Permute both alphabets (same as encryption - self-reciprocal)
        current_left = _permute_left_alphabet(current_left, char)
        current_right = _permute_right_alphabet(current_right, plain_char)
    
    return decrypted


def create_custom_alphabets(left_keyword: str = "", right_keyword: str = "") -> Tuple[List[str], List[str]]:
    """
    Create custom alphabets using keywords.
    
    Args:
        left_keyword: Keyword for left alphabet
        right_keyword: Keyword for right alphabet
    
    Returns:
        Tuple of (left_alphabet, right_alphabet)
    """
    alphabet = list(string.ascii_uppercase)
    
    # Create left alphabet
    if left_keyword:
        left_alphabet = []
        # Add keyword characters first
        for char in left_keyword.lower():
            if char in alphabet and char not in left_alphabet:
                left_alphabet.append(char)
        # Add remaining alphabet characters
        for char in alphabet:
            if char not in left_alphabet:
                left_alphabet.append(char)
    else:
        left_alphabet = alphabet.copy()
    
    # Create right alphabet
    if right_keyword:
        right_alphabet = []
        # Add keyword characters first
        for char in right_keyword.lower():
            if char in alphabet and char not in right_alphabet:
                right_alphabet.append(char)
        # Add remaining alphabet characters
        for char in alphabet:
            if char not in right_alphabet:
                right_alphabet.append(char)
    else:
        right_alphabet = alphabet.copy()
    
    return left_alphabet, right_alphabet


def create_alphabets_with_mono_ciphers(left_cipher: str = "atbash", left_params: dict = None, 
                                     right_cipher: str = "caesar", right_params: dict = None,
                                     alphabet: str = None) -> Tuple[List[str], List[str]]:
    """
    Create custom alphabets using monoalphabetic substitution ciphers.
    
    Args:
        left_cipher: Type of monoalphabetic cipher for left alphabet ("caesar", "atbash", "keyword", "affine")
        left_params: Parameters for the left cipher (e.g., {"shift": 5} for Caesar)
        right_cipher: Type of monoalphabetic cipher for right alphabet
        right_params: Parameters for the right cipher
        alphabet: Base alphabet to use (default: English uppercase with space)
    
    Returns:
        Tuple of (left_alphabet, right_alphabet)
    
    Example:
        >>> left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
        ...     left_cipher="caesar", left_params={"shift": 5},
        ...     right_cipher="keyword", right_params={"keyword": "SECRET"}
        ... )
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase + ' '
    
    if left_params is None:
        left_params = {}
    if right_params is None:
        right_params = {}
    
    # Import monoalphabetic ciphers
    from ..monoalphabetic.caesar import produce_alphabet as caesar_produce
    from ..monoalphabetic.atbash import produce_alphabet as atbash_produce
    from ..monoalphabetic.keyword import produce_alphabet as keyword_produce
    from ..monoalphabetic.affine import produce_alphabet as affine_produce
    
    # Create left alphabet
    if left_cipher == "caesar":
        left_alphabet_str = caesar_produce(**left_params, alphabet=alphabet)
    elif left_cipher == "atbash":
        left_alphabet_str = atbash_produce(alphabet=alphabet)
    elif left_cipher == "keyword":
        left_alphabet_str = keyword_produce(**left_params, alphabet=alphabet)
    elif left_cipher == "affine":
        left_alphabet_str = affine_produce(**left_params, alphabet=alphabet)
    else:
        raise ValueError(f"Unsupported left cipher: {left_cipher}")
    
    # Create right alphabet
    if right_cipher == "caesar":
        right_alphabet_str = caesar_produce(**right_params, alphabet=alphabet)
    elif right_cipher == "atbash":
        right_alphabet_str = atbash_produce(alphabet=alphabet)
    elif right_cipher == "keyword":
        right_alphabet_str = keyword_produce(**right_params, alphabet=alphabet)
    elif right_cipher == "affine":
        right_alphabet_str = affine_produce(**right_params, alphabet=alphabet)
    else:
        raise ValueError(f"Unsupported right cipher: {right_cipher}")
    
    # Convert to lists
    left_alphabet = list(left_alphabet_str.lower())
    right_alphabet = list(right_alphabet_str.lower())
    
    return left_alphabet, right_alphabet


def decrypt_with_alphabets(ciphertext: str, left_alphabet: List[str], right_alphabet: List[str]) -> str:
    """
    Decrypt ciphertext using provided alphabets.
    
    Args:
        ciphertext: Text to decrypt
        left_alphabet: Left alphabet used for encryption
        right_alphabet: Right alphabet used for encryption
    
    Returns:
        Decrypted text
    """
    return decrypt(ciphertext, left_alphabet, right_alphabet)