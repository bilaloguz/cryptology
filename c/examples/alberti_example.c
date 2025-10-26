/**
 * @file alberti_example.c
 * @brief Example demonstrating the Alberti cipher
 * 
 * This example shows how the Alberti cipher works with its rotating disk system,
 * various rotation strategies, and integration with the composable cipher system.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Include Alberti cipher header
#include "cryptology/classical/substitution/polyalphabetic/alberti.h"

// Include monoalphabetic cipher headers for composable system
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"

#define MAX_BUFFER_SIZE 1024
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"

void demonstrate_basic_alberti() {
    printf("=== Basic Alberti Cipher Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *rotation_strategy = "every_3";
    int initial_position = 0;
    int rotation_amount = 1;
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Rotation strategy: %s\n", rotation_strategy);
    printf("Initial position: %d\n", initial_position);
    printf("Rotation amount: %d\n", rotation_amount);
    printf("\n");
    
    // Encrypt
    if (alberti_encrypt(plaintext, NULL, NULL, initial_position, rotation_strategy, rotation_amount, 
                       encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (alberti_decrypt(encrypted, NULL, NULL, initial_position, rotation_strategy, rotation_amount,
                           decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_rotation_strategies() {
    printf("=== Rotation Strategies Demo ===\n");
    
    const char *plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    const char *strategies[] = {"every_3", "every_5", "on_vowel", "on_space", "on_consonant", "fibonacci"};
    int num_strategies = sizeof(strategies) / sizeof(strategies[0]);
    
    printf("Plaintext: %s\n", plaintext);
    printf("\n");
    
    for (int i = 0; i < num_strategies; i++) {
        char encrypted[MAX_BUFFER_SIZE];
        char decrypted[MAX_BUFFER_SIZE];
        
        printf("Strategy: %s\n", strategies[i]);
        
        if (alberti_encrypt(plaintext, NULL, NULL, 0, strategies[i], 1, 
                           encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            if (alberti_decrypt(encrypted, NULL, NULL, 0, strategies[i], 1,
                               decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: ✓\n");
            } else {
                printf("Error: Failed to decrypt\n");
            }
        } else {
            printf("Error: Failed to encrypt\n");
        }
        printf("\n");
    }
}

void demonstrate_custom_alphabets() {
    printf("=== Custom Alphabets Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *outer_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char *inner_alphabet = "ZYXWVUTSRQPONMLKJIHGFEDCBA";  // Reversed alphabet
    const char *rotation_strategy = "every_2";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Outer alphabet: %s\n", outer_alphabet);
    printf("Inner alphabet: %s\n", inner_alphabet);
    printf("Rotation strategy: %s\n", rotation_strategy);
    printf("\n");
    
    // Encrypt
    if (alberti_encrypt(plaintext, outer_alphabet, inner_alphabet, 0, rotation_strategy, 1,
                       encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (alberti_decrypt(encrypted, outer_alphabet, inner_alphabet, 0, rotation_strategy, 1,
                           decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_turkish_alphabet() {
    printf("=== Turkish Alphabet Demo ===\n");
    
    const char *plaintext = "MERHABA DÜNYA";
    const char *rotation_strategy = "every_4";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Turkish alphabet: %s\n", TURKISH_ALPHABET);
    printf("Rotation strategy: %s\n", rotation_strategy);
    printf("\n");
    
    // Encrypt
    if (alberti_encrypt(plaintext, TURKISH_ALPHABET, NULL, 0, rotation_strategy, 1,
                       encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (alberti_decrypt(encrypted, TURKISH_ALPHABET, NULL, 0, rotation_strategy, 1,
                           decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_composable_system() {
    printf("=== Composable System Demo ===\n");
    
    const char *plaintext = "COMPOSABLE CIPHER SYSTEM";
    char caesar_alphabet[MAX_BUFFER_SIZE];
    char keyword_alphabet[MAX_BUFFER_SIZE];
    char encrypted_caesar[MAX_BUFFER_SIZE];
    char encrypted_keyword[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("\n");
    
    // Layer 1: Caesar-produced alphabet
    if (caesar_produce_alphabet(5, DEFAULT_ALPHABET, caesar_alphabet, sizeof(caesar_alphabet)) == 0) {
        printf("Caesar-produced alphabet: %s\n", caesar_alphabet);
        
        // Layer 2: Keyword-produced alphabet
        if (keyword_produce_alphabet("SECRET", caesar_alphabet, keyword_alphabet, sizeof(keyword_alphabet)) == 0) {
            printf("Keyword-produced alphabet: %s\n", keyword_alphabet);
            printf("\n");
            
            // Use Caesar alphabet as inner alphabet
            if (alberti_encrypt(plaintext, NULL, caesar_alphabet, 0, "every_3", 1,
                               encrypted_caesar, sizeof(encrypted_caesar)) == 0) {
                printf("Alberti with Caesar alphabet: %s\n", encrypted_caesar);
            } else {
                printf("Error: Failed to encrypt with Caesar alphabet\n");
            }
            
            // Use keyword alphabet as inner alphabet
            if (alberti_encrypt(plaintext, NULL, keyword_alphabet, 0, "fibonacci", 1,
                               encrypted_keyword, sizeof(encrypted_keyword)) == 0) {
                printf("Alberti with keyword alphabet: %s\n", encrypted_keyword);
            } else {
                printf("Error: Failed to encrypt with keyword alphabet\n");
            }
        } else {
            printf("Error: Failed to produce keyword alphabet\n");
        }
    } else {
        printf("Error: Failed to produce Caesar alphabet\n");
    }
    printf("\n");
    
    printf("Multi-layer encryption provides:\n");
    printf("1. Caesar shift adds basic substitution\n");
    printf("2. Keyword rearrangement adds complexity\n");
    printf("3. Alberti rotation adds polyalphabetic security\n");
    printf("4. Multiple rotation strategies add unpredictability\n");
    printf("\n");
}

void demonstrate_historical_context() {
    printf("=== Historical Context ===\n");
    
    const char *plaintext = "HISTORICAL CIPHER";
    char encrypted[MAX_BUFFER_SIZE];
    
    printf("The Alberti cipher was invented by Leon Battista Alberti in 1467.\n");
    printf("It was the FIRST polyalphabetic cipher in history!\n");
    printf("This revolutionized cryptography by introducing the concept of\n");
    printf("using multiple alphabets for encryption.\n");
    printf("\n");
    
    printf("Plaintext: %s\n", plaintext);
    
    // Simulate historical usage with simple rotation
    if (alberti_encrypt(plaintext, NULL, NULL, 3, "every_5", 2,
                       encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted (historical style): %s\n", encrypted);
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
    
    printf("Key innovations of Alberti cipher:\n");
    printf("1. First polyalphabetic substitution\n");
    printf("2. Rotating disk mechanism\n");
    printf("3. Multiple alphabet concept\n");
    printf("4. Foundation for all later polyalphabetic ciphers\n");
    printf("5. Revolutionary security improvement over monoalphabetic ciphers\n");
    printf("\n");
}

void demonstrate_security_analysis() {
    printf("=== Security Analysis ===\n");
    
    const char *plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    const char *strategies[] = {"every_3", "every_5", "on_vowel", "fibonacci"};
    int num_strategies = sizeof(strategies) / sizeof(strategies[0]);
    
    printf("Plaintext: %s\n", plaintext);
    printf("\n");
    
    printf("Security benefits of different rotation strategies:\n");
    printf("\n");
    
    for (int i = 0; i < num_strategies; i++) {
        char encrypted[MAX_BUFFER_SIZE];
        
        printf("Strategy: %s\n", strategies[i]);
        
        if (alberti_encrypt(plaintext, NULL, NULL, 0, strategies[i], 1,
                           encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Analyze letter frequency
            int freq[26] = {0};
            for (int j = 0; encrypted[j] != '\0'; j++) {
                if (encrypted[j] >= 'A' && encrypted[j] <= 'Z') {
                    freq[encrypted[j] - 'A']++;
                }
            }
            
            // Show most frequent letters
            printf("Top letters: ");
            for (int k = 0; k < 5; k++) {
                int max_freq = 0;
                int max_char = 0;
                for (int l = 0; l < 26; l++) {
                    if (freq[l] > max_freq) {
                        max_freq = freq[l];
                        max_char = l;
                    }
                }
                if (max_freq > 0) {
                    printf("%c:%d ", 'A' + max_char, max_freq);
                    freq[max_char] = 0;  // Remove from consideration
                }
            }
            printf("\n");
        } else {
            printf("Error: Failed to encrypt\n");
        }
        printf("\n");
    }
    
    printf("Security advantages:\n");
    printf("1. Multiple alphabets break frequency analysis\n");
    printf("2. Rotation strategies add unpredictability\n");
    printf("3. Custom alphabets provide additional security\n");
    printf("4. Composable with other cipher systems\n");
    printf("5. Resistant to simple substitution attacks\n");
    printf("\n");
}

int main() {
    printf("Alberti Cipher Demo\n");
    printf("==================\n\n");
    
    demonstrate_basic_alberti();
    demonstrate_rotation_strategies();
    demonstrate_custom_alphabets();
    demonstrate_turkish_alphabet();
    demonstrate_composable_system();
    demonstrate_historical_context();
    demonstrate_security_analysis();
    
    printf("Demo completed!\n\n");
    printf("Key Features:\n");
    printf("1. First polyalphabetic cipher in history\n");
    printf("2. Rotating disk mechanism with multiple strategies\n");
    printf("3. Custom alphabet support for any language\n");
    printf("4. Composable with monoalphabetic ciphers\n");
    printf("5. Complex rotation patterns for enhanced security\n");
    printf("6. Deterministic scrambled alphabet generation\n");
    printf("7. Integration with existing cipher systems\n");
    
    return 0;
}
