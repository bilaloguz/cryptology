/**
 * @file beaufort_example.c
 * @brief Example demonstrating Beaufort cipher usage
 */

#include "cryptology/classical/substitution/polyalphabetic/beaufort.h"
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
    printf("=== Beaufort Cipher Example ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    char encrypted[256];
    char decrypted[256];
    char generated_key[256];
    
    printf("\n1. Basic Beaufort Encryption/Decryption\n");
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    
    // Encrypt
    if (beaufort_encrypt(plaintext, key, NULL, DEFAULT_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (beaufort_decrypt(encrypted, key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    printf("\n2. Beaufort Self-Reciprocal Property\n");
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    
    // Test self-reciprocal property
    if (beaufort_encrypt(plaintext, key, NULL, DEFAULT_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt using same function (self-reciprocal)
        if (beaufort_encrypt(encrypted, key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted (using encrypt): %s\n", decrypted);
        } else {
            printf("Self-reciprocal decryption failed!\n");
        }
    } else {
        printf("Encryption failed!\n");
    }
    
    printf("\n3. Beaufort with Random Key Generation\n");
    printf("Plaintext: %s\n", plaintext);
    
    // Generate random key and encrypt
    if (beaufort_encrypt_with_random_key(plaintext, NULL, DEFAULT_ALPHABET, 5, 
                                       encrypted, sizeof(encrypted),
                                       generated_key, sizeof(generated_key)) == 0) {
        printf("Generated Key: %s\n", generated_key);
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt using generated key
        if (beaufort_decrypt(encrypted, generated_key, NULL, DEFAULT_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Decryption failed!\n");
        }
    } else {
        printf("Random key encryption failed!\n");
    }
    
    printf("\n4. Beaufort Table Generation\n");
    
    // Classical table
    char **classical_table;
    size_t classical_size = 0;
    if (beaufort_produce_table("classical", DEFAULT_ALPHABET, &classical_table, &classical_size) == 0) {
        print_table("Classical Beaufort Table", classical_table, DEFAULT_ALPHABET);
        free_table(classical_table, classical_size);
    }
    
    // Caesar table
    char **caesar_table;
    size_t caesar_size = 0;
    if (beaufort_produce_table("caesar", DEFAULT_ALPHABET, &caesar_table, &caesar_size, 3) == 0) {
        print_table("Caesar Beaufort Table (shift=3)", caesar_table, DEFAULT_ALPHABET);
        free_table(caesar_table, caesar_size);
    }
    
    // Affine table
    char **affine_table;
    size_t affine_size = 0;
    if (beaufort_produce_table("affine", DEFAULT_ALPHABET, &affine_table, &affine_size, 3, 5) == 0) {
        print_table("Affine Beaufort Table (a=3, b=5)", affine_table, DEFAULT_ALPHABET);
        free_table(affine_table, affine_size);
    }
    
    // Keyword table
    char **keyword_table;
    size_t keyword_size = 0;
    if (beaufort_produce_table("keyword", DEFAULT_ALPHABET, &keyword_table, &keyword_size, "SECRET") == 0) {
        print_table("Keyword Beaufort Table (keyword=SECRET)", keyword_table, DEFAULT_ALPHABET);
        free_table(keyword_table, keyword_size);
    }
    
    // Atbash table
    char **atbash_table;
    size_t atbash_size = 0;
    if (beaufort_produce_table("atbash", DEFAULT_ALPHABET, &atbash_table, &atbash_size) == 0) {
        print_table("Atbash Beaufort Table", atbash_table, DEFAULT_ALPHABET);
        free_table(atbash_table, atbash_size);
    }
    
    printf("\n5. Turkish Alphabet Support\n");
    const char *turkish_text = "MERHABA DÜNYA";
    const char *turkish_key = "ANAHTAR";
    
    printf("Turkish Plaintext: %s\n", turkish_text);
    printf("Turkish Key: %s\n", turkish_key);
    
    if (beaufort_encrypt(turkish_text, turkish_key, NULL, TURKISH_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Turkish Encrypted: %s\n", encrypted);
        
        if (beaufort_decrypt(encrypted, turkish_key, NULL, TURKISH_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Turkish Decrypted: %s\n", decrypted);
        } else {
            printf("Turkish decryption failed!\n");
        }
    } else {
        printf("Turkish encryption failed!\n");
    }
    
    printf("\n6. Composable System Example\n");
    printf("Using Caesar-produced alphabet with Beaufort\n");
    
    // Generate Caesar alphabet
    char caesar_alphabet[256];
    if (caesar_produce_alphabet(3, DEFAULT_ALPHABET, caesar_alphabet, sizeof(caesar_alphabet)) == 0) {
        printf("Caesar Alphabet (shift=3): %s\n", caesar_alphabet);
        
        const char *composable_text = "TEST MESSAGE";
        const char *composable_key = "TEST";
        
        printf("Plaintext: %s\n", composable_text);
        printf("Key: %s\n", composable_key);
        
        if (beaufort_encrypt(composable_text, composable_key, NULL, caesar_alphabet, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted with Caesar alphabet: %s\n", encrypted);
            
            if (beaufort_decrypt(encrypted, composable_key, NULL, caesar_alphabet, decrypted, sizeof(decrypted)) == 0) {
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
    
    printf("\n=== Beaufort Example Complete ===\n");
    return 0;
}
