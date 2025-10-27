/**
 * @file straddling_checkerboard_example.c
 * @brief Straddling Checkerboard Cipher Example
 * 
 * Demonstrates the composite substitution cipher that combines
 * substitution, fractionation, and numeric key addition.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "../include/cryptology/classical/substitution/composite/straddling_checkerboard.h"

int main() {
    printf("=== Straddling Checkerboard Cipher Examples ===\n\n");
    
    char plaintext[] = "HELLO WORLD";
    char key[] = "12345";
    char encrypted[100];
    char decrypted[100];
    
    // Basic usage
    printf("1. Basic Encryption/Decryption\n");
    printf("----------------------------------------\n");
    
    if (straddling_checkerboard_encrypt(plaintext, key, NULL, "numeric", encrypted, sizeof(encrypted)) == 0) {
        printf("Plaintext:  %s\n", plaintext);
        printf("Key:        %s\n", key);
        printf("Encrypted:  %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt(encrypted, key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:  %s\n", decrypted);
            printf("Success:    %s\n", strcmp(plaintext, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Different key types
    printf("2. Key Types\n");
    printf("----------------------------------------\n");
    
    // Numeric key
    printf("Numeric Key:\n");
    if (straddling_checkerboard_encrypt(plaintext, key, NULL, "numeric", encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", plaintext);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt(encrypted, key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Alphabetic key
    char alphabetic_key[] = "KEY";
    printf("Alphabetic Key:\n");
    if (straddling_checkerboard_encrypt(plaintext, alphabetic_key, NULL, "alphabetic", encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", plaintext);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt(encrypted, alphabetic_key, NULL, "alphabetic", decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Different checkerboard types
    printf("3. Checkerboard Types\n");
    printf("----------------------------------------\n");
    
    char checkerboard[1000];
    
    // Standard checkerboard
    printf("Standard Checkerboard:\n");
    if (straddling_checkerboard_produce_checkerboard("standard", NULL, NULL, checkerboard, sizeof(checkerboard)) == 0) {
        printf("  Checkerboard created successfully\n");
        
        if (straddling_checkerboard_encrypt(plaintext, key, checkerboard, "numeric", encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", plaintext);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (straddling_checkerboard_decrypt(encrypted, key, checkerboard, "numeric", decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Keyword-based checkerboard
    char keyword[] = "SECRET";
    printf("Keyword Checkerboard (keyword: %s):\n", keyword);
    if (straddling_checkerboard_produce_checkerboard("keyword", keyword, NULL, checkerboard, sizeof(checkerboard)) == 0) {
        printf("  Checkerboard created successfully\n");
        
        if (straddling_checkerboard_encrypt(plaintext, key, checkerboard, "numeric", encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", plaintext);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (straddling_checkerboard_decrypt(encrypted, key, checkerboard, "numeric", decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Custom checkerboard
    printf("Custom Checkerboard:\n");
    if (straddling_checkerboard_produce_checkerboard("custom", NULL, NULL, checkerboard, sizeof(checkerboard)) == 0) {
        printf("  Checkerboard created successfully\n");
        
        if (straddling_checkerboard_encrypt(plaintext, key, checkerboard, "numeric", encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", plaintext);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (straddling_checkerboard_decrypt(encrypted, key, checkerboard, "numeric", decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Random key generation
    printf("4. Random Key Generation\n");
    printf("----------------------------------------\n");
    
    char generated_key[20];
    
    // Generate numeric key
    if (straddling_checkerboard_generate_random_key(5, "numeric", generated_key, sizeof(generated_key)) == 0) {
        printf("Random Numeric Key: %s\n", generated_key);
        
        if (straddling_checkerboard_encrypt(plaintext, generated_key, NULL, "numeric", encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext:  %s\n", plaintext);
            printf("Encrypted:  %s\n", encrypted);
            
            if (straddling_checkerboard_decrypt(encrypted, generated_key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Generate alphabetic key
    if (straddling_checkerboard_generate_random_key(5, "alphabetic", generated_key, sizeof(generated_key)) == 0) {
        printf("Random Alphabetic Key: %s\n", generated_key);
        
        if (straddling_checkerboard_encrypt(plaintext, generated_key, NULL, "alphabetic", encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext:  %s\n", plaintext);
            printf("Encrypted:  %s\n", encrypted);
            
            if (straddling_checkerboard_decrypt(encrypted, generated_key, NULL, "alphabetic", decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Encrypt with random key
    printf("Auto-generated Key:\n");
    if (straddling_checkerboard_encrypt_with_random_key(plaintext, 0, "numeric", encrypted, sizeof(encrypted), generated_key, sizeof(generated_key)) == 0) {
        printf("Auto-generated Key: %s\n", generated_key);
        printf("Plaintext:  %s\n", plaintext);
        printf("Encrypted:  %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt(encrypted, generated_key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Turkish alphabet support
    printf("5. Turkish Alphabet Support\n");
    printf("----------------------------------------\n");
    char turkish_text[] = "MERHABA DUNYA";
    char turkish_key[] = "12345";
    
    if (straddling_checkerboard_encrypt_turkish(turkish_text, turkish_key, NULL, "numeric", encrypted, sizeof(encrypted)) == 0) {
        printf("Turkish Text: %s\n", turkish_text);
        printf("Turkish Key:  %s\n", turkish_key);
        printf("Encrypted:    %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt_turkish(encrypted, turkish_key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:    %s\n", decrypted);
            printf("Success:      %s\n", strcmp(turkish_text, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Long text example
    printf("6. Long Text Example\n");
    printf("----------------------------------------\n");
    char long_text[] = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    char long_key[] = "123456789";
    
    if (straddling_checkerboard_encrypt(long_text, long_key, NULL, "numeric", encrypted, sizeof(encrypted)) == 0) {
        printf("Long Text:   %s\n", long_text);
        printf("Long Key:    %s\n", long_key);
        printf("Encrypted:   %s\n", encrypted);
        
        if (straddling_checkerboard_decrypt(encrypted, long_key, NULL, "numeric", decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:   %s\n", decrypted);
            printf("Success:     %s\n", strcmp(long_text, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Error handling
    printf("7. Error Handling\n");
    printf("----------------------------------------\n");
    
    // Test invalid parameters
    if (straddling_checkerboard_encrypt(NULL, key, NULL, "numeric", encrypted, sizeof(encrypted)) == -1) {
        printf("✓ Caught expected error: NULL plaintext\n");
    }
    
    if (straddling_checkerboard_encrypt(plaintext, NULL, NULL, "numeric", encrypted, sizeof(encrypted)) == -1) {
        printf("✓ Caught expected error: NULL key\n");
    }
    
    if (straddling_checkerboard_generate_random_key(-1, "numeric", generated_key, sizeof(generated_key)) == -1) {
        printf("✓ Caught expected error: negative key length\n");
    }
    
    if (straddling_checkerboard_produce_checkerboard("invalid", NULL, NULL, checkerboard, sizeof(checkerboard)) == -1) {
        printf("✓ Caught expected error: invalid checkerboard type\n");
    }
    
    printf("\n=== All Examples Completed Successfully! ===\n");
    
    return 0;
}
