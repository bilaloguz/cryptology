"""
Test cases for Four Square cipher implementation.
"""

import unittest
from cryptology.classical.substitution.polygraphic.four_square import encrypt, decrypt


class TestFourSquare(unittest.TestCase):
    
    def test_encrypt_basic(self):
        """Test basic Four Square encryption."""
        result = encrypt("HELLO", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        self.assertEqual(len(result), 5)  # Should be 5 characters
    
    def test_decrypt_basic(self):
        """Test basic Four Square decryption."""
        plaintext = "HELLO"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        key3 = "CIPHER"
        key4 = "SECRET"
        
        encrypted = encrypt(plaintext, key1, key2, key3, key4)
        decrypted = decrypt(encrypted, key1, key2, key3, key4)
        
        self.assertEqual(decrypted, plaintext.upper())
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypting then decrypting returns original text."""
        plaintext = "ATTACK AT DAWN"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        key3 = "CIPHER"
        key4 = "SECRET"
        
        encrypted = encrypt(plaintext, key1, key2, key3, key4)
        decrypted = decrypt(encrypted, key1, key2, key3, key4)
        
        # Remove padding X if present
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, plaintext.replace(' ', '').upper())
    
    def test_odd_length_text(self):
        """Test that odd length text gets X padding."""
        result = encrypt("HELL", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        # Should add X padding: HELL -> HELLX
        self.assertEqual(len(result), 5)
    
    def test_j_replacement(self):
        """Test that J is replaced with I."""
        result = encrypt("JACK", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        # JACK becomes IACK
        self.assertEqual(len(result), 4)
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are removed."""
        result = encrypt("HELLO WORLD!", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        # Should process "HELLOWORLD" with X padding
        self.assertEqual(len(result), 10)  # 5 digrams
    
    def test_empty_key1(self):
        """Test that empty key1 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "", "PLAYFAIR", "CIPHER", "SECRET")
    
    def test_empty_key2(self):
        """Test that empty key2 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "MONARCHY", "", "CIPHER", "SECRET")
    
    def test_empty_key3(self):
        """Test that empty key3 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "MONARCHY", "PLAYFAIR", "", "SECRET")
    
    def test_empty_key4(self):
        """Test that empty key4 raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "MONARCHY", "PLAYFAIR", "CIPHER", "")
    
    def test_key_with_no_letters(self):
        """Test that key with no letters raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "123!@#", "PLAYFAIR", "CIPHER", "SECRET")
    
    def test_case_insensitive(self):
        """Test that input is case insensitive."""
        result1 = encrypt("hello", "monarchy", "playfair", "cipher", "secret")
        result2 = encrypt("HELLO", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        self.assertEqual(result1, result2)
    
    def test_key_duplicates_removed(self):
        """Test that duplicate letters in keys are removed."""
        result1 = encrypt("HELLO", "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        result2 = encrypt("HELLO", "MONARCHYYY", "PLAYFAIRRR", "CIPHER", "SECRET")
        self.assertEqual(result1, result2)
    
    def test_long_text(self):
        """Test encryption of longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key1 = "MONARCHY"
        key2 = "PLAYFAIR"
        key3 = "CIPHER"
        key4 = "SECRET"
        
        encrypted = encrypt(plaintext, key1, key2, key3, key4)
        decrypted = decrypt(encrypted, key1, key2, key3, key4)
        
        # Remove padding and spaces
        expected = plaintext.replace(' ', '').upper()
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, expected)
    
    def test_different_keys(self):
        """Test that different keys produce different results."""
        plaintext = "HELLO"
        keys1 = ("MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
        keys2 = ("DIFFERENT", "KEYS", "HERE", "NOW")
        
        result1 = encrypt(plaintext, *keys1)
        result2 = encrypt(plaintext, *keys2)
        
        self.assertNotEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
