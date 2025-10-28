#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "cryptology/classical/transposition/route/boustrophedon.h"
#include "cryptology/classical/transposition/utf8_helpers.h"

#define MAX_TEXT_LEN 2048

int boustrophedon_encrypt(const char *plaintext, char *output, size_t max_len) {
    if (!plaintext || !output || max_len == 0) {
        return -1;
    }

    // Clean and normalize to lowercase (UTF-8 aware, supports Turkish)
    char text[MAX_TEXT_LEN * 3] = {0};  // Extra space for UTF-8

    if (clean_utf8_text(plaintext, text, sizeof(text)) != 0) {
        return -1;
    }

    int text_len = strlen(text);

    if (text_len == 0) {
        output[0] = '\0';
        return 0;
    }

    // Determine grid dimensions (approx square)
    int side = (int)sqrt(text_len);
    if (side * side < text_len) {
        side++;
    }

    // Allocate grid
    char **grid = (char **)malloc(side * sizeof(char *));
    if (!grid) return -1;
    for (int i = 0; i < side; i++) {
        grid[i] = (char *)malloc(side * sizeof(char));
        if (!grid[i]) {
            for (int j = 0; j < i; j++) free(grid[j]);
            free(grid);
            return -1;
        }
        for (int j = 0; j < side; j++) {
            grid[i][j] = 'x';
        }
    }

    // Write text in boustrophedon pattern
    int pos = 0;
    for (int row = 0; row < side; row++) {
        if (row % 2 == 0) {
            // Left to right
            for (int col = 0; col < side; col++) {
                if (pos < text_len) {
                    grid[row][col] = text[pos++];
                }
            }
        } else {
            // Right to left
            for (int col = side - 1; col >= 0; col--) {
                if (pos < text_len) {
                    grid[row][col] = text[pos++];
                }
            }
        }
    }

    // Read in linear order
    int output_pos = 0;
    for (int row = 0; row < side; row++) {
        for (int col = 0; col < side; col++) {
            if (output_pos < (int)max_len - 1 && grid[row][col] != 'x') {
                output[output_pos++] = grid[row][col];
            }
        }
    }
    output[output_pos] = '\0';

    // Free grid
    for (int i = 0; i < side; i++) {
        free(grid[i]);
    }
    free(grid);

    return 0;
}

int boustrophedon_decrypt(const char *ciphertext, char *output, size_t max_len) {
    if (!ciphertext || !output || max_len == 0) {
        return -1;
    }

    // Clean and normalize (UTF-8 aware, supports Turkish)
    char text[MAX_TEXT_LEN * 3] = {0};  // Extra space for UTF-8

    if (clean_utf8_text(ciphertext, text, sizeof(text)) != 0) {
        return -1;
    }

    int text_len = strlen(text);

    if (text_len == 0) {
        output[0] = '\0';
        return 0;
    }

    // Determine grid dimensions
    int side = (int)sqrt(text_len);
    if (side * side < text_len) {
        side++;
    }

    // Allocate grid
    char **grid = (char **)malloc(side * sizeof(char *));
    if (!grid) return -1;
    for (int i = 0; i < side; i++) {
        grid[i] = (char *)malloc(side * sizeof(char));
        if (!grid[i]) {
            for (int j = 0; j < i; j++) free(grid[j]);
            free(grid);
            return -1;
        }
        for (int j = 0; j < side; j++) {
            grid[i][j] = 'x';
        }
    }

    // Fill grid with ciphertext in linear order
    int pos = 0;
    for (int row = 0; row < side; row++) {
        for (int col = 0; col < side; col++) {
            if (pos < text_len) {
                grid[row][col] = text[pos++];
            }
        }
    }

    // Read in boustrophedon pattern (alternating directions)
    int output_pos = 0;
    for (int row = 0; row < side; row++) {
        if (row % 2 == 0) {
            // Left to right
            for (int col = 0; col < side; col++) {
                if (output_pos < (int)max_len - 1 && grid[row][col] != 'x') {
                    output[output_pos++] = grid[row][col];
                }
            }
        } else {
            // Right to left
            for (int col = side - 1; col >= 0; col--) {
                if (output_pos < (int)max_len - 1 && grid[row][col] != 'x') {
                    output[output_pos++] = grid[row][col];
                }
            }
        }
    }

    // Remove trailing 'x'
    while (output_pos > 0 && output[output_pos - 1] == 'x') {
        output_pos--;
    }
    output[output_pos] = '\0';

    // Free grid
    for (int i = 0; i < side; i++) {
        free(grid[i]);
    }
    free(grid);

    return 0;
}

