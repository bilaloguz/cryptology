"""
Alberti Cipher implementation.

The Alberti cipher is the first polyalphabetic cipher, invented by Leon Battista Alberti in 1467.
It uses two concentric disks - an outer disk with the plaintext alphabet and an inner disk 
with a scrambled ciphertext alphabet. The inner disk rotates according to a specified strategy.

This implementation supports:
- Custom alphabets for both outer and inner disks
- Complex rotation strategies (Fibonacci, keyword-based, mathematical sequences)
- Integration with monoalphabetic-produced alphabets
- Deterministic scrambled alphabet generation
"""

import random
from typing import List, Union
import cryptology.alphabets as ALPHABETS
from ..monoalphabetic.caesar import produce_alphabet as caesar_produce
from ..monoalphabetic.keyword import produce_alphabet as keyword_produce
from ..monoalphabetic.affine import produce_alphabet as affine_produce
from ..monoalphabetic.atbash import produce_alphabet as atbash_produce

DEFAULT_ALPHABET = ALPHABETS.ENGLISH_ALPHABET


def _generate_scrambled_alphabet(base_alphabet: str, seed: int = 42) -> str:
    """
    Generate a deterministic scrambled alphabet from the base alphabet.
    
    Args:
        base_alphabet: The alphabet to scramble
        seed: Seed for deterministic generation (default: 42)
        
    Returns:
        A scrambled version of the base alphabet
    """
    if not base_alphabet:
        return ""
    
    # Use seed for deterministic generation
    random.seed(seed)
    alphabet_list = list(base_alphabet)
    random.shuffle(alphabet_list)
    random.seed()  # Reset random seed
    
    return ''.join(alphabet_list)


def _parse_rotation_strategy(strategy: Union[str, List[int]], plaintext: str) -> List[int]:
    """
    Parse rotation strategy and return list of rotation points.
    
    Args:
        strategy: Rotation strategy (string or list)
        plaintext: Plaintext for context-dependent strategies
        
    Returns:
        List of positions where rotation should occur
        
    Raises:
        ValueError: If strategy is invalid
    """
    if isinstance(strategy, list):
        # User-defined pattern
        return strategy
    
    if isinstance(strategy, str):
        strategy = strategy.lower()
        
        if strategy.startswith("every_"):
            # Every N letters
            try:
                n = int(strategy.split("_")[1])
                return list(range(n, len(plaintext), n))
            except (ValueError, IndexError):
                raise ValueError(f"Invalid 'every_N' strategy: {strategy}")
        
        elif strategy == "on_vowel":
            # Rotate when plaintext is vowel
            vowels = "AEIOU"
            return [i for i, char in enumerate(plaintext.lower()) if char in vowels]
        
        elif strategy == "on_space":
            # Rotate when plaintext is space
            return [i for i, char in enumerate(plaintext) if char == " "]
        
        elif strategy == "on_consonant":
            # Rotate when plaintext is consonant
            vowels = "AEIOU"
            return [i for i, char in enumerate(plaintext.lower()) if char.isalpha() and char not in vowels]
        
        elif strategy == "fibonacci":
            # Rotate based on Fibonacci sequence
            fib_points = []
            a, b = 1, 1
            while a < len(plaintext):
                fib_points.append(a - 1)  # Convert to 0-based indexing
                a, b = b, a + b
            return fib_points
        
        elif strategy.startswith("on_keyword_"):
            # Rotate based on keyword pattern
            keyword = strategy.split("_", 2)[2]
            pattern = []
            for i, char in enumerate(plaintext):
                if char.lower() in keyword.lower():
                    pattern.append(i)
            return pattern
        
        else:
            raise ValueError(f"Unknown rotation strategy: {strategy}")
    
    raise ValueError("Rotation strategy must be string or list of integers")


def _rotate_alphabet(alphabet: str, amount: int) -> str:
    """
    Rotate alphabet by specified amount (clockwise).
    
    Args:
        alphabet: Alphabet to rotate
        amount: Number of positions to rotate
        
    Returns:
        Rotated alphabet
    """
    if not alphabet:
        return ""
    
    amount = amount % len(alphabet)
    return alphabet[amount:] + alphabet[:amount]


def _find_char_position(alphabet: str, char: str) -> int:
    """
    Find position of character in alphabet.
    
    Args:
        alphabet: Alphabet to search in
        char: Character to find
        
    Returns:
        Position of character (0-based)
        
    Raises:
        ValueError: If character not found
    """
    char_upper = char.lower()
    for i, c in enumerate(alphabet):
        if c.lower() == char_upper:
            return i
    raise ValueError(f"Character '{char}' not found in alphabet")


def encrypt(plaintext: str,
           outer_alphabet: str = None,
           inner_alphabet: str = None,
           initial_position: int = 0,
           rotation_strategy: Union[str, List[int]] = None,
           rotation_amount: int = 1) -> str:
    """
    Encrypt plaintext using Alberti cipher.
    
    Args:
        plaintext: Text to encrypt
        outer_alphabet: Plaintext alphabet (auto-generated if None)
        inner_alphabet: Ciphertext alphabet (auto-generated if None)
        initial_position: Starting position of inner disk
        rotation_strategy: When to rotate (required, no default)
        rotation_amount: How many positions to rotate
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If rotation_strategy is None or invalid
    """
    if not plaintext:
        return ""
    
    if rotation_strategy is None:
        raise ValueError("Rotation strategy is required (no default)")
    
    # Auto-generate alphabets if not provided
    if outer_alphabet is None:
        outer_alphabet = DEFAULT_ALPHABET
    
    if inner_alphabet is None:
        inner_alphabet = _generate_scrambled_alphabet(outer_alphabet)
    
    # Parse rotation strategy
    try:
        rotation_points = _parse_rotation_strategy(rotation_strategy, plaintext)
    except ValueError as e:
        raise ValueError(f"Invalid rotation strategy: {e}")
    
    # Clean plaintext
    plaintext_clean = ""
    for char in plaintext.lower():
        if char.isalpha():
            plaintext_clean += char
    
    if not plaintext_clean:
        return ""
    
    # Initialize inner disk position
    current_position = initial_position % len(inner_alphabet)
    inner_alphabet_current = _rotate_alphabet(inner_alphabet, current_position)
    
    result = ""
    rotation_index = 0
    
    for i, char in enumerate(plaintext_clean):
        try:
            # Find character in outer alphabet
            outer_pos = _find_char_position(outer_alphabet, char)
            
            # Map to inner alphabet
            if outer_pos < len(inner_alphabet_current):
                cipher_char = inner_alphabet_current[outer_pos]
            else:
                # Handle different alphabet sizes
                cipher_char = inner_alphabet_current[outer_pos % len(inner_alphabet_current)]
            
            result += cipher_char
            
            # Check if we need to rotate
            if rotation_index < len(rotation_points) and i == rotation_points[rotation_index]:
                current_position = (current_position + rotation_amount) % len(inner_alphabet)
                inner_alphabet_current = _rotate_alphabet(inner_alphabet, current_position)
                rotation_index += 1
                
        except ValueError:
            # Skip characters not in alphabet
            continue
    
    return result


def decrypt(ciphertext: str,
           outer_alphabet: str = None,
           inner_alphabet: str = None,
           initial_position: int = 0,
           rotation_strategy: Union[str, List[int]] = None,
           rotation_amount: int = 1) -> str:
    """
    Decrypt ciphertext using Alberti cipher.
    
    Args:
        ciphertext: Text to decrypt
        outer_alphabet: Plaintext alphabet (auto-generated if None)
        inner_alphabet: Ciphertext alphabet (auto-generated if None)
        initial_position: Starting position of inner disk
        rotation_strategy: When to rotate (required, no default)
        rotation_amount: How many positions to rotate
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If rotation_strategy is None or invalid
    """
    if not ciphertext:
        return ""
    
    if rotation_strategy is None:
        raise ValueError("Rotation strategy is required (no default)")
    
    # Auto-generate alphabets if not provided
    if outer_alphabet is None:
        outer_alphabet = DEFAULT_ALPHABET
    
    if inner_alphabet is None:
        inner_alphabet = _generate_scrambled_alphabet(outer_alphabet)
    
    # Parse rotation strategy
    try:
        rotation_points = _parse_rotation_strategy(rotation_strategy, ciphertext)
    except ValueError as e:
        raise ValueError(f"Invalid rotation strategy: {e}")
    
    # Clean ciphertext
    ciphertext_clean = ""
    for char in ciphertext.lower():
        if char.isalpha():
            ciphertext_clean += char
    
    if not ciphertext_clean:
        return ""
    
    # Initialize inner disk position
    current_position = initial_position % len(inner_alphabet)
    inner_alphabet_current = _rotate_alphabet(inner_alphabet, current_position)
    
    result = ""
    rotation_index = 0
    
    for i, char in enumerate(ciphertext_clean):
        try:
            # Find character in inner alphabet
            inner_pos = _find_char_position(inner_alphabet_current, char)
            
            # Map to outer alphabet
            if inner_pos < len(outer_alphabet):
                plain_char = outer_alphabet[inner_pos]
            else:
                # Handle different alphabet sizes
                plain_char = outer_alphabet[inner_pos % len(outer_alphabet)]
            
            result += plain_char
            
            # Check if we need to rotate
            if rotation_index < len(rotation_points) and i == rotation_points[rotation_index]:
                current_position = (current_position + rotation_amount) % len(inner_alphabet)
                inner_alphabet_current = _rotate_alphabet(inner_alphabet, current_position)
                rotation_index += 1
                
        except ValueError:
            # Skip characters not in alphabet
            continue
    
    return result
