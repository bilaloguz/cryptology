"""
Test and demonstrate letter combination strategies for polygraphic ciphers.

This example shows how different letter combination strategies handle
various languages and alphabet sizes for polygraphic ciphers.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polygraphic.letter_combination_strategies import (
    LetterCombinationEngine, CombinationStrategy
)
from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt


def test_turkish_alphabet():
    """Test Turkish alphabet combination strategies."""
    print("=== Turkish Alphabet Combination ===")
    
    # Turkish alphabet (29 letters)
    turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    engine = LetterCombinationEngine()
    
    print(f"Original Turkish alphabet: {turkish_alphabet}")
    print(f"Original size: {len(turkish_alphabet)}")
    print(f"Detected language: {engine.detect_language(turkish_alphabet)}")
    print()
    
    # Test different strategies
    strategies = {
        "Smart Combine": engine.combine_letters(turkish_alphabet, CombinationStrategy.SMART_COMBINE),
        "Preserve Base": engine.combine_letters(turkish_alphabet, CombinationStrategy.PRESERVE_BASE),
        "Generic": engine.combine_letters(turkish_alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
    }
    
    for strategy_name, result in strategies.items():
        print(f"{strategy_name}: {result}")
        print(f"  Size: {len(result)}")
        print()
    
    # Test with Playfair
    try:
        encrypted = playfair_encrypt("merhaba dünya", "gizli", strategies["Smart Combine"])
        decrypted = playfair_decrypt(encrypted, "gizli", strategies["Smart Combine"])
        print(f"Playfair test: '{encrypted}' -> '{decrypted}'")
    except Exception as e:
        print(f"Playfair test failed: {e}")
    
    print()


def test_russian_alphabet():
    """Test Russian alphabet combination strategies."""
    print("=== Russian Alphabet Combination ===")
    
    # Russian alphabet (33 letters)
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    engine = LetterCombinationEngine()
    
    print(f"Original Russian alphabet: {russian_alphabet}")
    print(f"Original size: {len(russian_alphabet)}")
    print(f"Detected language: {engine.detect_language(russian_alphabet)}")
    print()
    
    # Test different strategies
    strategies = {
        "Smart Combine": engine.combine_letters(russian_alphabet, CombinationStrategy.SMART_COMBINE),
        "Preserve Base": engine.combine_letters(russian_alphabet, CombinationStrategy.PRESERVE_BASE),
        "Generic": engine.combine_letters(russian_alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
    }
    
    for strategy_name, result in strategies.items():
        print(f"{strategy_name}: {result}")
        print(f"  Size: {len(result)}")
        print()
    
    print()


def test_german_alphabet():
    """Test German alphabet combination strategies."""
    print("=== German Alphabet Combination ===")
    
    # German alphabet with umlauts
    german_alphabet = "abcdefghijklmnopqrstuvwxyzäöüß"
    engine = LetterCombinationEngine()
    
    print(f"Original German alphabet: {german_alphabet}")
    print(f"Original size: {len(german_alphabet)}")
    print(f"Detected language: {engine.detect_language(german_alphabet)}")
    print()
    
    # Test different strategies
    strategies = {
        "Smart Combine": engine.combine_letters(german_alphabet, CombinationStrategy.SMART_COMBINE),
        "Preserve Base": engine.combine_letters(german_alphabet, CombinationStrategy.PRESERVE_BASE),
        "Generic": engine.combine_letters(german_alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
    }
    
    for strategy_name, result in strategies.items():
        print(f"{strategy_name}: {result}")
        print(f"  Size: {len(result)}")
        print()
    
    print()


def test_spanish_alphabet():
    """Test Spanish alphabet combination strategies."""
    print("=== Spanish Alphabet Combination ===")
    
    # Spanish alphabet with ñ and accents
    spanish_alphabet = "abcdefghijklmnñopqrstuvwxyzáéíóú"
    engine = LetterCombinationEngine()
    
    print(f"Original Spanish alphabet: {spanish_alphabet}")
    print(f"Original size: {len(spanish_alphabet)}")
    print(f"Detected language: {engine.detect_language(spanish_alphabet)}")
    print()
    
    # Test different strategies
    strategies = {
        "Smart Combine": engine.combine_letters(spanish_alphabet, CombinationStrategy.SMART_COMBINE),
        "Preserve Base": engine.combine_letters(spanish_alphabet, CombinationStrategy.PRESERVE_BASE),
        "Generic": engine.combine_letters(spanish_alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
    }
    
    for strategy_name, result in strategies.items():
        print(f"{strategy_name}: {result}")
        print(f"  Size: {len(result)}")
        print()
    
    print()


def test_french_alphabet():
    """Test French alphabet combination strategies."""
    print("=== French Alphabet Combination ===")
    
    # French alphabet with many accents
    french_alphabet = "abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüÿç"
    engine = LetterCombinationEngine()
    
    print(f"Original French alphabet: {french_alphabet}")
    print(f"Original size: {len(french_alphabet)}")
    print(f"Detected language: {engine.detect_language(french_alphabet)}")
    print()
    
    # Test different strategies
    strategies = {
        "Smart Combine": engine.combine_letters(french_alphabet, CombinationStrategy.SMART_COMBINE),
        "Preserve Base": engine.combine_letters(french_alphabet, CombinationStrategy.PRESERVE_BASE),
        "Generic": engine.combine_letters(french_alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
    }
    
    for strategy_name, result in strategies.items():
        print(f"{strategy_name}: {result}")
        print(f"  Size: {len(result)}")
        print()
    
    print()


def test_custom_combination_rules():
    """Test custom combination rules."""
    print("=== Custom Combination Rules ===")
    
    # Custom alphabet with special characters
    custom_alphabet = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()"
    engine = LetterCombinationEngine()
    
    print(f"Original custom alphabet: {custom_alphabet}")
    print(f"Original size: {len(custom_alphabet)}")
    print()
    
    # Custom combination rules
    custom_rules = {
        '!': 'i', '@': 'a', '#': 'h', '$': 's', '%': 'p',
        '^': 'v', '&': 'n', '*': 'x', '(': 'c', ')': 'o'
    }
    
    result = engine.combine_letters(custom_alphabet, CombinationStrategy.CUSTOM, custom_rules=custom_rules)
    print(f"Custom rules result: {result}")
    print(f"Size: {len(result)}")
    print()
    
    print()


def test_combination_reports():
    """Test combination strategy reports."""
    print("=== Combination Strategy Reports ===")
    
    test_alphabets = [
        ("Turkish", "abcçdefgğhıijklmnoöprsştuüvyz"),
        ("Russian", "абвгдежзийклмнопрстуфхцчшщъыьэюя"),
        ("German", "abcdefghijklmnopqrstuvwxyzäöüß"),
        ("Spanish", "abcdefghijklmnñopqrstuvwxyzáéíóú"),
        ("French", "abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüÿç")
    ]
    
    engine = LetterCombinationEngine()
    
    for language_name, alphabet in test_alphabets:
        print(f"--- {language_name} Report ---")
        report = engine.get_combination_report(alphabet)
        
        print(f"Original: {report['original_alphabet']}")
        print(f"Size: {report['original_size']}")
        print(f"Detected Language: {report['detected_language']}")
        print("Strategies:")
        for strategy_name, result in report['strategies'].items():
            print(f"  {strategy_name}: {result} (size: {len(result)})")
        print("Recommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
        print()


def test_edge_cases():
    """Test edge cases for letter combination."""
    print("=== Edge Cases ===")
    
    engine = LetterCombinationEngine()
    
    # Very short alphabet
    short_alphabet = "abc"
    print(f"Short alphabet: {short_alphabet}")
    result = engine.combine_letters(short_alphabet, CombinationStrategy.SMART_COMBINE, target_size=25)
    print(f"Result: {result} (size: {len(result)})")
    print()
    
    # Very long alphabet
    long_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?"
    print(f"Long alphabet: {long_alphabet}")
    result = engine.combine_letters(long_alphabet, CombinationStrategy.SMART_COMBINE, target_size=25)
    print(f"Result: {result} (size: {len(result)})")
    print()
    
    # Alphabet with duplicates
    duplicate_alphabet = "aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
    print(f"Duplicate alphabet: {duplicate_alphabet}")
    result = engine.combine_letters(duplicate_alphabet, CombinationStrategy.SMART_COMBINE, target_size=25)
    print(f"Result: {result} (size: {len(result)})")
    print()


if __name__ == "__main__":
    print("Letter Combination Strategies Test")
    print("=" * 50)
    print()
    
    test_turkish_alphabet()
    test_russian_alphabet()
    test_german_alphabet()
    test_spanish_alphabet()
    test_french_alphabet()
    test_custom_combination_rules()
    test_combination_reports()
    test_edge_cases()
    
    print("All tests completed!")
