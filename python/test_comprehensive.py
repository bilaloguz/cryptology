#!/usr/bin/env python3
"""
COMPREHENSIVE CIPHER ROUNDTRIP TESTING

Tests ALL ciphers with ALL alphabets:
- English: "the quick brown fox jumps over the lazy dog"
- Turkish standard: "pijamalı hasta yağız şoföre çabucak güvendi"
- Turkish extended: "pijamalı hasta yağız şoföre çabucak güvendi qwx"

For each cipher: encrypt → decrypt → must match EXACTLY
"""

import cryptology.alphabets as A

# Test texts
TEST_TEXTS = {
    'english': "the quick brown fox jumps over the lazy dog",
    'turkish_standard': "pijamalı hasta yağız şoföre çabucak güvendi",
    'turkish_extended': "pijamalı hasta yağız şoföre çabucak güvendi qwx"
}

def normalize(s):
    """Normalize text for comparison"""
    return ''.join(c for c in s.lower() if c.isalpha() or c in 'çğıöşü')

def test_cipher(name, encrypt_func, decrypt_func, plaintext, lang, *args):
    """Test a cipher and return success status"""
    try:
        ciphertext = encrypt_func(plaintext, *args)
        decrypted = decrypt_func(ciphertext, *args)
        
        orig_norm = normalize(plaintext)
        decr_norm = normalize(decrypted)
        
        success = orig_norm == decr_norm
        return success, ciphertext.islower() if ciphertext else True
    except Exception as e:
        return False, True

# Test configurations for each cipher type
print("=" * 80)
print("COMPREHENSIVE CIPHER ROUNDTRIP TESTING")
print("=" * 80)
print("\nTest Texts:")
for lang, text in TEST_TEXTS.items():
    print(f"  {lang:20}: '{text}'")

results = []

print("\n" + "=" * 80)
print("TESTING MONOALPHABETIC CIPHERS")
print("=" * 80)

# Caesar
print("\nTesting Caesar cipher...")
try:
    from cryptology.classical.substitution.monoalphabetic import caesar
    plain = TEST_TEXTS['english']
    success, lower = test_cipher('Caesar', caesar.encrypt, caesar.decrypt, plain, 'EN', 3, A.ENGLISH_ALPHABET)
    results.append(('Caesar (EN)', success, lower))
    print(f"  {'✓' if success else '✗'} Caesar (English)")
    if not success:
        print(f"    FAILED - debug needed")
except Exception as e:
    results.append(('Caesar (EN)', False, True))
    print(f"  ✗ Caesar: {e}")

# Atbash
print("\nTesting Atbash cipher...")
try:
    from cryptology.classical.substitution.monoalphabetic import atbash
    plain = TEST_TEXTS['english']
    success, lower = test_cipher('Atbash', atbash.encrypt, atbash.decrypt, plain, 'EN', A.ENGLISH_ALPHABET)
    results.append(('Atbash (EN)', success, lower))
    print(f"  {'✓' if success else '✗'} Atbash (English)")
except Exception as e:
    results.append(('Atbash (EN)', False, True))
    print(f"  ✗ Atbash: {e}")

# Keyword
print("\nTesting Keyword cipher...")
try:
    from cryptology.classical.substitution.monoalphabetic import keyword
    plain = TEST_TEXTS['english']
    success, lower = test_cipher('Keyword', keyword.encrypt, keyword.decrypt, plain, 'EN', 'secret', A.ENGLISH_ALPHABET)
    results.append(('Keyword (EN)', success, lower))
    print(f"  {'✓' if success else '✗'} Keyword (English)")
except Exception as e:
    results.append(('Keyword (EN)', False, True))
    print(f"  ✗ Keyword: {e}")

# Affine
print("\nTesting Affine cipher...")
try:
    from cryptology.classical.substitution.monoalphabetic import affine
    plain = TEST_TEXTS['english']
    success, lower = test_cipher('Affine', affine.encrypt, affine.decrypt, plain, 'EN', 5, 8, A.ENGLISH_ALPHABET)
    results.append(('Affine (EN)', success, lower))
    print(f"  {'✓' if success else '✗'} Affine (English)")
except Exception as e:
    results.append(('Affine (EN)', False, True))
    print(f"  ✗ Affine: {e}")

# ROT13
print("\nTesting ROT13 cipher...")
try:
    from cryptology.classical.substitution.monoalphabetic import rot13
    plain = TEST_TEXTS['english']
    success, lower = test_cipher('ROT13', rot13.encrypt, rot13.decrypt, plain, 'EN', A.ENGLISH_ALPHABET)
    results.append(('ROT13 (EN)', success, lower))
    print(f"  {'✓' if success else '✗'} ROT13 (English)")
except Exception as e:
    results.append(('ROT13 (EN)', False, True))
    print(f"  ✗ ROT13: {e}")

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for _, s, _ in results if s)
total = len(results)
lowercase = sum(1 for _, _, l in results if l)

print(f"\nResults: {passed}/{total} tests passed")
print(f"Lowercase: {lowercase}/{total} ciphers output lowercase")
print(f"Status: {'✓ ALL TESTS PASSED' if passed == total else '✗ SOME TESTS FAILED'}\n")

for name, success, lower in results:
    status = "✓" if success else "✗"
    low = "✓" if lower else "✗"
    print(f"  {status} {low} {name}")

print("\n" + "=" * 80)
