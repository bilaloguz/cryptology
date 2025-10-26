"""
Tests for Gronsfeld cipher implementation.
"""

import unittest
from cryptology.classical.substitution.polyalphabetic.gronsfeld import (
    encrypt, decrypt, produce_table, generate_random_numeric_key,
    generate_numeric_key_for_text, encrypt_with_random_key
)


class TestGronsfeldCipher(unittest.TestCase):
    """Test cases for Gronsfeld cipher."""
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        plaintext = "HELLO WORLD"
        key = "12312"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "IGOMQ XQUMF")
    
    def test_numeric_key_validation(self):
        """Test that only numeric keys are accepted."""
        plaintext = "HELLO"
        
        # Valid numeric key
        encrypt(plaintext, "12345")
        
        # Invalid keys should raise ValueError
        with self.assertRaises(ValueError):
            encrypt(plaintext, "abc123")
        
        with self.assertRaises(ValueError):
            encrypt(plaintext, "12a34")
        
        with self.assertRaises(ValueError):
            encrypt(plaintext, "")
    
    def test_key_repetition(self):
        """Test that key repeats for longer messages."""
        plaintext = "HELLO WORLD"
        key = "12"  # Short key
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_case_preservation(self):
        """Test that case is preserved."""
        plaintext = "Hello World"
        key = "12312"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "Igomq Xqumf")
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        plaintext = "HELLO, WORLD! 123"
        key = "12312"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_empty_input(self):
        """Test empty input handling."""
        self.assertEqual(encrypt("", "123"), "")
        self.assertEqual(decrypt("", "123"), "")
    
    def test_turkish_alphabet(self):
        """Test with Turkish alphabet."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        plaintext = "MERHABA"
        key = "12312"
        
        encrypted = encrypt(plaintext, key, alphabet=turkish_alphabet)
        decrypted = decrypt(encrypted, key, alphabet=turkish_alphabet)
        
        self.assertEqual(decrypted, plaintext)


class TestGronsfeldTableGeneration(unittest.TestCase):
    """Test cases for Gronsfeld table generation."""
    
    def test_classical_table(self):
        """Test classical table generation."""
        table = produce_table("classical")
        
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # First row should be original alphabet
        self.assertEqual(table[0], list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        
        # Second row should be Caesar shift by 1
        self.assertEqual(table[1], list("BCDEFGHIJKLMNOPQRSTUVWXYZA"))
    
    def test_caesar_table(self):
        """Test Caesar-based table generation."""
        table = produce_table("caesar", shift=5)
        
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # First row should be Caesar shift by 5
        self.assertEqual(table[0], list("FGHIJKLMNOPQRSTUVWXYZABCDE"))
    
    def test_affine_table(self):
        """Test Affine-based table generation."""
        table = produce_table("affine", a=3, b=7)
        
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
    
    def test_keyword_table(self):
        """Test Keyword-based table generation."""
        table = produce_table("keyword", keyword="SECRET")
        
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
    
    def test_atbash_table(self):
        """Test Atbash-based table generation."""
        table = produce_table("atbash")
        
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
    
    def test_invalid_table_type(self):
        """Test invalid table type raises error."""
        with self.assertRaises(ValueError):
            produce_table("invalid")
    
    def test_missing_parameters(self):
        """Test missing parameters raise errors."""
        with self.assertRaises(ValueError):
            produce_table("caesar")  # Missing shift
        
        with self.assertRaises(ValueError):
            produce_table("affine")  # Missing a and b
        
        with self.assertRaises(ValueError):
            produce_table("keyword")  # Missing keyword


class TestGronsfeldRandomKeyGeneration(unittest.TestCase):
    """Test cases for random key generation."""
    
    def test_generate_random_numeric_key(self):
        """Test random numeric key generation."""
        key = generate_random_numeric_key(10)
        
        self.assertEqual(len(key), 10)
        self.assertTrue(key.isdigit())
    
    def test_generate_numeric_key_for_text(self):
        """Test numeric key generation for text."""
        plaintext = "HELLO WORLD"
        key = generate_numeric_key_for_text(plaintext)
        
        # Should generate key for 10 alphabetic characters
        self.assertEqual(len(key), 10)
        self.assertTrue(key.isdigit())
    
    def test_empty_text_key_generation(self):
        """Test key generation for empty text."""
        key = generate_numeric_key_for_text("")
        self.assertEqual(key, "")
    
    def test_encrypt_with_random_key(self):
        """Test encryption with random key."""
        plaintext = "HELLO WORLD"
        encrypted, key = encrypt_with_random_key(plaintext)
        
        self.assertTrue(key.isdigit())
        self.assertEqual(len(key), 10)  # 10 alphabetic characters
        
        decrypted = decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_with_specified_key_length(self):
        """Test encryption with specified key length."""
        plaintext = "HELLO"
        encrypted, key = encrypt_with_random_key(plaintext, key_length=8)
        
        self.assertEqual(len(key), 8)
        self.assertTrue(key.isdigit())
        
        decrypted = decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)


class TestGronsfeldCustomTable(unittest.TestCase):
    """Test cases for custom table usage."""
    
    def test_custom_classical_table(self):
        """Test using custom classical table."""
        plaintext = "HELLO"
        key = "12312"
        
        table = produce_table("classical")
        encrypted = encrypt(plaintext, key, table)
        decrypted = decrypt(encrypted, key, table)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_custom_caesar_table(self):
        """Test using custom Caesar table."""
        plaintext = "HELLO"
        key = "12312"
        
        table = produce_table("caesar", shift=7)
        encrypted = encrypt(plaintext, key, table)
        decrypted = decrypt(encrypted, key, table)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_custom_affine_table(self):
        """Test using custom Affine table."""
        plaintext = "HELLO"
        key = "12312"
        
        table = produce_table("affine", a=5, b=3)
        encrypted = encrypt(plaintext, key, table)
        decrypted = decrypt(encrypted, key, table)
        
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
