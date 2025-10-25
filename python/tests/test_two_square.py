"""
Test cases for Two Square cipher implementation.
"""

import unittest
from cryptology.classical.substitution.polygraphic.two_square import encrypt, decrypt


class TestTwoSquare(unittest.TestCase):
    
    def test_encrypt_basic(self):
        """Test basic Two Square encryption."""
        result = encrypt("HELLO", "MONARCHY", "PLAYFAIR")
        self.assertEqual(len(result), 5)  # Should be 5 characters
    
    def test_decrypt_basic(self):
        """Test basic Two Square decryption."""
        plaintext = "HELLO"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        
        encrypted = encrypt(plaintext, key1, key2)
        decrypted = decrypt(encrypted, key1, key2)
        
        self.assertEqual(decrypted, plaintext.upper())
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypting then decrypting returns original text."""
        plaintext = "ATTACK AT DAWN"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        
        encrypted = encrypt(plaintext, key1, key2)
        decrypted = decrypt(encrypted, key1, key2)
        
        # Remove padding X if present
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, plaintext.replace(' ', '').upper())
    
    def test_odd_length_text(self):
        """Test that odd length text gets X padding."""
        result = encrypt("HELL", "MONARCHY", "PLAYFAIR")
        # Should add X padding: HELL -> HELLX
        self.assertEqual(len(result), 5)
    
    def test_j_replacement(self):
        """Test that J is replaced with I."""
        result = encrypt("JACK", "MONARCHY", "PLAYFAIR")
        # JACK becomes IACK
        self.assertEqual(len(result), 4)
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are removed."""
        result = encrypt("HELLO WORLD!", "MONARCHY", "PLAYFAIR")
        # Should process "HELLOWORLD" with X padding
        self.assertEqual(len(result), 10)  # 5 digrams
    
    def test_empty_key1(self):
        """Test that empty key1 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "", "PLAYFAIR")
    
    def test_empty_key2(self):
        """Test that empty key2 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "MONARCHY", "")
    
    def test_key_with_no_letters(self):
        """Test that key with no letters raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "123!@#", "PLAYFAIR")
    
    def test_case_insensitive(self):
        """Test that input is case insensitive."""
        result1 = encrypt("hello", "monarchy", "playfair")
        result2 = encrypt("HELLO", "MONARCHY", "PLAYFAIR")
        self.assertEqual(result1, result2)
    
    def test_key_duplicates_removed(self):
        """Test that duplicate letters in keys are removed."""
        result1 = encrypt("HELLO", "MONARCHY", "PLAYFAIR")
        result2 = encrypt("HELLO", "MONARCHYYY", "PLAYFAIRRR")
        self.assertEqual(result1, result2)
    
    def test_long_text(self):
        """Test encryption of longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        
        encrypted = encrypt(plaintext, key1, key2)
        decrypted = decrypt(encrypted, key1, key2)
        
        # Remove padding and spaces
        expected = plaintext.replace(' ', '').upper()
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, expected)
    
    def test_different_keys(self):
        """Test that different keys produce different results."""
        plaintext = "HELLO"
        key1a = "MONARCHY"
        key2a = "PLAYFAIR"
        key1b = "DIFFERENT"
        key2b = "KEYS"
        
        result1 = encrypt(plaintext, key1a, key2a)
        result2 = encrypt(plaintext, key1b, key2b)
        
        self.assertNotEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
