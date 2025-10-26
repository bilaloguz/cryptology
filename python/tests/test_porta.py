"""
Tests for Porta cipher implementation.
"""

import unittest
from cryptology.classical.substitution.polyalphabetic.porta import (
    encrypt, decrypt, generate_random_key, generate_key_for_text, encrypt_with_random_key
)


class TestPortaCipher(unittest.TestCase):
    """Test cases for Porta cipher."""
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "URYYB JBEYQ")
    
    def test_alphabetic_key_validation(self):
        """Test that only alphabetic keys are accepted."""
        plaintext = "HELLO"
        
        # Valid alphabetic key
        encrypt(plaintext, "ABC")
        
        # Invalid keys should raise ValueError
        with self.assertRaises(ValueError):
            encrypt(plaintext, "123")
        
        with self.assertRaises(ValueError):
            encrypt(plaintext, "AB1C")
        
        with self.assertRaises(ValueError):
            encrypt(plaintext, "")
    
    def test_key_repetition(self):
        """Test that key repeats for longer messages."""
        plaintext = "THIS IS A LONG MESSAGE THAT REQUIRES KEY REPETITION"
        key = "AB"  # Short key
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_case_preservation(self):
        """Test that case is preserved."""
        plaintext = "Hello World"
        key = "KEY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "Uryyb Jbeyq")
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        plaintext = "HELLO, WORLD! 123"
        key = "KEY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_empty_input(self):
        """Test empty input handling."""
        self.assertEqual(encrypt("", "ABC"), "")
        self.assertEqual(decrypt("", "ABC"), "")
    
    def test_self_reciprocal_property(self):
        """Test that Porta cipher is self-reciprocal."""
        plaintext = "SECRET MESSAGE"
        key = "PORTACIPHER"
        
        encrypted = encrypt(plaintext, key)
        
        # Self-reciprocal: encrypting the encrypted text should give back plaintext
        self.assertEqual(encrypt(encrypted, key), plaintext)
        
        # Self-reciprocal: decrypting the plaintext should give the encrypted text
        self.assertEqual(decrypt(plaintext, key), encrypted)
    
    def test_alphabet_pairs(self):
        """Test that alphabet pairs work correctly."""
        # Test with key 'A' (first pair: A↔N)
        encrypted_a = encrypt("A", "A")
        self.assertEqual(encrypted_a, "N")
        
        encrypted_n = encrypt("N", "A")
        self.assertEqual(encrypted_n, "A")
        
        # Test with key 'B' (same pair as A, but different mapping)
        encrypted_b = encrypt("A", "B")
        self.assertEqual(encrypted_b, "A")  # B maps A to A
        
        encrypted_b_n = encrypt("N", "B")
        self.assertEqual(encrypted_b_n, "N")  # B maps N to N
        
        # Test with key 'C' (second pair: C↔P)
        encrypted_c = encrypt("C", "C")
        self.assertEqual(encrypted_c, "P")
        
        encrypted_p = encrypt("P", "C")
        self.assertEqual(encrypted_p, "C")
    
    def test_turkish_alphabet(self):
        """Test with Turkish alphabet."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        plaintext = "MERHABA"
        key = "KEY"
        
        encrypted = encrypt(plaintext, key, alphabet=turkish_alphabet)
        decrypted = decrypt(encrypted, key, alphabet=turkish_alphabet)
        
        self.assertEqual(decrypted, plaintext)


class TestPortaRandomKeyGeneration(unittest.TestCase):
    """Test cases for random key generation."""
    
    def test_generate_random_key(self):
        """Test random key generation."""
        key = generate_random_key(10)
        
        self.assertEqual(len(key), 10)
        self.assertTrue(key.isalpha())
        self.assertTrue(key.isupper())
    
    def test_generate_key_for_text(self):
        """Test key generation for text."""
        plaintext = "HELLO WORLD"
        key = generate_key_for_text(plaintext)
        
        # Should generate key for 10 alphabetic characters
        self.assertEqual(len(key), 10)
        self.assertTrue(key.isalpha())
        self.assertTrue(key.isupper())
    
    def test_empty_text_key_generation(self):
        """Test key generation for empty text."""
        key = generate_key_for_text("")
        self.assertEqual(key, "")
    
    def test_encrypt_with_random_key(self):
        """Test encryption with random key."""
        plaintext = "HELLO WORLD"
        encrypted, key = encrypt_with_random_key(plaintext)
        
        self.assertTrue(key.isalpha())
        self.assertEqual(len(key), 10)  # 10 alphabetic characters
        
        decrypted = decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_with_specified_key_length(self):
        """Test encryption with specified key length."""
        plaintext = "HELLO"
        encrypted, key = encrypt_with_random_key(plaintext, key_length=8)
        
        self.assertEqual(len(key), 8)
        self.assertTrue(key.isalpha())
        
        decrypted = decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)


class TestPortaCustomAlphabet(unittest.TestCase):
    """Test cases for custom alphabet usage."""
    
    def test_custom_alphabet_pairs(self):
        """Test that custom alphabets create correct pairs."""
        # Test with a smaller alphabet
        custom_alphabet = "ABCDEFGHIJKL"  # 12 letters
        plaintext = "ABC"
        key = "ABC"
        
        encrypted = encrypt(plaintext, key, alphabet=custom_alphabet)
        decrypted = decrypt(encrypted, key, alphabet=custom_alphabet)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_turkish_alphabet_pairs(self):
        """Test Turkish alphabet pair creation."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        plaintext = "ABC"
        key = "ABC"
        
        encrypted = encrypt(plaintext, key, alphabet=turkish_alphabet)
        decrypted = decrypt(encrypted, key, alphabet=turkish_alphabet)
        
        self.assertEqual(decrypted, plaintext)


class TestPortaEdgeCases(unittest.TestCase):
    """Test cases for edge cases and error handling."""
    
    def test_single_character_key(self):
        """Test with single character key."""
        plaintext = "HELLO WORLD"
        key = "A"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_key_longer_than_text(self):
        """Test with key longer than text."""
        plaintext = "HI"
        key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_mixed_case_key(self):
        """Test with mixed case key."""
        plaintext = "HELLO"
        key = "Key"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_mixed_case_plaintext(self):
        """Test with mixed case plaintext."""
        plaintext = "HeLlO WoRlD"
        key = "KEY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
