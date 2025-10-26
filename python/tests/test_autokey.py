"""
Test suite for Auto-key cipher implementation.

This module tests the Auto-key cipher with different table types,
including classical tabula recta and custom tables generated using monoalphabetic ciphers.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polyalphabetic import (
    autokey_encrypt, autokey_decrypt, autokey_produce_table,
    autokey_generate_random_key, autokey_generate_key_for_text,
    autokey_encrypt_with_random_key
)


class TestAutokeyCipher(unittest.TestCase):
    """Test cases for Auto-key cipher implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        self.test_plaintext = "HELLO WORLD"
        self.test_key = "KEY"
    
    def test_classical_table_generation(self):
        """Test classical Auto-key table generation."""
        table = autokey_produce_table("classical")
        
        # Check table dimensions
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Check first row (should be alphabet)
        self.assertEqual(table[0], list(self.english_alphabet))
        
        # Check second row (should be alphabet shifted by 1)
        expected_second_row = list(self.english_alphabet[1:] + self.english_alphabet[0])
        self.assertEqual(table[1], expected_second_row)
    
    def test_caesar_table_generation(self):
        """Test Caesar-based Auto-key table generation."""
        table = autokey_produce_table("caesar", shift=3)
        
        # Check table dimensions
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Check first row (should be alphabet shifted by 3)
        expected_first_row = list(self.english_alphabet[3:] + self.english_alphabet[:3])
        self.assertEqual(table[0], expected_first_row)
    
    def test_affine_table_generation(self):
        """Test Affine-based Auto-key table generation."""
        table = autokey_produce_table("affine", a=3, b=5)
        
        # Check table dimensions
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Check that table is generated without errors
        self.assertIsInstance(table, list)
        self.assertTrue(all(isinstance(row, list) for row in table))
    
    def test_keyword_table_generation(self):
        """Test Keyword-based Auto-key table generation."""
        table = autokey_produce_table("keyword", keyword="SECRET")
        
        # Check table dimensions
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Check that table is generated without errors
        self.assertIsInstance(table, list)
        self.assertTrue(all(isinstance(row, list) for row in table))
    
    def test_atbash_table_generation(self):
        """Test Atbash-based Auto-key table generation."""
        table = autokey_produce_table("atbash")
        
        # Check table dimensions
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Check first row (should be reversed alphabet)
        expected_first_row = list(self.english_alphabet[::-1])
        self.assertEqual(table[0], expected_first_row)
    
    def test_turkish_alphabet_table(self):
        """Test table generation with Turkish alphabet."""
        table = autokey_produce_table("classical", alphabet=self.turkish_alphabet)
        
        # Check table dimensions (29x29 for Turkish)
        self.assertEqual(len(table), 29)
        self.assertEqual(len(table[0]), 29)
        
        # Check first row
        self.assertEqual(table[0], list(self.turkish_alphabet))
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        plaintext = "HELLO"
        key = "KEY"
        
        encrypted = autokey_encrypt(plaintext, key)
        decrypted = autokey_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_key_extension_mechanism(self):
        """Test that Auto-key extends the key using plaintext."""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = autokey_encrypt(plaintext, key)
        
        # The encrypted text should be different from Vigenère with the same key
        # because Auto-key extends the key with the plaintext
        from cryptology.classical.substitution.polyalphabetic import vigenere_encrypt
        vigenere_encrypted = vigenere_encrypt(plaintext, key)
        
        self.assertNotEqual(encrypted, vigenere_encrypted)
        
        # But decryption should still work
        decrypted = autokey_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_different_table_types(self):
        """Test encryption with different table types."""
        plaintext = "ATTACK AT DAWN"
        key = "LEMON"
        
        # Test with different table types
        table_types = [
            ("classical", {}),
            ("caesar", {"shift": 7}),
            ("affine", {"a": 3, "b": 5}),
            ("keyword", {"keyword": "SECRET"}),
            ("atbash", {})
        ]
        
        for table_type, params in table_types:
            with self.subTest(table_type=table_type):
                table = autokey_produce_table(table_type, **params)
                encrypted = autokey_encrypt(plaintext, key, table=table)
                decrypted = autokey_decrypt(encrypted, key, table=table)
                
                self.assertEqual(decrypted, plaintext)
    
    def test_turkish_alphabet_encryption(self):
        """Test encryption with Turkish alphabet."""
        turkish_text = "MERHABA DÜNYA"
        key = "GİZLİ"
        turkish_table = autokey_produce_table("classical", alphabet=self.turkish_alphabet)
        
        encrypted = autokey_encrypt(turkish_text, key, table=turkish_table, alphabet=self.turkish_alphabet)
        decrypted = autokey_decrypt(encrypted, key, table=turkish_table, alphabet=self.turkish_alphabet)
        
        # Note: Turkish characters are preserved when using Turkish alphabet
        expected_decrypted = "MERHABA DÜNYA"
        self.assertEqual(decrypted, expected_decrypted)
    
    def test_key_repetition(self):
        """Test that keys are extended for longer plaintext."""
        plaintext = "HELLO WORLD"  # 10 characters
        key = "KEY"  # 3 characters
        
        encrypted = autokey_encrypt(plaintext, key)
        
        # Should not raise an error and should produce output
        self.assertIsInstance(encrypted, str)
        self.assertGreater(len(encrypted), 0)
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        # Empty plaintext
        self.assertEqual(autokey_encrypt("", "KEY"), "")
        self.assertEqual(autokey_decrypt("", "KEY"), "")
        
        # Empty key
        self.assertEqual(autokey_encrypt("HELLO", ""), "")
        self.assertEqual(autokey_decrypt("HELLO", ""), "")
    
    def test_case_insensitive(self):
        """Test that encryption is case insensitive."""
        plaintext_upper = "HELLO WORLD"
        plaintext_lower = "hello world"
        key = "KEY"
        
        encrypted_upper = autokey_encrypt(plaintext_upper, key)
        encrypted_lower = autokey_encrypt(plaintext_lower, key)
        
        self.assertEqual(encrypted_upper, encrypted_lower)
    
    def test_space_preservation(self):
        """Test that spaces are preserved."""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = autokey_encrypt(plaintext, key)
        decrypted = autokey_decrypt(encrypted, key)
        
        # Spaces should be preserved
        self.assertEqual(decrypted, plaintext)
        self.assertIn(' ', encrypted)
    
    def test_special_characters(self):
        """Test handling of special characters."""
        plaintext = "HELLO, WORLD!"
        key = "KEY"
        
        encrypted = autokey_encrypt(plaintext, key)
        decrypted = autokey_decrypt(encrypted, key)
        
        # Special characters should be ignored, spaces preserved
        self.assertEqual(decrypted, "HELLO WORLD")
    
    def test_invalid_table_type(self):
        """Test error handling for invalid table type."""
        with self.assertRaises(ValueError):
            autokey_produce_table("invalid")
    
    def test_missing_parameters(self):
        """Test error handling for missing parameters."""
        with self.assertRaises(ValueError):
            autokey_produce_table("caesar")  # Missing shift
        
        with self.assertRaises(ValueError):
            autokey_produce_table("affine")  # Missing a and b
        
        with self.assertRaises(ValueError):
            autokey_produce_table("keyword")  # Missing keyword)


class TestAutokeyRandomKeyGeneration(unittest.TestCase):
    """Test cases for Auto-key random key generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        self.test_plaintext = "HELLO WORLD"
    
    def test_generate_random_key_basic(self):
        """Test basic random key generation."""
        # Test different lengths
        for length in [1, 5, 10, 20]:
            key = autokey_generate_random_key(length)
            self.assertEqual(len(key), length)
            self.assertTrue(all(c in self.english_alphabet for c in key))
    
    def test_generate_random_key_turkish(self):
        """Test random key generation with Turkish alphabet."""
        key = autokey_generate_random_key(10, self.turkish_alphabet)
        self.assertEqual(len(key), 10)
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
    
    def test_generate_random_key_invalid_length(self):
        """Test random key generation with invalid length."""
        with self.assertRaises(ValueError):
            autokey_generate_random_key(0)
        
        with self.assertRaises(ValueError):
            autokey_generate_random_key(-1)
    
    def test_generate_random_key_empty_alphabet(self):
        """Test random key generation with empty alphabet."""
        with self.assertRaises(ValueError):
            autokey_generate_random_key(5, "")
    
    def test_generate_key_for_text(self):
        """Test key generation for specific text."""
        key = autokey_generate_key_for_text(self.test_plaintext)
        
        # Key should match the length of alphabetic characters only
        alphabetic_chars = sum(1 for c in self.test_plaintext.upper() if c.isalpha())
        self.assertEqual(len(key), alphabetic_chars)
        self.assertTrue(all(c in self.english_alphabet for c in key))
    
    def test_generate_key_for_empty_text(self):
        """Test key generation for empty text."""
        key = autokey_generate_key_for_text("")
        self.assertEqual(key, "")
    
    def test_generate_key_for_text_turkish(self):
        """Test key generation for Turkish text."""
        turkish_text = "MERHABA DÜNYA"
        key = autokey_generate_key_for_text(turkish_text, self.turkish_alphabet)
        
        # Should handle Turkish characters properly
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
        self.assertGreater(len(key), 0)
    
    def test_encrypt_with_random_key_basic(self):
        """Test encryption with random key generation."""
        encrypted, key = autokey_encrypt_with_random_key(self.test_plaintext)
        
        # Should return both encrypted text and key
        self.assertIsInstance(encrypted, str)
        self.assertIsInstance(key, str)
        self.assertGreater(len(key), 0)
        
        # Should be able to decrypt
        decrypted = autokey_decrypt(encrypted, key)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_custom_length(self):
        """Test encryption with custom key length."""
        key_length = 15
        encrypted, key = autokey_encrypt_with_random_key(
            self.test_plaintext, key_length=key_length
        )
        
        self.assertEqual(len(key), key_length)
        
        # Should still decrypt correctly
        decrypted = autokey_decrypt(encrypted, key)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_custom_table(self):
        """Test encryption with random key and custom table."""
        caesar_table = autokey_produce_table("caesar", shift=5)
        encrypted, key = autokey_encrypt_with_random_key(
            self.test_plaintext, table=caesar_table
        )
        
        # Should decrypt correctly with the same table
        decrypted = autokey_decrypt(encrypted, key, table=caesar_table)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_turkish(self):
        """Test encryption with random key and Turkish alphabet."""
        turkish_text = "MERHABA DÜNYA"
        turkish_table = autokey_produce_table("classical", alphabet=self.turkish_alphabet)
        
        encrypted, key = autokey_encrypt_with_random_key(
            turkish_text, table=turkish_table, alphabet=self.turkish_alphabet
        )
        
        # Key should be Turkish characters
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
        
        # Should decrypt correctly (Turkish characters are preserved)
        decrypted = autokey_decrypt(encrypted, key, table=turkish_table, alphabet=self.turkish_alphabet)
        expected_decrypted = "MERHABA DÜNYA"  # Turkish characters are preserved
        self.assertEqual(decrypted, expected_decrypted)
    
    def test_encrypt_with_random_key_empty_text(self):
        """Test encryption with random key for empty text."""
        with self.assertRaises(ValueError):
            autokey_encrypt_with_random_key("")
    
    def test_key_uniqueness(self):
        """Test that generated keys are unique."""
        keys = set()
        
        # Generate multiple keys
        for _ in range(10):
            key = autokey_generate_random_key(10)
            keys.add(key)
        
        # Should have unique keys (very high probability)
        self.assertEqual(len(keys), 10)
    
    def test_key_randomness(self):
        """Test that generated keys appear random."""
        # Generate many keys and check character distribution
        keys = [autokey_generate_random_key(100) for _ in range(5)]
        
        # All keys should be different
        self.assertEqual(len(set(keys)), 5)
        
        # Keys should contain various characters
        all_chars = set(''.join(keys))
        self.assertGreater(len(all_chars), 10)  # Should use many different characters
    
    def test_integration_with_all_table_types(self):
        """Test random key generation with all table types."""
        plaintext = "CRYPTOGRAPHIC SECURITY"
        
        table_types = [
            ("classical", {}),
            ("caesar", {"shift": 7}),
            ("affine", {"a": 3, "b": 5}),
            ("atbash", {})
        ]
        
        for table_type, params in table_types:
            with self.subTest(table_type=table_type):
                table = autokey_produce_table(table_type, **params)
                encrypted, key = autokey_encrypt_with_random_key(plaintext, table=table)
                
                # Should decrypt correctly
                decrypted = autokey_decrypt(encrypted, key, table=table)
                self.assertEqual(decrypted, plaintext)
    
    def test_key_length_vs_text_length(self):
        """Test relationship between key length and text length."""
        texts = [
            "A",
            "HELLO",
            "HELLO WORLD",
            "VERY LONG MESSAGE WITH MANY WORDS"
        ]
        
        for text in texts:
            with self.subTest(text=text):
                key = autokey_generate_key_for_text(text)
                alphabetic_chars = sum(1 for c in text.upper() if c.isalpha())
                self.assertEqual(len(key), alphabetic_chars)
    
    def test_security_properties(self):
        """Test security properties of random keys."""
        # Test that random keys are not predictable
        key1 = autokey_generate_random_key(20)
        key2 = autokey_generate_random_key(20)
        
        # Keys should be different
        self.assertNotEqual(key1, key2)
        
        # Keys should not follow obvious patterns
        self.assertFalse(key1 == key1[0] * len(key1))  # Not all same character
        self.assertFalse(key1.isalpha() and key1.isupper() and len(set(key1)) == 1)  # Not single repeated letter


if __name__ == '__main__':
    unittest.main()
