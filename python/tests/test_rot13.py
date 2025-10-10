"""
Tests for ROT13 cipher implementation.
"""

import pytest
from cryptology.classical.substitution.monoalphabetic import rot13


class TestROT13:
    def test_basic_encryption(self):
        """Test basic ROT13 encryption."""
        assert rot13.encrypt("HELLO") == "uryyb"
    
    def test_lowercase_encryption(self):
        """Test ROT13 with lowercase letters."""
        assert rot13.encrypt("hello") == "uryyb"
    
    def test_mixed_case_converts_to_lowercase(self):
        """Test that ROT13 converts to lowercase."""
        assert rot13.encrypt("Hello World") == "uryyb jbeyq"
    
    def test_non_alphabetic_unchanged(self):
        """Test that non-alphabetic characters remain unchanged."""
        assert rot13.encrypt("Hello, World! 123") == "uryyb, jbeyq! 123"
    
    def test_decrypt_is_same_as_encrypt(self):
        """Test that decrypt and encrypt are the same operation."""
        text = "HELLO WORLD"
        assert rot13.decrypt(text) == rot13.encrypt(text)
    
    def test_double_application_returns_original(self):
        """Test that applying ROT13 twice returns the original text (lowercased)."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        encrypted = rot13.encrypt(original)
        decrypted = rot13.decrypt(encrypted)
        assert decrypted == original.lower()
    
    def test_alphabet_coverage(self):
        """Test ROT13 on the entire alphabet."""
        alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        expected_lower = "nopqrstuvwxyzabcdefghijklm"
        assert rot13.encrypt(alphabet_upper) == expected_lower
        
        alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
        expected_lower = "nopqrstuvwxyzabcdefghijklm"
        assert rot13.encrypt(alphabet_lower) == expected_lower
    
    def test_custom_alphabet(self):
        """Test ROT13 with custom alphabet."""
        # Simple lowercase alphabet
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        plaintext = "hello"
        encrypted = rot13.encrypt(plaintext, alphabet)
        decrypted = rot13.decrypt(encrypted, alphabet)
        assert decrypted == plaintext
        # Verify shift is half the alphabet (13 for 26 letters)
        assert rot13.encrypt("a", alphabet) == "n"
        assert rot13.encrypt("n", alphabet) == "a"

