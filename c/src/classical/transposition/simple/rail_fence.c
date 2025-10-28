#include "cryptology/classical/transposition/simple/rail_fence.h"
#include "cryptology/classical/transposition/utf8_helpers.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int rail_fence_encrypt(const char *plaintext, int rails, char *output, size_t output_size) {
    if (!plaintext || !output || rails <= 0 || output_size == 0) {
        return -1;
    }

    // Clean and normalize text (UTF-8 aware, supports Turkish)
    char *clean_input = malloc(strlen(plaintext) * 3 + 1);
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

    if (rails == 1) {
        // Single rail = no encryption
        strncpy(output, clean_input, output_size - 1);
        output[output_size - 1] = '\0';
        free(clean_input);
        return 0;
    }

    size_t text_len = strlen(clean_input);

    // Build zigzag pattern
    char **pattern = malloc(rails * sizeof(char*));
    if (!pattern) {
        free(clean_input);
        return -1;
    }

    for (int i = 0; i < rails; i++) {
        pattern[i] = malloc(text_len * sizeof(char));
        if (!pattern[i]) {
            // Clean up allocated memory
            for (int j = 0; j < i; j++) {
                free(pattern[j]);
            }
            free(pattern);
            free(clean_input);
            return -1;
        }
        memset(pattern[i], 0, text_len);
    }

    int direction = 1;  // 1 for down, -1 for up
    int rail = 0;

    for (size_t i = 0; i < text_len; i++) {
        pattern[rail][i] = clean_input[i];

        // Change direction at the edges
        if (rail == 0) {
            direction = 1;
        } else if (rail == rails - 1) {
            direction = -1;
        }

        rail += direction;
    }

    // Concatenate all rails
    size_t output_index = 0;
    for (int rail_num = 0; rail_num < rails && output_index < output_size - 1; rail_num++) {
        for (size_t i = 0; i < text_len && output_index < output_size - 1; i++) {
            if (pattern[rail_num][i] != 0) {
                output[output_index++] = pattern[rail_num][i];
            }
        }
    }
    output[output_index] = '\0';

    // Clean up
    for (int i = 0; i < rails; i++) {
        free(pattern[i]);
    }
    free(pattern);
    free(clean_input);

    return 0;
}

int rail_fence_decrypt(const char *ciphertext, int rails, char *output, size_t output_size) {
    if (!ciphertext || !output || rails <= 0 || output_size == 0) {
        return -1;
    }

    // Clean the ciphertext (UTF-8 aware, supports Turkish)
    char *clean_input = malloc(strlen(ciphertext) * 3 + 1);
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

    if (rails == 1) {
        strncpy(output, clean_input, output_size - 1);
        output[output_size - 1] = '\0';
        free(clean_input);
        return 0;
    }

    size_t text_len = strlen(clean_input);

    // Calculate how many characters are in each rail
    int *pattern_lengths = malloc(rails * sizeof(int));
    if (!pattern_lengths) {
        free(clean_input);
        return -1;
    }
    memset(pattern_lengths, 0, rails * sizeof(int));

    int direction = 1;
    int rail = 0;

    for (size_t i = 0; i < text_len; i++) {
        pattern_lengths[rail]++;

        if (rail == 0) {
            direction = 1;
        } else if (rail == rails - 1) {
            direction = -1;
        }

        rail += direction;
    }

    // Distribute ciphertext across rails
    char **pattern = malloc(rails * sizeof(char*));
    if (!pattern) {
        free(pattern_lengths);
        free(clean_input);
        return -1;
    }

    for (int i = 0; i < rails; i++) {
        pattern[i] = malloc(pattern_lengths[i] * sizeof(char));
        if (!pattern[i]) {
            // Clean up allocated memory
            for (int j = 0; j < i; j++) {
                free(pattern[j]);
            }
            free(pattern);
            free(pattern_lengths);
            free(clean_input);
            return -1;
        }
    }

    size_t text_pos = 0;
    for (int rail_num = 0; rail_num < rails; rail_num++) {
        for (int i = 0; i < pattern_lengths[rail_num]; i++) {
            if (text_pos < text_len) {
                pattern[rail_num][i] = clean_input[text_pos++];
            }
        }
    }

    // Read off in zigzag order
    size_t output_index = 0;
    direction = 1;
    rail = 0;
    int *rail_positions = malloc(rails * sizeof(int));
    if (!rail_positions) {
        // Clean up
        for (int i = 0; i < rails; i++) {
            free(pattern[i]);
        }
        free(pattern);
        free(pattern_lengths);
        free(clean_input);
        return -1;
    }
    memset(rail_positions, 0, rails * sizeof(int));

    for (size_t i = 0; i < text_len && output_index < output_size - 1; i++) {
        if (rail_positions[rail] < pattern_lengths[rail]) {
            output[output_index++] = pattern[rail][rail_positions[rail]];
            rail_positions[rail]++;
        }

        if (rail == 0) {
            direction = 1;
        } else if (rail == rails - 1) {
            direction = -1;
        }

        rail += direction;
    }
    output[output_index] = '\0';

    // Clean up
    for (int i = 0; i < rails; i++) {
        free(pattern[i]);
    }
    free(pattern);
    free(pattern_lengths);
    free(rail_positions);
    free(clean_input);

    return 0;
}

int rail_fence_visualize(const char *text, int rails, char *output, size_t output_size) {
    if (!text || !output || rails <= 0 || output_size == 0) {
        return -1;
    }

    // Clean text (UTF-8 aware, supports Turkish)
    char *clean_input = malloc(strlen(text) * 3 + 1);
    if (!clean_input) return -1;

    if (clean_utf8_text(text, clean_input, strlen(text) * 3 + 1) != 0) {
        free(clean_input);
        return -1;
    }

    size_t text_len = strlen(clean_input);
    if (text_len == 0) {
        output[0] = '\0';
        free(clean_input);
        return 0;
    }

    // Create grid
    char **grid = malloc(rails * sizeof(char*));
    if (!grid) {
        free(clean_input);
        return -1;
    }

    for (int i = 0; i < rails; i++) {
        grid[i] = malloc(text_len * sizeof(char));
        if (!grid[i]) {
            // Clean up allocated memory
            for (int j = 0; j < i; j++) {
                free(grid[j]);
            }
            free(grid);
            free(clean_input);
            return -1;
        }
        memset(grid[i], ' ', text_len);
    }

    int direction = 1;
    int rail = 0;

    for (size_t col = 0; col < text_len; col++) {
        grid[rail][col] = clean_input[col];

        if (rail == 0) {
            direction = 1;
        } else if (rail == rails - 1) {
            direction = -1;
        }

        rail += direction;
    }

    // Convert to string
    size_t output_index = 0;
    for (int row = 0; row < rails && output_index < output_size - 1; row++) {
        for (size_t col = 0; col < text_len && output_index < output_size - 1; col++) {
            output[output_index++] = grid[row][col];
            if (col < text_len - 1 && output_index < output_size - 1) {
                output[output_index++] = ' ';
            }
        }
        if (row < rails - 1 && output_index < output_size - 1) {
            output[output_index++] = '\n';
        }
    }
    output[output_index] = '\0';

    // Clean up
    for (int i = 0; i < rails; i++) {
        free(grid[i]);
    }
    free(grid);
    free(clean_input);

    return 0;
}

void rail_fence_get_key_range(size_t text_length, int *min_key, int *max_key) {
    if (text_length <= 0) {
        *min_key = 0;
        *max_key = 0;
    } else {
        *min_key = 1;
        *max_key = (int)(text_length < 10 ? text_length : 10);  // Practical limit
    }
}
