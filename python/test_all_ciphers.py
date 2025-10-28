#!/usr/bin/env python3
"""
Comprehensive cipher roundtrip testing.

Tests ALL cipher systems with:
- English alphabet: "the quick brown fox jumps over the lazy dog"
- Turkish standard: "pijamalı hasta yağız şoföre çabucak güvendi"
- Turkish extended: "pijamalı hasta yağız şoföre çabucak güvendi qwx"
"""

import sys
import traceback

def normalize(s):
    """Normalize text for comparison (remove spaces and non-letters)"""
    return ''.join(c for c in s.lower() if c.isalpha() or c in 'çğıöşü')

def test_cipher(name, encrypt_func, decrypt_func, plaintext, *args, **kwargs):
    """Test a cipher with given functions and parameters"""
    try:
        ciphertext = encrypt_func(plaintext, *args)
        decrypted = decrypt_func(ciphertext, *args)
        
        # Normalize for comparison
        orig_norm = normalize(plaintext)
        decr_norm = normalize(decrypted)
        
        success = orig_norm == decr_norm
        
        if not success:
            debug = kwargs.get('debug', False)
            if debug:
                print(f"      FAILED:")
                print(f"         Original: '{plaintext[:60]}'")
                print(f"         Encrypted: '{ciphertext[:60]}'")
                print(f"         Decrypted: '{decrypted[:60]}'")
                print(f"         Orig norm: '{orig_norm}'")
                print(f"         Decr norm: '{decr_norm}'")
        
        return success
    except Exception as e:
        if kwargs.get('debug', False):
            print(f"      ERROR: {e}")
            traceback.print_exc()
        return False

# Import alphabets
import cryptology.alphabets as A

# Test texts
TEST_TEXTS = {
    'english': "the quick brown fox jumps over the lazy dog",
    'turkish_standard': "pijamalı hasta yağız şoföre çabucak güvendi",
    'turkish_extended': "pijamalı hasta yağız şoföre çabucak güvendi qwx"
}

print("=" * 80)
print("COMPREHENSIVE CIPHER ROUNDTRIP TESTING")
print("=" * 80)
print("\nTest Texts:")
print(f"  English: '{TEST_TEXTS['english']}'")
print(f"  Turkish (std): '{TEST_TEXTS['turkish_standard']}'")
print(f"  Turkish (ext): '{TEST_TEXTS['turkish_extended']}'")

# Collect results
results = []

# Test all ciphers
print("\n" + "=" * 80)
print("TESTING CIPHERS")
print("=" * 80)

# Monoalphabetic ciphers
print("\n1. Monoalphabetic Ciphers")
print("-" * 80)

# Caesar
try:
    from cryptology.classical.substitution.monoalphabetic import caesar
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Caesar', caesar.encrypt, caesar.decrypt, plain, 3, A.ENGLISH_ALPHABET
    )
    results.append(('Caesar (EN)', success))
    print(f"  {'✓' if success else '✗'} Caesar (English)")
    if not success:
        print(f"    Encrypted: {cipher[:50]}")
        print(f"    Decrypted: {decr[:50]}")
except Exception as e:
    results.append(('Caesar (EN)', False))
    print(f"  ✗ Caesar: {e}")

# Atbash
try:
    from cryptology.classical.substitution.monoalphabetic import atbash
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Atbash', atbash.encrypt, atbash.decrypt, plain, A.ENGLISH_ALPHABET
    )
    results.append(('Atbash (EN)', success))
    print(f"  {'✓' if success else '✗'} Atbash (English)")
except Exception as e:
    results.append(('Atbash (EN)', False))
    print(f"  ✗ Atbash: {e}")

# Keyword
try:
    from cryptology.classical.substitution.monoalphabetic import keyword
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Keyword', keyword.encrypt, keyword.decrypt, plain, 'secret', A.ENGLISH_ALPHABET
    )
    results.append(('Keyword (EN)', success))
    print(f"  {'✓' if success else '✗'} Keyword (English)")
except Exception as e:
    results.append(('Keyword (EN)', False))
    print(f"  ✗ Keyword: {e}")

# Polygraphic ciphers
print("\n2. Polygraphic Ciphers")
print("-" * 80)

# Playfair
try:
    from cryptology.classical.substitution.polygraphic import playfair
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Playfair', playfair.encrypt, playfair.decrypt, plain, 'secret', A.ENGLISH_ALPHABET
    )
    results.append(('Playfair (EN)', success))
    print(f"  {'✓' if success else '✗'} Playfair (English)")
except Exception as e:
    results.append(('Playfair (EN)', False))
    print(f"  ✗ Playfair: {e}")

# Polyalphabetic ciphers
print("\n3. Polyalphabetic Ciphers")
print("-" * 80)

# Vigenère
try:
    from cryptology.classical.substitution.polyalphabetic import vigenere
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Vigenere', vigenere.encrypt, vigenere.decrypt, plain, 'key', A.ENGLISH_ALPHABET
    )
    results.append(('Vigenère (EN)', success))
    print(f"  {'✓' if success else '✗'} Vigenère (English)")
except Exception as e:
    results.append(('Vigenère (EN)', False))
    print(f"  ✗ Vigenère: {e}")

# Beaufort
try:
    from cryptology.classical.substitution.polyalphabetic import beaufort
    plain = TEST_TEXTS['english']
    success, cipher, decr = test_cipher(
        'Beaufort', beaufort.encrypt, beaufort.decrypt, plain, 'key', A.ENGLISH_ALPHABET
    )
    results.append(('Beaufort (EN)', success))
    print(f"  {'✓' if success else '✗'} Beaufort (English)")
except Exception as e:
    results.append(('Beaufort (EN)', False))
    print(f"  ✗ Beaufort: {e}")

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for _, s in results if s)
total = len(results)

print(f"\nResults: {passed}/{total} tests passed")
print(f"Status: {'✓ ALL TESTS PASSED' if passed == total else '✗ SOME TESTS FAILED'}\n")

for name, success in results:
    status = "✓" if success else "✗"
    print(f"  {status} {name}")

print("\n" + "=" * 80)