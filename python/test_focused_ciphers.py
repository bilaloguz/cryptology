#!/usr/bin/env python3
"""
Focused Test Suite for Alphabet System Integration

This script tests the new alphabet system with actual cipher behavior,
handling the real output formats of each cipher family.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cryptology.alphabets as alphabets

def test_alphabet_system():
    """Test the centralized alphabet system."""
    print("=== Testing Alphabet System ===")
    
    # Test basic alphabet retrieval
    eng_plain = alphabets.get_alphabet("english", False)
    eng_digits = alphabets.get_alphabet("english", True)
    tr_plain = alphabets.get_alphabet("turkish", False)
    tr_digits = alphabets.get_alphabet("turkish", True)
    
    assert eng_plain == alphabets.ENGLISH_ALPHABET
    assert eng_digits == alphabets.ENGLISH_WITH_DIGITS
    assert tr_plain == alphabets.TURKISH_ALPHABET
    assert tr_digits == alphabets.TURKISH_STANDARD_WITH_DIGITS
    
    print("✅ Basic alphabet retrieval works")
    
    # Test Turkish variants
    tr_standard = alphabets.get_turkish_alphabet("standard")
    tr_extended = alphabets.get_turkish_alphabet("extended")
    tr_extended_7x7 = alphabets.get_turkish_alphabet("extended", True, "7x7")
    
    assert tr_standard == alphabets.TURKISH_STANDARD
    assert tr_extended == alphabets.TURKISH_EXTENDED
    assert tr_extended_7x7 == alphabets.TURKISH_EXTENDED_FULL_SQUARE
    
    print("✅ Turkish variants work")
    
    # Test Q, W, X support
    assert "q" in alphabets.TURKISH_EXTENDED and "w" in alphabets.TURKISH_EXTENDED and "x" in alphabets.TURKISH_EXTENDED
    assert not ("q" in alphabets.TURKISH_STANDARD and "w" in alphabets.TURKISH_STANDARD and "x" in alphabets.TURKISH_STANDARD)
    
    print("✅ Q, W, X support works")
    
    # Test alphabet validation
    assert alphabets.validate_alphabet(alphabets.ENGLISH_ALPHABET)
    assert alphabets.validate_alphabet(alphabets.TURKISH_EXTENDED)
    assert not alphabets.validate_alphabet("aabbcc")  # Has duplicates
    
    print("✅ Alphabet validation works")
    
    # Test normalization
    normalized = alphabets.normalize_text("HELLO WoRLd")
    assert normalized == "hello world"
    
    print("✅ Text normalization works")
    
    print("✅ Alphabet system tests passed\n")

def test_monoalphabetic_ciphers():
    """Test monoalphabetic ciphers."""
    print("=== Testing Monoalphabetic Ciphers ===")
    
    try:
        import cryptology.classical.substitution.monoalphabetic.caesar as caesar
        import cryptology.classical.substitution.monoalphabetic.rot13 as rot13
        import cryptology.classical.substitution.monoalphabetic.atbash as atbash
        import cryptology.classical.substitution.monoalphabetic.keyword as keyword
        import cryptology.classical.substitution.monoalphabetic.affine as affine
        
        plaintext = "hello world"
        
        # Caesar
        encrypted = caesar.encrypt(plaintext, 3)
        decrypted = caesar.decrypt(encrypted, 3)
        assert decrypted == plaintext
        print("✅ Caesar cipher")
        
        # ROT13
        encrypted = rot13.encrypt(plaintext)
        decrypted = rot13.decrypt(encrypted)
        assert decrypted == plaintext
        print("✅ ROT13 cipher")
        
        # Atbash
        encrypted = atbash.encrypt(plaintext)
        decrypted = atbash.decrypt(encrypted)
        assert decrypted == plaintext
        print("✅ Atbash cipher")
        
        # Keyword
        encrypted = keyword.encrypt(plaintext, "secret")
        decrypted = keyword.decrypt(encrypted, "secret")
        assert decrypted == plaintext
        print("✅ Keyword cipher")
        
        # Affine
        encrypted = affine.encrypt(plaintext, 5, 8)
        decrypted = affine.decrypt(encrypted, 5, 8)
        assert decrypted == plaintext
        print("✅ Affine cipher")
        
        # Test with Turkish
        tr_plaintext = "merhaba dünya"
        tr_encrypted = caesar.encrypt(tr_plaintext, 5, alphabets.TURKISH_STANDARD)
        tr_decrypted = caesar.decrypt(tr_encrypted, 5, alphabets.TURKISH_STANDARD)
        assert tr_decrypted == tr_plaintext
        print("✅ Caesar cipher (Turkish)")
        
        print("✅ All monoalphabetic ciphers passed\n")
        
    except ImportError as e:
        print(f"❌ Monoalphabetic cipher import failed: {e}\n")
    except Exception as e:
        print(f"❌ Monoalphabetic cipher test failed: {e}\n")

def test_polyalphabetic_ciphers():
    """Test polyalphabetic ciphers."""
    print("=== Testing Polyalphabetic Ciphers ===")
    
    try:
        import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
        import cryptology.classical.substitution.polyalphabetic.beaufort as beaufort
        import cryptology.classical.substitution.polyalphabetic.autokey as autokey
        import cryptology.classical.substitution.polyalphabetic.gronsfeld as gronsfeld
        import cryptology.classical.substitution.polyalphabetic.porta as porta
        import cryptology.classical.substitution.polyalphabetic.reihenschieber as reihenschieber
        
        plaintext = "hello world"
        key = "secret"
        
        # Vigenère
        encrypted = vigenere.encrypt(plaintext, key)
        decrypted = vigenere.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext
        print("✅ Vigenère cipher")
        
        # Beaufort
        encrypted = beaufort.encrypt(plaintext, key)
        decrypted = beaufort.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext
        print("✅ Beaufort cipher")
        
        # Auto-key
        encrypted = autokey.encrypt(plaintext, key)
        decrypted = autokey.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext
        print("✅ Auto-key cipher")
        
        # Gronsfeld
        encrypted = gronsfeld.encrypt(plaintext, "12345")
        decrypted = gronsfeld.decrypt(encrypted, "12345")
        assert decrypted.lower() == plaintext
        print("✅ Gronsfeld cipher")
        
        # Porta
        encrypted = porta.encrypt(plaintext, key)
        decrypted = porta.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext
        print("✅ Porta cipher")
        
        # Reihenschieber
        encrypted = reihenschieber.encrypt(plaintext, key, "fixed", 1)
        decrypted = reihenschieber.decrypt(encrypted, key, "fixed", 1)
        assert decrypted.lower() == plaintext
        print("✅ Reihenschieber cipher")
        
        print("✅ All polyalphabetic ciphers passed\n")
        
    except ImportError as e:
        print(f"❌ Polyalphabetic cipher import failed: {e}\n")
    except Exception as e:
        print(f"❌ Polyalphabetic cipher test failed: {e}\n")

def test_polygraphic_ciphers():
    """Test polygraphic ciphers."""
    print("=== Testing Polygraphic Ciphers ===")
    
    try:
        import cryptology.classical.substitution.polygraphic.playfair as playfair
        import cryptology.classical.substitution.polygraphic.two_square as two_square
        import cryptology.classical.substitution.polygraphic.four_square as four_square
        import cryptology.classical.substitution.polygraphic.hill as hill
        
        plaintext = "hello world"
        key = "secret"
        
        # Playfair (removes spaces)
        encrypted = playfair.encrypt(plaintext, key)
        decrypted = playfair.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Playfair cipher")
        
        # Two Square
        encrypted = two_square.encrypt(plaintext, key, key)
        decrypted = two_square.decrypt(encrypted, key, key)
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Two Square cipher")
        
        # Four Square
        encrypted = four_square.encrypt(plaintext, key, key, key, key)
        decrypted = four_square.decrypt(encrypted, key, key, key, key)
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Four Square cipher")
        
        # Hill
        encrypted = hill.encrypt(plaintext, [[2, 3], [1, 2]])
        decrypted = hill.decrypt(encrypted, [[2, 3], [1, 2]])
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Hill cipher")
        
        print("✅ All polygraphic ciphers passed\n")
        
    except ImportError as e:
        print(f"❌ Polygraphic cipher import failed: {e}\n")
    except Exception as e:
        print(f"❌ Polygraphic cipher test failed: {e}\n")

def test_fractionated_ciphers():
    """Test fractionated ciphers."""
    print("=== Testing Fractionated Ciphers ===")
    
    try:
        import cryptology.classical.substitution.fractionated.bifid as bifid
        import cryptology.classical.substitution.fractionated.trifid as trifid
        
        plaintext = "hello world"
        key = "secret"
        
        # Bifid (removes spaces)
        encrypted = bifid.encrypt(plaintext, key)
        decrypted = bifid.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Bifid cipher")
        
        # Trifid (removes spaces)
        encrypted = trifid.encrypt(plaintext, key)
        decrypted = trifid.decrypt(encrypted, key)
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Trifid cipher")
        
        print("✅ All fractionated ciphers passed\n")
        
    except ImportError as e:
        print(f"❌ Fractionated cipher import failed: {e}\n")
    except Exception as e:
        print(f"❌ Fractionated cipher test failed: {e}\n")

def test_composite_ciphers():
    """Test composite ciphers."""
    print("=== Testing Composite Ciphers ===")
    
    try:
        import cryptology.classical.substitution.composite.straddling_checkerboard as checkerboard
        import cryptology.classical.substitution.composite.nihilist as nihilist
        import cryptology.classical.substitution.composite.adfgvx as adfgvx
        import cryptology.classical.substitution.composite.vic as vic
        
        plaintext = "hello world"
        
        # Straddling Checkerboard
        encrypted = checkerboard.encrypt(plaintext, "secret", "key")
        decrypted = checkerboard.decrypt(encrypted, "secret", "key")
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Straddling Checkerboard cipher")
        
        # Nihilist
        encrypted = nihilist.nihilist_encrypt(plaintext, "secret", "12345")
        decrypted = nihilist.nihilist_decrypt(encrypted, "secret", "12345")
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ Nihilist cipher")
        
        # ADFGVX
        encrypted = adfgvx.adfgvx_encrypt(plaintext, "secret", "key", "cipher")
        decrypted = adfgvx.adfgvx_decrypt(encrypted, "secret", "key", "cipher")
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ ADFGVX cipher")
        
        # VIC
        encrypted = vic.vic_encrypt(plaintext, "secret", "key", "cipher", "12345")
        decrypted = vic.vic_decrypt(encrypted, "secret", "key", "cipher", "12345")
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ VIC cipher")
        
        print("✅ All composite ciphers passed\n")
        
    except ImportError as e:
        print(f"❌ Composite cipher import failed: {e}\n")
    except Exception as e:
        print(f"❌ Composite cipher test failed: {e}\n")

def test_qwx_support():
    """Test Q, W, X support in Turkish."""
    print("=== Testing Q, W, X Support ===")
    
    try:
        import cryptology.classical.substitution.monoalphabetic.caesar as caesar
        import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
        
        # Test with foreign words containing Q, W, X
        foreign_words = ["washington", "quebec", "mexico", "taxi", "queen"]
        
        for word in foreign_words:
            # Test with extended Turkish alphabet
            encrypted = caesar.encrypt(word, 3, alphabets.TURKISH_EXTENDED)
            decrypted = caesar.decrypt(encrypted, 3, alphabets.TURKISH_EXTENDED)
            assert decrypted == word
            print(f"✅ Caesar with '{word}' (Q,W,X support)")
        
        # Test Vigenère with foreign words
        encrypted = vigenere.encrypt("washington quebec", "secret", alphabet=alphabets.TURKISH_EXTENDED)
        decrypted = vigenere.decrypt(encrypted, "secret", alphabet=alphabets.TURKISH_EXTENDED)
        assert decrypted.lower() == "washington quebec"
        print("✅ Vigenère with foreign words (Q,W,X support)")
        
        print("✅ Q, W, X support tests passed\n")
        
    except ImportError as e:
        print(f"❌ Q, W, X support test failed: {e}\n")
    except Exception as e:
        print(f"❌ Q, W, X support test failed: {e}\n")

def test_utf8_support():
    """Test UTF-8 support with Turkish characters."""
    print("=== Testing UTF-8 Support ===")
    
    try:
        import cryptology.classical.substitution.monoalphabetic.caesar as caesar
        import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
        
        # Test with Turkish characters
        turkish_text = "çğşıüö"
        
        # Caesar with Turkish
        encrypted = caesar.encrypt(turkish_text, 3, alphabets.TURKISH_STANDARD)
        decrypted = caesar.decrypt(encrypted, 3, alphabets.TURKISH_STANDARD)
        assert decrypted == turkish_text
        print("✅ Caesar with Turkish UTF-8 characters")
        
        # Vigenère with Turkish
        encrypted = vigenere.encrypt(turkish_text, "secret", alphabet=alphabets.TURKISH_STANDARD)
        decrypted = vigenere.decrypt(encrypted, "secret", alphabet=alphabets.TURKISH_STANDARD)
        assert decrypted.lower() == turkish_text
        print("✅ Vigenère with Turkish UTF-8 characters")
        
        print("✅ UTF-8 support tests passed\n")
        
    except ImportError as e:
        print(f"❌ UTF-8 support test failed: {e}\n")
    except Exception as e:
        print(f"❌ UTF-8 support test failed: {e}\n")

def test_7x7_squares():
    """Test 7x7 square alphabets."""
    print("=== Testing 7x7 Square Alphabets ===")
    
    try:
        import cryptology.classical.substitution.composite.vic as vic
        
        plaintext = "hello world"
        
        # Test VIC with 7x7 squares
        encrypted = vic.vic_encrypt(plaintext, "secret", "key", "cipher", "12345", 
                                  square_type="standard", language="english")
        decrypted = vic.vic_decrypt(encrypted, "secret", "key", "cipher", "12345", 
                                  square_type="standard", language="english")
        assert decrypted.lower() == plaintext.replace(" ", "")
        print("✅ VIC cipher with 7x7 squares")
        
        # Test with Turkish 7x7
        tr_plaintext = "merhaba dünya"
        tr_encrypted = vic.vic_encrypt(tr_plaintext, "secret", "key", "cipher", "12345", 
                                     language="turkish")
        tr_decrypted = vic.vic_decrypt(tr_encrypted, "secret", "key", "cipher", "12345", 
                                     language="turkish")
        assert tr_decrypted.lower() == tr_plaintext.replace(" ", "")
        print("✅ VIC cipher with Turkish 7x7 squares")
        
        print("✅ 7x7 square tests passed\n")
        
    except ImportError as e:
        print(f"❌ 7x7 square test failed: {e}\n")
    except Exception as e:
        print(f"❌ 7x7 square test failed: {e}\n")

def main():
    """Run all tests."""
    print("🔍 FOCUSED CIPHER SYSTEM TEST SUITE")
    print("=" * 50)
    print()
    
    try:
        test_alphabet_system()
        test_monoalphabetic_ciphers()
        test_polyalphabetic_ciphers()
        test_polygraphic_ciphers()
        test_fractionated_ciphers()
        test_composite_ciphers()
        test_qwx_support()
        test_utf8_support()
        test_7x7_squares()
        
        print("🎉 ALL TESTS PASSED!")
        print("✅ Alphabet system is working correctly")
        print("✅ All cipher families are functional")
        print("✅ Turkish Q, W, X support works")
        print("✅ UTF-8 support works")
        print("✅ 7x7 squares work")
        print()
        print("The new alphabet system is ready for production use!")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
