"""
Tests for Caesar cipher implementation.
"""

import pytest
from cryptology.classical.substitution.monoalphabetic import caesar


class TestCaesarEncryption:
    def test_basic_encryption(self):
        """Test basic encryption with default shift."""
        assert caesar.encrypt("HELLO", 3) == "khoor"
    
    def test_lowercase_encryption(self):
        """Test encryption with lowercase input."""
        assert caesar.encrypt("hello", 3) == "khoor"
    
    def test_mixed_case_converts_to_lowercase(self):
        """Test that mixed case is converted to lowercase."""
        assert caesar.encrypt("Hello World", 3) == "khoor zruog"
    
    def test_wrap_around(self):
        """Test that encryption wraps around the alphabet."""
        assert caesar.encrypt("XYZ", 3) == "abc"
    
    def test_non_alphabetic_unchanged(self):
        """Test that non-alphabetic characters remain unchanged."""
        assert caesar.encrypt("Hello, World! 123", 3) == "khoor, zruog! 123"
    
    def test_custom_shift(self):
        """Test encryption with custom shift value."""
        assert caesar.encrypt("ABC", 1) == "bcd"
        assert caesar.encrypt("ABC", 13) == "nop"
    
    def test_custom_alphabet(self):
        """Test encryption with custom alphabet."""
        # Simple lowercase alphabet
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        assert caesar.encrypt("abc", 1, alphabet) == "bcd"
        assert caesar.encrypt("xyz", 3, alphabet) == "abc"
    
    def test_custom_alphabet_non_latin(self):
        """Test encryption with non-Latin alphabet."""
        # Turkish alphabet (simplified)
        turkish = "abcçdefgğhıijklmnoöprsştuüvyz"
        plaintext = "merhaba"
        encrypted = caesar.encrypt(plaintext, 3, turkish)
        decrypted = caesar.decrypt(encrypted, 3, turkish)
        assert decrypted == plaintext


class TestCaesarDecryption:
    def test_basic_decryption(self):
        """Test basic decryption with default shift."""
        assert caesar.decrypt("KHOOR", 3) == "hello"
    
    def test_lowercase_decryption(self):
        """Test decryption with lowercase input."""
        assert caesar.decrypt("khoor", 3) == "hello"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that decrypt(encrypt(text)) == text (lowercased)."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        encrypted = caesar.encrypt(original, 7)
        decrypted = caesar.decrypt(encrypted, 7)
        assert decrypted == original.lower()

