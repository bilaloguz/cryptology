"""
Tests for Atbash cipher implementation.
"""

import pytest
from cryptology.classical.substitution.monoalphabetic import atbash


class TestAtbash:
    def test_basic_encryption(self):
        """Test basic Atbash encryption."""
        assert atbash.encrypt("HELLO") == "svool"
    
    def test_lowercase_encryption(self):
        """Test Atbash with lowercase letters."""
        assert atbash.encrypt("hello") == "svool"
    
    def test_mixed_case_converts_to_lowercase(self):
        """Test that Atbash converts to lowercase."""
        assert atbash.encrypt("Hello World") == "svool dliow"
    
    def test_non_alphabetic_unchanged(self):
        """Test that non-alphabetic characters remain unchanged."""
        assert atbash.encrypt("Hello, World! 123") == "svool, dliow! 123"
    
    def test_decrypt_is_same_as_encrypt(self):
        """Test that decrypt and encrypt are the same operation."""
        text = "HELLO WORLD"
        assert atbash.decrypt(text) == atbash.encrypt(text)
    
    def test_double_application_returns_original(self):
        """Test that applying Atbash twice returns the original text (lowercased)."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        encrypted = atbash.encrypt(original)
        decrypted = atbash.decrypt(encrypted)
        assert decrypted == original.lower()
    
    def test_alphabet_coverage(self):
        """Test Atbash on the entire alphabet."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        expected = "zyxwvutsrqponmlkjihgfedcba"
        assert atbash.encrypt(alphabet) == expected
        
        # Test uppercase converts to lowercase
        alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert atbash.encrypt(alphabet_upper) == expected
    
    def test_custom_alphabet(self):
        """Test Atbash with custom alphabet."""
        # Simple lowercase alphabet
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        plaintext = "hello"
        encrypted = atbash.encrypt(plaintext, alphabet)
        decrypted = atbash.decrypt(encrypted, alphabet)
        assert decrypted == plaintext
        # Verify reversal: a -> z, z -> a
        assert atbash.encrypt("a", alphabet) == "z"
        assert atbash.encrypt("z", alphabet) == "a"
    
    def test_custom_alphabet_digits(self):
        """Test Atbash with digit alphabet."""
        digits = "0123456789"
        assert atbash.encrypt("123", digits) == "876"
        assert atbash.encrypt("0", digits) == "9"
        assert atbash.encrypt("9", digits) == "0"
    
    def test_symmetric_property(self):
        """Test that Atbash is symmetric."""
        text = "symmetric"
        assert atbash.decrypt(atbash.encrypt(text)) == text

