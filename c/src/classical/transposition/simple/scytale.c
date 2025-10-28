#include "cryptology/classical/transposition/simple/scytale.h"
#include "cryptology/classical/transposition/utf8_helpers.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int scytale_encrypt(const char *plaintext, int key, char *output, size_t output_size) {
    if (!plaintext || !output || key <= 0 || output_size == 0) {
        return -1;
    }
    
    // Clean and normalize text (UTF-8 aware, supports Turkish)
    char *clean_input = malloc(strlen(plaintext) * 3 + 1);  // Extra space for UTF-8
    if (!clean_input) return -1;
    
    if (clean_utf8_text(plaintext, clean_input, strlen(plaintext) * 3 + 1) != 0) {
        free(clean_input);
        return -1;
    }
    
    if (strlen(clean_input) == 0) {
        output[0] = '\0';
        free(clean_input);
        return 0;
    }
    
    size_t text_len = strlen(clean_input);
    size_t rows = (text_len + key - 1) / key;  // Ceiling division
    
    // Create matrix
    char **matrix = malloc(rows * sizeof(char*));
    if (!matrix) {
        free(clean_input);
        return -1;
    }
    
    for (size_t i = 0; i < rows; i++) {
        matrix[i] = malloc(key * sizeof(char));
        if (!matrix[i]) {
            // Clean up allocated memory
            for (size_t j = 0; j < i; j++) {
                free(matrix[j]);
            }
            free(matrix);
            free(clean_input);
            return -1;
        }
    }
    
    // Fill matrix row by row
    size_t text_index = 0;
    for (size_t row = 0; row < rows; row++) {
        for (size_t col = 0; col < key; col++) {
            if (text_index < text_len) {
                matrix[row][col] = clean_input[text_index++];
            } else {
                matrix[row][col] = ' ';  // Padding
            }
        }
    }
    
    // Read column by column
    size_t output_index = 0;
    for (size_t col = 0; col < key && output_index < output_size - 1; col++) {
        for (size_t row = 0; row < rows && output_index < output_size - 1; row++) {
            output[output_index++] = matrix[row][col];
        }
    }
    output[output_index] = '\0';
    
    // Clean up
    for (size_t i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
    free(clean_input);
    
    return 0;
}

int scytale_decrypt(const char *ciphertext, int key, char *output, size_t output_size) {
    if (!ciphertext || !output || key <= 0 || output_size == 0) {
        return -1;
    }
    
    // Clean the ciphertext (UTF-8 aware, supports Turkish)
    char *clean_input = malloc(strlen(ciphertext) * 3 + 1);  // Extra space for UTF-8
    if (!clean_input) return -1;
    
    if (clean_utf8_text(ciphertext, clean_input, strlen(ciphertext) * 3 + 1) != 0) {
        free(clean_input);
        return -1;
    }
    
    if (strlen(clean_input) == 0) {
        output[0] = '\0';
        free(clean_input);
        return 0;
    }
    
    size_t text_len = strlen(clean_input);
    size_t rows = text_len / key;
    if (text_len % key != 0) {
        rows++;
    }
    
    // Create matrix
    char **matrix = malloc(rows * sizeof(char*));
    if (!matrix) {
        free(clean_input);
        return -1;
    }
    
    for (size_t i = 0; i < rows; i++) {
        matrix[i] = malloc(key * sizeof(char));
        if (!matrix[i]) {
            // Clean up allocated memory
            for (size_t j = 0; j < i; j++) {
                free(matrix[j]);
            }
            free(matrix);
            free(clean_input);
            return -1;
        }
    }
    
    // Fill matrix column by column
    size_t text_index = 0;
    for (size_t col = 0; col < key; col++) {
        for (size_t row = 0; row < rows; row++) {
            if (text_index < text_len) {
                matrix[row][col] = clean_input[text_index++];
            }
        }
    }
    
    // Read row by row
    size_t output_index = 0;
    for (size_t row = 0; row < rows && output_index < output_size - 1; row++) {
        for (size_t col = 0; col < key && output_index < output_size - 1; col++) {
            output[output_index++] = matrix[row][col];
        }
    }
    output[output_index] = '\0';
    
    // Clean up
    for (size_t i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
    free(clean_input);
    
    return 0;
}

void scytale_get_key_range(size_t text_length, int *min_key, int *max_key) {
    if (text_length <= 0) {
        *min_key = 0;
        *max_key = 0;
    } else {
        *min_key = 1;
        *max_key = (int)text_length;
    }
}
