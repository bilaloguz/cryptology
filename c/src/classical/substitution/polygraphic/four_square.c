/**
 * @file four_square.c
 * @brief Four Square Cipher implementation
 */

#include "cryptology/classical/substitution/polygraphic/four_square.h"
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_KEY_SIZE 256
#define SQUARE_SIZE 5

static int find_char_in_square(char square[SQUARE_SIZE][SQUARE_SIZE], char c, int *row, int *col) {
    for (int i = 0; i < SQUARE_SIZE; i++) {
        for (int j = 0; j < SQUARE_SIZE; j++) {
            if (square[i][j] == c) {
                *row = i;
                *col = j;
                return 0;
            }
        }
    }
    return -1;
}

static int create_key_square(const char *key, char square[SQUARE_SIZE][SQUARE_SIZE]) {
    if (!key) {
        return -1;
    }
    
    bool seen[26] = {false};
    int pos = 0;
    
    // Add keyword letters (removing duplicates)
    for (size_t i = 0; key[i] != '\0' && pos < 25; i++) {
        char c = toupper((unsigned char)key[i]);
        if (c >= 'A' && c <= 'Z') {
            int idx = c - 'A';
            if (!seen[idx]) {
                square[pos / SQUARE_SIZE][pos % SQUARE_SIZE] = c;
                seen[idx] = true;
                pos++;
            }
        }
    }
    
    // Add remaining letters (I and J are combined)
    for (char c = 'A'; c <= 'Z' && pos < 25; c++) {
        if (c == 'J') continue; // Skip J, I and J are combined
        int idx = c - 'A';
        if (!seen[idx]) {
            square[pos / SQUARE_SIZE][pos % SQUARE_SIZE] = c;
            pos++;
        }
    }
    
    return 0;
}

static int prepare_text(const char *input, char *output, size_t output_size) {
    if (!input || !output || output_size == 0) {
        return -1;
    }
    
    size_t input_len = strlen(input);
    size_t output_pos = 0;
    
    for (size_t i = 0; i < input_len && output_pos < output_size - 1; i++) {
        char c = toupper((unsigned char)input[i]);
        if (c >= 'A' && c <= 'Z') {
            // Replace J with I
            if (c == 'J') {
                c = 'I';
            }
            output[output_pos++] = c;
        }
    }
    
    // Add X padding for odd length
    if (output_pos % 2 == 1) {
        if (output_pos < output_size - 1) {
            output[output_pos++] = 'X';
        }
    }
    
    output[output_pos] = '\0';
    return 0;
}

static int encrypt_digram(char square1[SQUARE_SIZE][SQUARE_SIZE], 
                         char square2[SQUARE_SIZE][SQUARE_SIZE],
                         char square3[SQUARE_SIZE][SQUARE_SIZE],
                         char square4[SQUARE_SIZE][SQUARE_SIZE],
                         char char1, char char2, char *result) {
    int row1, col1, row2, col2;
    
    if (find_char_in_square(square1, char1, &row1, &col1) != 0 ||
        find_char_in_square(square4, char2, &row2, &col2) != 0) {
        return -1;
    }
    
    // Use the intersection of the row from square1 and column from square4
    // in square2, and the intersection of the column from square1 and row from square4
    // in square3
    result[0] = square2[row1][col2];
    result[1] = square3[row2][col1];
    
    return 0;
}

static int decrypt_digram(char square1[SQUARE_SIZE][SQUARE_SIZE], 
                         char square2[SQUARE_SIZE][SQUARE_SIZE],
                         char square3[SQUARE_SIZE][SQUARE_SIZE],
                         char square4[SQUARE_SIZE][SQUARE_SIZE],
                         char char1, char char2, char *result) {
    int row1, col1, row2, col2;
    
    if (find_char_in_square(square2, char1, &row1, &col1) != 0 ||
        find_char_in_square(square3, char2, &row2, &col2) != 0) {
        return -1;
    }
    
    // Use the intersection of the row from square2 and column from square3
    // in square1, and the intersection of the column from square2 and row from square3
    // in square4
    result[0] = square1[row1][col2];
    result[1] = square4[row2][col1];
    
    return 0;
}

int four_square_encrypt(const char *plaintext, const char *key1, const char *key2,
                        const char *key3, const char *key4,
                        char *result, size_t result_size) {
    if (!plaintext || !key1 || !key2 || !key3 || !key4 || !result || result_size == 0) {
        return -1;
    }
    
    char square1[SQUARE_SIZE][SQUARE_SIZE];
    char square2[SQUARE_SIZE][SQUARE_SIZE];
    char square3[SQUARE_SIZE][SQUARE_SIZE];
    char square4[SQUARE_SIZE][SQUARE_SIZE];
    
    if (create_key_square(key1, square1) != 0 || create_key_square(key2, square2) != 0 ||
        create_key_square(key3, square3) != 0 || create_key_square(key4, square4) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(plaintext, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += 2) {
        if (i + 1 < prepared_len) {
            char digram[3];
            if (encrypt_digram(square1, square2, square3, square4, 
                              prepared_text[i], prepared_text[i + 1], digram) != 0) {
                return -1;
            }
            result[i] = digram[0];
            result[i + 1] = digram[1];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}

int four_square_decrypt(const char *ciphertext, const char *key1, const char *key2,
                        const char *key3, const char *key4,
                        char *result, size_t result_size) {
    if (!ciphertext || !key1 || !key2 || !key3 || !key4 || !result || result_size == 0) {
        return -1;
    }
    
    char square1[SQUARE_SIZE][SQUARE_SIZE];
    char square2[SQUARE_SIZE][SQUARE_SIZE];
    char square3[SQUARE_SIZE][SQUARE_SIZE];
    char square4[SQUARE_SIZE][SQUARE_SIZE];
    
    if (create_key_square(key1, square1) != 0 || create_key_square(key2, square2) != 0 ||
        create_key_square(key3, square3) != 0 || create_key_square(key4, square4) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(ciphertext, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += 2) {
        if (i + 1 < prepared_len) {
            char digram[3];
            if (decrypt_digram(square1, square2, square3, square4, 
                              prepared_text[i], prepared_text[i + 1], digram) != 0) {
                return -1;
            }
            result[i] = digram[0];
            result[i + 1] = digram[1];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}
