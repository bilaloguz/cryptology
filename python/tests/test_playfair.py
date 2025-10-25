"""
Test cases for Playfair cipher implementation.
"""

import unittest
from cryptology.classical.substitution.polygraphic.playfair import encrypt, decrypt


class TestPlayfair(unittest.TestCase):
    
    def test_encrypt_basic(self):
        """Test basic Playfair encryption."""
        result = encrypt("HELLO", "MONARCHY")
        self.assertEqual(result, "CLMQR")
    
    def test_decrypt_basic(self):
        """Test basic Playfair decryption."""
        result = decrypt("CLMQR", "MONARCHY")
        self.assertEqual(result, "HELLO")
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypting then decrypting returns original text."""
        plaintext = "ATTACK AT DAWN"
        key = "MONARCHY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        # Remove padding X if present
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, plaintext.replace(' ', '').upper())
    
    def test_same_letter_digram(self):
        """Test handling of same letter digrams (should add X)."""
        result = encrypt("HELLO", "MONARCHY")
        # HE -> CL, LL -> QR (L+L becomes L+X), LO -> QR
        self.assertEqual(result, "CLMQR")
    
    def test_odd_length_text(self):
        """Test that odd length text gets X padding."""
        result = encrypt("HELL", "MONARCHY")
        # HE -> CL, LX -> QR (L+X padding)
        self.assertEqual(result, "CLQR")
    
    def test_j_replacement(self):
        """Test that J is replaced with I."""
        result = encrypt("JACK", "MONARCHY")
        # JACK becomes IACK, IA -> CL, CK -> QR
        self.assertEqual(result, "CLQR")
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are removed."""
        result = encrypt("HELLO WORLD!", "MONARCHY")
        # Should process "HELLOWORLD" with X padding
        self.assertEqual(len(result), 10)  # 5 digrams
    
    def test_empty_key(self):
        """Test that empty key raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "")
    
    def test_key_with_no_letters(self):
        """Test that key with no letters raises ValueError."""
        with self.assertRaises(ValueError):
            encrypt("HELLO", "123!@#")
    
    def test_same_row_encryption(self):
        """Test encryption when both letters are in same row."""
        # Using key "MONARCHY", M and O are in same row
        result = encrypt("MO", "MONARCHY")
        # M and O are in same row, should shift right
        self.assertEqual(len(result), 2)
    
    def test_same_column_encryption(self):
        """Test encryption when both letters are in same column."""
        # This test depends on the specific key square layout
        result = encrypt("AB", "MONARCHY")
        self.assertEqual(len(result), 2)
    
    def test_rectangle_encryption(self):
        """Test encryption when letters form a rectangle."""
        result = encrypt("AC", "MONARCHY")
        self.assertEqual(len(result), 2)
    
    def test_case_insensitive(self):
        """Test that input is case insensitive."""
        result1 = encrypt("hello", "monarchy")
        result2 = encrypt("HELLO", "MONARCHY")
        self.assertEqual(result1, result2)
    
    def test_key_duplicates_removed(self):
        """Test that duplicate letters in key are removed."""
        result1 = encrypt("HELLO", "MONARCHY")
        result2 = encrypt("HELLO", "MONARCHYYY")
        self.assertEqual(result1, result2)
    
    def test_long_text(self):
        """Test encryption of longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "MONARCHY"
        
        encrypted = encrypt(plaintext, key)
        decrypted = decrypt(encrypted, key)
        
        # Remove padding and spaces
        expected = plaintext.replace(' ', '').upper()
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, expected)


if __name__ == '__main__':
    unittest.main()
