"""
Tests for Keyword cipher implementation.
"""

import pytest
from cryptology.classical.substitution.monoalphabetic import keyword


class TestKeyword:
    def test_basic_encryption(self):
        """Test basic keyword encryption."""
        assert keyword.encrypt("HELLO", "zebra") == "dclla"
    
    def test_lowercase_encryption(self):
        """Test keyword with lowercase input."""
        assert keyword.encrypt("hello", "zebra") == "dclla"
    
    def test_mixed_case_converts_to_lowercase(self):
        """Test that keyword converts to lowercase."""
        assert keyword.encrypt("Hello World", "zebra") == "dclla tloas"
    
    def test_keyword_with_duplicates(self):
        """Test that duplicate letters in keyword are removed."""
        # "HELLO" has duplicate L and O, should become "HELO..."
        encrypted1 = keyword.encrypt("abc", "hello")
        encrypted2 = keyword.encrypt("abc", "helo")
        assert encrypted1 == encrypted2
    
    def test_non_alphabetic_unchanged(self):
        """Test that non-alphabetic characters remain unchanged."""
        assert keyword.encrypt("Hello, World! 123", "key") == "dahhk, sknhz! 123"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that decrypt(encrypt(text)) == text (lowercased)."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        key = "secret"
        encrypted = keyword.encrypt(original, key)
        decrypted = keyword.decrypt(encrypted, key)
        assert decrypted == original.lower()
    
    def test_different_keywords_different_results(self):
        """Test that different keywords produce different encryptions."""
        text = "hello"
        encrypted1 = keyword.encrypt(text, "key")
        encrypted2 = keyword.encrypt(text, "word")
        assert encrypted1 != encrypted2
    
    def test_alphabet_coverage(self):
        """Test encryption covers entire alphabet."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        key = "zebra"
        encrypted = keyword.encrypt(alphabet, key)
        # Should be: zebracdfghijklmnopqstuvwxy (keyword first, then remaining)
        assert encrypted == "zcdhefklqrsuvwxyabgijmnopt"
    
    def test_custom_alphabet(self):
        """Test keyword with custom alphabet."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        plaintext = "hello"
        key = "key"
        encrypted = keyword.encrypt(plaintext, key, alphabet)
        decrypted = keyword.decrypt(encrypted, key, alphabet)
        assert decrypted == plaintext
    
    def test_keyword_case_insensitive(self):
        """Test that keyword case doesn't matter."""
        text = "hello"
        encrypted1 = keyword.encrypt(text, "KEY")
        encrypted2 = keyword.encrypt(text, "key")
        assert encrypted1 == encrypted2
    
    def test_empty_keyword_uses_original_alphabet(self):
        """Test that empty keyword results in no substitution."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        text = "hello"
        encrypted = keyword.encrypt(text, "", alphabet)
        # Empty keyword means cipher alphabet = plain alphabet
        assert encrypted == text
    
    def test_keyword_from_alphabet(self):
        """Test keyword that contains letters from alphabet."""
        text = "abc"
        key = "xyz"
        encrypted = keyword.encrypt(text, key)
        decrypted = keyword.decrypt(encrypted, key)
        assert decrypted == text

