#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "cryptology/classical/transposition/columnar/single.h"
#include "cryptology/classical/transposition/utf8_helpers.h"

#define MAX_KEY_LEN 100
#define MAX_TEXT_LEN 1024

/**
 * Sort indices by keyword characters (stable sort).
 */
static void sort_indices(int *indices, int len, const char *keyword) {
    // Simple insertion sort for stability
    for (int i = 1; i < len; i++) {
        int key = indices[i];
        int j = i - 1;

        while (j >= 0 && keyword[indices[j]] > keyword[key]) {
            indices[j + 1] = indices[j];
            j--;
        }
        indices[j + 1] = key;
    }
}

int single_columnar_encrypt(const char *plaintext, const char *keyword,
                            char *output, size_t max_len) {
    if (!plaintext || !keyword || !output || max_len == 0) {
        return -1;
    }

    // Clean and normalize text to lowercase (UTF-8 aware, supports Turkish)
    char text[MAX_TEXT_LEN * 3] = {0};  // Extra space for UTF-8
    char keyword_lower[MAX_KEY_LEN * 3] = {0};

    if (clean_utf8_text(plaintext, text, sizeof(text)) != 0) {
        return -1;
    }

    if (clean_utf8_text(keyword, keyword_lower, sizeof(keyword_lower)) != 0) {
        return -1;
    }

    int text_len = strlen(text);
    int key_len = strlen(keyword_lower);

    if (text_len == 0 || key_len == 0) {
        output[0] = '\0';
        return 0;
    }

    // Create sorted indices
    int indices[MAX_KEY_LEN];
    for (int i = 0; i < key_len; i++) {
        indices[i] = i;
    }

    sort_indices(indices, key_len, keyword_lower);

    // Calculate grid dimensions
    int num_rows = (text_len + key_len - 1) / key_len;
    int total_cells = num_rows * key_len;

    // Pad text
    for (int i = text_len; i < total_cells; i++) {
        text[i] = 'x';
    }

    // Encrypt by reading columns in sorted order
    int output_pos = 0;
    for (int i = 0; i < key_len; i++) {
        int col_idx = indices[i];
        for (int row = 0; row < num_rows; row++) {
            if (output_pos < (int)max_len - 1) {
                char c = text[row * key_len + col_idx];
                output[output_pos++] = c;
            }
        }
    }

    // Remove trailing 'x' characters
    while (output_pos > 0 && output[output_pos - 1] == 'x') {
        output_pos--;
    }
    output[output_pos] = '\0';

    return 0;
}

int single_columnar_decrypt(const char *ciphertext, const char *keyword,
                            char *output, size_t max_len) {
    if (!ciphertext || !keyword || !output || max_len == 0) {
        return -1;
    }

    // Clean and normalize (UTF-8 aware, supports Turkish)
    char text[MAX_TEXT_LEN * 3] = {0};
    char keyword_lower[MAX_KEY_LEN * 3] = {0};

    if (clean_utf8_text(ciphertext, text, sizeof(text)) != 0) {
        return -1;
    }

    if (clean_utf8_text(keyword, keyword_lower, sizeof(keyword_lower)) != 0) {
        return -1;
    }

    int text_len = strlen(text);
    int key_len = strlen(keyword_lower);

    if (text_len == 0 || key_len == 0) {
        output[0] = '\0';
        return 0;
    }

    // Create sorted indices
    int indices[MAX_KEY_LEN];
    for (int i = 0; i < key_len; i++) {
        indices[i] = i;
    }

    sort_indices(indices, key_len, keyword_lower);

    // Calculate grid dimensions
    int num_rows = (text_len + key_len - 1) / key_len;
    int total_cells = num_rows * key_len;

    // Pad text to total_cells
    for (int i = text_len; i < total_cells; i++) {
        text[i] = 'x';
    }

    // Allocate grid
    char **grid = (char **)malloc(num_rows * sizeof(char *));
    if (!grid) {
        return -1;
    }
    for (int i = 0; i < num_rows; i++) {
        grid[i] = (char *)malloc(key_len * sizeof(char));
        if (!grid[i]) {
            for (int j = 0; j < i; j++) free(grid[j]);
            free(grid);
            return -1;
        }
        for (int j = 0; j < key_len; j++) {
            grid[i][j] = '\0';
        }
    }

    // Fill grid by columns in sorted order
    int cipher_pos = 0;
    for (int i = 0; i < key_len; i++) {
        int col_idx = indices[i];
        for (int row = 0; row < num_rows; row++) {
            if (cipher_pos < total_cells) {
                grid[row][col_idx] = text[cipher_pos++];
            }
        }
    }

    // Read by rows
    int output_pos = 0;
    for (int row = 0; row < num_rows; row++) {
        for (int col = 0; col < key_len; col++) {
            if (output_pos < (int)max_len - 1) {
                output[output_pos++] = grid[row][col];
            }
        }
    }

    // Remove trailing 'x' characters
    while (output_pos > 0 && output[output_pos - 1] == 'x') {
        output_pos--;
    }
    output[output_pos] = '\0';

    // Free grid
    for (int i = 0; i < num_rows; i++) {
        free(grid[i]);
    }
    free(grid);

    return 0;
}

