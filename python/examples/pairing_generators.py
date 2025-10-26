#!/usr/bin/env python3
"""
Custom Pairing Strategy Generator for Porta Cipher
Provides utility functions to generate various pairing strategies
"""

import random
import string
from typing import List, Tuple, Dict
from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs

def generate_frequency_based_pairs(alphabet: str, num_pairs: int = None) -> List[Tuple[str, str]]:
    """
    Generate frequency-based pairs (common letters paired with rare letters)
    
    Args:
        alphabet: The alphabet to create pairs from
        num_pairs: Number of pairs to generate (default: half of alphabet length)
    
    Returns:
        List of tuples representing frequency-based pairs
    """
    if num_pairs is None:
        num_pairs = len(alphabet) // 2
    
    # English letter frequency order (most common to least common)
    frequency_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    
    # Filter to only include letters in our alphabet
    available_letters = [c for c in frequency_order if c in alphabet.upper()]
    
    pairs = []
    for i in range(min(num_pairs, len(available_letters) // 2)):
        if i < len(available_letters) // 2:
            common_letter = available_letters[i]
            rare_letter = available_letters[-(i + 1)]
            pairs.append((common_letter, rare_letter))
    
    return pairs

def generate_caesar_pairs(alphabet: str, shift: int = 13, num_pairs: int = None) -> List[Tuple[str, str]]:
    """
    Generate Caesar-shifted pairs
    
    Args:
        alphabet: The alphabet to create pairs from
        shift: The shift amount (default: 13)
        num_pairs: Number of pairs to generate (default: half of alphabet length)
    
    Returns:
        List of tuples representing Caesar-shifted pairs
    """
    if num_pairs is None:
        num_pairs = len(alphabet) // 2
    
    pairs = []
    used_letters = set()
    
    for i in range(len(alphabet)):
        if len(pairs) >= num_pairs:
            break
        
        if alphabet[i] not in used_letters:
            shifted_index = (i + shift) % len(alphabet)
            if alphabet[shifted_index] not in used_letters:
                pairs.append((alphabet[i], alphabet[shifted_index]))
                used_letters.add(alphabet[i])
                used_letters.add(alphabet[shifted_index])
    
    return pairs

def generate_atbash_symmetric_pairs(alphabet: str, num_pairs: int = None) -> List[Tuple[str, str]]:
    """
    Generate Atbash/Symmetric pairs (mirror positions)
    Note: Atbash and Symmetric pairs are identical - both use mirror positions
    
    Args:
        alphabet: The alphabet to create pairs from
        num_pairs: Number of pairs to generate (default: half of alphabet length)
    
    Returns:
        List of tuples representing Atbash/Symmetric pairs
    """
    if num_pairs is None:
        num_pairs = len(alphabet) // 2
    
    pairs = []
    for i in range(min(num_pairs, len(alphabet) // 2)):
        pairs.append((alphabet[i], alphabet[-(i + 1)]))
    
    return pairs

def generate_affine_pairs(alphabet: str, a: int = 3, b: int = 1, num_pairs: int = None) -> List[Tuple[str, str]]:
    """
    Generate Affine-based pairs using the formula: E(x) = (ax + b) mod 26
    
    Args:
        alphabet: The alphabet to create pairs from
        a: Multiplier (must be coprime with alphabet length)
        b: Shift amount
        num_pairs: Number of pairs to generate (default: half of alphabet length)
    
    Returns:
        List of tuples representing Affine-based pairs
    """
    if num_pairs is None:
        num_pairs = len(alphabet) // 2
    
    def gcd(a_val, b_val):
        while b_val:
            a_val, b_val = b_val, a_val % b_val
        return a_val
    
    # Ensure 'a' is coprime with alphabet length
    alphabet_len = len(alphabet)
    while gcd(a, alphabet_len) != 1:
        a = (a + 1) % alphabet_len
        if a == 0:
            a = 1
    
    pairs = []
    used_letters = set()
    
    for i in range(len(alphabet)):
        if len(pairs) >= num_pairs:
            break
        
        if alphabet[i] not in used_letters:
            # Calculate Affine transformation: E(x) = (ax + b) mod 26
            encrypted_index = (a * i + b) % alphabet_len
            encrypted_letter = alphabet[encrypted_index]
            
            if encrypted_letter not in used_letters:
                pairs.append((alphabet[i], encrypted_letter))
                used_letters.add(alphabet[i])
                used_letters.add(encrypted_letter)
    
    return pairs

def generate_prime_position_pairs(alphabet: str, num_pairs: int = None) -> List[Tuple[str, str]]:
    """
    Generate pairs based on prime number positions
    
    Args:
        alphabet: The alphabet to create pairs from
        num_pairs: Number of pairs to generate (default: half of alphabet length)
    
    Returns:
        List of tuples representing prime position pairs
    """
    if num_pairs is None:
        num_pairs = len(alphabet) // 2
    
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    pairs = []
    used_letters = set()
    
    for i in range(len(alphabet)):
        if len(pairs) >= num_pairs:
            break
        
        if is_prime(i + 1) and alphabet[i] not in used_letters:
            # Find next prime position
            for j in range(i + 1, len(alphabet)):
                if is_prime(j + 1) and alphabet[j] not in used_letters:
                    pairs.append((alphabet[i], alphabet[j]))
                    used_letters.add(alphabet[i])
                    used_letters.add(alphabet[j])
                    break
    
    return pairs

def analyze_pairing_strategy(pairs: List[Tuple[str, str]], alphabet: str, 
                           test_text: str = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG") -> Dict:
    """
    Analyze a pairing strategy
    
    Args:
        pairs: List of pairs to analyze
        alphabet: The alphabet used
        test_text: Text to test with
    
    Returns:
        Dictionary with analysis results
    """
    from cryptology.classical.substitution.polyalphabetic import porta_encrypt, porta_decrypt
    
    try:
        # Test encryption/decryption
        encrypted = porta_encrypt(test_text, "TEST", alphabet, pairs)
        decrypted = porta_decrypt(encrypted, "TEST", alphabet, pairs)
        
        # Calculate statistics
        total_chars = len([c for c in test_text if c.isalpha()])
        changed_chars = sum(1 for i, c in enumerate(test_text) if c.isalpha() and encrypted[i] != c)
        change_rate = (changed_chars / total_chars) * 100 if total_chars > 0 else 0
        
        return {
            'success': test_text == decrypted,
            'change_rate': change_rate,
            'pairs_count': len(pairs),
            'encrypted': encrypted,
            'decrypted': decrypted
        }
    except Exception as e:
        return {'error': str(e)}

def demonstrate_pairing_generators():
    """Demonstrate all pairing strategy generators"""
    
    print("=" * 80)
    print("CUSTOM PAIRING STRATEGY GENERATORS")
    print("=" * 80)
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    test_text = "HELLO WORLD"
    
    generators = {
        "Frequency-Based": lambda: generate_frequency_based_pairs(alphabet, 10),
        "Atbash/Symmetric": lambda: generate_atbash_symmetric_pairs(alphabet, 10),
        "Caesar-Shifted (+13)": lambda: generate_caesar_pairs(alphabet, 13, 10),
        "Affine-Based (a=3, b=1)": lambda: generate_affine_pairs(alphabet, 3, 1, 10),
        "Affine-Based (a=5, b=2)": lambda: generate_affine_pairs(alphabet, 5, 2, 10),
        "Prime Position": lambda: generate_prime_position_pairs(alphabet, 10)
    }
    
    for strategy_name, generator_func in generators.items():
        print(f"\n{strategy_name}")
        print("-" * 50)
        
        try:
            pairs = generator_func()
            print(f"Generated pairs: {pairs}")
            
            # Analyze the strategy
            analysis = analyze_pairing_strategy(pairs, alphabet, test_text)
            
            if 'error' in analysis:
                print(f"Error: {analysis['error']}")
            else:
                print(f"Test text: {test_text}")
                print(f"Encrypted: {analysis['encrypted']}")
                print(f"Decrypted: {analysis['decrypted']}")
                print(f"Success: {analysis['success']}")
                print(f"Change rate: {analysis['change_rate']:.1f}%")
                print(f"Pairs count: {analysis['pairs_count']}")
        
        except Exception as e:
            print(f"Error generating pairs: {e}")
    
    print("\n" + "=" * 80)
    print("GENERATOR DEMONSTRATION COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_pairing_generators()
