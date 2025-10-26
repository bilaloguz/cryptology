/**
 * @file vigenere_example.c
 * @brief Example demonstrating the Vigenère cipher with customizable tables
 * 
 * This example shows how the Vigenère cipher works with different table types,
 * including classical tabula recta and custom tables generated using monoalphabetic ciphers.
 */

#include "cryptology/classical/substitution/polyalphabetic/vigenere.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFFER_SIZE 1024

void demonstrate_classical_vigenere() {
    printf("=== Classical Vigenère Cipher Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Encrypt
    if (vigenere_encrypt(plaintext, key, NULL, NULL, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (vigenere_decrypt(encrypted, key, NULL, NULL, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        }
    }
    printf("\n");
}

void demonstrate_caesar_table() {
    printf("=== Vigenère with Caesar Table Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    int shift = 3;
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Caesar shift: %d\n", shift);
    printf("\n");
    
    // Generate Caesar table
    char **caesar_table = NULL;
    size_t table_size = 0;
    if (vigenere_produce_table("caesar", NULL, &caesar_table, &table_size, shift) == 0) {
        printf("Caesar table generated (each row shifts by base_shift + row_index)\n");
        printf("\n");
        
        // Encrypt
        if (vigenere_encrypt(plaintext, key, &caesar_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Decrypt
            if (vigenere_decrypt(encrypted, key, &caesar_table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
            }
        }
        
        // Clean up table
        for (size_t i = 0; i < table_size; i++) {
            free(caesar_table[i]);
        }
        free(caesar_table);
    }
    printf("\n");
}

void demonstrate_affine_table() {
    printf("=== Vigenère with Affine Table Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    int a = 3, b = 5;
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Affine parameters: a=%d, b=%d\n", a, b);
    printf("\n");
    
    // Generate Affine table
    char **affine_table = NULL;
    size_t table_size = 0;
    if (vigenere_produce_table("affine", NULL, &affine_table, &table_size, a, b) == 0) {
        printf("Affine table generated (each row uses a*x + (b + row_index) mod 26)\n");
        printf("\n");
        
        // Encrypt
        if (vigenere_encrypt(plaintext, key, &affine_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Decrypt
            if (vigenere_decrypt(encrypted, key, &affine_table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
            }
        }
        
        // Clean up table
        for (size_t i = 0; i < table_size; i++) {
            free(affine_table[i]);
        }
        free(affine_table);
    }
    printf("\n");
}

void demonstrate_keyword_table() {
    printf("=== Vigenère with Keyword Table Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    const char *keyword = "SECRET";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Keyword: %s\n", keyword);
    printf("\n");
    
    // Generate Keyword table
    char **keyword_table = NULL;
    size_t table_size = 0;
    if (vigenere_produce_table("keyword", NULL, &keyword_table, &table_size, keyword) == 0) {
        printf("Keyword table generated (each row uses keyword + row_character)\n");
        printf("\n");
        
        // Encrypt
        if (vigenere_encrypt(plaintext, key, &keyword_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Decrypt
            if (vigenere_decrypt(encrypted, key, &keyword_table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
            }
        }
        
        // Clean up table
        for (size_t i = 0; i < table_size; i++) {
            free(keyword_table[i]);
        }
        free(keyword_table);
    }
    printf("\n");
}

void demonstrate_atbash_table() {
    printf("=== Vigenère with Atbash Table Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Generate Atbash table
    char **atbash_table = NULL;
    size_t table_size = 0;
    if (vigenere_produce_table("atbash", NULL, &atbash_table, &table_size) == 0) {
        printf("Atbash table generated (each row uses Atbash with rotation)\n");
        printf("\n");
        
        // Encrypt
        if (vigenere_encrypt(plaintext, key, &atbash_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Decrypt
            if (vigenere_decrypt(encrypted, key, &atbash_table, NULL, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
            }
        }
        
        // Clean up table
        for (size_t i = 0; i < table_size; i++) {
            free(atbash_table[i]);
        }
        free(atbash_table);
    }
    printf("\n");
}

void demonstrate_turkish_alphabet() {
    printf("=== Vigenère with Turkish Alphabet Demo ===\n");
    
    const char *turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ";
    const char *plaintext = "MERHABA DÜNYA";
    const char *key = "ANAHTAR";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Turkish Alphabet: %s\n", turkish_alphabet);
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Generate Turkish table
    char **turkish_table = NULL;
    size_t table_size = 0;
    if (vigenere_produce_table("classical", turkish_alphabet, &turkish_table, &table_size) == 0) {
        printf("Turkish table generated (29x29)\n");
        printf("\n");
        
        // Encrypt
        if (vigenere_encrypt(plaintext, key, &turkish_table, turkish_alphabet, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted: %s\n", encrypted);
            
            // Decrypt
            if (vigenere_decrypt(encrypted, key, &turkish_table, turkish_alphabet, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted: %s\n", decrypted);
            }
        }
        
        // Clean up table
        for (size_t i = 0; i < table_size; i++) {
            free(turkish_table[i]);
        }
        free(turkish_table);
    }
    printf("\n");
}

void demonstrate_table_comparison() {
    printf("=== Table Comparison Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "KEY";
    char encrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Generate different tables
    char **classical_table = NULL;
    char **caesar_table = NULL;
    char **affine_table = NULL;
    char **keyword_table = NULL;
    char **atbash_table = NULL;
    
    size_t classical_size = 0, caesar_size = 0, affine_size = 0, keyword_size = 0, atbash_size = 0;
    
    if (vigenere_produce_table("classical", NULL, &classical_table, &classical_size) == 0 &&
        vigenere_produce_table("caesar", NULL, &caesar_table, &caesar_size, 5) == 0 &&
        vigenere_produce_table("affine", NULL, &affine_table, &affine_size, 3, 7) == 0 &&
        vigenere_produce_table("keyword", NULL, &keyword_table, &keyword_size, "SECRET") == 0 &&
        vigenere_produce_table("atbash", NULL, &atbash_table, &atbash_size) == 0) {
        
        printf("All tables generated successfully!\n");
        printf("\n");
        
        // Encrypt with different tables
        if (vigenere_encrypt(plaintext, key, &classical_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Classical table encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &caesar_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Caesar table encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &affine_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Affine table encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &keyword_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Keyword table encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &atbash_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Atbash table encrypted: %s\n", encrypted);
        }
        
        // Clean up all tables
        for (size_t i = 0; i < classical_size; i++) free(classical_table[i]);
        for (size_t i = 0; i < caesar_size; i++) free(caesar_table[i]);
        for (size_t i = 0; i < affine_size; i++) free(affine_table[i]);
        for (size_t i = 0; i < keyword_size; i++) free(keyword_table[i]);
        for (size_t i = 0; i < atbash_size; i++) free(atbash_table[i]);
        
        free(classical_table);
        free(caesar_table);
        free(affine_table);
        free(keyword_table);
        free(atbash_table);
    }
    printf("\n");
}

void demonstrate_security_analysis() {
    printf("=== Security Analysis Demo ===\n");
    
    const char *plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    const char *key = "SECRET";
    char encrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Generate different tables for security comparison
    char **classical_table = NULL;
    char **caesar_table = NULL;
    char **affine_table = NULL;
    
    size_t classical_size = 0, caesar_size = 0, affine_size = 0;
    
    if (vigenere_produce_table("classical", NULL, &classical_table, &classical_size) == 0 &&
        vigenere_produce_table("caesar", NULL, &caesar_table, &caesar_size, 13) == 0 &&
        vigenere_produce_table("affine", NULL, &affine_table, &affine_size, 5, 11) == 0) {
        
        printf("Security Analysis:\n");
        printf("- Classical Vigenère: Vulnerable to frequency analysis\n");
        printf("- Caesar-based Vigenère: Still vulnerable to frequency analysis\n");
        printf("- Affine-based Vigenère: More complex, harder to break\n");
        printf("\n");
        
        // Encrypt with different tables
        if (vigenere_encrypt(plaintext, key, &classical_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Classical encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &caesar_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Caesar encrypted: %s\n", encrypted);
        }
        
        if (vigenere_encrypt(plaintext, key, &affine_table, NULL, encrypted, sizeof(encrypted)) == 0) {
            printf("Affine encrypted: %s\n", encrypted);
        }
        
        // Clean up tables
        for (size_t i = 0; i < classical_size; i++) free(classical_table[i]);
        for (size_t i = 0; i < caesar_size; i++) free(caesar_table[i]);
        for (size_t i = 0; i < affine_size; i++) free(affine_table[i]);
        
        free(classical_table);
        free(caesar_table);
        free(affine_table);
    }
    printf("\n");
}

int main() {
    printf("=== Vigenère Cipher Example ===\n");
    printf("This example demonstrates the Vigenère cipher with customizable tables.\n");
    printf("Different table types provide varying levels of security.\n");
    printf("\n");
    
    demonstrate_classical_vigenere();
    demonstrate_caesar_table();
    demonstrate_affine_table();
    demonstrate_keyword_table();
    demonstrate_atbash_table();
    demonstrate_turkish_alphabet();
    demonstrate_table_comparison();
    demonstrate_security_analysis();
    
    printf("=== Vigenère Example Complete ===\n");
    return 0;
}