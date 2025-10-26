"""
Tests for Reihenschieber Cipher Implementation
"""

import unittest
import string
from cryptology.classical.substitution.polyalphabetic.reihenschieber import (
    reihenschieber_encrypt,
    reihenschieber_decrypt,
    reihenschieber_generate_random_key,
    reihenschieber_generate_key_for_text,
    reihenschieber_encrypt_with_random_key,
    reihenschieber_produce_custom_shifts,
    reihenschieber_encrypt_turkish,
    reihenschieber_decrypt_turkish,
    TURKISH_ALPHABET
)


class TestReihenschieberCipher(unittest.TestCase):
    
    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        plaintext = "HELLO"
        key = "KEY"
        
        encrypted = reihenschieber_encrypt(plaintext, key)
        decrypted = reihenschieber_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertNotEqual(encrypted, plaintext)
    
    def test_fixed_shift_mode(self):
        """Test fixed shift mode."""
        plaintext = "HELLO"
        key = "KEY"
        
        # Forward shift
        encrypted_forward = reihenschieber_encrypt(plaintext, key, shift_mode="fixed", shift_direction="forward", shift_amount=2)
        decrypted_forward = reihenschieber_decrypt(encrypted_forward, key, shift_mode="fixed", shift_direction="forward", shift_amount=2)
        self.assertEqual(decrypted_forward, plaintext)
        
        # Backward shift
        encrypted_backward = reihenschieber_encrypt(plaintext, key, shift_mode="fixed", shift_direction="backward", shift_amount=2)
        decrypted_backward = reihenschieber_decrypt(encrypted_backward, key, shift_mode="fixed", shift_direction="backward", shift_amount=2)
        self.assertEqual(decrypted_backward, plaintext)
    
    def test_progressive_shift_mode(self):
        """Test progressive shift mode."""
        plaintext = "HELLO"
        key = "KEY"
        
        encrypted = reihenschieber_encrypt(plaintext, key, shift_mode="progressive", shift_amount=1)
        decrypted = reihenschieber_decrypt(encrypted, key, shift_mode="progressive", shift_amount=1)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_custom_shift_mode(self):
        """Test custom shift mode."""
        plaintext = "HELLO"
        key = "KEY"
        custom_shifts = [1, -1, 2, -2, 0]
        
        encrypted = reihenschieber_encrypt(plaintext, key, shift_mode="custom", custom_shifts=custom_shifts)
        decrypted = reihenschieber_decrypt(encrypted, key, shift_mode="custom", custom_shifts=custom_shifts)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_key_repetition(self):
        """Test that key repeats properly."""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = reihenschieber_encrypt(plaintext, key)
        decrypted = reihenschieber_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_case_preservation(self):
        """Test that case is handled properly."""
        plaintext = "Hello World"
        key = "key"
        
        encrypted = reihenschieber_encrypt(plaintext, key)
        decrypted = reihenschieber_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext.upper())
    
    def test_custom_alphabet(self):
        """Test custom alphabet support."""
        plaintext = "ABC"
        key = "KEY"
        custom_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        encrypted = reihenschieber_encrypt(plaintext, key, alphabet=custom_alphabet)
        decrypted = reihenschieber_decrypt(encrypted, key, alphabet=custom_alphabet)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_turkish_alphabet(self):
        """Test Turkish alphabet support."""
        plaintext = "MERHABA"
        key = "ANAHTAR"
        
        encrypted = reihenschieber_encrypt_turkish(plaintext, key)
        decrypted = reihenschieber_decrypt_turkish(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_random_key_generation(self):
        """Test random key generation."""
        key = reihenschieber_generate_random_key(5)
        self.assertEqual(len(key), 5)
        self.assertTrue(all(c in string.ascii_uppercase for c in key))
    
    def test_key_for_text_generation(self):
        """Test key generation for specific text length."""
        text_length = 10
        key = reihenschieber_generate_key_for_text(text_length)
        
        self.assertTrue(3 <= len(key) <= min(text_length, 10))
        self.assertTrue(all(c in string.ascii_uppercase for c in key))
    
    def test_encrypt_with_random_key(self):
        """Test encryption with random key generation."""
        plaintext = "HELLO WORLD"
        
        encrypted, generated_key = reihenschieber_encrypt_with_random_key(plaintext)
        decrypted = reihenschieber_decrypt(encrypted, generated_key)
        
        self.assertEqual(decrypted, plaintext)
        self.assertTrue(len(generated_key) >= 3)
    
    def test_custom_shift_patterns(self):
        """Test custom shift pattern generation."""
        # Alternating pattern
        alternating = reihenschieber_produce_custom_shifts("alternating", 5)
        self.assertEqual(alternating, [1, -1, 1, -1, 1])
        
        # Fibonacci pattern
        fibonacci = reihenschieber_produce_custom_shifts("fibonacci", 5)
        self.assertEqual(fibonacci, [1, 1, 2, 3, 5])
        
        # Prime pattern
        prime = reihenschieber_produce_custom_shifts("prime", 5)
        self.assertEqual(prime, [2, 3, 5, 7, 11])
        
        # Random pattern
        random_shifts = reihenschieber_produce_custom_shifts("random", 5)
        self.assertEqual(len(random_shifts), 5)
        self.assertTrue(all(-5 <= shift <= 5 for shift in random_shifts))
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        self.assertEqual(reihenschieber_encrypt("", "KEY"), "")
        self.assertEqual(reihenschieber_encrypt("HELLO", ""), "")
        self.assertEqual(reihenschieber_decrypt("", "KEY"), "")
        self.assertEqual(reihenschieber_decrypt("HELLO", ""), "")
    
    def test_invalid_characters(self):
        """Test handling of invalid characters."""
        plaintext = "HELLO123"
        key = "KEY"
        
        with self.assertRaises(ValueError):
            reihenschieber_encrypt(plaintext, key)
        
        with self.assertRaises(ValueError):
            reihenschieber_encrypt("HELLO", "KEY123")
    
    def test_invalid_shift_mode(self):
        """Test handling of invalid shift mode."""
        plaintext = "HELLO"
        key = "KEY"
        
        with self.assertRaises(ValueError):
            reihenschieber_encrypt(plaintext, key, shift_mode="invalid")
    
    def test_invalid_shift_direction(self):
        """Test handling of invalid shift direction."""
        plaintext = "HELLO"
        key = "KEY"
        
        # Should not raise error, just use default
        encrypted = reihenschieber_encrypt(plaintext, key, shift_direction="invalid")
        self.assertIsInstance(encrypted, str)
    
    def test_negative_key_length(self):
        """Test handling of negative key length."""
        with self.assertRaises(ValueError):
            reihenschieber_generate_random_key(-1)
        
        with self.assertRaises(ValueError):
            reihenschieber_generate_key_for_text(-1)
    
    def test_invalid_pattern_type(self):
        """Test handling of invalid pattern type."""
        with self.assertRaises(ValueError):
            reihenschieber_produce_custom_shifts("invalid", 5)
    
    def test_negative_pattern_length(self):
        """Test handling of negative pattern length."""
        with self.assertRaises(ValueError):
            reihenschieber_produce_custom_shifts("alternating", -1)
    
    def test_long_text(self):
        """Test with longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "SECRET"
        
        encrypted = reihenschieber_encrypt(plaintext, key)
        decrypted = reihenschieber_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_special_characters(self):
        """Test handling of special characters."""
        plaintext = "HELLO, WORLD!"
        key = "KEY"
        
        # Should preserve non-alphabetic characters
        encrypted = reihenschieber_encrypt(plaintext, key)
        decrypted = reihenschieber_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, plaintext.upper())


if __name__ == '__main__':
    unittest.main()
