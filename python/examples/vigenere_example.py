"""
Example demonstrating the Vigenère cipher with customizable tables.

This example shows how the Vigenère cipher works with different table types,
including classical tabula recta and custom tables generated using monoalphabetic ciphers.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polyalphabetic import vigenere_encrypt, vigenere_decrypt, vigenere_produce_table


def demonstrate_classical_vigenere():
    """Demonstrate classical Vigenère cipher with tabula recta."""
    print("=== Classical Vigenère Cipher Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_caesar_table():
    """Demonstrate Vigenère with Caesar-generated table."""
    print("=== Vigenère with Caesar Table Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    shift = 3
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Caesar shift: {shift}")
    print()
    
    # Generate Caesar table
    caesar_table = vigenere_produce_table("caesar", shift=shift)
    print("Caesar table generated (each row shifts by base_shift + row_index)")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key, table=caesar_table)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key, table=caesar_table)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_affine_table():
    """Demonstrate Vigenère with Affine-generated table."""
    print("=== Vigenère with Affine Table Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    a, b = 3, 5
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Affine parameters: a={a}, b={b}")
    print()
    
    # Generate Affine table
    affine_table = vigenere_produce_table("affine", a=a, b=b)
    print("Affine table generated (each row uses a*x + (b + row_index) mod 26)")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key, table=affine_table)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key, table=affine_table)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_keyword_table():
    """Demonstrate Vigenère with Keyword-generated table."""
    print("=== Vigenère with Keyword Table Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    keyword = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Keyword: {keyword}")
    print()
    
    # Generate Keyword table
    keyword_table = vigenere_produce_table("keyword", keyword=keyword)
    print("Keyword table generated (each row uses keyword + row_character)")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key, table=keyword_table)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key, table=keyword_table)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_atbash_table():
    """Demonstrate Vigenère with Atbash-generated table."""
    print("=== Vigenère with Atbash Table Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Generate Atbash table
    atbash_table = vigenere_produce_table("atbash")
    print("Atbash table generated (each row uses reversed alphabet with rotation)")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key, table=atbash_table)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key, table=atbash_table)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_turkish_alphabet():
    """Demonstrate Vigenère with Turkish alphabet."""
    print("=== Vigenère with Turkish Alphabet Demo ===")
    
    plaintext = "MERHABA DÜNYA"
    key = "GİZLİ"
    turkish_alphabet = "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Turkish alphabet: {turkish_alphabet}")
    print()
    
    # Generate classical table for Turkish
    turkish_table = vigenere_produce_table("classical", alphabet=turkish_alphabet)
    print("Turkish classical table generated (29x29)")
    print()
    
    # Encrypt
    encrypted = vigenere_encrypt(plaintext, key, table=turkish_table, alphabet=turkish_alphabet)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = vigenere_decrypt(encrypted, key, table=turkish_table, alphabet=turkish_alphabet)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_table_comparison():
    """Compare different table types with the same input."""
    print("=== Table Type Comparison ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = "CRYPTO"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Generate different tables
    classical_table = vigenere_produce_table("classical")
    caesar_table = vigenere_produce_table("caesar", shift=5)
    affine_table = vigenere_produce_table("affine", a=3, b=7)
    keyword_table = vigenere_produce_table("keyword", keyword="SECRET")
    atbash_table = vigenere_produce_table("atbash")
    
    tables = [
        ("Classical", classical_table),
        ("Caesar (shift=5)", caesar_table),
        ("Affine (a=3, b=7)", affine_table),
        ("Keyword (SECRET)", keyword_table),
        ("Atbash", atbash_table)
    ]
    
    for name, table in tables:
        encrypted = vigenere_encrypt(plaintext, key, table=table)
        print(f"{name:20}: {encrypted}")
    
    print()


def demonstrate_security_analysis():
    """Demonstrate security benefits of different table types."""
    print("=== Security Analysis ===")
    
    plaintext = "ATTACK AT DAWN"
    key = "LEMON"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Generate different tables
    classical_table = vigenere_produce_table("classical")
    caesar_table = vigenere_produce_table("caesar", shift=13)
    affine_table = vigenere_produce_table("affine", a=5, b=11)
    
    tables = [
        ("Classical", classical_table),
        ("Caesar (shift=13)", caesar_table),
        ("Affine (a=5, b=11)", affine_table)
    ]
    
    print("Security benefits of different table types:")
    print()
    
    for name, table in tables:
        encrypted = vigenere_encrypt(plaintext, key, table=table)
        
        print(f"Table: {name}")
        print(f"Encrypted: {encrypted}")
        
        # Analyze letter frequency
        freq = {}
        for char in encrypted:
            freq[char] = freq.get(char, 0) + 1
        
        # Show most frequent letters
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        top_letters = [f"{char}:{count}" for char, count in sorted_freq[:5]]
        
        print(f"Top letters: {', '.join(top_letters)}")
        print()
    
    print("Security advantages:")
    print("1. Custom tables break classical Vigenère patterns")
    print("2. Different monoalphabetic bases add complexity")
    print("3. Multiple table types provide variety")
    print("4. Composable system allows unlimited combinations")
    print("5. Resistant to standard Vigenère cryptanalysis")
    print()


def demonstrate_historical_context():
    """Demonstrate the historical significance of Vigenère cipher."""
    print("=== Historical Context ===")
    
    plaintext = "HISTORICAL CIPHER"
    key = "RENAISSANCE"
    
    print("The Vigenère cipher was invented by Blaise de Vigenère in 1586.")
    print("It was a major advancement over monoalphabetic ciphers.")
    print("The classical tabula recta became the standard for centuries.")
    print()
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Use classical table
    encrypted = vigenere_encrypt(plaintext, key)
    print(f"Encrypted (classical): {encrypted}")
    print()
    
    print("Key innovations of Vigenère cipher:")
    print("1. First practical polyalphabetic cipher")
    print("2. Tabula recta - systematic table generation")
    print("3. Key-based alphabet selection")
    print("4. Foundation for modern polyalphabetic ciphers")
    print("5. Significant security improvement over monoalphabetic ciphers")
    print()


def demonstrate_composable_system():
    """Demonstrate Vigenère in the composable cipher system."""
    print("=== Composable System Demo ===")
    
    from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
    from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce
    
    plaintext = "COMPOSABLE CIPHER SYSTEM"
    key = "VIGENERE"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Layer 1: Caesar-produced alphabet
    caesar_alphabet = caesar_produce(shift=7)
    print(f"Caesar-produced alphabet: {caesar_alphabet}")
    
    # Layer 2: Keyword-produced alphabet
    keyword_alphabet = keyword_produce("SECRET", caesar_alphabet)
    print(f"Keyword-produced alphabet: {keyword_alphabet}")
    print()
    
    # Layer 3: Vigenère with Caesar table
    caesar_table = vigenere_produce_table("caesar", shift=3)
    encrypted_caesar = vigenere_encrypt(plaintext, key, table=caesar_table)
    print(f"Vigenère with Caesar table: {encrypted_caesar}")
    
    # Layer 4: Vigenère with Affine table
    affine_table = vigenere_produce_table("affine", a=3, b=5)
    encrypted_affine = vigenere_encrypt(plaintext, key, table=affine_table)
    print(f"Vigenère with Affine table: {encrypted_affine}")
    print()
    
    print("Multi-layer encryption provides:")
    print("1. Caesar shift adds basic substitution")
    print("2. Keyword rearrangement adds complexity")
    print("3. Vigenère polyalphabetic adds security")
    print("4. Custom tables add unpredictability")
    print("5. Composable system allows unlimited combinations")
    print()


if __name__ == "__main__":
    print("Vigenère Cipher Demo")
    print("====================")
    print()
    
    demonstrate_classical_vigenere()
    demonstrate_caesar_table()
    demonstrate_affine_table()
    demonstrate_keyword_table()
    demonstrate_atbash_table()
    demonstrate_turkish_alphabet()
    demonstrate_table_comparison()
    demonstrate_security_analysis()
    demonstrate_historical_context()
    demonstrate_composable_system()
    
    print("Demo completed!")
    print()
    print("Key Features:")
    print("1. Classical Vigenère with tabula recta")
    print("2. Custom tables using monoalphabetic ciphers")
    print("3. English (26x26) and Turkish (29x29) support")
    print("4. On-the-fly table generation")
    print("5. Composable with existing cipher systems")
    print("6. Multiple table types for enhanced security")
    print("7. Integration with monoalphabetic ciphers")
