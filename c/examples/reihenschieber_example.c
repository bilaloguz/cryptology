/**
 * @file reihenschieber_example.c
 * @brief Reihenschieber Cipher Example
 * 
 * Demonstrates the mechanical polyalphabetic substitution cipher with
 * multiple shift modes, directions, and custom patterns.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "../include/cryptology/classical/substitution/polyalphabetic/reihenschieber.h"

int main() {
    printf("=== Reihenschieber Cipher Examples ===\n\n");
    
    char plaintext[] = "HELLO WORLD";
    char key[] = "SECRET";
    char encrypted[100];
    char decrypted[100];
    
    // Basic usage
    printf("1. Basic Encryption/Decryption\n");
    printf("----------------------------------------\n");
    
    if (reihenschieber_encrypt(plaintext, key, NULL, "fixed", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("Plaintext:  %s\n", plaintext);
        printf("Key:        %s\n", key);
        printf("Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, key, NULL, "fixed", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:  %s\n", decrypted);
            printf("Success:    %s\n", strcmp(plaintext, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Different shift modes
    printf("2. Shift Modes\n");
    printf("----------------------------------------\n");
    
    char test_text[] = "HELLO";
    char test_key[] = "KEY";
    
    // Fixed mode
    printf("Fixed Mode:\n");
    if (reihenschieber_encrypt(test_text, test_key, NULL, "fixed", "forward", 2, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", test_text);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, test_key, NULL, "fixed", "forward", 2, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Progressive mode
    printf("Progressive Mode:\n");
    if (reihenschieber_encrypt(test_text, test_key, NULL, "progressive", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", test_text);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, test_key, NULL, "progressive", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Custom mode
    printf("Custom Mode:\n");
    int custom_shifts[] = {1, -1, 2, -2, 0};
    if (reihenschieber_encrypt(test_text, test_key, NULL, "custom", "forward", 0, custom_shifts, 5, encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", test_text);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, test_key, NULL, "custom", "forward", 0, custom_shifts, 5, decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Shift directions
    printf("3. Shift Directions\n");
    printf("----------------------------------------\n");
    
    // Forward (default)
    printf("Forward Direction:\n");
    if (reihenschieber_encrypt(test_text, test_key, NULL, "fixed", "forward", 2, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", test_text);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, test_key, NULL, "fixed", "forward", 2, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Backward
    printf("Backward Direction:\n");
    if (reihenschieber_encrypt(test_text, test_key, NULL, "fixed", "backward", 2, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("  Plaintext:  %s\n", test_text);
        printf("  Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, test_key, NULL, "fixed", "backward", 2, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("  Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Custom shift patterns
    printf("4. Custom Shift Patterns\n");
    printf("----------------------------------------\n");
    
    int shifts[10];
    char generated_key[20];
    
    // Alternating pattern
    printf("Alternating Pattern:\n");
    if (reihenschieber_produce_custom_shifts("alternating", 5, shifts, sizeof(shifts)) == 0) {
        printf("  Shifts: [");
        for (int i = 0; i < 5; i++) {
            printf("%d", shifts[i]);
            if (i < 4) printf(", ");
        }
        printf("]\n");
        
        if (reihenschieber_encrypt(test_text, test_key, NULL, "custom", "forward", 0, shifts, 5, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (reihenschieber_decrypt(encrypted, test_key, NULL, "custom", "forward", 0, shifts, 5, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Fibonacci pattern
    printf("Fibonacci Pattern:\n");
    if (reihenschieber_produce_custom_shifts("fibonacci", 5, shifts, sizeof(shifts)) == 0) {
        printf("  Shifts: [");
        for (int i = 0; i < 5; i++) {
            printf("%d", shifts[i]);
            if (i < 4) printf(", ");
        }
        printf("]\n");
        
        if (reihenschieber_encrypt(test_text, test_key, NULL, "custom", "forward", 0, shifts, 5, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (reihenschieber_decrypt(encrypted, test_key, NULL, "custom", "forward", 0, shifts, 5, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Prime pattern
    printf("Prime Pattern:\n");
    if (reihenschieber_produce_custom_shifts("prime", 5, shifts, sizeof(shifts)) == 0) {
        printf("  Shifts: [");
        for (int i = 0; i < 5; i++) {
            printf("%d", shifts[i]);
            if (i < 4) printf(", ");
        }
        printf("]\n");
        
        if (reihenschieber_encrypt(test_text, test_key, NULL, "custom", "forward", 0, shifts, 5, encrypted, sizeof(encrypted)) == 0) {
            printf("  Plaintext:  %s\n", test_text);
            printf("  Encrypted:  %s\n", encrypted);
            
            if (reihenschieber_decrypt(encrypted, test_key, NULL, "custom", "forward", 0, shifts, 5, decrypted, sizeof(decrypted)) == 0) {
                printf("  Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Random key generation
    printf("5. Random Key Generation\n");
    printf("----------------------------------------\n");
    
    char random_text[] = "HELLO WORLD";
    
    // Generate random key
    if (reihenschieber_generate_random_key(5, generated_key, sizeof(generated_key)) == 0) {
        printf("Random Key: %s\n", generated_key);
        
        if (reihenschieber_encrypt(random_text, generated_key, NULL, "fixed", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
            printf("Plaintext:  %s\n", random_text);
            printf("Encrypted:  %s\n", encrypted);
            
            if (reihenschieber_decrypt(encrypted, generated_key, NULL, "fixed", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
            }
        }
    }
    printf("\n");
    
    // Encrypt with random key
    printf("Auto-generated Key:\n");
    if (reihenschieber_encrypt_with_random_key(random_text, 0, encrypted, sizeof(encrypted), generated_key, sizeof(generated_key)) == 0) {
        printf("Auto-generated Key: %s\n", generated_key);
        printf("Plaintext:  %s\n", random_text);
        printf("Encrypted:  %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, generated_key, NULL, "fixed", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:  %s\n", decrypted);
        }
    }
    printf("\n");
    
    // Turkish alphabet support
    printf("6. Turkish Alphabet Support\n");
    printf("----------------------------------------\n");
    char turkish_text[] = "MERHABA DUNYA";
    char turkish_key[] = "ANAHTAR";
    
    if (reihenschieber_encrypt_turkish(turkish_text, turkish_key, "fixed", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("Turkish Text: %s\n", turkish_text);
        printf("Turkish Key:  %s\n", turkish_key);
        printf("Encrypted:    %s\n", encrypted);
        
        if (reihenschieber_decrypt_turkish(encrypted, turkish_key, "fixed", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:    %s\n", decrypted);
            printf("Success:      %s\n", strcmp(turkish_text, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Long text example
    printf("7. Long Text Example\n");
    printf("----------------------------------------\n");
    char long_text[] = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    char long_key[] = "SECRETKEY";
    
    if (reihenschieber_encrypt(long_text, long_key, NULL, "progressive", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("Long Text:   %s\n", long_text);
        printf("Long Key:    %s\n", long_key);
        printf("Encrypted:   %s\n", encrypted);
        
        if (reihenschieber_decrypt(encrypted, long_key, NULL, "progressive", "forward", 1, NULL, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted:   %s\n", decrypted);
            printf("Success:     %s\n", strcmp(long_text, decrypted) == 0 ? "Yes" : "No");
        }
    }
    printf("\n");
    
    // Error handling
    printf("8. Error Handling\n");
    printf("----------------------------------------\n");
    
    // Test invalid parameters
    if (reihenschieber_encrypt(NULL, "KEY", NULL, "fixed", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == -1) {
        printf("✓ Caught expected error: NULL plaintext\n");
    }
    
    if (reihenschieber_encrypt("HELLO", NULL, NULL, "fixed", "forward", 1, NULL, 0, encrypted, sizeof(encrypted)) == -1) {
        printf("✓ Caught expected error: NULL key\n");
    }
    
    if (reihenschieber_generate_random_key(-1, generated_key, sizeof(generated_key)) == -1) {
        printf("✓ Caught expected error: negative key length\n");
    }
    
    printf("\n=== All Examples Completed Successfully! ===\n");
    
    return 0;
}
