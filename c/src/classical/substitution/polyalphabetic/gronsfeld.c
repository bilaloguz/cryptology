/**
 * @file gronsfeld.c
 * @brief Gronsfeld Cipher implementation with customizable tables
 */

#include "cryptology/classical/substitution/polyalphabetic/gronsfeld.h"
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

// Helper function to validate numeric key
static int validate_numeric_key(const char* key) {
    if (!key || strlen(key) == 0) {
        return -1;
    }
    
    for (const char* p = key; *p; p++) {
        if (!isdigit(*p)) {
            return -1;
        }
    }
    
    return 0;
}

// Helper function to find character position in alphabet
static int find_char_position(const char* alphabet, char c) {
    char upper_c = toupper(c);
    const char* pos = strchr(alphabet, upper_c);
    if (pos) {
        return pos - alphabet;
    }
    return -1;
}

// Helper function to calculate GCD
static int gcd(int a, int b) {
    while (b) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Helper function to create classical table
static int create_classical_table(const char* alphabet, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    // Allocate memory for table
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
        
        // Create Caesar-shifted alphabet for this row
        char shifted_alphabet[64];
        if (caesar_produce_alphabet(i, alphabet, shifted_alphabet, sizeof(shifted_alphabet)) != 0) {
            // Cleanup on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Copy to table row
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = shifted_alphabet[j];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Helper function to create Caesar-based table
static int create_caesar_table(const char* alphabet, int shift, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    // Allocate memory for table
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
        
        // Create Caesar-shifted alphabet for this row
        int row_shift = (shift + i) % alphabet_len;
        char shifted_alphabet[64];
        if (caesar_produce_alphabet(row_shift, alphabet, shifted_alphabet, sizeof(shifted_alphabet)) != 0) {
            // Cleanup on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Copy to table row
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = shifted_alphabet[j];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Helper function to create Affine-based table
static int create_affine_table(const char* alphabet, int a, int b, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    // Ensure base 'a' is coprime with alphabet length
    if (a == 0) a = 1;
    
    // Allocate memory for table
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
        
        // Calculate row parameters
        int row_a = (a + i) % alphabet_len;
        int row_b = (b + i) % alphabet_len;
        
        // Ensure row_a is coprime with alphabet length
        if (row_a == 0) row_a = 1;
        
        // Find next coprime number if needed
        while (row_a < alphabet_len && gcd(row_a, alphabet_len) != 1) {
            row_a++;
        }
        
        // If we can't find a coprime, use 1
        if (row_a >= alphabet_len) row_a = 1;
        
        // Create Affine-transformed alphabet for this row
        char transformed_alphabet[64];
        if (affine_produce_alphabet(row_a, row_b, alphabet, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            // Cleanup on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Copy to table row
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = transformed_alphabet[j];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Helper function to create Keyword-based table
static int create_keyword_table(const char* alphabet, const char* keyword, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    // Allocate memory for table
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
        
        // Create modified keyword for this row
        char row_keyword[64];
        snprintf(row_keyword, sizeof(row_keyword), "%s%c", keyword, alphabet[i]);
        
        // Create Keyword-transformed alphabet for this row
        char transformed_alphabet[64];
        if (keyword_produce_alphabet(row_keyword, alphabet, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            // Cleanup on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            return -1;
        }
        
        // Copy to table row
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = transformed_alphabet[j];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

// Helper function to create Atbash-based table
static int create_atbash_table(const char* alphabet, char*** table, size_t* table_size) {
    size_t alphabet_len = strlen(alphabet);
    *table_size = alphabet_len;
    
    // Allocate memory for table
    *table = malloc(alphabet_len * sizeof(char*));
    if (!*table) return -1;
    
    // Create reversed alphabet
    char reversed_alphabet[64];
    if (atbash_produce_alphabet(alphabet, reversed_alphabet, sizeof(reversed_alphabet)) != 0) {
        free(*table);
        return -1;
    }
    
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
        
        // Rotate the reversed alphabet by row index
        for (size_t j = 0; j < alphabet_len; j++) {
            size_t rotated_index = (i + j) % alphabet_len;
            (*table)[i][j] = reversed_alphabet[rotated_index];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

int gronsfeld_produce_table(const char *table_type,
                           const char *alphabet,
                           char ***table,
                           size_t *table_size,
                           ...) {
    if (!table_type || !table || !table_size) {
        return -1;
    }
    
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_ALPHABET;
    }
    
    va_list args;
    va_start(args, table_size);
    
    int result = -1;
    
    if (strcmp(table_type, "classical") == 0) {
        result = create_classical_table(use_alphabet, table, table_size);
    }
    else if (strcmp(table_type, "caesar") == 0) {
        int shift = va_arg(args, int);
        result = create_caesar_table(use_alphabet, shift, table, table_size);
    }
    else if (strcmp(table_type, "affine") == 0) {
        int a = va_arg(args, int);
        int b = va_arg(args, int);
        result = create_affine_table(use_alphabet, a, b, table, table_size);
    }
    else if (strcmp(table_type, "keyword") == 0) {
        const char* keyword = va_arg(args, const char*);
        result = create_keyword_table(use_alphabet, keyword, table, table_size);
    }
    else if (strcmp(table_type, "atbash") == 0) {
        result = create_atbash_table(use_alphabet, table, table_size);
    }
    
    va_end(args);
    return result;
}

int gronsfeld_encrypt(const char *plaintext,
                     const char *key,
                     char ***table,
                     const char *alphabet,
                     char *result, size_t result_size) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    // Validate numeric key
    if (validate_numeric_key(key) != 0) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    char** use_table = table ? *table : NULL;
    
    // Create table if none provided
    char** temp_table = NULL;
    if (!use_table) {
        size_t table_size;
        if (gronsfeld_produce_table("classical", use_alphabet, &temp_table, &table_size) != 0) {
            return -1;
        }
        use_table = temp_table;
    }
    
    char prepared_text[1000];
    prepare_text(plaintext, prepared_text, use_alphabet);
    
    size_t key_index = 0;
    size_t result_pos = 0;
    
    for (const char* p = prepared_text; *p && result_pos < result_size - 1; p++) {
        if (isalpha(*p)) {
            // Get the shift value from the numeric key
            int shift = key[key_index % strlen(key)] - '0';
            
            // Find character position in alphabet
            int char_pos = find_char_position(use_alphabet, *p);
            if (char_pos == -1) {
                if (temp_table) {
                    // Cleanup temp table
                    size_t alphabet_len = strlen(use_alphabet);
                    for (size_t i = 0; i < alphabet_len; i++) {
                        free(temp_table[i]);
                    }
                    free(temp_table);
                }
                return -1;
            }
            
            // Apply shift using the table
            char encrypted_char = use_table[shift][char_pos];
            
            // Preserve case
            if (islower(*p)) {
                encrypted_char = tolower(encrypted_char);
            }
            
            result[result_pos++] = encrypted_char;
            key_index++;
        } else {
            // Preserve non-alphabetic characters
            result[result_pos++] = *p;
        }
    }
    
    result[result_pos] = '\0';
    
    // Cleanup temp table if we created it
    if (temp_table) {
        size_t alphabet_len = strlen(use_alphabet);
        for (size_t i = 0; i < alphabet_len; i++) {
            free(temp_table[i]);
        }
        free(temp_table);
    }
    
    return 0;
}

int gronsfeld_decrypt(const char *ciphertext,
                     const char *key,
                     char ***table,
                     const char *alphabet,
                     char *result, size_t result_size) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    // Validate numeric key
    if (validate_numeric_key(key) != 0) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    char** use_table = table ? *table : NULL;
    
    // Create table if none provided
    char** temp_table = NULL;
    if (!use_table) {
        size_t table_size;
        if (gronsfeld_produce_table("classical", use_alphabet, &temp_table, &table_size) != 0) {
            return -1;
        }
        use_table = temp_table;
    }
    
    char prepared_ciphertext[1000];
    prepare_ciphertext(ciphertext, prepared_ciphertext);
    
    size_t key_index = 0;
    size_t result_pos = 0;
    
    for (const char* p = prepared_ciphertext; *p && result_pos < result_size - 1; p++) {
        if (isalpha(*p)) {
            // Get the shift value from the numeric key
            int shift = key[key_index % strlen(key)] - '0';
            
            // Find character position in the shifted alphabet (table row)
            int char_pos = find_char_position(use_table[shift], *p);
            if (char_pos == -1) {
                if (temp_table) {
                    // Cleanup temp table
                    size_t alphabet_len = strlen(use_alphabet);
                    for (size_t i = 0; i < alphabet_len; i++) {
                        free(temp_table[i]);
                    }
                    free(temp_table);
                }
                return -1;
            }
            
            // Get original character from base alphabet
            char decrypted_char = use_alphabet[char_pos];
            
            // Preserve case
            if (islower(*p)) {
                decrypted_char = tolower(decrypted_char);
            }
            
            result[result_pos++] = decrypted_char;
            key_index++;
        } else {
            // Preserve non-alphabetic characters
            result[result_pos++] = *p;
        }
    }
    
    result[result_pos] = '\0';
    
    // Cleanup temp table if we created it
    if (temp_table) {
        size_t alphabet_len = strlen(use_alphabet);
        for (size_t i = 0; i < alphabet_len; i++) {
            free(temp_table[i]);
        }
        free(temp_table);
    }
    
    return 0;
}

int gronsfeld_generate_random_numeric_key(int length,
                                         char *result, size_t result_size) {
    if (length <= 0 || !result || result_size == 0) {
        return -1;
    }
    
    if (result_size < length + 1) {
        return -1;
    }
    
    srand(time(NULL));
    
    for (int i = 0; i < length; i++) {
        result[i] = '0' + (rand() % 10);
    }
    
    result[length] = '\0';
    return 0;
}

int gronsfeld_generate_numeric_key_for_text(const char *plaintext,
                                           char *result, size_t result_size) {
    if (!plaintext || !result || result_size == 0) {
        return -1;
    }
    
    // Count alphabetic characters
    int alphabetic_chars = 0;
    for (const char* p = plaintext; *p; p++) {
        if (isalpha(*p)) {
            alphabetic_chars++;
        }
    }
    
    return gronsfeld_generate_random_numeric_key(alphabetic_chars, result, result_size);
}

int gronsfeld_encrypt_with_random_key(const char *plaintext,
                                     char ***table,
                                     const char *alphabet,
                                     int key_length,
                                     char *encrypted_result, size_t encrypted_size,
                                     char *key_result, size_t key_size) {
    if (!plaintext || !encrypted_result || !key_result || 
        encrypted_size == 0 || key_size == 0) {
        return -1;
    }
    
    // Generate random key
    int actual_key_length = key_length;
    if (actual_key_length <= 0) {
        // Count alphabetic characters
        actual_key_length = 0;
        for (const char* p = plaintext; *p; p++) {
            if (isalpha(*p)) {
                actual_key_length++;
            }
        }
    }
    
    if (gronsfeld_generate_random_numeric_key(actual_key_length, key_result, key_size) != 0) {
        return -1;
    }
    
    // Encrypt using the generated key
    return gronsfeld_encrypt(plaintext, key_result, table, alphabet, 
                            encrypted_result, encrypted_size);
}
