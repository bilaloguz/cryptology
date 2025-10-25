/**
 * @file composable_ciphers.c
 * @brief Example demonstrating the composable cipher system
 * 
 * This example shows how monoalphabetic ciphers can produce custom alphabets
 * that are then used with polygraphic ciphers for enhanced security.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Include monoalphabetic cipher headers
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"

// Include polygraphic cipher headers
#include "cryptology/classical/substitution/polygraphic/playfair.h"

#define MAX_BUFFER_SIZE 1024
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"

void demonstrate_caesar_playfair() {
    printf("=== Caesar + Playfair Composable System ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *playfair_key = "MONARCHY";
    int caesar_shift = 5;
    
    char caesar_alphabet[MAX_BUFFER_SIZE];
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Caesar shift: %d\n", caesar_shift);
    printf("Playfair key: %s\n", playfair_key);
    printf("\n");
    
    // Step 1: Produce Caesar-shifted alphabet
    if (caesar_produce_alphabet(caesar_shift, DEFAULT_ALPHABET, caesar_alphabet, sizeof(caesar_alphabet)) != 0) {
        printf("Error: Failed to produce Caesar alphabet\n");
        return;
    }
    printf("Caesar-produced alphabet: %s\n", caesar_alphabet);
    
    // Step 2: Use Caesar alphabet with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, caesar_alphabet, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair\n");
        return;
    }
    printf("Encrypted: %s\n", encrypted);
    
    // Step 3: Decrypt with same alphabet
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, caesar_alphabet, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

void demonstrate_keyword_playfair() {
    printf("=== Keyword + Playfair Composable System ===\n");
    
    const char *plaintext = "SECRET MESSAGE";
    const char *keyword = "SECRET";
    const char *playfair_key = "MONARCHY";
    
    char keyword_alphabet[MAX_BUFFER_SIZE];
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Keyword: %s\n", keyword);
    printf("Playfair key: %s\n", playfair_key);
    printf("\n");
    
    // Step 1: Produce keyword-based alphabet
    if (keyword_produce_alphabet(keyword, DEFAULT_ALPHABET, keyword_alphabet, sizeof(keyword_alphabet)) != 0) {
        printf("Error: Failed to produce keyword alphabet\n");
        return;
    }
    printf("Keyword-produced alphabet: %s\n", keyword_alphabet);
    
    // Step 2: Use keyword alphabet with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, keyword_alphabet, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair\n");
        return;
    }
    printf("Encrypted: %s\n", encrypted);
    
    // Step 3: Decrypt with same alphabet
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, keyword_alphabet, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

void demonstrate_affine_playfair() {
    printf("=== Affine + Playfair Composable System ===\n");
    
    const char *plaintext = "AFFINE CIPHER";
    int a = 3, b = 5;  // Affine parameters
    const char *playfair_key = "MONARCHY";
    
    char affine_alphabet[MAX_BUFFER_SIZE];
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Affine parameters: a=%d, b=%d\n", a, b);
    printf("Playfair key: %s\n", playfair_key);
    printf("\n");
    
    // Step 1: Produce affine-transformed alphabet
    if (affine_produce_alphabet(a, b, DEFAULT_ALPHABET, affine_alphabet, sizeof(affine_alphabet)) != 0) {
        printf("Error: Failed to produce affine alphabet\n");
        return;
    }
    printf("Affine-produced alphabet: %s\n", affine_alphabet);
    
    // Step 2: Use affine alphabet with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, affine_alphabet, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair\n");
        return;
    }
    printf("Encrypted: %s\n", encrypted);
    
    // Step 3: Decrypt with same alphabet
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, affine_alphabet, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

void demonstrate_atbash_playfair() {
    printf("=== Atbash + Playfair Composable System ===\n");
    
    const char *plaintext = "ATBASH CIPHER";
    const char *playfair_key = "MONARCHY";
    
    char atbash_alphabet[MAX_BUFFER_SIZE];
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Playfair key: %s\n", playfair_key);
    printf("\n");
    
    // Step 1: Produce Atbash-reversed alphabet
    if (atbash_produce_alphabet(DEFAULT_ALPHABET, atbash_alphabet, sizeof(atbash_alphabet)) != 0) {
        printf("Error: Failed to produce Atbash alphabet\n");
        return;
    }
    printf("Atbash-produced alphabet: %s\n", atbash_alphabet);
    
    // Step 2: Use Atbash alphabet with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, atbash_alphabet, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair\n");
        return;
    }
    printf("Encrypted: %s\n", encrypted);
    
    // Step 3: Decrypt with same alphabet
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, atbash_alphabet, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

void demonstrate_turkish_playfair() {
    printf("=== Turkish Alphabet + Playfair ===\n");
    
    const char *plaintext = "MERHABA DÜNYA";
    const char *playfair_key = "GİZLİ";
    
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Playfair key: %s\n", playfair_key);
    printf("Turkish alphabet: %s\n", TURKISH_ALPHABET);
    printf("\n");
    
    // Use Turkish alphabet directly with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, TURKISH_ALPHABET, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair using Turkish alphabet\n");
        return;
    }
    printf("Encrypted: %s\n", encrypted);
    
    // Decrypt with same alphabet
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, TURKISH_ALPHABET, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair using Turkish alphabet\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

void demonstrate_multi_layer_encryption() {
    printf("=== Multi-Layer Encryption ===\n");
    
    const char *plaintext = "MULTI LAYER";
    const char *keyword = "SECRET";
    int caesar_shift = 3;
    const char *playfair_key = "MONARCHY";
    
    char keyword_alphabet[MAX_BUFFER_SIZE];
    char caesar_alphabet[MAX_BUFFER_SIZE];
    char final_alphabet[MAX_BUFFER_SIZE];
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Layer 1 - Keyword: %s\n", keyword);
    printf("Layer 2 - Caesar shift: %d\n", caesar_shift);
    printf("Layer 3 - Playfair key: %s\n", playfair_key);
    printf("\n");
    
    // Layer 1: Keyword alphabet
    if (keyword_produce_alphabet(keyword, DEFAULT_ALPHABET, keyword_alphabet, sizeof(keyword_alphabet)) != 0) {
        printf("Error: Failed to produce keyword alphabet\n");
        return;
    }
    printf("Keyword alphabet: %s\n", keyword_alphabet);
    
    // Layer 2: Caesar shift the keyword alphabet
    if (caesar_produce_alphabet(caesar_shift, keyword_alphabet, caesar_alphabet, sizeof(caesar_alphabet)) != 0) {
        printf("Error: Failed to produce Caesar alphabet\n");
        return;
    }
    printf("Caesar-shifted alphabet: %s\n", caesar_alphabet);
    
    // Layer 3: Use with Playfair
    if (playfair_encrypt_with_alphabet(plaintext, playfair_key, caesar_alphabet, encrypted, sizeof(encrypted)) != 0) {
        printf("Error: Failed to encrypt with Playfair\n");
        return;
    }
    printf("Final encrypted: %s\n", encrypted);
    
    // Decrypt (reverse the process)
    if (playfair_decrypt_with_alphabet(encrypted, playfair_key, caesar_alphabet, decrypted, sizeof(decrypted)) != 0) {
        printf("Error: Failed to decrypt with Playfair\n");
        return;
    }
    printf("Decrypted: %s\n", decrypted);
    printf("\n");
}

int main() {
    printf("Composable Cipher System Demo\n");
    printf("=============================\n\n");
    
    demonstrate_caesar_playfair();
    demonstrate_keyword_playfair();
    demonstrate_affine_playfair();
    demonstrate_atbash_playfair();
    demonstrate_turkish_playfair();
    demonstrate_multi_layer_encryption();
    
    printf("Summary:\n");
    printf("1. Monoalphabetic ciphers can produce custom alphabets\n");
    printf("2. Polygraphic ciphers can use these custom alphabets\n");
    printf("3. Multiple layers of encryption for enhanced security\n");
    printf("4. Support for different languages (English, Turkish)\n");
    printf("5. Composable system provides flexible encryption options\n");
    
    return 0;
}
