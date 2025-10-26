"""
Test suite for Vigenère cipher implementation.

This module tests the Vigenère cipher with different table types,
including classical tabula recta and custom tables generated using monoalphabetic ciphers.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polyalphabetic import (
    vigenere_encrypt, vigenere_decrypt, vigenere_produce_table,
    vigenere_generate_random_key, vigenere_generate_key_for_text,
    vigenere_encrypt_with_random_key
)


class TestVigenereCipher(unittest.TestCase):
    """Test cases for Vigenère cipher implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.plaintext = "HELLO WORLD"
        self.key = "KEY"
        self.turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        self.turkish_plaintext = "MERHABA DUNYA"
        self.turkish_key = "GIZLI"
    
    def test_classical_vigenere_encrypt_decrypt(self):
        """Test classical Vigenère encryption and decryption."""
        # Encrypt
        encrypted = vigenere_encrypt(self.plaintext, self.key)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, self.plaintext)
        
        # Decrypt
        decrypted = vigenere_decrypt(encrypted, self.key)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_classical_vigenere_with_custom_table(self):
        """Test classical Vigenère with explicitly provided table."""
        # Generate classical table
        table = vigenere_produce_table("classical")
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 26)  # 26 rows
        self.assertEqual(len(table[0]), 26)  # 26 columns
        
        # Encrypt with custom table
        encrypted = vigenere_encrypt(self.plaintext, self.key, table=table)
        self.assertIsInstance(encrypted, str)
        
        # Decrypt with same table
        decrypted = vigenere_decrypt(encrypted, self.key, table=table)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_caesar_table_generation(self):
        """Test Caesar-based table generation."""
        # Generate Caesar table with shift=3
        table = vigenere_produce_table("caesar", shift=3)
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.plaintext, self.key, table=table)
        decrypted = vigenere_decrypt(encrypted, self.key, table=table)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_affine_table_generation(self):
        """Test Affine-based table generation."""
        # Generate Affine table with a=3, b=5
        table = vigenere_produce_table("affine", a=3, b=5)
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.plaintext, self.key, table=table)
        decrypted = vigenere_decrypt(encrypted, self.key, table=table)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_keyword_table_generation(self):
        """Test Keyword-based table generation."""
        # Generate Keyword table
        table = vigenere_produce_table("keyword", keyword="SECRET")
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.plaintext, self.key, table=table)
        decrypted = vigenere_decrypt(encrypted, self.key, table=table)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_atbash_table_generation(self):
        """Test Atbash-based table generation."""
        # Generate Atbash table
        table = vigenere_produce_table("atbash")
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 26)
        self.assertEqual(len(table[0]), 26)
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.plaintext, self.key, table=table)
        decrypted = vigenere_decrypt(encrypted, self.key, table=table)
        self.assertEqual(decrypted, self.plaintext)
    
    def test_turkish_alphabet_support(self):
        """Test Vigenère with Turkish alphabet."""
        # Generate classical table for Turkish
        table = vigenere_produce_table("classical", alphabet=self.turkish_alphabet)
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 29)  # 29 rows for Turkish
        self.assertEqual(len(table[0]), 29)  # 29 columns for Turkish
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.turkish_plaintext, self.turkish_key, 
                                   table=table, alphabet=self.turkish_alphabet)
        decrypted = vigenere_decrypt(encrypted, self.turkish_key, 
                                  table=table, alphabet=self.turkish_alphabet)
        self.assertEqual(decrypted, self.turkish_plaintext)
    
    def test_caesar_table_with_turkish_alphabet(self):
        """Test Caesar table generation with Turkish alphabet."""
        # Generate Caesar table for Turkish
        table = vigenere_produce_table("caesar", alphabet=self.turkish_alphabet, shift=5)
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 29)
        self.assertEqual(len(table[0]), 29)
        
        # Test encryption/decryption
        encrypted = vigenere_encrypt(self.turkish_plaintext, self.turkish_key, 
                                   table=table, alphabet=self.turkish_alphabet)
        decrypted = vigenere_decrypt(encrypted, self.turkish_key, 
                                  table=table, alphabet=self.turkish_alphabet)
        self.assertEqual(decrypted, self.turkish_plaintext)
    
    def test_different_table_types_produce_different_results(self):
        """Test that different table types produce different encryption results."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "CRYPTO"
        
        # Generate different tables
        classical_table = vigenere_produce_table("classical")
        caesar_table = vigenere_produce_table("caesar", shift=5)
        affine_table = vigenere_produce_table("affine", a=3, b=7)
        keyword_table = vigenere_produce_table("keyword", keyword="SECRET")
        atbash_table = vigenere_produce_table("atbash")
        
        # Encrypt with different tables
        classical_encrypted = vigenere_encrypt(plaintext, key, table=classical_table)
        caesar_encrypted = vigenere_encrypt(plaintext, key, table=caesar_table)
        affine_encrypted = vigenere_encrypt(plaintext, key, table=affine_table)
        keyword_encrypted = vigenere_encrypt(plaintext, key, table=keyword_table)
        atbash_encrypted = vigenere_encrypt(plaintext, key, table=atbash_table)
        
        # All results should be different
        results = [classical_encrypted, caesar_encrypted, affine_encrypted, 
                  keyword_encrypted, atbash_encrypted]
        
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                self.assertNotEqual(results[i], results[j], 
                                  f"Tables {i} and {j} produced identical results")
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        # Empty plaintext
        result = vigenere_encrypt("", self.key)
        self.assertEqual(result, "")
        
        # Empty key
        result = vigenere_encrypt(self.plaintext, "")
        self.assertEqual(result, "")
        
        # Empty ciphertext
        result = vigenere_decrypt("", self.key)
        self.assertEqual(result, "")
        
        # Empty key for decryption
        result = vigenere_decrypt("SOME CIPHERTEXT", "")
        self.assertEqual(result, "")
    
    def test_special_characters_handling(self):
        """Test handling of special characters and non-alphabetic characters."""
        plaintext_with_special = "HELLO, WORLD! 123 @#$"
        key = "KEY"
        
        # Should handle special characters gracefully
        encrypted = vigenere_encrypt(plaintext_with_special, key)
        decrypted = vigenere_decrypt(encrypted, key)
        
        # Should only contain alphabetic characters and spaces
        self.assertTrue(all(c.isalpha() or c == ' ' for c in encrypted))
        self.assertTrue(all(c.isalpha() or c == ' ' for c in decrypted))
        
        # Should be able to decrypt back to original (alphabetic part with spaces)
        self.assertEqual(decrypted, "HELLO WORLD  ")
    
    def test_case_insensitivity(self):
        """Test that the cipher is case-insensitive."""
        plaintext_upper = "HELLO WORLD"
        plaintext_lower = "hello world"
        plaintext_mixed = "Hello World"
        key_upper = "KEY"
        key_lower = "key"
        key_mixed = "Key"
        
        # All should produce the same result
        encrypted_upper = vigenere_encrypt(plaintext_upper, key_upper)
        encrypted_lower = vigenere_encrypt(plaintext_lower, key_lower)
        encrypted_mixed = vigenere_encrypt(plaintext_mixed, key_mixed)
        
        self.assertEqual(encrypted_upper, encrypted_lower)
        self.assertEqual(encrypted_upper, encrypted_mixed)
    
    def test_key_repetition(self):
        """Test that keys are properly repeated for longer plaintexts."""
        long_plaintext = "A" * 100  # 100 A's
        short_key = "KEY"  # 3 characters
        
        encrypted = vigenere_encrypt(long_plaintext, short_key)
        decrypted = vigenere_decrypt(encrypted, short_key)
        
        self.assertEqual(decrypted, long_plaintext)
    
    def test_table_consistency(self):
        """Test that the same table produces consistent results."""
        table = vigenere_produce_table("classical")
        
        # Multiple encryptions with same table should be consistent
        encrypted1 = vigenere_encrypt(self.plaintext, self.key, table=table)
        encrypted2 = vigenere_encrypt(self.plaintext, self.key, table=table)
        
        self.assertEqual(encrypted1, encrypted2)
    
    def test_invalid_table_type(self):
        """Test handling of invalid table types."""
        with self.assertRaises(ValueError):
            vigenere_produce_table("invalid_type")
    
    def test_missing_parameters(self):
        """Test handling of missing required parameters."""
        # Missing shift for Caesar
        with self.assertRaises(ValueError):
            vigenere_produce_table("caesar")
        
        # Missing a or b for Affine
        with self.assertRaises(ValueError):
            vigenere_produce_table("affine", a=3)
        
        with self.assertRaises(ValueError):
            vigenere_produce_table("affine", b=5)
        
        # Missing keyword for Keyword
        with self.assertRaises(ValueError):
            vigenere_produce_table("keyword")
    
    def test_historical_examples(self):
        """Test with historical Vigenère examples."""
        # Classic Vigenère example
        plaintext = "ATTACKATDAWN"
        key = "LEMON"
        
        # Expected result for classical Vigenère
        expected = "LXFOPVEFRNHR"
        
        encrypted = vigenere_encrypt(plaintext, key)
        self.assertEqual(encrypted, expected)
        
        # Decrypt back
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_composable_system_integration(self):
        """Test integration with the composable cipher system."""
        from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
        from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce
        
        plaintext = "COMPOSABLE SYSTEM"
        key = "VIGENERE"
        
        # Layer 1: Caesar-produced alphabet
        caesar_alphabet = caesar_produce(shift=7)
        
        # Layer 2: Keyword-produced alphabet
        keyword_alphabet = keyword_produce("SECRET", caesar_alphabet)
        
        # Layer 3: Vigenère with Caesar table
        caesar_table = vigenere_produce_table("caesar", shift=3)
        encrypted = vigenere_encrypt(plaintext, key, table=caesar_table)
        
        # Should be able to decrypt
        decrypted = vigenere_decrypt(encrypted, key, table=caesar_table)
        self.assertEqual(decrypted, plaintext)
    
    def test_security_properties(self):
        """Test security properties of different table types."""
        plaintext = "ATTACK AT DAWN"
        key = "LEMON"
        
        # Generate different tables
        classical_table = vigenere_produce_table("classical")
        caesar_table = vigenere_produce_table("caesar", shift=13)
        affine_table = vigenere_produce_table("affine", a=5, b=11)
        
        # Encrypt with different tables
        classical_encrypted = vigenere_encrypt(plaintext, key, table=classical_table)
        caesar_encrypted = vigenere_encrypt(plaintext, key, table=caesar_table)
        affine_encrypted = vigenere_encrypt(plaintext, key, table=affine_table)
        
        # All should be different from plaintext
        self.assertNotEqual(classical_encrypted, plaintext)
        self.assertNotEqual(caesar_encrypted, plaintext)
        self.assertNotEqual(affine_encrypted, plaintext)
        
        # All should be different from each other
        self.assertNotEqual(classical_encrypted, caesar_encrypted)
        self.assertNotEqual(classical_encrypted, affine_encrypted)
        self.assertNotEqual(caesar_encrypted, affine_encrypted)


class TestVigenereRandomKeyGeneration(unittest.TestCase):
    """Test cases for Vigenère random key generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        self.test_plaintext = "HELLO WORLD"
    
    def test_generate_random_key_basic(self):
        """Test basic random key generation."""
        # Test different lengths
        for length in [1, 5, 10, 20]:
            key = vigenere_generate_random_key(length)
            self.assertEqual(len(key), length)
            self.assertTrue(all(c in self.english_alphabet for c in key))
    
    def test_generate_random_key_turkish(self):
        """Test random key generation with Turkish alphabet."""
        key = vigenere_generate_random_key(10, self.turkish_alphabet)
        self.assertEqual(len(key), 10)
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
    
    def test_generate_random_key_invalid_length(self):
        """Test random key generation with invalid length."""
        with self.assertRaises(ValueError):
            vigenere_generate_random_key(0)
        
        with self.assertRaises(ValueError):
            vigenere_generate_random_key(-1)
    
    def test_generate_random_key_empty_alphabet(self):
        """Test random key generation with empty alphabet."""
        with self.assertRaises(ValueError):
            vigenere_generate_random_key(5, "")
    
    def test_generate_key_for_text(self):
        """Test key generation for specific text."""
        key = vigenere_generate_key_for_text(self.test_plaintext)
        
        # Key should match the length of alphabetic characters only
        alphabetic_chars = sum(1 for c in self.test_plaintext.upper() if c.isalpha())
        self.assertEqual(len(key), alphabetic_chars)
        self.assertTrue(all(c in self.english_alphabet for c in key))
    
    def test_generate_key_for_empty_text(self):
        """Test key generation for empty text."""
        key = vigenere_generate_key_for_text("")
        self.assertEqual(key, "")
    
    def test_generate_key_for_text_turkish(self):
        """Test key generation for Turkish text."""
        turkish_text = "MERHABA DÜNYA"
        key = vigenere_generate_key_for_text(turkish_text, self.turkish_alphabet)
        
        # Should handle Turkish characters properly
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
        self.assertGreater(len(key), 0)
    
    def test_encrypt_with_random_key_basic(self):
        """Test encryption with random key generation."""
        encrypted, key = vigenere_encrypt_with_random_key(self.test_plaintext)
        
        # Should return both encrypted text and key
        self.assertIsInstance(encrypted, str)
        self.assertIsInstance(key, str)
        self.assertGreater(len(key), 0)
        
        # Should be able to decrypt
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_custom_length(self):
        """Test encryption with custom key length."""
        key_length = 15
        encrypted, key = vigenere_encrypt_with_random_key(
            self.test_plaintext, key_length=key_length
        )
        
        self.assertEqual(len(key), key_length)
        
        # Should still decrypt correctly
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_custom_table(self):
        """Test encryption with random key and custom table."""
        caesar_table = vigenere_produce_table("caesar", shift=5)
        encrypted, key = vigenere_encrypt_with_random_key(
            self.test_plaintext, table=caesar_table
        )
        
        # Should decrypt correctly with the same table
        decrypted = vigenere_decrypt(encrypted, key, table=caesar_table)
        self.assertEqual(decrypted, self.test_plaintext)
    
    def test_encrypt_with_random_key_turkish(self):
        """Test encryption with random key and Turkish alphabet."""
        turkish_text = "MERHABA DÜNYA"
        turkish_table = vigenere_produce_table("classical", alphabet=self.turkish_alphabet)
        
        encrypted, key = vigenere_encrypt_with_random_key(
            turkish_text, table=turkish_table, alphabet=self.turkish_alphabet
        )
        
        # Key should be Turkish characters
        self.assertTrue(all(c in self.turkish_alphabet for c in key))
        
        # Should decrypt correctly (note: Ü becomes U due to text preparation)
        decrypted = vigenere_decrypt(encrypted, key, table=turkish_table, alphabet=self.turkish_alphabet)
        expected_decrypted = "MERHABA DUNYA"  # Ü becomes U after text preparation
        self.assertEqual(decrypted, expected_decrypted)
    
    def test_encrypt_with_random_key_empty_text(self):
        """Test encryption with random key for empty text."""
        with self.assertRaises(ValueError):
            vigenere_encrypt_with_random_key("")
    
    def test_key_uniqueness(self):
        """Test that generated keys are unique."""
        keys = set()
        
        # Generate multiple keys
        for _ in range(10):
            key = vigenere_generate_random_key(10)
            keys.add(key)
        
        # Should have unique keys (very high probability)
        self.assertEqual(len(keys), 10)
    
    def test_key_randomness(self):
        """Test that generated keys appear random."""
        # Generate many keys and check character distribution
        keys = [vigenere_generate_random_key(100) for _ in range(5)]
        
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
                table = vigenere_produce_table(table_type, **params)
                encrypted, key = vigenere_encrypt_with_random_key(plaintext, table=table)
                
                # Should decrypt correctly
                decrypted = vigenere_decrypt(encrypted, key, table=table)
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
                key = vigenere_generate_key_for_text(text)
                alphabetic_chars = sum(1 for c in text.upper() if c.isalpha())
                self.assertEqual(len(key), alphabetic_chars)
    
    def test_security_properties(self):
        """Test security properties of random keys."""
        # Test that random keys are not predictable
        key1 = vigenere_generate_random_key(20)
        key2 = vigenere_generate_random_key(20)
        
        # Keys should be different
        self.assertNotEqual(key1, key2)
        
        # Keys should not follow obvious patterns
        self.assertFalse(key1 == key1[0] * len(key1))  # Not all same character
        self.assertFalse(key1.isalpha() and key1.isupper() and len(set(key1)) == 1)  # Not single repeated letter


if __name__ == '__main__':
    unittest.main()
