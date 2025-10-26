/**
 * @file beaufort.c
 * @brief Beaufort cipher implementation
 * 
 * The Beaufort cipher is a polyalphabetic substitution cipher that is essentially
 * a reverse Vigenère cipher. It uses the same tabula recta but with subtraction
 * instead of addition for encryption.
 */

#include "cryptology/classical/substitution/polyalphabetic/beaufort.h"
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <stdarg.h>

#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

int beaufort_generate_random_key(int length, const char *alphabet, 
                                char *result, size_t result_size) {
    if (length <= 0 || !alphabet || !result || result_size == 0) {
        return -1;
    }
    
    if (strlen(alphabet) == 0) {
        return -1;
    }
    
    if (result_size < (size_t)length + 1) {
        return -1;
    }
    
    // Initialize random seed
    srand((unsigned int)time(NULL));
    
    // Generate random key
    for (int i = 0; i < length; i++) {
        int random_index = rand() % (int)strlen(alphabet);
        result[i] = alphabet[random_index];
    }
    result[length] = '\0';
    
    return 0;
}

int beaufort_generate_key_for_text(const char *plaintext, const char *alphabet,
                                  char *result, size_t result_size) {
    if (!plaintext || !alphabet || !result || result_size == 0) {
        return -1;
    }
    
    // Count only alphabetic characters (spaces are preserved in encryption)
    int alphabetic_chars = 0;
    for (size_t i = 0; plaintext[i] != '\0'; i++) {
        if (isalpha(plaintext[i])) {
            alphabetic_chars++;
        }
    }
    
    return beaufort_generate_random_key(alphabetic_chars, alphabet, result, result_size);
}

int beaufort_encrypt_with_random_key(const char *plaintext, char ***table, 
                                    const char *alphabet, int key_length,
                                    char *encrypted, size_t encrypted_size,
                                    char *generated_key, size_t key_size) {
    if (!plaintext || !alphabet || !encrypted || !generated_key) {
        return -1;
    }
    
    if (strlen(plaintext) == 0) {
        return -1;
    }
    
    // Generate random key
    char *key;
    if (key_length <= 0) {
        // Generate key matching text length
        if (beaufort_generate_key_for_text(plaintext, alphabet, generated_key, key_size) != 0) {
            return -1;
        }
        key = generated_key;
    } else {
        // Generate key of specified length
        if (beaufort_generate_random_key(key_length, alphabet, generated_key, key_size) != 0) {
            return -1;
        }
        key = generated_key;
    }
    
    // Encrypt using the generated key
    return beaufort_encrypt(plaintext, key, table, alphabet, encrypted, encrypted_size);
}

int beaufort_create_classical_table(const char *alphabet, char ***table) {
    if (!alphabet || !table) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Allocate memory for table
    *table = (char**)malloc(alphabet_len * sizeof(char*));
    if (!*table) {
        return -1;
    }
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = (char*)malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Clean up on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
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

int beaufort_create_caesar_table(const char *alphabet, int shift, char ***table) {
    if (!alphabet || !table) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Allocate memory for table
    *table = (char**)malloc(alphabet_len * sizeof(char*));
    if (!*table) {
        return -1;
    }
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = (char*)malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Clean up on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
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

int beaufort_create_affine_table(const char *alphabet, int a, int b, char ***table) {
    if (!alphabet || !table) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Allocate memory for table
    *table = (char**)malloc(alphabet_len * sizeof(char*));
    if (!*table) {
        return -1;
    }
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = (char*)malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Clean up on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
            return -1;
        }
        
        // Each row uses Affine cipher with modified b
        int row_b = b + (int)i;
        for (size_t j = 0; j < alphabet_len; j++) {
            int affine_result = (a * (int)j + row_b) % (int)alphabet_len;
            (*table)[i][j] = alphabet[affine_result];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

int beaufort_create_keyword_table(const char *alphabet, const char *keyword, char ***table) {
    if (!alphabet || !keyword || !table) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Allocate memory for table
    *table = (char**)malloc(alphabet_len * sizeof(char*));
    if (!*table) {
        return -1;
    }
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = (char*)malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Clean up on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
            return -1;
        }
        
        // Each row uses keyword cipher with row character appended
        char row_keyword[256];
        snprintf(row_keyword, sizeof(row_keyword), "%s%c", keyword, alphabet[i]);
        
        char transformed_alphabet[256];
        if (keyword_produce_alphabet(row_keyword, alphabet, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            // Clean up on error
            for (size_t j = 0; j <= i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
            return -1;
        }
        
        for (size_t j = 0; j < alphabet_len; j++) {
            (*table)[i][j] = transformed_alphabet[j];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

int beaufort_create_atbash_table(const char *alphabet, char ***table) {
    if (!alphabet || !table) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len == 0) {
        return -1;
    }
    
    // Allocate memory for table
    *table = (char**)malloc(alphabet_len * sizeof(char*));
    if (!*table) {
        return -1;
    }
    
    for (size_t i = 0; i < alphabet_len; i++) {
        (*table)[i] = (char*)malloc((alphabet_len + 1) * sizeof(char));
        if (!(*table)[i]) {
            // Clean up on error
            for (size_t j = 0; j < i; j++) {
                free((*table)[j]);
            }
            free(*table);
            *table = NULL;
            return -1;
        }
        
        // Each row uses Atbash cipher with rotation by row index
        for (size_t j = 0; j < alphabet_len; j++) {
            int atbash_index = ((int)alphabet_len - 1 - (int)j + (int)i) % (int)alphabet_len;
            (*table)[i][j] = alphabet[atbash_index];
        }
        (*table)[i][alphabet_len] = '\0';
    }
    
    return 0;
}

int beaufort_produce_table(const char *table_type, const char *alphabet, 
                          char ***table, ...) {
    if (!table_type || !alphabet || !table) {
        return -1;
    }
    
    if (strlen(table_type) == 0) {
        return -1;
    }
    
    va_list args;
    va_start(args, table);
    
    int result = -1;
    
    if (strcmp(table_type, "classical") == 0) {
        result = beaufort_create_classical_table(alphabet, table);
    } else if (strcmp(table_type, "caesar") == 0) {
        int shift = va_arg(args, int);
        result = beaufort_create_caesar_table(alphabet, shift, table);
    } else if (strcmp(table_type, "affine") == 0) {
        int a = va_arg(args, int);
        int b = va_arg(args, int);
        result = beaufort_create_affine_table(alphabet, a, b, table);
    } else if (strcmp(table_type, "keyword") == 0) {
        const char *keyword = va_arg(args, const char*);
        result = beaufort_create_keyword_table(alphabet, keyword, table);
    } else if (strcmp(table_type, "atbash") == 0) {
        result = beaufort_create_atbash_table(alphabet, table);
    }
    
    va_end(args);
    return result;
}

int beaufort_prepare_text(const char *text, const char *alphabet,
                         char *result, size_t result_size) {
    if (!text || !alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t result_index = 0;
    
    for (size_t i = 0; text[i] != '\0' && result_index < result_size - 1; i++) {
        char char_upper = toupper(text[i]);
        
        if (isalpha(char_upper)) {
            // Handle custom alphabets
            if (strcmp(alphabet, DEFAULT_ALPHABET) == 0) {
                // Apply language-specific replacements for English alphabet
                if (strstr(alphabet, "ç") || strstr(alphabet, "Ç")) {
                    // Turkish character replacements
                    if (char_upper == 'Ç') {
                        char_upper = 'C';
                    } else if (char_upper == 'Ğ') {
                        char_upper = 'G';
                    } else if (char_upper == 'I') {
                        char_upper = 'I';
                    } else if (char_upper == 'Ö') {
                        char_upper = 'O';
                    } else if (char_upper == 'Ş') {
                        char_upper = 'S';
                    } else if (char_upper == 'Ü') {
                        char_upper = 'U';
                    }
                }
            }
            result[result_index++] = char_upper;
        } else if (char_upper == ' ') {
            result[result_index++] = ' ';  // Preserve spaces
        }
    }
    
    result[result_index] = '\0';
    return 0;
}

int beaufort_prepare_ciphertext(const char *ciphertext,
                               char *result, size_t result_size) {
    if (!ciphertext || !result || result_size == 0) {
        return -1;
    }
    
    size_t result_index = 0;
    
    for (size_t i = 0; ciphertext[i] != '\0' && result_index < result_size - 1; i++) {
        char char_upper = toupper(ciphertext[i]);
        
        if (isalpha(char_upper) || char_upper == ' ') {
            result[result_index++] = char_upper;
        }
    }
    
    result[result_index] = '\0';
    return 0;
}

int beaufort_encrypt(const char *plaintext, const char *key, char ***table,
                    const char *alphabet, char *encrypted, size_t encrypted_size) {
    (void)table;  // Table parameter is not used in current implementation
    if (!plaintext || !key || !alphabet || !encrypted || encrypted_size == 0) {
        return -1;
    }
    
    if (strlen(plaintext) == 0 || strlen(key) == 0) {
        encrypted[0] = '\0';
        return 0;
    }
    
    // Prepare text
    char prepared_text[1024];
    if (beaufort_prepare_text(plaintext, alphabet, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t encrypted_index = 0;
    size_t key_index = 0;
    
    for (size_t i = 0; prepared_text[i] != '\0' && encrypted_index < encrypted_size - 1; i++) {
        if (prepared_text[i] == ' ') {
            encrypted[encrypted_index++] = ' ';
            continue;
        }
        
        // Find character position in alphabet
        const char *char_pos_str = strchr(alphabet, prepared_text[i]);
        if (!char_pos_str) {
            continue;  // Skip characters not in alphabet
        }
        
        size_t char_pos = char_pos_str - alphabet;
        
        // Get key character
        char key_char = key[key_index % strlen(key)];
        const char *key_pos_str = strchr(alphabet, key_char);
        if (!key_pos_str) {
            continue;  // Skip if key character not in alphabet
        }
        
        size_t key_pos = key_pos_str - alphabet;
        
        // Beaufort encryption: always use modular arithmetic (C = (K - P) mod alphabet_len)
        size_t encrypted_pos = (key_pos - char_pos + strlen(alphabet)) % strlen(alphabet);
        encrypted[encrypted_index++] = alphabet[encrypted_pos];
        
        key_index++;  // Only increment key_index when we actually process a character
    }
    
    encrypted[encrypted_index] = '\0';
    return 0;
}

int beaufort_decrypt(const char *ciphertext, const char *key, char ***table,
                    const char *alphabet, char *decrypted, size_t decrypted_size) {
    // Beaufort is self-reciprocal: decryption is the same as encryption
    return beaufort_encrypt(ciphertext, key, table, alphabet, decrypted, decrypted_size);
}
