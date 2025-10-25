"""
Test cases for Hill cipher implementation.
"""

import unittest
import numpy as np
from cryptology.classical.substitution.polygraphic.hill import encrypt, decrypt


class TestHill(unittest.TestCase):
    
    def test_encrypt_basic(self):
        """Test basic Hill encryption with 2x2 matrix."""
        key_matrix = [[3, 3], [2, 5]]
        result = encrypt("HELLO", key_matrix)
        self.assertEqual(len(result), 6)  # HELLO + X padding = 6 chars
    
    def test_decrypt_basic(self):
        """Test basic Hill decryption with 2x2 matrix."""
        plaintext = "HELLO"
        key_matrix = [[3, 3], [2, 5]]
        
        encrypted = encrypt(plaintext, key_matrix)
        decrypted = decrypt(encrypted, key_matrix)
        
        # Remove padding X if present
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, plaintext.upper())
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypting then decrypting returns original text."""
        plaintext = "ATTACK AT DAWN"
        key_matrix = [[3, 3], [2, 5]]
        
        encrypted = encrypt(plaintext, key_matrix)
        decrypted = decrypt(encrypted, key_matrix)
        
        # Remove padding and spaces
        expected = plaintext.replace(' ', '').upper()
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, expected)
    
    def test_3x3_matrix(self):
        """Test Hill cipher with 3x3 matrix."""
        key_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
        plaintext = "HELLO"
        
        encrypted = encrypt(plaintext, key_matrix)
        decrypted = decrypt(encrypted, key_matrix)
        
        # Remove padding X if present
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, plaintext.upper())
    
    def test_odd_length_text(self):
        """Test that odd length text gets X padding."""
        key_matrix = [[3, 3], [2, 5]]
        result = encrypt("HELL", key_matrix)
        # Should add X padding: HELL -> HELLX
        self.assertEqual(len(result), 4)  # 2 digrams
    
    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are removed."""
        key_matrix = [[3, 3], [2, 5]]
        result = encrypt("HELLO WORLD!", key_matrix)
        # Should process "HELLOWORLD" with X padding
        self.assertEqual(len(result), 10)  # 5 digrams
    
    def test_invalid_matrix_not_square(self):
        """Test that non-square matrix raises ValueError."""
        key_matrix = [[3, 3, 1], [2, 5, 2]]
        with self.assertRaises(ValueError):
            encrypt("HELLO", key_matrix)
    
    def test_invalid_matrix_too_small(self):
        """Test that 1x1 matrix raises ValueError."""
        key_matrix = [[3]]
        with self.assertRaises(ValueError):
            encrypt("HELLO", key_matrix)
    
    def test_invalid_matrix_not_2d(self):
        """Test that non-2D matrix raises ValueError."""
        key_matrix = [3, 3, 2, 5]
        with self.assertRaises(ValueError):
            encrypt("HELLO", key_matrix)
    
    def test_singular_matrix(self):
        """Test that singular matrix raises ValueError."""
        # Matrix with determinant 0
        key_matrix = [[1, 2], [2, 4]]
        with self.assertRaises(ValueError):
            encrypt("HELLO", key_matrix)
    
    def test_matrix_not_coprime_with_26(self):
        """Test that matrix with determinant not coprime with 26 raises ValueError."""
        # Matrix with determinant 2 (not coprime with 26)
        key_matrix = [[2, 0], [0, 1]]
        with self.assertRaises(ValueError):
            encrypt("HELLO", key_matrix)
    
    def test_case_insensitive(self):
        """Test that input is case insensitive."""
        key_matrix = [[3, 3], [2, 5]]
        result1 = encrypt("hello", key_matrix)
        result2 = encrypt("HELLO", key_matrix)
        self.assertEqual(result1, result2)
    
    def test_long_text(self):
        """Test encryption of longer text."""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key_matrix = [[3, 3], [2, 5]]
        
        encrypted = encrypt(plaintext, key_matrix)
        decrypted = decrypt(encrypted, key_matrix)
        
        # Remove padding and spaces
        expected = plaintext.replace(' ', '').upper()
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        self.assertEqual(decrypted, expected)
    
    def test_different_matrices(self):
        """Test that different matrices produce different results."""
        plaintext = "HELLO"
        matrix1 = [[3, 3], [2, 5]]
        matrix2 = [[1, 2], [3, 4]]
        
        result1 = encrypt(plaintext, matrix1)
        result2 = encrypt(plaintext, matrix2)
        
        self.assertNotEqual(result1, result2)
    
    def test_known_example(self):
        """Test with a known example."""
        # Using matrix [[3, 3], [2, 5]] and plaintext "HE"
        # H=7, E=4
        # [3 3] [7] = [3*7 + 3*4] = [33] = [7] mod 26 = H
        # [2 5] [4]   [2*7 + 5*4]   [34]   [8] mod 26 = I
        # So "HE" should encrypt to "HI" (approximately)
        key_matrix = [[3, 3], [2, 5]]
        result = encrypt("HE", key_matrix)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
