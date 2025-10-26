/**
 * @file chaocipher_example.c
 * @brief Example program demonstrating Chaocipher usage
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cryptology/classical/substitution/polyalphabetic/chaocipher.h"

#define MAX_TEXT_LEN 1024
#define MAX_ALPHABET_LEN 64

void print_alphabet(const char *name, const char *alphabet, size_t len) {
    printf("%s: ", name);
    for (size_t i = 0; i < len; i++) {
        printf("%c", alphabet[i]);
    }
    printf(" (length: %zu)\n", len);
}

int main() {
    printf("=== Chaocipher Example ===\n\n");
    
    // Example 1: Basic encryption/decryption with default alphabets
    printf("1. Basic Encryption/Decryption\n");
    printf("===============================\n");
    
    const char *plaintext = "HELLO WORLD";
    char left_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    char right_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    
    char encrypted[MAX_TEXT_LEN];
    char decrypted[MAX_TEXT_LEN];
    
    int encrypt_len = chaocipher_encrypt(plaintext, left_alphabet, right_alphabet, 
                                       27, encrypted, sizeof(encrypted));
    
    int decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                       27, decrypted, sizeof(decrypted));
    
    printf("Plaintext:  %s\n", plaintext);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n", decrypted);
    printf("Success: %s\n\n", strcmp(decrypted, plaintext) == 0 ? "YES" : "NO");
    
    // Example 2: Custom alphabets with keywords
    printf("2. Custom Alphabets with Keywords\n");
    printf("===================================\n");
    
    char custom_left[MAX_ALPHABET_LEN];
    char custom_right[MAX_ALPHABET_LEN];
    
    chaocipher_create_custom_alphabets("SECRET", "KEYWORD", 
                                      custom_left, custom_right, 27);
    
    print_alphabet("Custom Left (SECRET)", custom_left, 27);
    print_alphabet("Custom Right (KEYWORD)", custom_right, 27);
    
    encrypt_len = chaocipher_encrypt(plaintext, custom_left, custom_right, 
                                   27, encrypted, sizeof(encrypted));
    
    decrypt_len = chaocipher_decrypt(encrypted, custom_left, custom_right, 
                                   27, decrypted, sizeof(decrypted));
    
    printf("Plaintext:  %s\n", plaintext);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n", decrypted);
    printf("Success: %s\n\n", strcmp(decrypted, plaintext) == 0 ? "YES" : "NO");
    
    // Example 3: Turkish alphabet
    printf("3. Turkish Alphabet Support\n");
    printf("============================\n");
    
    const char *turkish_text = "MERHABA DÜNYA";
    char turkish_left[] = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ";
    char turkish_right[] = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ";
    
    encrypt_len = chaocipher_encrypt(turkish_text, turkish_left, turkish_right, 
                                   29, encrypted, sizeof(encrypted));
    
    decrypt_len = chaocipher_decrypt(encrypted, turkish_left, turkish_right, 
                                   29, decrypted, sizeof(decrypted));
    
    printf("Turkish text: %s\n", turkish_text);
    printf("Encrypted:   %s\n", encrypted);
    printf("Decrypted:   %s\n", decrypted);
    printf("Success: %s\n\n", strcmp(decrypted, turkish_text) == 0 ? "YES" : "NO");
    
    // Example 4: Long text
    printf("4. Long Text Processing\n");
    printf("=======================\n");
    
    const char *long_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    
    encrypt_len = chaocipher_encrypt(long_text, left_alphabet, right_alphabet, 
                                    27, encrypted, sizeof(encrypted));
    
    decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                    27, decrypted, sizeof(decrypted));
    
    printf("Long text length: %zu\n", strlen(long_text));
    printf("Encrypted length: %d\n", encrypt_len);
    printf("Decrypted length: %d\n", decrypt_len);
    printf("Success: %s\n", strcmp(decrypted, long_text) == 0 ? "YES" : "NO");
    
    printf("\n=== Example completed successfully! ===\n");
    return 0;
}
