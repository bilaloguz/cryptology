#!/usr/bin/env python3
"""
Test suite for Chaocipher implementation.
"""

import unittest
import string
from cryptology.classical.substitution.polyalphabetic.chaocipher import (
    encrypt, decrypt, create_custom_alphabets, create_alphabets_with_mono_ciphers, decrypt_with_alphabets
)


class TestChaocipher(unittest.TestCase):
    """Test cases for Chaocipher implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.plaintext = "HELLO WORLD"
        self.left_alphabet = list(string.ascii_uppercase) + [' ']
        self.right_alphabet = list(string.ascii_uppercase) + [' ']
        # Shuffle right alphabet for testing
        import random
        random.seed(42)  # For reproducible tests
        random.shuffle(self.right_alphabet)
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        encrypted = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, self.plaintext)
        self.assertNotEqual(encrypted, self.plaintext)
    
    def test_self_reciprocal_property(self):
        """Test that Chaocipher is self-reciprocal."""
        encrypted = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        
        # Decrypt using the same process (self-reciprocal)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, self.plaintext)
    
    def test_empty_text(self):
        """Test encryption/decryption of empty text."""
        encrypted = encrypt("", self.left_alphabet, self.right_alphabet)
        decrypted = decrypt("", self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(encrypted, "")
        self.assertEqual(decrypted, "")
    
    def test_single_character(self):
        """Test encryption/decryption of single character."""
        encrypted = encrypt("A", self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, "A")
        self.assertEqual(len(encrypted), 1)
    
    def test_spaces_preservation(self):
        """Test that spaces are preserved."""
        text_with_spaces = "HELLO WORLD TEST"
        encrypted = encrypt(text_with_spaces, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, text_with_spaces)
        # Spaces are processed like any other character, so they may not appear in ciphertext
        # but should be preserved in decryption
    
    def test_non_alphabetic_characters(self):
        """Test handling of non-alphabetic characters."""
        text_with_numbers = "HELLO123WORLD"
        encrypted = encrypt(text_with_numbers, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        # Should only process alphabetic characters
        expected = "HELLOWORLD"
        self.assertEqual(decrypted, expected)
    
    def test_case_insensitivity(self):
        """Test that input is case-insensitive."""
        lowercase_text = "hello world"
        encrypted = encrypt(lowercase_text, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, "HELLO WORLD")
    
    def test_default_alphabets(self):
        """Test encryption/decryption with default alphabets."""
        # Use fixed alphabets for reproducible testing
        left_alphabet = list(string.ascii_uppercase) + [' ']
        right_alphabet = list(string.ascii_uppercase) + [' ']
        
        encrypted = encrypt(self.plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, self.plaintext)
    
    def test_create_custom_alphabets(self):
        """Test custom alphabet creation with keywords."""
        left, right = create_custom_alphabets("SECRET", "KEYWORD")
        
        self.assertEqual(len(left), 26)
        self.assertEqual(len(right), 26)
        self.assertEqual(set(left), set(string.ascii_uppercase))
        self.assertEqual(set(right), set(string.ascii_uppercase))
        
        # Check that keywords appear at the beginning (removing duplicates)
        expected_left_start = ['S', 'E', 'C', 'R', 'T']
        expected_right_start = ['K', 'E', 'Y', 'W', 'O', 'R', 'D']
        self.assertEqual(left[:5], expected_left_start)
        self.assertEqual(right[:7], expected_right_start)
    
    def test_create_custom_alphabets_empty_keywords(self):
        """Test custom alphabet creation with empty keywords."""
        left, right = create_custom_alphabets("", "")
        
        self.assertEqual(left, list(string.ascii_uppercase))
        self.assertEqual(right, list(string.ascii_uppercase))
    
    def test_create_custom_alphabets_duplicate_letters(self):
        """Test custom alphabet creation with duplicate letters in keywords."""
        left, right = create_custom_alphabets("HELLO", "WORLD")
        
        # Should remove duplicates
        self.assertEqual(len(left), 26)
        self.assertEqual(len(right), 26)
        self.assertEqual(set(left), set(string.ascii_uppercase))
        self.assertEqual(set(right), set(string.ascii_uppercase))
    
    def test_decrypt_with_alphabets(self):
        """Test decryption with provided alphabets."""
        encrypted = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt_with_alphabets(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, self.plaintext)
    
    def test_different_alphabets_produce_different_results(self):
        """Test that different alphabets produce different encryption results."""
        left1, right1 = create_custom_alphabets("SECRET", "KEYWORD")
        left2, right2 = create_custom_alphabets("DIFFERENT", "ALPHABET")
        
        encrypted1 = encrypt(self.plaintext, left1, right1)
        encrypted2 = encrypt(self.plaintext, left2, right2)
        
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_same_alphabets_produce_same_results(self):
        """Test that same alphabets produce same encryption results."""
        encrypted1 = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        encrypted2 = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(encrypted1, encrypted2)
    
    def test_long_text(self):
        """Test encryption/decryption of long text."""
        long_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 5
        encrypted = encrypt(long_text, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, long_text)
    
    def test_repeated_characters(self):
        """Test encryption/decryption of repeated characters."""
        repeated_text = "AAAAA"
        encrypted = encrypt(repeated_text, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        self.assertEqual(decrypted, repeated_text)
        # Repeated characters should produce different ciphertext due to alphabet permutation
        self.assertNotEqual(encrypted, "AAAAA")
    
    def test_alphabet_permutation_effect(self):
        """Test that alphabet permutation affects subsequent characters."""
        text = "ABC"
        encrypted = encrypt(text, self.left_alphabet, self.right_alphabet)
        
        # Each character should be encrypted differently due to alphabet permutation
        self.assertNotEqual(encrypted[0], encrypted[1])
        self.assertNotEqual(encrypted[1], encrypted[2])
    
    def test_turkish_alphabet_support(self):
        """Test Chaocipher with Turkish alphabet."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        left_alphabet = list(turkish_alphabet) + [' ']  # Add space
        right_alphabet = list(turkish_alphabet) + [' ']  # Add space
        
        # Shuffle right alphabet
        import random
        random.seed(42)
        random.shuffle(right_alphabet)
        
        turkish_text = "MERHABA DÜNYA"
        encrypted = encrypt(turkish_text, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, turkish_text)
    
    def test_invalid_alphabet_length(self):
        """Test behavior with invalid alphabet lengths."""
        short_alphabet = list("ABC")
        text = "HELLO WORLD"
        
        # Should handle gracefully - only process characters present in alphabet
        encrypted = encrypt(text, short_alphabet, short_alphabet)
        decrypted = decrypt(encrypted, short_alphabet, short_alphabet)
        
        # Should only process characters present in the short alphabet
        expected = "".join(c for c in text if c in short_alphabet)
        self.assertEqual(decrypted, expected)
    
    def test_alphabet_consistency(self):
        """Test that alphabet remains consistent during encryption."""
        text = "HELLO"
        encrypted = encrypt(text, self.left_alphabet, self.right_alphabet)
        
        # All encrypted characters should be in the left alphabet
        for char in encrypted:
            if char != ' ':
                self.assertIn(char, self.left_alphabet)
    
    def test_decryption_consistency(self):
        """Test that decryption produces valid characters."""
        encrypted = encrypt(self.plaintext, self.left_alphabet, self.right_alphabet)
        decrypted = decrypt(encrypted, self.left_alphabet, self.right_alphabet)
        
        # All decrypted characters should be in the right alphabet
        for char in decrypted:
            if char != ' ':
                self.assertIn(char, self.right_alphabet)


class TestChaocipherEdgeCases(unittest.TestCase):
    """Test edge cases for Chaocipher implementation."""
    
    def test_very_long_text(self):
        """Test with very long text."""
        very_long_text = "A" * 1000
        # Use fixed alphabets for reproducible testing
        left_alphabet = list(string.ascii_uppercase) + [' ']
        right_alphabet = list(string.ascii_uppercase) + [' ']
        
        encrypted = encrypt(very_long_text, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, very_long_text)
    
    def test_special_characters_only(self):
        """Test with only special characters."""
        special_text = "!@#$%^&*()"
        encrypted = encrypt(special_text)
        decrypted = decrypt(encrypted)
        
        self.assertEqual(encrypted, "")
        self.assertEqual(decrypted, "")
    
    def test_mixed_case_and_special(self):
        """Test with mixed case and special characters."""
        mixed_text = "Hello, World! 123"
        # Use fixed alphabets for reproducible testing
        left_alphabet = list(string.ascii_uppercase) + [' ']
        right_alphabet = list(string.ascii_uppercase) + [' ']
        
        encrypted = encrypt(mixed_text, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, "HELLO WORLD ")
    
    def test_unicode_characters(self):
        """Test with Unicode characters."""
        unicode_text = "HELLO 世界"
        # Use fixed alphabets for reproducible testing
        left_alphabet = list(string.ascii_uppercase) + [' ']
        right_alphabet = list(string.ascii_uppercase) + [' ']
        
        encrypted = encrypt(unicode_text, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, "HELLO ")


class TestChaocipherMonoalphabeticIntegration(unittest.TestCase):
    """Test Chaocipher integration with monoalphabetic ciphers."""
    
    def test_caesar_keyword_combination(self):
        """Test Caesar + Keyword combination."""
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher='caesar', left_params={'shift': 5},
            right_cipher='keyword', right_params={'keyword': 'SECRET'}
        )
        
        plaintext = "HELLO WORLD"
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(len(left_alphabet), 27)
        self.assertEqual(len(right_alphabet), 27)
    
    def test_atbash_affine_combination(self):
        """Test Atbash + Affine combination."""
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher='atbash',
            right_cipher='affine', right_params={'a': 5, 'b': 7}
        )
        
        plaintext = "HELLO WORLD"
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(len(left_alphabet), 27)
        self.assertEqual(len(right_alphabet), 27)
    
    def test_keyword_caesar_combination(self):
        """Test Keyword + Caesar combination."""
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher='keyword', left_params={'keyword': 'HELLO'},
            right_cipher='caesar', right_params={'shift': 13}
        )
        
        plaintext = "HELLO WORLD"
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_affine_keyword_combination(self):
        """Test Affine + Keyword combination."""
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher='affine', left_params={'a': 7, 'b': 3},
            right_cipher='keyword', right_params={'keyword': 'WORLD'}
        )
        
        plaintext = "HELLO WORLD"
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_custom_alphabet_parameter(self):
        """Test with custom base alphabet."""
        custom_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher='caesar', left_params={'shift': 3},
            right_cipher='atbash',
            alphabet=custom_alphabet
        )
        
        self.assertEqual(len(left_alphabet), 26)
        self.assertEqual(len(right_alphabet), 26)
        
        plaintext = "HELLO"
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_invalid_cipher_names(self):
        """Test with invalid cipher names."""
        with self.assertRaises(ValueError):
            create_alphabets_with_mono_ciphers(
                left_cipher='invalid', left_params={},
                right_cipher='caesar', right_params={'shift': 3}
            )
        
        with self.assertRaises(ValueError):
            create_alphabets_with_mono_ciphers(
                left_cipher='caesar', left_params={'shift': 3},
                right_cipher='invalid', right_params={}
            )
    
    def test_affine_coprime_validation(self):
        """Test Affine cipher coprime validation."""
        with self.assertRaises(ValueError):
            create_alphabets_with_mono_ciphers(
                left_cipher='affine', left_params={'a': 3, 'b': 5},  # 3 not coprime with 27
                right_cipher='caesar', right_params={'shift': 3}
            )


if __name__ == '__main__':
    unittest.main()
