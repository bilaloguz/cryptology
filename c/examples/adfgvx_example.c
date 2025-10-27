#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/cryptology/classical/substitution/composite/adfgvx.h"

int main() {
    printf("=== ADFGVX Cipher Example ===\n\n");
    
    // Test data
    const char* plaintext = "HELLO";
    const char* key = "SECRET";
    char encrypted[1024];
    char decrypted[1024];
    char square[1024];
    char generated_key[256];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n\n", key);
    
    // Test 1: Basic encryption/decryption with English alphabet
    printf("1. Basic English ADFGVX:\n");
    if (adfgvx_encrypt(plaintext, key, NULL, "english", NULL, encrypted, sizeof(encrypted)) == 0) {
        printf("   Encrypted: %s\n", encrypted);
        
        if (adfgvx_decrypt(encrypted, key, NULL, "english", NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("   Decrypted: %s\n", decrypted);
            printf("   Success: %s\n", strcmp(decrypted, plaintext) == 0 ? "Yes" : "No");
        } else {
            printf("   Decryption failed!\n");
        }
    } else {
        printf("   Encryption failed!\n");
    }
    printf("\n");
    
    // Test 2: Square generation
    printf("2. Square Generation:\n");
    if (adfgvx_produce_square("standard", NULL, NULL, "english", NULL, square, sizeof(square)) == 0) {
        printf("   Standard English Square:\n");
        char* line = strtok(square, "\n");
        int row = 1;
        while (line) {
            printf("     Row %d: %s\n", row++, line);
            line = strtok(NULL, "\n");
        }
    }
    printf("\n");
    
    // Test 3: Random key generation
    printf("3. Random Key Generation:\n");
    if (adfgvx_generate_random_key(8, generated_key, sizeof(generated_key)) == 0) {
        printf("   Generated key: %s\n", generated_key);
        
        // Test encryption with generated key
        if (adfgvx_encrypt(plaintext, generated_key, NULL, "english", NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("   Encrypted with generated key: %s\n", encrypted);
        }
    }
    printf("\n");
    
    // Test 4: Turkish alphabet
    printf("4. Turkish Alphabet:\n");
    const char* turkish_text = "MERHABA";
    const char* turkish_key = "ANAHTAR";
    
    if (adfgvx_encrypt(turkish_text, turkish_key, NULL, "turkish", NULL, encrypted, sizeof(encrypted)) == 0) {
        printf("   Turkish encrypted: %s\n", encrypted);
        
        if (adfgvx_decrypt(encrypted, turkish_key, NULL, "turkish", NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("   Turkish decrypted: %s\n", decrypted);
            printf("   Success: %s\n", strcmp(decrypted, turkish_text) == 0 ? "Yes" : "No");
        } else {
            printf("   Turkish decryption failed!\n");
        }
    } else {
        printf("   Turkish encryption failed!\n");
    }
    printf("\n");
    
    // Test 5: Monoalphabetic square integration
    printf("5. Monoalphabetic Square Integration:\n");
    if (adfgvx_produce_square("caesar", NULL, NULL, "english", "{\"shift\": 3}", square, sizeof(square)) == 0) {
        printf("   Caesar-shifted square generated\n");
        
        if (adfgvx_encrypt(plaintext, key, square, "english", NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("   Encrypted with Caesar square: %s\n", encrypted);
        }
    }
    printf("\n");
    
    printf("=== ADFGVX Example Complete ===\n");
    return 0;
}
