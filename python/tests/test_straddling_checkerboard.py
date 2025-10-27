"""
Tests for Straddling Checkerboard Cipher Implementation
"""

import unittest
import string
from cryptology.classical.substitution.composite.straddling_checkerboard import (
    straddling_checkerboard_encrypt,
    straddling_checkerboard_decrypt,
    straddling_checkerboard_produce_checkerboard,
    straddling_checkerboard_generate_random_key,
    straddling_checkerboard_generate_key_for_text,
    straddling_checkerboard_encrypt_with_random_key,
    straddling_checkerboard_encrypt_turkish,
    straddling_checkerboard_decrypt_turkish,
    TURKISH_ALPHABET
)


class TestStraddlingCheckerboardCipher(unittest.TestCase):
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        plaintext = "HELLO"
        key = "12345"
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key)
        decrypted = straddling_checkerboard_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertNotEqual(encrypted, plaintext)
    
    def test_numeric_key(self):
        """Test numeric key encryption/decryption."""
        plaintext = "HELLO WORLD"
        key = "12345"
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key, key_type="numeric")
        decrypted = straddling_checkerboard_decrypt(encrypted, key, key_type="numeric")
        
        self.assertEqual(decrypted, plaintext)
    
    def test_alphabetic_key(self):
        """Test alphabetic key encryption/decryption."""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key, key_type="alphabetic")
        decrypted = straddling_checkerboard_decrypt(encrypted, key, key_type="alphabetic")
        
        self.assertEqual(decrypted, plaintext)
    
    def test_standard_checkerboard(self):
        """Test standard checkerboard generation."""
        checkerboard = straddling_checkerboard_produce_checkerboard("standard")
        
        self.assertIsInstance(checkerboard, str)
        self.assertIn("A:0", checkerboard)  # A should map to 0
        self.assertIn("K:10", checkerboard)  # K should map to 10
        self.assertIn("U:20", checkerboard)  # U should map to 20
    
    def test_keyword_checkerboard(self):
        """Test keyword-based checkerboard generation."""
        keyword = "SECRET"
        checkerboard = straddling_checkerboard_produce_checkerboard("keyword", keyword)
        
        self.assertIsInstance(checkerboard, str)
        # S should be first in keyword-based checkerboard
        self.assertIn("S:0", checkerboard)
    
    def test_custom_checkerboard(self):
        """Test custom checkerboard generation."""
        custom_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        checkerboard = straddling_checkerboard_produce_checkerboard("custom", alphabet=custom_alphabet)
        
        self.assertIsInstance(checkerboard, str)
        self.assertIn("A:0", checkerboard)
        self.assertIn("K:10", checkerboard)
        self.assertIn("U:20", checkerboard)
    
    def test_custom_checkerboard_encryption(self):
        """Test encryption with custom checkerboard."""
        plaintext = "HELLO"
        key = "12345"
        custom_checkerboard = straddling_checkerboard_produce_checkerboard("custom")
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key, custom_checkerboard)
        decrypted = straddling_checkerboard_decrypt(encrypted, key, custom_checkerboard)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_keyword_checkerboard_encryption(self):
        """Test encryption with keyword-based checkerboard."""
        plaintext = "HELLO"
        key = "12345"
        keyword = "SECRET"
        keyword_checkerboard = straddling_checkerboard_produce_checkerboard("keyword", keyword)
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key, keyword_checkerboard)
        decrypted = straddling_checkerboard_decrypt(encrypted, key, keyword_checkerboard)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_random_key_generation(self):
        """Test random key generation."""
        # Numeric key
        numeric_key = straddling_checkerboard_generate_random_key(5, "numeric")
        self.assertEqual(len(numeric_key), 5)
        self.assertTrue(all(c.isdigit() for c in numeric_key))
        
        # Alphabetic key
        alphabetic_key = straddling_checkerboard_generate_random_key(5, "alphabetic")
        self.assertEqual(len(alphabetic_key), 5)
        self.assertTrue(all(c.isalpha() for c in alphabetic_key))
    
    def test_key_for_text_generation(self):
        """Test key generation for specific text length."""
        text_length = 10
        key = straddling_checkerboard_generate_key_for_text(text_length)
        
        self.assertTrue(3 <= len(key) <= min(text_length, 10))
        self.assertTrue(all(c.isdigit() for c in key))
    
    def test_encrypt_with_random_key(self):
        """Test encryption with random key generation."""
        plaintext = "HELLO WORLD"
        
        encrypted, generated_key = straddling_checkerboard_encrypt_with_random_key(plaintext)
        decrypted = straddling_checkerboard_decrypt(encrypted, generated_key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertTrue(len(generated_key) >= 3)
    
    def test_turkish_alphabet(self):
        """Test Turkish alphabet support."""
        plaintext = "MERHABA"
        key = "12345"
        
        encrypted = straddling_checkerboard_encrypt_turkish(plaintext, key)
        decrypted = straddling_checkerboard_decrypt_turkish(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_turkish_alphabet_custom_checkerboard(self):
        """Test Turkish alphabet with custom checkerboard."""
        plaintext = "MERHABA"
        key = "12345"
        turkish_checkerboard = straddling_checkerboard_produce_checkerboard("custom", alphabet=TURKISH_ALPHABET)
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key, turkish_checkerboard)
        decrypted = straddling_checkerboard_decrypt(encrypted, key, turkish_checkerboard)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_long_text(self):
        """Test with longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "123456789"
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key)
        decrypted = straddling_checkerboard_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext.replace(" ", ""))
    
    def test_key_repetition(self):
        """Test that key repeats properly for longer text."""
        plaintext = "HELLO WORLD HELLO WORLD"
        key = "123"
        
        encrypted = straddling_checkerboard_encrypt(plaintext, key)
        decrypted = straddling_checkerboard_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext.replace(" ", ""))
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        self.assertEqual(straddling_checkerboard_encrypt("", "12345"), "")
        self.assertEqual(straddling_checkerboard_encrypt("HELLO", ""), "")
        self.assertEqual(straddling_checkerboard_decrypt("", "12345"), "")
        self.assertEqual(straddling_checkerboard_decrypt("HELLO", ""), "")
    
    def test_invalid_checkerboard_type(self):
        """Test handling of invalid checkerboard type."""
        with self.assertRaises(ValueError):
            straddling_checkerboard_produce_checkerboard("invalid")
    
    def test_keyword_required(self):
        """Test that keyword is required for keyword-based checkerboard."""
        with self.assertRaises(ValueError):
            straddling_checkerboard_produce_checkerboard("keyword")
    
    def test_invalid_key_type(self):
        """Test handling of invalid key type."""
        with self.assertRaises(ValueError):
            straddling_checkerboard_generate_random_key(5, "invalid")
    
    def test_negative_key_length(self):
        """Test handling of negative key length."""
        with self.assertRaises(ValueError):
            straddling_checkerboard_generate_random_key(-1)
        
        with self.assertRaises(ValueError):
            straddling_checkerboard_generate_key_for_text(-1)
    
    def test_special_characters(self):
        """Test handling of special characters."""
        plaintext = "HELLO, WORLD!"
        key = "12345"
        
        # Should preserve only alphabetic characters
        encrypted = straddling_checkerboard_encrypt(plaintext, key)
        decrypted = straddling_checkerboard_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, "HELLOWORLD")
    
    def test_case_insensitive(self):
        """Test that encryption is case insensitive."""
        plaintext_lower = "hello world"
        plaintext_upper = "HELLO WORLD"
        key = "12345"
        
        encrypted_lower = straddling_checkerboard_encrypt(plaintext_lower, key)
        encrypted_upper = straddling_checkerboard_encrypt(plaintext_upper, key)
        
        self.assertEqual(encrypted_lower, encrypted_upper)
    
    def test_different_checkerboards_same_text(self):
        """Test that different checkerboards produce different results."""
        plaintext = "HELLO"
        key = "12345"
        
        standard_checkerboard = straddling_checkerboard_produce_checkerboard("standard")
        keyword_checkerboard = straddling_checkerboard_produce_checkerboard("keyword", "SECRET")
        
        encrypted_standard = straddling_checkerboard_encrypt(plaintext, key, standard_checkerboard)
        encrypted_keyword = straddling_checkerboard_encrypt(plaintext, key, keyword_checkerboard)
        
        # Should produce different results
        self.assertNotEqual(encrypted_standard, encrypted_keyword)
        
        # But both should decrypt correctly
        decrypted_standard = straddling_checkerboard_decrypt(encrypted_standard, key, standard_checkerboard)
        decrypted_keyword = straddling_checkerboard_decrypt(encrypted_keyword, key, keyword_checkerboard)
        
        self.assertEqual(decrypted_standard, plaintext)
        self.assertEqual(decrypted_keyword, plaintext)


if __name__ == '__main__':
    unittest.main()
