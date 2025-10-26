#!/usr/bin/env python3
"""
Custom Pairing Strategy Analysis for Porta Cipher
Analyzes security implications and effectiveness of different pairing approaches
"""

from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs, porta_encrypt, porta_decrypt
import string

def analyze_pairing_strategies():
    """Analyze different custom pairing strategies"""
    
    print("=" * 80)
    print("CUSTOM PAIRING STRATEGY ANALYSIS FOR PORTA CIPHER")
    print("=" * 80)
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    test_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    test_key = "SECRET"
    
    strategies = {
        "Frequency-Based (Common ↔ Rare)": [
            ('E', 'Z'), ('T', 'Q'), ('A', 'X'), ('O', 'J'), ('I', 'K'),
            ('N', 'V'), ('S', 'B'), ('H', 'Y'), ('R', 'W'), ('D', 'F')
        ],
        "Symmetric (Mirror Positions)": [
            ('A', 'Z'), ('B', 'Y'), ('C', 'X'), ('D', 'W'), ('E', 'V'),
            ('F', 'U'), ('G', 'T'), ('H', 'S'), ('I', 'R'), ('J', 'Q'),
            ('K', 'P'), ('L', 'O'), ('M', 'N')
        ],
        "Caesar-Shifted (+3)": [
            ('A', 'D'), ('B', 'E'), ('C', 'F'), ('G', 'J'), ('H', 'K'),
            ('I', 'L'), ('M', 'P'), ('N', 'Q'), ('O', 'R'), ('S', 'V'),
            ('T', 'W'), ('U', 'X'), ('Y', 'Z')
        ],
        "Vowel-Consonant": [
            ('A', 'B'), ('E', 'C'), ('I', 'D'), ('O', 'F'), ('U', 'G')
        ],
        "Prime Position": [
            ('A', 'C'), ('B', 'E'), ('D', 'G'), ('F', 'I'), ('H', 'K')
        ],
        "Keyboard-Based": [
            ('Q', 'W'), ('E', 'R'), ('T', 'Y'), ('U', 'I'), ('O', 'P'),
            ('A', 'S'), ('D', 'F'), ('G', 'H'), ('J', 'K'), ('L', 'Z')
        ]
    }
    
    results = {}
    
    for strategy_name, pairs in strategies.items():
        print(f"\n{strategy_name}")
        print("-" * 60)
        
        # Generate pairs
        try:
            generated_pairs = porta_produce_pairs('custom', alphabet, pairs)
            print(f"Pairs: {generated_pairs}")
            
            # Encrypt and decrypt
            encrypted = porta_encrypt(test_text, test_key, alphabet, generated_pairs)
            decrypted = porta_decrypt(encrypted, test_key, alphabet, generated_pairs)
            
            # Calculate statistics
            total_chars = len([c for c in test_text if c.isalpha()])
            changed_chars = sum(1 for i, c in enumerate(test_text) if c.isalpha() and encrypted[i] != c)
            unchanged_chars = total_chars - changed_chars
            
            change_rate = (changed_chars / total_chars) * 100 if total_chars > 0 else 0
            
            print(f"Original: {test_text}")
            print(f"Encrypted: {encrypted}")
            print(f"Decrypted: {decrypted}")
            print(f"Success: {test_text == decrypted}")
            print(f"Characters changed: {changed_chars}/{total_chars} ({change_rate:.1f}%)")
            
            results[strategy_name] = {
                'pairs': generated_pairs,
                'encrypted': encrypted,
                'change_rate': change_rate,
                'success': test_text == decrypted
            }
            
        except Exception as e:
            print(f"Error: {e}")
            results[strategy_name] = {'error': str(e)}
    
    # Security Analysis
    print("\n" + "=" * 80)
    print("SECURITY ANALYSIS")
    print("=" * 80)
    
    print("\n1. FREQUENCY ANALYSIS RESISTANCE")
    print("-" * 40)
    print("Frequency-based pairs (Common ↔ Rare) provide the best resistance")
    print("to frequency analysis attacks because:")
    print("• Most common letters (E, T, A, O, I) are paired with rare letters (Z, Q, X, J, K)")
    print("• This disrupts natural letter frequency patterns")
    print("• Makes statistical analysis much more difficult")
    
    print("\n2. PATTERN RECOGNITION RESISTANCE")
    print("-" * 40)
    print("Symmetric pairs (A-Z, B-Y, etc.) are vulnerable because:")
    print("• They follow a predictable mathematical pattern")
    print("• Easy to reverse-engineer if discovered")
    print("• Should be avoided for security-critical applications")
    
    print("\n3. KEYBOARD-BASED PAIRS")
    print("-" * 40)
    print("Keyboard-based pairs have mixed security:")
    print("• Good: Adjacent keys are not obviously related")
    print("• Bad: If attacker knows keyboard layout, pairs become predictable")
    print("• Moderate security for casual use")
    
    print("\n4. MATHEMATICAL PATTERN PAIRS")
    print("-" * 40)
    print("Caesar-shifted and prime position pairs:")
    print("• Vulnerable to pattern recognition")
    print("• Easy to reverse-engineer")
    print("• Not recommended for security applications")
    
    print("\n5. RECOMMENDED STRATEGIES")
    print("-" * 40)
    print("For maximum security, use:")
    print("• Frequency-based pairs (Common ↔ Rare)")
    print("• Randomly generated pairs")
    print("• Pairs that don't follow obvious patterns")
    print("• Avoid mathematical relationships between paired letters")
    
    # Change Rate Analysis
    print("\n" + "=" * 80)
    print("CHANGE RATE ANALYSIS")
    print("=" * 80)
    
    print("\nStrategy Change Rates:")
    for strategy_name, result in results.items():
        if 'change_rate' in result:
            print(f"{strategy_name}: {result['change_rate']:.1f}%")
    
    print("\nHigher change rates generally indicate better encryption strength.")
    print("However, the quality of the pairing strategy is more important than")
    print("the raw change rate.")
    
    # Practical Recommendations
    print("\n" + "=" * 80)
    print("PRACTICAL RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1. FOR MAXIMUM SECURITY:")
    print("   • Use frequency-based pairs (Common ↔ Rare)")
    print("   • Generate pairs randomly")
    print("   • Avoid predictable patterns")
    print("   • Use long, random keys")
    
    print("\n2. FOR EDUCATIONAL PURPOSES:")
    print("   • Any pairing strategy demonstrates the concept")
    print("   • Symmetric pairs are easy to understand")
    print("   • Mathematical patterns show the relationship to other ciphers")
    
    print("\n3. FOR PRACTICAL USE:")
    print("   • Frequency-based pairs provide good security")
    print("   • Avoid patterns that are easy to guess")
    print("   • Consider the threat model")
    print("   • Combine with other security measures")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    analyze_pairing_strategies()
