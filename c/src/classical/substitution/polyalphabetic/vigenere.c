/**
 * @file vigenere.c
 * @brief Vigenère Cipher implementation with customizable tables
 */

#include "cryptology/classical/substitution/polyalphabetic/vigenere.h"
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include <time.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>

#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

// Helper function to prepare text for encryption
static void prepare_text(const char* text, char* result, const char* alphabet) {
    int pos = 0;
    for (const char* p = text; *p && pos < 1000; p++) {
        char c = toupper(*p);
        if (isalpha(c)) {
            // Handle custom alphabets
            if (strcmp(alphabet, DEFAULT_ALPHABET) != 0) {
                // Apply language-specific replacements
                if (strchr(alphabet, 'Ç') || strchr(alphabet, 'ç')) {
                    // Turkish character replacements
                    if (c == 'Ç') c = 'C';
                    else if (c == 'Ğ') c = 'G';
                    else if (c == 'I') c = 'I';
                    else if (c == 'Ö') c = 'O';
                    else if (c == 'Ş') c = 'S';
                    else if (c == 'Ü') c = 'U';
                }
            }
            result[pos++] = c;
        } else if (c == ' ') {
            result[pos++] = ' ';  // Preserve spaces
        }
    }
    result[pos] = '\0';
}

// Helper function to prepare ciphertext for decryption
static void prepare_ciphertext(const char* ciphertext, char* result) {
    int pos = 0;
    for (const char* p = ciphertext; *p && pos < 1000; p++) {
        char c = toupper(*p);
        if (isalpha(c) || c == ' ') {
            result[pos++] = c;
        }
    }
    result[pos] = '\0';
}

// Create classical Vigenère table
static int create_classical_table(const char* alphabet, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Cleanup on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Each row is a Caesar cipher shifted by row index
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = alphabet[(j + i) % alphabet_len];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Create Caesar-based Vigenère table
static int create_caesar_table(const char* alphabet, int shift, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Cleanup on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Each row uses Caesar cipher with base_shift + row_index
        int row_shift = shift + (int)i;
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = alphabet[(j + row_shift) % alphabet_len];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Create Affine-based Vigenère table
static int create_affine_table(const char* alphabet, int a, int b, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Cleanup on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Each row uses Affine cipher with modified b
        int row_b = b + (int)i;
        for (size_t j = 0; j < alphabet_len; j++) {
            int affine_result = (a * (int)j + row_b) % (int)alphabet_len;
            if (affine_result < 0) affine_result += (int)alphabet_len;
            (*table)[i][j] = alphabet[affine_result];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Create Keyword-based Vigenère table
static int create_keyword_table(const char* alphabet, const char* keyword, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Cleanup on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Each row uses keyword cipher with row character appended
        char row_keyword[100];
        snprintf(row_keyword, sizeof(row_keyword), "%s%c", keyword, alphabet[i]);
        
        // Generate transformed alphabet for this row
        char transformed_alphabet[100];
        if (keyword_produce_alphabet(row_keyword, alphabet, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            // Cleanup on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        strcpy((*table)[i], transformed_alphabet);
    }
    
    return 0;
}

// Create Atbash-based Vigenère table
static int create_atbash_table(const char* alphabet, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Cleanup on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Each row uses Atbash cipher with rotation by row index
        for (size_t j = 0; j < alphabet_len; j++) {
            size_t atbash_index = (alphabet_len - 1 - j + i) % alphabet_len;
            (*table)[i][j] = alphabet[atbash_index];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

int vigenere_produce_table(const char *table_type,
                          const char *alphabet,
                          char ***table,
                          size_t *table_size,
                          ...) {
    if (!table_type || !alphabet || !table || !table_size) {
        return -1;
    }
    
    va_list args;
    va_start(args, table_size);
    
    int result = -1;
    
    if (strcmp(table_type, "classical") == 0) {
        result = create_classical_table(alphabet, table, table_size);
    }
    else if (strcmp(table_type, "caesar") == 0) {
        int shift = va_arg(args, int);
        result = create_caesar_table(alphabet, shift, table, table_size);
    }
    else if (strcmp(table_type, "affine") == 0) {
        int a = va_arg(args, int);
        int b = va_arg(args, int);
        result = create_affine_table(alphabet, a, b, table, table_size);
    }
    else if (strcmp(table_type, "keyword") == 0) {
        const char* keyword = va_arg(args, const char*);
        result = create_keyword_table(alphabet, keyword, table, table_size);
    }
    else if (strcmp(table_type, "atbash") == 0) {
        result = create_atbash_table(alphabet, table, table_size);
    }
    
    va_end(args);
    return result;
}

int vigenere_encrypt(const char *plaintext,
                    const char *key,
                    char ***table,
                    const char *alphabet,
                    char *result, size_t result_size) {
    if (!plaintext || !key || !result) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    char*** use_table = table;
    
    // Generate table if not provided
    if (!use_table) {
        size_t table_size;
        char** temp_table;
        if (vigenere_produce_table("classical", use_alphabet, &temp_table, &table_size) != 0) {
            return -1;
        }
        use_table = &temp_table;
    }
    
    char prepared_text[1000];
    prepare_text(plaintext, prepared_text, use_alphabet);
    
    size_t key_len = strlen(key);
    size_t text_len = strlen(prepared_text);
    
    size_t result_pos = 0;
    size_t key_index = 0;
    
    for (size_t i = 0; i < text_len && result_pos < result_size - 1; i++) {
        char c = prepared_text[i];
        
        if (c == ' ') {
            result[result_pos++] = ' ';
            continue;
        }
        
        // Find character in alphabet
        const char* char_pos = strchr(use_alphabet, c);
        if (!char_pos) continue;
        
        size_t char_index = char_pos - use_alphabet;
        char key_char = key[key_index % key_len];
        
        // Find key character in alphabet
        const char* key_pos = strchr(use_alphabet, key_char);
        if (!key_pos) continue;
        
        size_t key_char_index = key_pos - use_alphabet;
        
        // Use table for encryption
        result[result_pos++] = (*use_table)[key_char_index][char_index];
        key_index++;
    }
    
    result[result_pos] = '\0';
    
    if (!table) {
        // Free the table we created
        size_t table_size = strlen(use_alphabet);
        for (size_t i = 0; i < table_size; i++) {
            free((*use_table)[i]);
        }
        free(*use_table);
    }
    
    return 0;
}

int vigenere_decrypt(const char *ciphertext,
                    const char *key,
                    char ***table,
                    const char *alphabet,
                    char *result, size_t result_size) {
    if (!ciphertext || !key || !result) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    char*** use_table = table;
    
    // Generate table if not provided
    if (!use_table) {
        size_t table_size;
        char** temp_table;
        if (vigenere_produce_table("classical", use_alphabet, &temp_table, &table_size) != 0) {
            return -1;
        }
        use_table = &temp_table;
    }
    
    char prepared_ciphertext[1000];
    prepare_ciphertext(ciphertext, prepared_ciphertext);
    
    size_t key_len = strlen(key);
    size_t text_len = strlen(prepared_ciphertext);
    
    size_t result_pos = 0;
    size_t key_index = 0;
    
    for (size_t i = 0; i < text_len && result_pos < result_size - 1; i++) {
        char c = prepared_ciphertext[i];
        
        if (c == ' ') {
            result[result_pos++] = ' ';
            continue;
        }
        
        // Find key character in alphabet
        char key_char = key[key_index % key_len];
        const char* key_pos = strchr(use_alphabet, key_char);
        if (!key_pos) continue;
        
        size_t key_char_index = key_pos - use_alphabet;
        
        // Find ciphertext character in the key row
        const char* char_pos = strchr((*use_table)[key_char_index], c);
        if (!char_pos) continue;
        
        size_t char_index = char_pos - (*use_table)[key_char_index];
        result[result_pos++] = use_alphabet[char_index];
        key_index++;
    }
    
    result[result_pos] = '\0';
    
    if (!table) {
        // Free the table we created
        size_t table_size = strlen(use_alphabet);
        for (size_t i = 0; i < table_size; i++) {
            free((*use_table)[i]);
        }
        free(*use_table);
    }
    
    return 0;
}

// Random key generation functions

int vigenere_generate_random_key(int length, const char *alphabet,
                                char *result, size_t result_size) {
    if (length <= 0 || !result || result_size < (size_t)(length + 1)) {
        return -1;
    }
    
    const char *use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    size_t alphabet_len = strlen(use_alphabet);
    
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Initialize random seed
    srand(time(NULL));
    
    // Generate random key
    for (int i = 0; i < length; i++) {
        int random_index = rand() % alphabet_len;
        result[i] = use_alphabet[random_index];
    }
    
    result[length] = '\0';
    return 0;
}

int vigenere_generate_key_for_text(const char *plaintext, const char *alphabet,
                                  char *result, size_t result_size) {
    if (!plaintext || !result) {
        return -1;
    }
    
    // Count alphabetic characters
    int alphabetic_count = 0;
    for (const char *p = plaintext; *p; p++) {
        if (isalpha(*p)) {
            alphabetic_count++;
        }
    }
    
    if (alphabetic_count == 0) {
        result[0] = '\0';
        return 0;
    }
    
    return vigenere_generate_random_key(alphabetic_count, alphabet, result, result_size);
}

int vigenere_encrypt_with_random_key(const char *plaintext, char ***table,
                                   const char *alphabet, int key_length,
                                   char *encrypted, size_t encrypted_size,
                                   char *generated_key, size_t key_size) {
    if (!plaintext || !encrypted || !generated_key) {
        return -1;
    }
    
    // Generate random key
    int actual_key_length = key_length;
    if (actual_key_length <= 0) {
        // Count alphabetic characters for auto key length
        actual_key_length = 0;
        for (const char *p = plaintext; *p; p++) {
            if (isalpha(*p)) {
                actual_key_length++;
            }
        }
    }
    
    if (vigenere_generate_random_key(actual_key_length, alphabet, 
                                   generated_key, key_size) != 0) {
        return -1;
    }
    
    // Encrypt using the generated key
    return vigenere_encrypt(plaintext, generated_key, table, alphabet, 
                          encrypted, encrypted_size);
}
