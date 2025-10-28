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
    return ''.join(c for c in s.lower() if c.isalpha() or c in 'çğıöşüı')

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

def test_cipher_with_alphabet(cipher_name, encrypt_func, decrypt_func, alphabet_name, alphabet, plaintext, *args):
    """Test a cipher with a specific alphabet"""
    try:
        # Create a new args tuple with alphabet inserted at position 2 (after plaintext and first arg)
        # But for Affine, it should be (plaintext, a, b, alphabet), so alphabet is last
        if args:
            # Check if this is Affine (has 2 int args before alphabet)
            if cipher_name == 'Affine' and len(args) == 2 and all(isinstance(x, int) for x in args):
                new_args = args + (alphabet,)  # (a, b, alphabet)
            else:
                new_args = (args[0], alphabet) + args[1:]  # (key, alphabet, square_type, mono_params)
        else:
            new_args = (alphabet,)  # just alphabet
        ciphertext = encrypt_func(plaintext, *new_args)
        decrypted = decrypt_func(ciphertext, *new_args)
        
        orig_norm = normalize(plaintext)
        decr_norm = normalize(decrypted)
        
        success = orig_norm == decr_norm
        is_lowercase = ciphertext.islower() if ciphertext else True
        
        return success, is_lowercase
    except Exception as e:
        return False, True

def test_all_ciphers_all_alphabets():
    """Test all ciphers with all alphabets"""
    print("=" * 100)
    print("COMPREHENSIVE CIPHER TESTING - ALL ALPHABETS")
    print("=" * 100)
    print("\nTest Texts:")
    for lang, text in TEST_TEXTS.items():
        print(f"  {lang:20}: '{text}'")

    results = []

    # ============================================================================
    # 1. MONOALPHABETIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 100)
    print("1. MONOALPHABETIC CIPHERS")
    print("=" * 100)

    # Caesar - English
    print("  Caesar (English)...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import caesar
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Caesar', caesar.encrypt, caesar.decrypt, plain, 3, A.ENGLISH_ALPHABET)
        results.append(('Caesar', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Caesar', 'EN', False, True))
        print(f"✗: {e}")

    # Caesar - Turkish Standard
    print("  Caesar (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Caesar', caesar.encrypt, caesar.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 3)
        results.append(('Caesar', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Caesar', 'TR', False, True))
        print(f"✗: {e}")

    # Caesar - Turkish Extended
    print("  Caesar (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Caesar', caesar.encrypt, caesar.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 3)
        results.append(('Caesar', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Caesar', 'TRX', False, True))
        print(f"✗: {e}")

    # Atbash - English
    print("  Atbash (English)...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import atbash
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Atbash', atbash.encrypt, atbash.decrypt, plain, A.ENGLISH_ALPHABET)
        results.append(('Atbash', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Atbash', 'EN', False, True))
        print(f"✗: {e}")

    # Atbash - Turkish Standard
    print("  Atbash (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Atbash', atbash.encrypt, atbash.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'])
        results.append(('Atbash', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Atbash', 'TR', False, True))
        print(f"✗: {e}")

    # Atbash - Turkish Extended
    print("  Atbash (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Atbash', atbash.encrypt, atbash.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'])
        results.append(('Atbash', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Atbash', 'TRX', False, True))
        print(f"✗: {e}")

    # Keyword - English
    print("  Keyword (English)...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import keyword
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Keyword', keyword.encrypt, keyword.decrypt, plain, 'secret', A.ENGLISH_ALPHABET)
        results.append(('Keyword', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Keyword', 'EN', False, True))
        print(f"✗: {e}")

    # Keyword - Turkish Standard
    print("  Keyword (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Keyword', keyword.encrypt, keyword.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'gizli')
        results.append(('Keyword', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Keyword', 'TR', False, True))
        print(f"✗: {e}")

    # Keyword - Turkish Extended
    print("  Keyword (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Keyword', keyword.encrypt, keyword.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'gizli')
        results.append(('Keyword', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Keyword', 'TRX', False, True))
        print(f"✗: {e}")

    # Affine - English
    print("  Affine (English)...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import affine
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Affine', affine.encrypt, affine.decrypt, plain, 5, 8, A.ENGLISH_ALPHABET)
        results.append(('Affine', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Affine', 'EN', False, True))
        print(f"✗: {e}")

    # Affine - Turkish Standard
    print("  Affine (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Affine', affine.encrypt, affine.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 5, 8)
        results.append(('Affine', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Affine', 'TR', False, True))
        print(f"✗: {e}")

    # Affine - Turkish Extended
    print("  Affine (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Affine', affine.encrypt, affine.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 5, 8)
        results.append(('Affine', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Affine', 'TRX', False, True))
        print(f"✗: {e}")

    # ROT13 - English
    print("  ROT13 (English)...", end=' ')
    try:
        from cryptology.classical.substitution.monoalphabetic import rot13
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('ROT13', rot13.encrypt, rot13.decrypt, plain, A.ENGLISH_ALPHABET)
        results.append(('ROT13', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('ROT13', 'EN', False, True))
        print(f"✗: {e}")

    # ROT13 - Turkish Standard
    print("  ROT13 (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('ROT13', rot13.encrypt, rot13.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'])
        results.append(('ROT13', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('ROT13', 'TR', False, True))
        print(f"✗: {e}")

    # ROT13 - Turkish Extended
    print("  ROT13 (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('ROT13', rot13.encrypt, rot13.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'])
        results.append(('ROT13', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('ROT13', 'TRX', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 2. POLYGRAPHIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 100)
    print("2. POLYGRAPHIC CIPHERS")
    print("=" * 100)

    # Playfair - English
    print("  Playfair (English)...", end=' ')
    try:
        from cryptology.classical.substitution.polygraphic import playfair
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Playfair', playfair.encrypt, playfair.decrypt, plain, 'secret', A.ENGLISH_ALPHABET)
        results.append(('Playfair', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Playfair', 'EN', False, True))
        print(f"✗: {e}")

    # Playfair - Turkish Standard
    print("  Playfair (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Playfair', playfair.encrypt, playfair.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'gizli')
        results.append(('Playfair', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Playfair', 'TR', False, True))
        print(f"✗: {e}")

    # Playfair - Turkish Extended
    print("  Playfair (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Playfair', playfair.encrypt, playfair.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'gizli')
        results.append(('Playfair', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Playfair', 'TRX', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 3. FRACTIONATED CIPHERS
    # ============================================================================
    print("\n" + "=" * 100)
    print("3. FRACTIONATED CIPHERS")
    print("=" * 100)

    # Bifid - English
    print("  Bifid (English)...", end=' ')
    try:
        from cryptology.classical.substitution.fractionated import bifid
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Bifid', bifid.encrypt, bifid.decrypt, plain, 'test', A.ENGLISH_ALPHABET, 'standard', None)
        results.append(('Bifid', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Bifid', 'EN', False, True))
        print(f"✗: {e}")

    # Bifid - Turkish Standard
    print("  Bifid (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Bifid', bifid.encrypt, bifid.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'test', 'standard', None)
        results.append(('Bifid', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Bifid', 'TR', False, True))
        print(f"✗: {e}")

    # Bifid - Turkish Extended
    print("  Bifid (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Bifid', bifid.encrypt, bifid.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'test', 'standard', None)
        results.append(('Bifid', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Bifid', 'TRX', False, True))
        print(f"✗: {e}")

    # Trifid - English
    print("  Trifid (English)...", end=' ')
    try:
        from cryptology.classical.substitution.fractionated import trifid
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Trifid', trifid.encrypt, trifid.decrypt, plain, 'test', A.ENGLISH_ALPHABET, 'standard', None)
        results.append(('Trifid', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Trifid', 'EN', False, True))
        print(f"✗: {e}")

    # Trifid - Turkish Standard
    print("  Trifid (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Trifid', trifid.encrypt, trifid.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'test', 'standard', None)
        results.append(('Trifid', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Trifid', 'TR', False, True))
        print(f"✗: {e}")

    # Trifid - Turkish Extended
    print("  Trifid (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Trifid', trifid.encrypt, trifid.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'test', 'standard', None)
        results.append(('Trifid', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Trifid', 'TRX', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 4. POLYALPHABETIC CIPHERS
    # ============================================================================
    print("\n" + "=" * 100)
    print("4. POLYALPHABETIC CIPHERS")
    print("=" * 100)

    # Vigenère - English
    print("  Vigenère (English)...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import vigenere
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Vigenère', vigenere.encrypt, vigenere.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Vigenère', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Vigenère', 'EN', False, True))
        print(f"✗: {e}")

    # Vigenère - Turkish Standard
    print("  Vigenère (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Vigenère', vigenere.encrypt, vigenere.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'anahtar')
        results.append(('Vigenère', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Vigenère', 'TR', False, True))
        print(f"✗: {e}")

    # Vigenère - Turkish Extended
    print("  Vigenère (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Vigenère', vigenere.encrypt, vigenere.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'anahtar')
        results.append(('Vigenère', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Vigenère', 'TRX', False, True))
        print(f"✗: {e}")

    # Beaufort - English
    print("  Beaufort (English)...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import beaufort
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Beaufort', beaufort.encrypt, beaufort.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Beaufort', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Beaufort', 'EN', False, True))
        print(f"✗: {e}")

    # Beaufort - Turkish Standard
    print("  Beaufort (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Beaufort', beaufort.encrypt, beaufort.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'anahtar')
        results.append(('Beaufort', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Beaufort', 'TR', False, True))
        print(f"✗: {e}")

    # Beaufort - Turkish Extended
    print("  Beaufort (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Beaufort', beaufort.encrypt, beaufort.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'anahtar')
        results.append(('Beaufort', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Beaufort', 'TRX', False, True))
        print(f"✗: {e}")

    # Auto-key - English
    print("  Auto-key (English)...", end=' ')
    try:
        from cryptology.classical.substitution.polyalphabetic import autokey
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Auto-key', autokey.encrypt, autokey.decrypt, plain, 'key', A.ENGLISH_ALPHABET)
        results.append(('Auto-key', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Auto-key', 'EN', False, True))
        print(f"✗: {e}")

    # Auto-key - Turkish Standard
    print("  Auto-key (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Auto-key', autokey.encrypt, autokey.decrypt, 'Turkish Standard', A.TURKISH_ALPHABET, TEST_TEXTS['turkish_standard'], 'anahtar')
        results.append(('Auto-key', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Auto-key', 'TR', False, True))
        print(f"✗: {e}")

    # Auto-key - Turkish Extended
    print("  Auto-key (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher_with_alphabet('Auto-key', autokey.encrypt, autokey.decrypt, 'Turkish Extended', A.TURKISH_EXTENDED, TEST_TEXTS['turkish_extended'], 'anahtar')
        results.append(('Auto-key', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Auto-key', 'TRX', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # 5. TRANSPOSITION CIPHERS
    # ============================================================================
    print("\n" + "=" * 100)
    print("5. TRANSPOSITION CIPHERS")
    print("=" * 100)

    # Scytale - English
    print("  Scytale (English)...", end=' ')
    try:
        from cryptology.classical.transposition.simple import scytale
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Scytale', scytale.encrypt, scytale.decrypt, plain, 3)
        results.append(('Scytale', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Scytale', 'EN', False, True))
        print(f"✗: {e}")

    # Scytale - Turkish Standard
    print("  Scytale (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher('Scytale', scytale.encrypt, scytale.decrypt, TEST_TEXTS['turkish_standard'], 3)
        results.append(('Scytale', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Scytale', 'TR', False, True))
        print(f"✗: {e}")

    # Scytale - Turkish Extended
    print("  Scytale (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher('Scytale', scytale.encrypt, scytale.decrypt, TEST_TEXTS['turkish_extended'], 3)
        results.append(('Scytale', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Scytale', 'TRX', False, True))
        print(f"✗: {e}")

    # Rail Fence - English
    print("  Rail Fence (English)...", end=' ')
    try:
        from cryptology.classical.transposition.simple import rail_fence
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Rail Fence', rail_fence.encrypt, rail_fence.decrypt, plain, 3)
        results.append(('Rail Fence', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Rail Fence', 'EN', False, True))
        print(f"✗: {e}")

    # Rail Fence - Turkish Standard
    print("  Rail Fence (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher('Rail Fence', rail_fence.encrypt, rail_fence.decrypt, TEST_TEXTS['turkish_standard'], 3)
        results.append(('Rail Fence', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Rail Fence', 'TR', False, True))
        print(f"✗: {e}")

    # Rail Fence - Turkish Extended
    print("  Rail Fence (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher('Rail Fence', rail_fence.encrypt, rail_fence.decrypt, TEST_TEXTS['turkish_extended'], 3)
        results.append(('Rail Fence', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Rail Fence', 'TRX', False, True))
        print(f"✗: {e}")

    # Columnar Transposition - English
    print("  Columnar Transposition (English)...", end=' ')
    try:
        from cryptology.classical.transposition.columnar import single
        plain = TEST_TEXTS['english']
        success, lower = test_cipher('Columnar', single.encrypt, single.decrypt, plain, 'cipher')
        results.append(('Columnar', 'EN', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Columnar', 'EN', False, True))
        print(f"✗: {e}")

    # Columnar Transposition - Turkish Standard
    print("  Columnar Transposition (Turkish Standard)...", end=' ')
    try:
        success, lower = test_cipher('Columnar', single.encrypt, single.decrypt, TEST_TEXTS['turkish_standard'], 'şifre')
        results.append(('Columnar', 'TR', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Columnar', 'TR', False, True))
        print(f"✗: {e}")

    # Columnar Transposition - Turkish Extended
    print("  Columnar Transposition (Turkish Extended)...", end=' ')
    try:
        success, lower = test_cipher('Columnar', single.encrypt, single.decrypt, TEST_TEXTS['turkish_extended'], 'şifre')
        results.append(('Columnar', 'TRX', success, lower))
        print(f"{'✓' if success else '✗'}")
    except Exception as e:
        results.append(('Columnar', 'TRX', False, True))
        print(f"✗: {e}")

    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 100)
    print("TEST SUMMARY")
    print("=" * 100)

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

    print("\n" + "=" * 100)

if __name__ == "__main__":
    test_all_ciphers_all_alphabets()
