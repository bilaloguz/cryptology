/**
 * @file gronsfeld_example.c
 * @brief Example usage of the Gronsfeld cipher
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cryptology/classical/substitution/polyalphabetic/gronsfeld.h"

#define MAX_BUFFER_SIZE 256

int main() {
    printf("============================================================\n");
    printf("GRONSFELD CIPHER EXAMPLE\n");
    printf("============================================================\n");
    
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    char key[MAX_BUFFER_SIZE];
    char** table = NULL;
    size_t table_size;
    
    // Example 1: Basic encryption/decryption
    printf("\n1. Basic Encryption/Decryption\n");
    printf("----------------------------------------\n");
    
    const char* plaintext = "HELLO WORLD";
    const char* numeric_key = "12312";
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key:       %s\n", numeric_key);
    
    if (gronsfeld_encrypt(plaintext, numeric_key, NULL, NULL, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (gronsfeld_decrypt(encrypted, numeric_key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
            printf("Success:   %s\n", strcmp(plaintext, decrypted) == 0 ? "YES" : "NO");
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    // Example 2: Key repetition for longer messages
    printf("\n2. Key Repetition\n");
    printf("----------------------------------------\n");
    
    const char* long_text = "THIS IS A LONG MESSAGE THAT REQUIRES KEY REPETITION";
    const char* short_key = "123";
    
    printf("Text:      %s\n", long_text);
    printf("Key:       %s\n", short_key);
    
    if (gronsfeld_encrypt(long_text, short_key, NULL, NULL, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (gronsfeld_decrypt(encrypted, short_key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
            printf("Success:   %s\n", strcmp(long_text, decrypted) == 0 ? "YES" : "NO");
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    // Example 3: Custom table generation
    printf("\n3. Custom Table Generation\n");
    printf("----------------------------------------\n");
    
    const char* test_text = "SECRET MESSAGE";
    const char* test_key = "12345";
    
    // Classical table
    printf("Classical Table:\n");
    if (gronsfeld_produce_table("classical", NULL, &table, &table_size) == 0) {
        if (gronsfeld_encrypt(test_text, test_key, &table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, test_key, &table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
                printf("  Success:    %s\n", strcmp(test_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
        
        // Cleanup table
        for (size_t i = 0; i < table_size; i++) {
            free(table[i]);
        }
        free(table);
        table = NULL;
    }
    
    // Caesar-based table
    printf("\nCaesar Table (shift=5):\n");
    if (gronsfeld_produce_table("caesar", NULL, &table, &table_size, 5) == 0) {
        if (gronsfeld_encrypt(test_text, test_key, &table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, test_key, &table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
                printf("  Success:    %s\n", strcmp(test_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
        
        // Cleanup table
        for (size_t i = 0; i < table_size; i++) {
            free(table[i]);
        }
        free(table);
        table = NULL;
    }
    
    // Affine-based table
    printf("\nAffine Table (a=5, b=7):\n");
    if (gronsfeld_produce_table("affine", NULL, &table, &table_size, 5, 7) == 0) {
        if (gronsfeld_encrypt(test_text, test_key, &table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, test_key, &table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
                printf("  Success:    %s\n", strcmp(test_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
        
        // Cleanup table
        for (size_t i = 0; i < table_size; i++) {
            free(table[i]);
        }
        free(table);
        table = NULL;
    }
    
    // Keyword-based table
    printf("\nKeyword Table (keyword=SECRET):\n");
    if (gronsfeld_produce_table("keyword", NULL, &table, &table_size, "SECRET") == 0) {
        if (gronsfeld_encrypt(test_text, test_key, &table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, test_key, &table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
                printf("  Success:    %s\n", strcmp(test_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
        
        // Cleanup table
        for (size_t i = 0; i < table_size; i++) {
            free(table[i]);
        }
        free(table);
        table = NULL;
    }
    
    // Atbash-based table
    printf("\nAtbash Table:\n");
    if (gronsfeld_produce_table("atbash", NULL, &table, &table_size) == 0) {
        if (gronsfeld_encrypt(test_text, test_key, &table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, test_key, &table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
                printf("  Success:    %s\n", strcmp(test_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
        
        // Cleanup table
        for (size_t i = 0; i < table_size; i++) {
            free(table[i]);
        }
        free(table);
        table = NULL;
    }
    
    // Example 4: Random key generation
    printf("\n4. Random Key Generation\n");
    printf("----------------------------------------\n");
    
    const char* random_text = "RANDOM KEY EXAMPLE";
    
    // Generate random key
    if (gronsfeld_generate_random_numeric_key(10, key, sizeof(key)) == 0) {
        printf("Random key (length 10): %s\n", key);
        
        if (gronsfeld_encrypt(random_text, key, NULL, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext:  %s\n", random_text);
            printf("Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
                printf("Success:    %s\n", strcmp(random_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Generate key for specific text
    if (gronsfeld_generate_numeric_key_for_text(random_text, key, sizeof(key)) == 0) {
        printf("\nAuto-generated key: %s\n", key);
        
        if (gronsfeld_encrypt(random_text, key, NULL, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext:  %s\n", random_text);
            printf("Encrypted:  %s\n", encrypted);
            
            if (gronsfeld_decrypt(encrypted, key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
                printf("Success:    %s\n", strcmp(random_text, decrypted) == 0 ? "YES" : "NO");
            }
        }
    }
    
    // Example 5: Encrypt with random key (returns both ciphertext and key)
    printf("\n5. Encrypt with Random Key\n");
    printf("----------------------------------------\n");
    
    const char* confidential_text = "CONFIDENTIAL MESSAGE";
    
    if (gronsfeld_encrypt_with_random_key(confidential_text, NULL, NULL, 0,
                                         encrypted, sizeof(encrypted),
                                         key, sizeof(key)) == 0) {
        printf("Plaintext:     %s\n", confidential_text);
        printf("Generated Key: %s\n", key);
        printf("Encrypted:     %s\n", encrypted);
        
        if (gronsfeld_decrypt(encrypted, key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:     %s\n", decrypted);
            printf("Success:       %s\n", strcmp(confidential_text, decrypted) == 0 ? "YES" : "NO");
        }
    }
    
    // Example 6: Turkish alphabet support
    printf("\n6. Turkish Alphabet Support\n");
    printf("----------------------------------------\n");
    
    const char* turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ";
    const char* turkish_text = "MERHABA DÜNYA";
    const char* turkish_key = "12312";
    
    printf("Turkish Alphabet: %s\n", turkish_alphabet);
    printf("Turkish Text:     %s\n", turkish_text);
    printf("Key:              %s\n", turkish_key);
    
    if (gronsfeld_encrypt(turkish_text, turkish_key, NULL, turkish_alphabet, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted:        %s\n", encrypted);
        
        if (gronsfeld_decrypt(encrypted, turkish_key, NULL, turkish_alphabet, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:        %s\n", decrypted);
            printf("Success:          %s\n", strcmp(turkish_text, decrypted) == 0 ? "YES" : "NO");
        }
    }
    
    // Example 7: Error handling
    printf("\n7. Error Handling\n");
    printf("----------------------------------------\n");
    
    // Test invalid key
    if (gronsfeld_encrypt("HELLO", "abc123", NULL, NULL, encrypted, sizeof(encrypted)) == -1) {
        printf("Invalid key error: Correctly rejected non-numeric key\n");
    }
    
    // Test empty key
    if (gronsfeld_encrypt("HELLO", "", NULL, NULL, encrypted, sizeof(encrypted)) == -1) {
        printf("Empty key error: Correctly rejected empty key\n");
    }
    
    // Test invalid table type
    if (gronsfeld_produce_table("invalid", NULL, &table, &table_size) == -1) {
        printf("Invalid table type error: Correctly rejected invalid table type\n");
    }
    
    // Test missing parameters
    if (gronsfeld_produce_table("caesar", NULL, &table, &table_size) == -1) {
        printf("Missing parameter error: Correctly rejected missing shift parameter\n");
    }
    
    printf("\n============================================================\n");
    printf("GRONSFELD CIPHER EXAMPLE COMPLETED\n");
    printf("============================================================\n");
    
    return 0;
}
