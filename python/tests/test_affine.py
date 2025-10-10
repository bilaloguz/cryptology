"""
Tests for Affine cipher implementation.
"""

import pytest
from cryptology.classical.substitution.monoalphabetic import affine


class TestAffine:
    def test_basic_encryption(self):
        """Test basic affine encryption."""
        assert affine.encrypt("HELLO", 5, 8) == "rclla"
    
    def test_lowercase_encryption(self):
        """Test affine with lowercase input."""
        assert affine.encrypt("hello", 5, 8) == "rclla"
    
    def test_mixed_case_converts_to_lowercase(self):
        """Test that affine converts to lowercase."""
        assert affine.encrypt("Hello World", 5, 8) == "rclla oalvx"
    
    def test_non_alphabetic_unchanged(self):
        """Test that non-alphabetic characters remain unchanged."""
        assert affine.encrypt("Hello, World! 123", 5, 8) == "rclla, oalvx! 123"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that decrypt(encrypt(text)) == text (lowercased)."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        a, b = 5, 8
        encrypted = affine.encrypt(original, a, b)
        decrypted = affine.decrypt(encrypted, a, b)
        assert decrypted == original.lower()
    
    def test_different_keys_different_results(self):
        """Test that different keys produce different encryptions."""
        text = "hello"
        encrypted1 = affine.encrypt(text, 5, 8)
        encrypted2 = affine.encrypt(text, 7, 3)
        assert encrypted1 != encrypted2
    
    def test_a_equals_1_is_caesar(self):
        """Test that a=1 reduces to Caesar cipher."""
        text = "hello"
        shift = 3
        # Affine with a=1, b=shift should equal Caesar with shift
        from cryptology.classical.substitution.monoalphabetic import caesar
        affine_result = affine.encrypt(text, 1, shift)
        caesar_result = caesar.encrypt(text, shift)
        assert affine_result == caesar_result
    
    def test_coprime_validation(self):
        """Test that non-coprime 'a' raises ValueError."""
        with pytest.raises(ValueError, match="must be coprime"):
            affine.encrypt("hello", 2, 5)  # gcd(2, 26) = 2, not coprime
        
        with pytest.raises(ValueError, match="must be coprime"):
            affine.encrypt("hello", 13, 5)  # gcd(13, 26) = 13, not coprime
    
    def test_valid_coprime_keys(self):
        """Test encryption with various valid coprime keys."""
        text = "hello"
        # Valid a values for m=26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
        valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        for a in valid_a_values:
            encrypted = affine.encrypt(text, a, 0)
            decrypted = affine.decrypt(encrypted, a, 0)
            assert decrypted == text, f"Failed for a={a}"
    
    def test_b_zero(self):
        """Test affine cipher with b=0."""
        text = "abc"
        encrypted = affine.encrypt(text, 5, 0)
        decrypted = affine.decrypt(encrypted, 5, 0)
        assert decrypted == text
    
    def test_custom_alphabet(self):
        """Test affine with custom alphabet."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        text = "hello"
        a, b = 5, 8
        encrypted = affine.encrypt(text, a, b, alphabet)
        decrypted = affine.decrypt(encrypted, a, b, alphabet)
        assert decrypted == text
    
    def test_custom_alphabet_digits(self):
        """Test affine with digit alphabet."""
        digits = "0123456789"
        # For m=10, valid a values: 1, 3, 7, 9
        text = "12345"
        a, b = 3, 5
        encrypted = affine.encrypt(text, a, b, digits)
        decrypted = affine.decrypt(encrypted, a, b, digits)
        assert decrypted == text
    
    def test_full_alphabet_coverage(self):
        """Test encryption covers entire alphabet uniquely."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        a, b = 5, 8
        encrypted = affine.encrypt(alphabet, a, b)
        # All characters should be different (bijection)
        assert len(set(encrypted)) == len(alphabet)
    
    def test_modular_inverse_calculation(self):
        """Test modular inverse calculation."""
        # Test some known modular inverses mod 26
        assert affine._mod_inverse(5, 26) == 21  # 5 * 21 = 105 ≡ 1 (mod 26)
        assert affine._mod_inverse(7, 26) == 15  # 7 * 15 = 105 ≡ 1 (mod 26)
        assert affine._mod_inverse(11, 26) == 19  # 11 * 19 = 209 ≡ 1 (mod 26)
    
    def test_decrypt_invalid_key(self):
        """Test that decryption with invalid key raises error."""
        with pytest.raises(ValueError, match="must be coprime"):
            affine.decrypt("test", 2, 5)

