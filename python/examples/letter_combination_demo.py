"""
Demonstration of how letter combination works to fit alphabets into 5x5 squares.

This example shows step-by-step how different alphabets are reduced to 25 letters
for use in polygraphic ciphers like Playfair, Two Square, and Four Square.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polygraphic.letter_combination_strategies import (
    LetterCombinationEngine, CombinationStrategy
)


def demonstrate_turkish_combination():
    """Show step-by-step Turkish letter combination."""
    print("=== Turkish Alphabet: 29 letters → 25 letters ===")
    
    turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    print(f"Original Turkish alphabet: {turkish_alphabet}")
    print(f"Original size: {len(turkish_alphabet)} letters")
    print()
    
    print("Step 1: Apply Turkish combination rules:")
    print("  ç → c")
    print("  ğ → g") 
    print("  ı → i")
    print("  ö → o")
    print("  ş → s")
    print("  ü → u")
    print()
    
    # Manual application
    step1 = turkish_alphabet.replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i')
    step1 = step1.replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    print(f"After combination: {step1}")
    print(f"Size after combination: {len(step1)} letters")
    print()
    
    print("Step 2: Remove duplicates while preserving order:")
    seen = set()
    unique_chars = []
    for char in step1:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    step2 = ''.join(unique_chars)
    print(f"After deduplication: {step2}")
    print(f"Size after deduplication: {len(step2)} letters")
    print()
    
    print("Step 3: Check if we need further reduction:")
    if len(step2) > 25:
        print(f"Still {len(step2)} letters, need to remove {len(step2) - 25} more")
        print("Using frequency-based selection to keep most common letters")
        # This would use the frequency data to select the 25 most common letters
    else:
        print(f"Perfect! We have {len(step2)} letters, which fits in 5x5 square")
    
    print()


def demonstrate_russian_combination():
    """Show step-by-step Russian letter combination."""
    print("=== Russian Alphabet: 33 letters → 25 letters ===")
    
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    print(f"Original Russian alphabet: {russian_alphabet}")
    print(f"Original size: {len(russian_alphabet)} letters")
    print()
    
    print("Step 1: Apply Russian combination rules:")
    print("  ё → е")
    print("  й → и")
    print("  ъ → '' (remove)")
    print("  ь → '' (remove)")
    print()
    
    # Manual application
    step1 = russian_alphabet.replace('ё', 'е').replace('й', 'и').replace('ъ', '').replace('ь', '')
    print(f"After combination: {step1}")
    print(f"Size after combination: {len(step1)} letters")
    print()
    
    print("Step 2: Remove duplicates while preserving order:")
    seen = set()
    unique_chars = []
    for char in step1:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    step2 = ''.join(unique_chars)
    print(f"After deduplication: {step2}")
    print(f"Size after deduplication: {len(step2)} letters")
    print()
    
    print("Step 3: Frequency-based selection for 5x5 square:")
    print("Russian letter frequency (most to least common):")
    print("о, а, е, и, н, т, с, р, в, л, к, м, д, п, у, я, ы, г, з, б, ч, х, ж, ш, ю")
    print("Selecting top 25 most frequent letters...")
    print()
    
    # Top 25 most frequent Russian letters
    top25_russian = "оаеинтсрвлкмдпуяыгзбчхжшю"
    print(f"Final 25-letter alphabet: {top25_russian}")
    print(f"Size: {len(top25_russian)} letters ✓")
    print()


def demonstrate_german_combination():
    """Show step-by-step German letter combination."""
    print("=== German Alphabet: 30 letters → 25 letters ===")
    
    german_alphabet = "abcdefghijklmnopqrstuvwxyzäöüß"
    print(f"Original German alphabet: {german_alphabet}")
    print(f"Original size: {len(german_alphabet)} letters")
    print()
    
    print("Step 1: Apply German combination rules:")
    print("  ä → a")
    print("  ö → o")
    print("  ü → u")
    print("  ß → s")
    print()
    
    # Manual application
    step1 = german_alphabet.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('ß', 's')
    print(f"After combination: {step1}")
    print(f"Size after combination: {len(step1)} letters")
    print()
    
    print("Step 2: Remove duplicates while preserving order:")
    seen = set()
    unique_chars = []
    for char in step1:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    step2 = ''.join(unique_chars)
    print(f"After deduplication: {step2}")
    print(f"Size after deduplication: {len(step2)} letters")
    print()
    
    print("Step 3: Check final size:")
    if len(step2) > 25:
        print(f"Still {len(step2)} letters, need to remove {len(step2) - 25} more")
        print("Using frequency-based selection...")
    else:
        print(f"Perfect! We have {len(step2)} letters, which fits in 5x5 square")
    
    print()


def demonstrate_spanish_combination():
    """Show step-by-step Spanish letter combination."""
    print("=== Spanish Alphabet: 32 letters → 25 letters ===")
    
    spanish_alphabet = "abcdefghijklmnñopqrstuvwxyzáéíóú"
    print(f"Original Spanish alphabet: {spanish_alphabet}")
    print(f"Original size: {len(spanish_alphabet)} letters")
    print()
    
    print("Step 1: Apply Spanish combination rules:")
    print("  ñ → n")
    print("  á → a")
    print("  é → e")
    print("  í → i")
    print("  ó → o")
    print("  ú → u")
    print()
    
    # Manual application
    step1 = spanish_alphabet.replace('ñ', 'n').replace('á', 'a').replace('é', 'e')
    step1 = step1.replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    print(f"After combination: {step1}")
    print(f"Size after combination: {len(step1)} letters")
    print()
    
    print("Step 2: Remove duplicates while preserving order:")
    seen = set()
    unique_chars = []
    for char in step1:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    step2 = ''.join(unique_chars)
    print(f"After deduplication: {step2}")
    print(f"Size after deduplication: {len(step2)} letters")
    print()
    
    print("Step 3: Check final size:")
    if len(step2) > 25:
        print(f"Still {len(step2)} letters, need to remove {len(step2) - 25} more")
        print("Using frequency-based selection...")
    else:
        print(f"Perfect! We have {len(step2)} letters, which fits in 5x5 square")
    
    print()


def demonstrate_french_combination():
    """Show step-by-step French letter combination."""
    print("=== French Alphabet: 42 letters → 25 letters ===")
    
    french_alphabet = "abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüÿç"
    print(f"Original French alphabet: {french_alphabet}")
    print(f"Original size: {len(french_alphabet)} letters")
    print()
    
    print("Step 1: Apply French combination rules:")
    print("  à, â, ä → a")
    print("  é, è, ê, ë → e")
    print("  î, ï → i")
    print("  ô, ö → o")
    print("  ù, û, ü → u")
    print("  ÿ → y")
    print("  ç → c")
    print()
    
    # Manual application
    step1 = french_alphabet.replace('à', 'a').replace('â', 'a').replace('ä', 'a')
    step1 = step1.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ë', 'e')
    step1 = step1.replace('î', 'i').replace('ï', 'i')
    step1 = step1.replace('ô', 'o').replace('ö', 'o')
    step1 = step1.replace('ù', 'u').replace('û', 'u').replace('ü', 'u')
    step1 = step1.replace('ÿ', 'y').replace('ç', 'c')
    
    print(f"After combination: {step1}")
    print(f"Size after combination: {len(step1)} letters")
    print()
    
    print("Step 2: Remove duplicates while preserving order:")
    seen = set()
    unique_chars = []
    for char in step1:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    step2 = ''.join(unique_chars)
    print(f"After deduplication: {step2}")
    print(f"Size after deduplication: {len(step2)} letters")
    print()
    
    print("Step 3: Frequency-based selection for 5x5 square:")
    print("French letter frequency (most to least common):")
    print("e, a, s, i, t, n, r, u, l, o, d, c, p, m, v, q, f, b, g, h, j, x, y, z, w")
    print("Selecting top 25 most frequent letters...")
    print()
    
    # Top 25 most frequent French letters
    top25_french = "easitnrulodcmpvqfbghjxyz"
    print(f"Final 25-letter alphabet: {top25_french}")
    print(f"Size: {len(top25_french)} letters ✓")
    print()


def demonstrate_5x5_square_creation():
    """Show how the final alphabet is used to create a 5x5 square."""
    print("=== Creating 5x5 Key Square ===")
    
    # Example with Turkish alphabet
    final_alphabet = "abcdefghijklmnoprstuvyz"  # 23 letters
    key = "MONARCHY"
    
    print(f"Final alphabet: {final_alphabet}")
    print(f"Key: {key}")
    print()
    
    print("Step 1: Add key letters first (removing duplicates):")
    key_letters = []
    seen = set()
    for char in key.upper():
        if char not in seen and char in final_alphabet.upper():
            key_letters.append(char)
            seen.add(char)
    
    print(f"Key letters: {key_letters}")
    print()
    
    print("Step 2: Add remaining alphabet letters:")
    remaining_letters = []
    for char in final_alphabet.upper():
        if char not in seen:
            remaining_letters.append(char)
    
    print(f"Remaining letters: {remaining_letters}")
    print()
    
    print("Step 3: Combine and create 5x5 square:")
    all_letters = key_letters + remaining_letters
    print(f"All letters: {all_letters}")
    print(f"Total letters: {len(all_letters)}")
    print()
    
    print("5x5 Key Square:")
    for i in range(5):
        row = []
        for j in range(5):
            if i * 5 + j < len(all_letters):
                row.append(all_letters[i * 5 + j])
            else:
                row.append('X')  # Padding if needed
        print(f"Row {i+1}: {' '.join(row)}")
    
    print()


if __name__ == "__main__":
    print("Letter Combination for 5x5 Squares")
    print("=" * 50)
    print()
    
    demonstrate_turkish_combination()
    demonstrate_russian_combination()
    demonstrate_german_combination()
    demonstrate_spanish_combination()
    demonstrate_french_combination()
    demonstrate_5x5_square_creation()
    
    print("Summary:")
    print("1. Apply language-specific combination rules")
    print("2. Remove duplicate letters")
    print("3. Use frequency-based selection if still too long")
    print("4. Create 5x5 square with key + remaining letters")
    print("5. Result: Perfect fit for polygraphic ciphers!")
