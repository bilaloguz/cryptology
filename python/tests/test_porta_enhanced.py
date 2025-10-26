"""
Enhanced tests for Porta cipher implementation with custom pairing support.
"""

import unittest
from cryptology.classical.substitution.polyalphabetic.porta import (
    encrypt, decrypt, produce_pairs, generate_random_key, generate_key_for_text, encrypt_with_random_key
)


class TestPortaEnhancedFeatures(unittest.TestCase):
    """Test cases for enhanced Porta cipher features."""
    
    def test_produce_pairs_default(self):
        """Test default pair generation."""
        pairs = produce_pairs("default")
        
        # Should create 13 pairs for English alphabet
        self.assertEqual(len(pairs), 13)
        
        # Check first few pairs
        expected_pairs = [("A", "N"), ("B", "O"), ("C", "P"), ("D", "Q"), ("E", "R")]
        for i, expected in enumerate(expected_pairs):
            self.assertEqual(pairs[i], expected)
    
    def test_produce_pairs_turkish(self):
        """Test Turkish pair generation."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        pairs = produce_pairs("turkish", turkish_alphabet)
        
        # Should create 14 pairs for Turkish alphabet
        self.assertEqual(len(pairs), 14)
        
        # Check that all pairs contain valid Turkish letters
        for pair in pairs:
            self.assertIn(pair[0], turkish_alphabet)
            self.assertIn(pair[1], turkish_alphabet)
    
    def test_produce_pairs_custom(self):
        """Test custom pair generation."""
        custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X")]
        validated_pairs = produce_pairs("custom", custom_pairs=custom_pairs)
        
        self.assertEqual(validated_pairs, custom_pairs)
    
    def test_produce_pairs_custom_validation(self):
        """Test custom pair validation."""
        # Test invalid pairs
        with self.assertRaises(ValueError):
            produce_pairs("custom")  # Missing custom_pairs
        
        with self.assertRaises(ValueError):
            produce_pairs("custom", custom_pairs=[])  # Empty pairs
        
        with self.assertRaises(ValueError):
            produce_pairs("custom", custom_pairs=[("A", "Z"), ("A", "Y")])  # Duplicate letter
        
        with self.assertRaises(ValueError):
            produce_pairs("custom", custom_pairs=[("A", "Z"), ("B", "Z")])  # Duplicate letter
    
    def test_produce_pairs_balanced(self):
        """Test balanced pair generation."""
        alphabet = "ABCDEFGHIJKL"  # 12 letters
        pairs = produce_pairs("balanced", alphabet)
        
        # Should create 6 pairs
        self.assertEqual(len(pairs), 6)
        
        # Check pairs
        expected_pairs = [("A", "G"), ("B", "H"), ("C", "I"), ("D", "J"), ("E", "K"), ("F", "L")]
        self.assertEqual(pairs, expected_pairs)
    
    def test_encrypt_with_custom_pairs(self):
        """Test encryption with custom pairs."""
        custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X")]
        plaintext = "ABC"
        key = "ABC"
        
        encrypted = encrypt(plaintext, key, pairs=custom_pairs)
        decrypted = decrypt(encrypted, key, pairs=custom_pairs)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "ZBX")
    
    def test_encrypt_with_turkish_pairs(self):
        """Test encryption with Turkish pairs."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        turkish_pairs = produce_pairs("turkish", turkish_alphabet)
        
        plaintext = "MERHABA"
        key = "A"
        
        encrypted = encrypt(plaintext, key, turkish_alphabet, turkish_pairs)
        decrypted = decrypt(encrypted, key, turkish_alphabet, turkish_pairs)
        
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(encrypted, "BPFTLML")
    
    def test_encrypt_with_balanced_pairs(self):
        """Test encryption with balanced pairs."""
        alphabet = "ABCDEFGHIJKL"  # 12 letters
        balanced_pairs = produce_pairs("balanced", alphabet)
        
        plaintext = "ABC"
        key = "ABC"
        
        encrypted = encrypt(plaintext, key, alphabet, balanced_pairs)
        decrypted = decrypt(encrypted, key, alphabet, balanced_pairs)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_turkish_alphabet_comprehensive(self):
        """Test comprehensive Turkish alphabet functionality."""
        turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        turkish_pairs = produce_pairs("turkish", turkish_alphabet)
        
        # Test various Turkish texts
        test_cases = [
            ("MERHABA", "KEY"),
            ("ÇOK", "AB"),
            ("GÜZEL", "ABC"),
            ("ŞARKI", "DEF")
        ]
        
        for plaintext, key in test_cases:
            encrypted = encrypt(plaintext, key, turkish_alphabet, turkish_pairs)
            decrypted = decrypt(encrypted, key, turkish_alphabet, turkish_pairs)
            
            self.assertEqual(decrypted, plaintext)
    
    def test_custom_pairs_comprehensive(self):
        """Test comprehensive custom pairs functionality."""
        # Test with different custom pair configurations
        test_configs = [
            [("A", "Z"), ("B", "Y"), ("C", "X")],
            [("A", "M"), ("B", "N"), ("C", "O"), ("D", "P")],
            [("A", "B"), ("C", "D"), ("E", "F")]
        ]
        
        for custom_pairs in test_configs:
            plaintext = "ABC"
            key = "ABC"
            
            encrypted = encrypt(plaintext, key, pairs=custom_pairs)
            decrypted = decrypt(encrypted, key, pairs=custom_pairs)
            
            self.assertEqual(decrypted, plaintext)
    
    def test_invalid_pair_types(self):
        """Test invalid pair types."""
        with self.assertRaises(ValueError):
            produce_pairs("invalid")
    
    def test_self_reciprocal_with_custom_pairs(self):
        """Test self-reciprocal property with custom pairs."""
        custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X")]
        plaintext = "ABC"
        key = "ABC"
        
        encrypted = encrypt(plaintext, key, pairs=custom_pairs)
        
        # Self-reciprocal: encrypting the encrypted text should give back plaintext
        self.assertEqual(encrypt(encrypted, key, pairs=custom_pairs), plaintext)
        
        # Self-reciprocal: decrypting the plaintext should give the encrypted text
        self.assertEqual(decrypt(plaintext, key, pairs=custom_pairs), encrypted)
    
    def test_mixed_alphabet_sizes(self):
        """Test with different alphabet sizes."""
        test_cases = [
            ("ABCDEFGHIJKL", "balanced"),  # 12 letters
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "default"),  # 26 letters
            ("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ", "turkish")  # 29 letters
        ]
        
        for alphabet, pair_type in test_cases:
            pairs = produce_pairs(pair_type, alphabet)
            
            # All pairs should be valid
            for pair in pairs:
                self.assertIn(pair[0], alphabet)
                self.assertIn(pair[1], alphabet)
            
            # Test encryption/decryption
            plaintext = alphabet[:3]  # Use first 3 letters
            key = "ABC"
            
            encrypted = encrypt(plaintext, key, alphabet, pairs)
            decrypted = decrypt(encrypted, key, alphabet, pairs)
            
            self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
