#!/usr/bin/env python3
"""
Advanced Custom Pairing Strategies for Porta Cipher
Demonstrates various user-defined pairing approaches
"""

from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs, porta_encrypt, porta_decrypt

def demonstrate_custom_pairing_strategies():
    """Demonstrate various custom pairing strategies"""
    
    print("=" * 80)
    print("ADVANCED CUSTOM PAIRING STRATEGIES FOR PORTA CIPHER")
    print("=" * 80)
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    test_text = "HELLO WORLD"
    test_key = "KEY"
    
    # Strategy 1: Frequency-based pairs (common letters paired with rare letters)
    print("\n1. FREQUENCY-BASED PAIRS (Common ↔ Rare)")
    print("-" * 50)
    freq_pairs = [
        ('E', 'Z'),  # Most common with least common
        ('T', 'Q'),  # Second most common with second least common
        ('A', 'X'),  # Third most common with third least common
        ('O', 'J'),  # Fourth most common with fourth least common
        ('I', 'K'),  # Fifth most common with fifth least common
        ('N', 'V'),  # Sixth most common with sixth least common
        ('S', 'B')   # Seventh most common with seventh least common
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, freq_pairs)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    # Strategy 2: Atbash/Symmetric pairs (mirror positions)
    print("\n2. ATBASH/SYMMETRIC PAIRS (Mirror Positions)")
    print("-" * 50)
    atbash_pairs = [
        ('A', 'Z'), ('B', 'Y'), ('C', 'X'), ('D', 'W'), ('E', 'V'),
        ('F', 'U'), ('G', 'T'), ('H', 'S'), ('I', 'R'), ('J', 'Q'),
        ('K', 'P'), ('L', 'O'), ('M', 'N')
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, atbash_pairs)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    # Strategy 3: Caesar-shifted pairs
    print("\n3. CAESAR-SHIFTED PAIRS (+3)")
    print("-" * 50)
    caesar_pairs = [
        ('A', 'D'), ('B', 'E'), ('C', 'F'), ('G', 'J'), ('H', 'K'),
        ('I', 'L'), ('M', 'P'), ('N', 'Q'), ('O', 'R'), ('S', 'V'),
        ('T', 'W'), ('U', 'X'), ('Y', 'Z')
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, caesar_pairs)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    # Strategy 4: Affine-based pairs (a=3, b=1)
    print("\n4. AFFINE-BASED PAIRS (a=3, b=1)")
    print("-" * 50)
    affine_pairs = [
        ('A', 'D'), ('B', 'G'), ('C', 'J'), ('E', 'P'),
        ('F', 'S'), ('H', 'Y'), ('I', 'L'), ('K', 'O'),
        ('M', 'R'), ('N', 'U'), ('Q', 'X'), ('T', 'W'),
        ('V', 'Z')
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, affine_pairs)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    # Strategy 5: Affine-based pairs (a=5, b=2)
    print("\n5. AFFINE-BASED PAIRS (a=5, b=2)")
    print("-" * 50)
    affine_pairs_2 = [
        ('A', 'C'), ('B', 'H'), ('D', 'N'), ('E', 'S'), ('F', 'X'),
        ('G', 'L'), ('I', 'Q'), ('J', 'V'), ('K', 'Z'), ('M', 'P'),
        ('O', 'T'), ('R', 'W'), ('U', 'Y')
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, affine_pairs_2)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    # Strategy 6: Custom security-focused pairs
    print("\n6. SECURITY-FOCUSED PAIRS")
    print("-" * 50)
    security_pairs = [
        ('E', 'Z'),  # Most common with least common
        ('T', 'Q'),  # Second most common with second least common
        ('A', 'X'),  # Third most common with third least common
        ('O', 'J'),  # Fourth most common with fourth least common
        ('I', 'K'),  # Fifth most common with fifth least common
        ('N', 'V'),  # Sixth most common with sixth least common
        ('S', 'B'),  # Seventh most common with seventh least common
        ('H', 'Y'),  # Eighth most common with eighth least common
        ('R', 'W'),  # Ninth most common with ninth least common
        ('D', 'F')   # Tenth most common with tenth least common
    ]
    
    pairs = porta_produce_pairs('custom', alphabet, security_pairs)
    print(f"Pairs: {pairs}")
    
    encrypted = porta_encrypt(test_text, test_key, alphabet, pairs)
    decrypted = porta_decrypt(encrypted, test_key, alphabet, pairs)
    print(f"Text: {test_text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {test_text == decrypted}")
    
    print("\n" + "=" * 80)
    print("CUSTOM PAIRING STRATEGIES DEMONSTRATION COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_custom_pairing_strategies()
