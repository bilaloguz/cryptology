/**
 * @file porta_example.c
 * @brief Example usage of the enhanced Porta cipher with custom pairing support
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cryptology/classical/substitution/polyalphabetic/porta.h"

#define MAX_BUFFER_SIZE 256
#define MAX_PAIRS 20

int main() {
    printf("======================================================================\n");
    printf("ENHANCED PORTA CIPHER EXAMPLE - CUSTOM PAIRING SUPPORT\n");
    printf("======================================================================\n");
    
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    char key[MAX_BUFFER_SIZE];
    porta_pair_t pairs[MAX_PAIRS];
    size_t pairs_count;
    
    // Example 1: Default pairs
    printf("\n1. Default Alphabet Pairs\n");
    printf("--------------------------------------------------\n");
    
    if (porta_produce_pairs("default", NULL, pairs, &pairs_count, NULL, 0) == 0) {
        printf("Default pairs (first 5): ");
        for (size_t i = 0; i < 5 && i < pairs_count; i++) {
            printf("(%c,%c) ", pairs[i].first, pairs[i].second);
        }
        printf("\nTotal pairs: %zu\n", pairs_count);
        
        const char* plaintext = "HELLO";
        const char* key_str = "KEY";
        
        if (porta_encrypt(plaintext, key_str, NULL, pairs, pairs_count, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext: %s\n", plaintext);
            printf("Encrypted: %s\n", encrypted);
            
            if (porta_decrypt(encrypted, key_str, NULL, pairs, pairs_count, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: %s\n", strcmp(plaintext, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 2: Turkish alphabet pairs
    printf("\n2. Turkish Alphabet Pairs\n");
    printf("--------------------------------------------------\n");
    
    const char* turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ";
    printf("Turkish alphabet: %s\n", turkish_alphabet);
    
    if (porta_produce_pairs("turkish", turkish_alphabet, pairs, &pairs_count, NULL, 0) == 0) {
        printf("Turkish pairs: ");
        for (size_t i = 0; i < pairs_count; i++) {
            printf("(%c,%c) ", pairs[i].first, pairs[i].second);
        }
        printf("\nTotal Turkish pairs: %zu\n", pairs_count);
        
        const char* turkish_text = "MERHABA";
        const char* key_str = "A";
        
        if (porta_encrypt(turkish_text, key_str, turkish_alphabet, pairs, pairs_count, encrypted, sizeof(encrypted)) == 0) {
            printf("Turkish text: %s\n", turkish_text);
            printf("Encrypted: %s\n", encrypted);
            
            if (porta_decrypt(encrypted, key_str, turkish_alphabet, pairs, pairs_count, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: %s\n", strcmp(turkish_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 3: Custom user-defined pairs
    printf("\n3. Custom User-Defined Pairs\n");
    printf("--------------------------------------------------\n");
    
    porta_pair_t custom_pairs[] = {
        {'A', 'Z'}, {'B', 'Y'}, {'C', 'X'}, {'D', 'W'}, {'E', 'V'}
    };
    size_t custom_pairs_count = sizeof(custom_pairs) / sizeof(custom_pairs[0]);
    
    printf("Custom pairs: ");
    for (size_t i = 0; i < custom_pairs_count; i++) {
        printf("(%c,%c) ", custom_pairs[i].first, custom_pairs[i].second);
    }
    printf("\n");
    
    if (porta_produce_pairs("custom", NULL, pairs, &pairs_count, custom_pairs, custom_pairs_count) == 0) {
        const char* plaintext = "ABCDE";
        const char* key_str = "ABCDE";
        
        if (porta_encrypt(plaintext, key_str, NULL, pairs, pairs_count, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext: %s\n", plaintext);
            printf("Encrypted: %s\n", encrypted);
            
            if (porta_decrypt(encrypted, key_str, NULL, pairs, pairs_count, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: %s\n", strcmp(plaintext, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 4: Balanced pairs
    printf("\n4. Balanced Alphabet Pairs\n");
    printf("--------------------------------------------------\n");
    
    const char* alphabet = "ABCDEFGHIJKL";  // 12 letters
    printf("Alphabet: %s\n", alphabet);
    
    if (porta_produce_pairs("balanced", alphabet, pairs, &pairs_count, NULL, 0) == 0) {
        printf("Balanced pairs: ");
        for (size_t i = 0; i < pairs_count; i++) {
            printf("(%c,%c) ", pairs[i].first, pairs[i].second);
        }
        printf("\n");
        
        const char* plaintext = "ABC";
        const char* key_str = "ABC";
        
        if (porta_encrypt(plaintext, key_str, alphabet, pairs, pairs_count, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext: %s\n", plaintext);
            printf("Encrypted: %s\n", encrypted);
            
            if (porta_decrypt(encrypted, key_str, alphabet, pairs, pairs_count, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: %s\n", strcmp(plaintext, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 5: Self-reciprocal property
    printf("\n5. Self-Reciprocal Property\n");
    printf("--------------------------------------------------\n");
    
    const char* plaintext = "SECRET MESSAGE";
    const char* key_str = "PORTACIPHER";
    
    if (porta_encrypt(plaintext, key_str, NULL, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("Plaintext: %s\n", plaintext);
        printf("Encrypted: %s\n", encrypted);
        
        // Demonstrate self-reciprocal property
        char encrypted_again[MAX_BUFFER_SIZE];
        if (porta_encrypt(encrypted, key_str, NULL, NULL, 0, encrypted_again, sizeof(encrypted_again)) == 0) {
            printf("Encrypt encrypted text: %s\n", encrypted_again);
            printf("Self-reciprocal: %s\n", strcmp(encrypted_again, plaintext) == 0 ? "YES" : "NO");
        }
    }
    
    // Example 6: Random key generation
    printf("\n6. Random Key Generation\n");
    printf("--------------------------------------------------\n");
    
    const char* random_text = "RANDOM KEY EXAMPLE";
    
    // Generate random key
    if (porta_generate_random_key(10, NULL, key, sizeof(key)) == 0) {
        printf("Random key (length 10): %s\n", key);
        
        if (porta_encrypt(random_text, key, NULL, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext: %s\n", random_text);
            printf("Encrypted: %s\n", encrypted);
            
            if (porta_decrypt(encrypted, key, NULL, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
                printf("Success: %s\n", strcmp(random_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 7: Encrypt with random key
    printf("\n7. Encrypt with Random Key\n");
    printf("--------------------------------------------------\n");
    
    const char* confidential_text = "CONFIDENTIAL MESSAGE";
    
    if (porta_encrypt_with_random_key(confidential_text, NULL, NULL, 0, 0,
                                     encrypted, sizeof(encrypted),
                                     key, sizeof(key)) == 0) {
        printf("Plaintext: %s\n", confidential_text);
        printf("Generated Key: %s\n", key);
        printf("Encrypted: %s\n", encrypted);
        
        if (porta_decrypt(encrypted, key, NULL, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
            printf("Success: %s\n", strcmp(confidential_text, decrypted) == 0 ? "YES" : "NO");
        }
    }
    
    // Example 8: Error handling
    printf("\n8. Error Handling\n");
    printf("--------------------------------------------------\n");
    
    // Test invalid key
    if (porta_encrypt("HELLO", "123", NULL, NULL, 0, encrypted, sizeof(encrypted)) == -1) {
        printf("Invalid key error: Correctly rejected non-alphabetic key\n");
    }
    
    // Test empty key
    if (porta_encrypt("HELLO", "", NULL, NULL, 0, encrypted, sizeof(encrypted)) == -1) {
        printf("Empty key error: Correctly rejected empty key\n");
    }
    
    // Test invalid pair type
    if (porta_produce_pairs("invalid", NULL, pairs, &pairs_count, NULL, 0) == -1) {
        printf("Invalid pair type error: Correctly rejected invalid pair type\n");
    }
    
    // Test missing custom pairs
    if (porta_produce_pairs("custom", NULL, pairs, &pairs_count, NULL, 0) == -1) {
        printf("Missing custom pairs error: Correctly rejected missing custom pairs\n");
    }
    
    printf("\n======================================================================\n");
    printf("ENHANCED PORTA CIPHER EXAMPLE COMPLETED\n");
    printf("======================================================================\n");
    
    return 0;
}
