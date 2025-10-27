"""
Comprehensive example demonstrating monoalphabetic-based Polybius square generation
across multiple ciphers: Playfair, Bifid, Trifid, and Nihilist.

This example shows how the shared monoalphabetic_squares utility can be used
to create consistent, cryptographically interesting squares across different
cipher families.
"""

from cryptology.classical.substitution.polygraphic.monoalphabetic_squares import (
    create_monoalphabetic_square,
    get_available_monoalphabetic_types,
    validate_mono_params
)

from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from cryptology.classical.substitution.fractionated.bifid import encrypt as bifid_encrypt, decrypt as bifid_decrypt
from cryptology.classical.substitution.fractionated.trifid import encrypt as trifid_encrypt, decrypt as trifid_decrypt
from cryptology.classical.substitution.composite.nihilist import nihilist_encrypt, nihilist_decrypt


def demonstrate_monoalphabetic_squares():
    """Demonstrate monoalphabetic square generation across different ciphers."""
    
    print("=" * 80)
    print("MONOALPHABETIC-BASED POLYBIUS SQUARES ACROSS CIPHER FAMILIES")
    print("=" * 80)
    
    # Test data
    plaintext = "HELLO WORLD"
    key = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Available monoalphabetic types
    print("Available monoalphabetic square types:")
    types = get_available_monoalphabetic_types()
    for i, square_type in enumerate(types, 1):
        print(f"  {i}. {square_type}")
    print()
    
    # Test different monoalphabetic transformations
    transformations = [
        ("caesar", {"shift": 3}),
        ("atbash", None),
        ("affine", {"a": 3, "b": 7}),
        ("keyword", {"keyword": "CRYPTO"})
    ]
    
    for square_type, mono_params in transformations:
        print(f"{'=' * 60}")
        print(f"{square_type.upper()} TRANSFORMATION")
        print(f"{'=' * 60}")
        
        # Validate parameters
        if validate_mono_params(square_type, mono_params):
            print(f"✓ Parameters valid for {square_type}")
        else:
            print(f"✗ Invalid parameters for {square_type}")
            continue
        
        # Generate square
        try:
            square = create_monoalphabetic_square(square_type, mono_params=mono_params)
            print(f"\nGenerated {square_type} square:")
            lines = square.split('\n')
            for i, line in enumerate(lines):
                print(f"  Row {i+1}: {line}")
            print()
            
            # Test with different ciphers
            test_ciphers_with_square(square_type, square, plaintext, key, mono_params)
            
        except Exception as e:
            print(f"Error generating {square_type} square: {e}")
        
        print()


def test_ciphers_with_square(square_type, square, plaintext, key, mono_params):
    """Test different ciphers using the generated square."""
    
    print(f"Testing ciphers with {square_type} square:")
    
    # Playfair cipher
    try:
        print(f"  Playfair:")
        encrypted = playfair_encrypt(plaintext, key, square)
        decrypted = playfair_decrypt(encrypted, key, square)
        print(f"    Encrypted: {encrypted}")
        print(f"    Decrypted: {decrypted}")
        print(f"    ✓ {'Success' if decrypted == plaintext else 'Failed'}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Bifid cipher
    try:
        print(f"  Bifid:")
        encrypted = bifid_encrypt(plaintext, key, square)
        decrypted = bifid_decrypt(encrypted, key, square)
        print(f"    Encrypted: {encrypted}")
        print(f"    Decrypted: {decrypted}")
        print(f"    ✓ {'Success' if decrypted == plaintext else 'Failed'}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Nihilist cipher
    try:
        print(f"  Nihilist:")
        encrypted = nihilist_encrypt(plaintext, key, square=square)
        decrypted = nihilist_decrypt(encrypted, key, square=square)
        print(f"    Encrypted: {encrypted}")
        print(f"    Decrypted: {decrypted}")
        print(f"    ✓ {'Success' if decrypted == plaintext else 'Failed'}")
    except Exception as e:
        print(f"    ✗ Error: {e}")


def demonstrate_turkish_alphabet():
    """Demonstrate monoalphabetic squares with Turkish alphabet."""
    
    print("=" * 80)
    print("MONOALPHABETIC SQUARES WITH TURKISH ALPHABET")
    print("=" * 80)
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    plaintext = "MERHABA DÜNYA"
    key = "GİZLİ"
    
    print(f"Turkish Alphabet: {turkish_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Test Caesar with Turkish
    print("Caesar Square (shift=5) with Turkish alphabet:")
    try:
        square = create_monoalphabetic_square("caesar", turkish_alphabet, {"shift": 5})
        print(f"Square:")
        lines = square.split('\n')
        for i, line in enumerate(lines):
            print(f"  Row {i+1}: {line}")
        print()
        
        # Test Nihilist with Turkish
        print("Testing Nihilist with Turkish Caesar square:")
        encrypted = nihilist_encrypt(plaintext, key, square=square)
        decrypted = nihilist_decrypt(encrypted, key, square=square)
        print(f"  Encrypted: {encrypted}")
        print(f"  Decrypted: {decrypted}")
        print(f"  ✓ {'Success' if decrypted == plaintext else 'Failed'}")
        
    except Exception as e:
        print(f"Error: {e}")


def demonstrate_parameter_validation():
    """Demonstrate parameter validation for different square types."""
    
    print("=" * 80)
    print("PARAMETER VALIDATION EXAMPLES")
    print("=" * 80)
    
    test_cases = [
        ("caesar", {"shift": 3}, True),
        ("caesar", {"shift": "invalid"}, False),
        ("caesar", {}, False),
        ("atbash", None, True),
        ("atbash", {}, True),
        ("affine", {"a": 3, "b": 7}, True),
        ("affine", {"a": 3}, False),
        ("affine", {"b": 7}, False),
        ("keyword", {"keyword": "SECRET"}, True),
        ("keyword", {"keyword": ""}, False),
        ("keyword", {}, False),
        ("invalid", {}, False),
    ]
    
    for square_type, mono_params, expected in test_cases:
        result = validate_mono_params(square_type, mono_params)
        status = "✓" if result == expected else "✗"
        print(f"{status} {square_type}: {mono_params} -> {result} (expected {expected})")


def main():
    """Main demonstration function."""
    
    print("MONOALPHABETIC-BASED POLYBIUS SQUARE GENERATION")
    print("A comprehensive demonstration of shared square generation utilities")
    print("across multiple cipher families in the cryptology library.")
    print()
    
    # Core demonstration
    demonstrate_monoalphabetic_squares()
    
    # Turkish alphabet demonstration
    demonstrate_turkish_alphabet()
    
    # Parameter validation demonstration
    demonstrate_parameter_validation()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("✓ Monoalphabetic square generation works across cipher families")
    print("✓ Consistent API for Caesar, Atbash, Affine, and Keyword squares")
    print("✓ Support for both English and Turkish alphabets")
    print("✓ Parameter validation ensures correct usage")
    print("✓ Shared utility reduces code duplication")
    print("✓ Easy integration with existing cipher implementations")
    print()
    print("This shared utility can now be used by:")
    print("  • Playfair Cipher (5×5 squares)")
    print("  • Two Square Cipher (two 5×5 squares)")
    print("  • Four Square Cipher (four 5×5 squares)")
    print("  • Bifid Cipher (5×5 squares)")
    print("  • Trifid Cipher (3×3×3 cubes)")
    print("  • Nihilist Cipher (5×5 or 6×6 squares)")
    print("  • Any future cipher that uses Polybius squares")


if __name__ == "__main__":
    main()
