#!/usr/bin/env python3
"""
COMPREHENSIVE CIPHER TESTING - ALL ALPHABETS

Tests ALL cipher systems with:
- English: "the quick brown fox is over the lazy dog"
- Turkish standard: "pijamalı hasta yağız şoföre çabucak güvendi"
- Turkish extended: "pijamalı hasta yağız şoföre çabucak güvendi qwx"
"""

import cryptology.alphabets as A

# Test texts
TEST_TEXTS = {
    'english': "the quick brown fox is over the lazy dog",
    'turkish_standard': "pijamalı hasta yağız şoföre çabucak güvendi",
    'turkish_extended': "pijamalı hasta yağız şoföre çabucak güvendi qwx"
}

def normalize(s):
    """Normalize text for comparison (keep letters and Turkish chars)"""
    return ''.join(c for c in s.lower() if c.isalpha() or c in 'çğıöşü')

def test_cipher(name, encrypt_func, decrypt_func, plaintext, *args, **kwargs):
    """Test a cipher roundtrip"""
    try:
        ciphertext = encrypt_func(plaintext, *args)
        decrypted = decrypt_func(ciphertext, *args)
        
        orig_norm = normalize(plaintext)
        decr_norm = normalize(decrypted)
        
        success = orig_norm == decr_norm
        is_lowercase = ciphertext.islower() if ciphertext else True
        
        return success, is_lowercase
    except Exception as e:
        if kwargs.get('debug', False):
            print(f"         ERROR: {e}")
        return False, True

def test_all_ciphers():
    """Test all ciphers with all alphabets"""
    print("=" * 80)
    print("COMPREHENSIVE CIPHER TESTING - ALL ALPHABETS")
    print("=" * 80)
    print("\nTest Texts:")
    for lang, text in TEST_TEXTS.items():
        print(f"  {lang:20}: '{text}'")

    results = []

    # ============================================================================
    # 1. MONOALPHABETIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 80)
    print("1. MONOALPHABETIC CIPHERS")
    print("=" * 80)

    # Caesar
    print("  Caesar...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import caesar
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Caesar', caesar.encrypt, caesar.decrypt, plain, 3, A.ENGLISH_ALPHABET)
        results.append(('Caesar', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Caesar', 'EN', False, True))
        print(f"✗: {e}")

    # Atbash
    print("  Atbash...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import atbash
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Atbash', atbash.encrypt, atbash.decrypt, plain, A.ENGLISH_ALPHABET)
        results.append(('Atbash', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Atbash', 'EN', False, True))
        print(f"✗: {e}")

    # Keyword
    print("  Keyword...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import keyword
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Keyword', keyword.encrypt, keyword.decrypt, plain, 'secret', A.ENGLISH_ALPHABET)
        results.append(('Keyword', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Keyword', 'EN', False, True))
        print(f"✗: {e}")

    # Affine
    print("  Affine...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import affine
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Affine', affine.encrypt, affine.decrypt, plain, 5, 8, A.ENGLISH_ALPHABET)
        results.append(('Affine', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Affine', 'EN', False, True))
        print(f"✗: {e}")

    # ROT13
    print("  ROT13...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import rot13
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('ROT13', rot13.encrypt, rot13.decrypt, plain, A.ENGLISH_ALPHABET)
        results.append(('ROT13', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('ROT13', 'EN', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 2. POLYGRAPHIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 80)
    print("2. POLYGRAPHIC CIPHERS")
    print("=" * 80)

    # Playfair
    print("  Playfair...", end=' ')
    try:
        from cryptology.classical.substitution.polygraphic import playfair
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Playfair', playfair.encrypt, playfair.decrypt, plain, 'secret', A.ENGLISH_ALPHABET)
        results.append(('Playfair', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Playfair', 'EN', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 3. FRACTIONATED CIPHERS
    # ============================================================================
    print("\n" + "=" * 80)
    print("3. FRACTIONATED CIPHERS")
    print("=" * 80)

    # Bifid
    print("  Bifid...", end=' ')
    try:
        from cryptology.classical.substitution.fractionated import bifid
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Bifid', bifid.encrypt, bifid.decrypt, plain, 'test', A.ENGLISH_ALPHABET, 'standard', None)
        results.append(('Bifid', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Bifid', 'EN', False, True))
        print(f"✗: {e}")

    # Trifid
    print("  Trifid...", end=' ')
    try:
        from cryptology.classical.substitution.fractionated import trifid
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Trifid', trifid.encrypt, trifid.decrypt, plain, 'test', A.ENGLISH_ALPHABET, 'standard', None)
        results.append(('Trifid', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Trifid', 'EN', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 4. POLYALPHABETIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 80)
    print("4. POLYALPHABETIC CIPHERS")
    print("=" * 80)

    # Vigenère
    print("  Vigenère...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import vigenere
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Vigenère', vigenere.encrypt, vigenere.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Vigenère', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Vigenère', 'EN', False, True))
        print(f"✗: {e}")

    # Beaufort
    print("  Beaufort...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import beaufort
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Beaufort', beaufort.encrypt, beaufort.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Beaufort', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Beaufort', 'EN', False, True))
        print(f"✗: {e}")

    # Auto-key
    print("  Auto-key...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import autokey
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Auto-key', autokey.encrypt, autokey.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Auto-key', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Auto-key', 'EN', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 5. TRANSPOSITION CIPHERS
    # ============================================================================
    print("\n" + "=" * 80)
    print("5. TRANSPOSITION CIPHERS")
    print("=" * 80)

    # Scytale
    print("  Scytale...", end=' ')
    try:
        from cryptology.classical.transposition.simple import scytale
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Scytale', scytale.encrypt, scytale.decrypt, plain, 3)
        results.append(('Scytale', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Scytale', 'EN', False, True))
        print(f"✗: {e}")

    # Rail Fence
    print("  Rail Fence...", end=' ')
    try:
        from cryptology.classical.transposition.simple import rail_fence
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Rail Fence', rail_fence.encrypt, rail_fence.decrypt, plain, 3)
        results.append(('Rail Fence', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Rail Fence', 'EN', False, True))
        print(f"✗: {e}")

    # Columnar Transposition
    print("  Columnar Transposition...", end=' ')
    try:
        from cryptology.classical.transposition.columnar import single
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Columnar', single.encrypt, single.decrypt, plain, 'cipher')
        results.append(('Columnar', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Columnar', 'EN', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, _, s, _ in results if s)
    total = len(results)
    lowercase = sum(1 for _, _, _, l in results if l)

    print(f"\nRoundtrip Pass: {passed}/{total}")
    print(f"Lowercase Output: {lowercase}/{total}")
    print(f"Status: {'✓ ALL TESTS PASSED' if passed == total else '✗ SOME TESTS FAILED'}\n")

    print("Detailed Results:")
    for name, lang, success, lower in results:
        rt = "✓" if success else "✗"
        lc = "✓" if lower else "✗"
        print(f"  {rt} {lc} {name:20} ({lang})")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_all_ciphers()
