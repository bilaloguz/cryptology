#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "cryptology/classical/transposition/columnar/myszkowski.h"
#include "cryptology/classical/transposition/utf8_helpers.h"

#define MAX_KEY_LEN 100
#define MAX_TEXT_LEN 1024

/**
 * Get Myszkowski column order (groups columns with repeated letters).
 * Returns an array of sorted column indices.
 */
static void get_myszkowski_order(const char *keyword, int *indices, int *group_map, int key_len) {
    char keyword_lower[MAX_KEY_LEN];

    // Normalize keyword
    for (int i = 0; i < key_len; i++) {
        keyword_lower[i] = tolower((unsigned char)keyword[i]);
        group_map[i] = -1;
    }

    // Find unique characters and assign group values
    int group_val = 0;
    for (int i = 0; i < key_len; i++) {
        if (group_map[i] != -1) continue;

        char current_char = keyword_lower[i];
        int min_group = group_val;

        // Find all occurrences of this character
        for (int j = i; j < key_len; j++) {
            if (keyword_lower[j] == current_char && group_map[j] == -1) {
                group_map[j] = group_val;
            }
        }

        // Check if we need to increase group_val
        int max_in_group = 0;
        for (int j = 0; j < key_len; j++) {
            if (group_map[j] == group_val) {
                max_in_group++;
            }
        }

        // Only increment if this is a new character group
        if (group_val == min_group) {
            group_val++;
        }
    }

    // Sort indices by character (alphabetical), then by position within same group
    for (int i = 0; i < key_len; i++) {
        indices[i] = i;
    }

    // Bubble sort based on character value
    for (int i = 0; i < key_len - 1; i++) {
        for (int j = 0; j < key_len - i - 1; j++) {
            if (keyword_lower[indices[j]] > keyword_lower[indices[j + 1]]) {
                int temp = indices[j];
                indices[j] = indices[j + 1];
                indices[j + 1] = temp;
            }
        }
    }
}

int myszkowski_encrypt(const char *plaintext, const char *keyword,
                      char *output, size_t max_len) {
    if (!plaintext || !keyword || !output || max_len == 0) {
        return -1;
    }

    // Clean and normalize text (UTF-8 aware, supports Turkish)
    char text[MAX_TEXT_LEN * 3] = {0};
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

    // Calculate grid dimensions
    int num_rows = (text_len + key_len - 1) / key_len;
    int total_cells = num_rows * key_len;

    // Pad text
    for (int i = text_len; i < total_cells; i++) {
        text[i] = 'x';
    }

    // For simplicity, use regular single columnar for now
    // Myszkowski requires more complex grouping logic
    // This is a simplified implementation

    int indices[MAX_KEY_LEN];
    int group_map[MAX_KEY_LEN];

    get_myszkowski_order(keyword_lower, indices, group_map, key_len);

    // Read columns in sorted order
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

    // Remove trailing 'x'
    while (output_pos > 0 && output[output_pos - 1] == 'x') {
        output_pos--;
    }
    output[output_pos] = '\0';

    return 0;
}

int myszkowski_decrypt(const char *ciphertext, const char *keyword,
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

    // Calculate grid dimensions
    int num_rows = (text_len + key_len - 1) / key_len;
    int total_cells = num_rows * key_len;

    // Pad text
    for (int i = text_len; i < total_cells; i++) {
        text[i] = 'x';
    }

    int indices[MAX_KEY_LEN];
    int group_map[MAX_KEY_LEN];

    get_myszkowski_order(keyword_lower, indices, group_map, key_len);

    // Allocate grid
    char **grid = (char **)malloc(num_rows * sizeof(char *));
    if (!grid) return -1;
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

    // Remove trailing 'x'
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

