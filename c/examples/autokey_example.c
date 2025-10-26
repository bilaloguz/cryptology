/**
 * @file autokey_example.c
 * @brief Example demonstrating Auto-key cipher usage
 */

#include "cryptology/classical/substitution/polyalphabetic/autokey.h"
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

void print_table(const char *title, char **table, const char *alphabet) {
    printf("\n%s:\n", title);
    printf("   ");
    for (size_t i = 0; i < strlen(alphabet); i++) {
        printf("%c ", alphabet[i]);
    }
    printf("\n");
    
    for (size_t i = 0; i < strlen(alphabet); i++) {
        printf("%c: ", alphabet[i]);
        for (size_t j = 0; j < strlen(alphabet); j++) {
            printf("%c ", table[i][j]);
        }
        printf("\n");
    }
}

void free_table(char **table, size_t alphabet_len) {
    if (table) {
        for (size_t i = 0; i < alphabet_len; i++) {
            free(table[i]);
        }
        free(table);
    }
}

int main() {
    printf("=== Auto-key Cipher Example ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    char encrypted[256];
    char decrypted[256];
    char generated_key[256];
    
    printf("\n1. Basic Auto-key Encryption/Decryption\n");
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    
    // Encrypt
    if (autokey_encrypt(plaintext, key, NULL, DEFAULT_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (autokey_decrypt(encrypted, key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    printf("\n2. Auto-key with Random Key Generation\n");
    printf("Plaintext: %s\n", plaintext);
    
    // Generate random key and encrypt
    if (autokey_encrypt_with_random_key(plaintext, NULL, DEFAULT_ALPHABET, 5, 
                                       encrypted, sizeof(encrypted),
                                       generated_key, sizeof(generated_key)) == 0) {
        printf("Generated Key: %s\n", generated_key);
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt using generated key
        if (autokey_decrypt(encrypted, generated_key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Random key encryption failed!\n");
    }
    
    printf("\n3. Auto-key Table Generation\n");
    
    // Classical table
    char **classical_table;
    if (autokey_produce_table("classical", DEFAULT_ALPHABET, &classical_table) == 0) {
        print_table("Classical Auto-key Table", classical_table, DEFAULT_ALPHABET);
        free_table(classical_table, strlen(DEFAULT_ALPHABET));
    }
    
    // Caesar table
    char **caesar_table;
    if (autokey_produce_table("caesar", DEFAULT_ALPHABET, &caesar_table, 3) == 0) {
        print_table("Caesar Auto-key Table (shift=3)", caesar_table, DEFAULT_ALPHABET);
        free_table(caesar_table, strlen(DEFAULT_ALPHABET));
    }
    
    // Affine table
    char **affine_table;
    if (autokey_produce_table("affine", DEFAULT_ALPHABET, &affine_table, 3, 5) == 0) {
        print_table("Affine Auto-key Table (a=3, b=5)", affine_table, DEFAULT_ALPHABET);
        free_table(affine_table, strlen(DEFAULT_ALPHABET));
    }
    
    // Keyword table
    char **keyword_table;
    if (autokey_produce_table("keyword", DEFAULT_ALPHABET, &keyword_table, "SECRET") == 0) {
        print_table("Keyword Auto-key Table (keyword=SECRET)", keyword_table, DEFAULT_ALPHABET);
        free_table(keyword_table, strlen(DEFAULT_ALPHABET));
    }
    
    // Atbash table
    char **atbash_table;
    if (autokey_produce_table("atbash", DEFAULT_ALPHABET, &atbash_table) == 0) {
        print_table("Atbash Auto-key Table", atbash_table, DEFAULT_ALPHABET);
        free_table(atbash_table, strlen(DEFAULT_ALPHABET));
    }
    
    printf("\n4. Turkish Alphabet Support\n");
    const char *turkish_text = "MERHABA DÜNYA";
    const char *turkish_key = "ANAHTAR";
    
    printf("Turkish Plaintext: %s\n", turkish_text);
    printf("Turkish Key: %s\n", turkish_key);
    
    if (autokey_encrypt(turkish_text, turkish_key, NULL, TURKISH_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Turkish Encrypted: %s\n", encrypted);
        
        if (autokey_decrypt(encrypted, turkish_key, NULL, TURKISH_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Turkish Decrypted: %s\n", decrypted);
        } else {
            printf("Turkish decryption failed!\n");
        }
    } else {
        printf("Turkish encryption failed!\n");
    }
    
    printf("\n5. Composable System Example\n");
    printf("Using Caesar-produced alphabet with Auto-key\n");
    
    // Generate Caesar alphabet
    char caesar_alphabet[256];
    if (caesar_produce_alphabet(3, DEFAULT_ALPHABET, caesar_alphabet, sizeof(caesar_alphabet)) == 0) {
        printf("Caesar Alphabet (shift=3): %s\n", caesar_alphabet);
        
        const char *composable_text = "TEST MESSAGE";
        const char *composable_key = "TEST";
        
        printf("Plaintext: %s\n", composable_text);
        printf("Key: %s\n", composable_key);
        
        if (autokey_encrypt(composable_text, composable_key, NULL, caesar_alphabet, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted with Caesar alphabet: %s\n", encrypted);
            
            if (autokey_decrypt(encrypted, composable_key, NULL, caesar_alphabet, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted with Caesar alphabet: %s\n", decrypted);
            } else {
                printf("Decryption failed!\n");
            }
        } else {
            printf("Encryption failed!\n");
        }
    } else {
        printf("Failed to generate Caesar alphabet!\n");
    }
    
    printf("\n6. Key Extension Demonstration\n");
    const char *long_text = "THIS IS A LONG MESSAGE TO DEMONSTRATE KEY EXTENSION";
    const char *short_key = "KEY";
    
    printf("Long Plaintext: %s\n", long_text);
    printf("Short Key: %s\n", short_key);
    
    if (autokey_encrypt(long_text, short_key, NULL, DEFAULT_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (autokey_decrypt(encrypted, short_key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    printf("\n=== Auto-key Example Complete ===\n");
    return 0;
}
