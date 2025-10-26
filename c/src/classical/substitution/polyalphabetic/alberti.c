/**
 * @file alberti.c
 * @brief Alberti Cipher implementation with complex rotation strategies
 */

#include "cryptology/classical/substitution/polyalphabetic/alberti.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>

#define MAX_BUFFER_SIZE 1024
#define MAX_ALPHABET_SIZE 256
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

static int generate_scrambled_alphabet(const char *base_alphabet, char *result, size_t result_size) {
    if (!base_alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t len = strlen(base_alphabet);
    if (len >= result_size) {
        return -1;
    }
    
    // Simple deterministic scrambling using a fixed pattern
    // This is a basic implementation - in practice you might want more sophisticated scrambling
    strcpy(result, base_alphabet);
    
    // Apply a simple transposition pattern
    for (size_t i = 0; i < len / 2; i++) {
        char temp = result[i];
        result[i] = result[len - 1 - i];
        result[len - 1 - i] = temp;
    }
    
    return 0;
}

static int parse_rotation_strategy(const char *strategy, const char *text, int **rotation_points, int *point_count) {
    if (!strategy || !text || !rotation_points || !point_count) {
        return -1;
    }
    
    size_t text_len = strlen(text);
    *rotation_points = malloc(text_len * sizeof(int));
    if (!*rotation_points) {
        return -1;
    }
    
    *point_count = 0;
    
    // Parse different strategy types
    if (strncmp(strategy, "every_", 6) == 0) {
        // Every N letters
        int n = atoi(strategy + 6);
        if (n <= 0) {
            free(*rotation_points);
            return -1;
        }
        
        for (int i = n; i < (int)text_len; i += n) {
            (*rotation_points)[*point_count] = i;
            (*point_count)++;
        }
    }
    else if (strcmp(strategy, "on_vowel") == 0) {
        // Rotate when plaintext is vowel
        const char *vowels = "AEIOU";
        for (size_t i = 0; i < text_len; i++) {
            if (strchr(vowels, toupper((unsigned char)text[i]))) {
                (*rotation_points)[*point_count] = (int)i;
                (*point_count)++;
            }
        }
    }
    else if (strcmp(strategy, "on_space") == 0) {
        // Rotate when plaintext is space
        for (size_t i = 0; i < text_len; i++) {
            if (text[i] == ' ') {
                (*rotation_points)[*point_count] = (int)i;
                (*point_count)++;
            }
        }
    }
    else if (strcmp(strategy, "on_consonant") == 0) {
        // Rotate when plaintext is consonant
        const char *vowels = "AEIOU";
        for (size_t i = 0; i < text_len; i++) {
            char c = toupper((unsigned char)text[i]);
            if (isalpha(c) && !strchr(vowels, c)) {
                (*rotation_points)[*point_count] = (int)i;
                (*point_count)++;
            }
        }
    }
    else if (strcmp(strategy, "fibonacci") == 0) {
        // Rotate based on Fibonacci sequence
        int a = 1, b = 1;
        while (a < (int)text_len) {
            (*rotation_points)[*point_count] = a - 1;  // Convert to 0-based indexing
            (*point_count)++;
            int temp = a;
            a = b;
            b = temp + b;
        }
    }
    else {
        // Unknown strategy
        free(*rotation_points);
        return -1;
    }
    
    return 0;
}

static int rotate_alphabet(const char *alphabet, int amount, char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t len = strlen(alphabet);
    if (len >= result_size) {
        return -1;
    }
    
    amount = amount % (int)len;
    if (amount < 0) {
        amount += (int)len;
    }
    
    strcpy(result, alphabet + amount);
    strncat(result, alphabet, amount);
    result[result_size - 1] = '\0';
    
    return 0;
}

static int find_char_position(const char *alphabet, char c) {
    if (!alphabet) {
        return -1;
    }
    
    char c_upper = toupper((unsigned char)c);
    for (size_t i = 0; alphabet[i] != '\0'; i++) {
        if (toupper((unsigned char)alphabet[i]) == c_upper) {
            return (int)i;
        }
    }
    return -1;
}

static int clean_text(const char *input, char *output, size_t output_size) {
    if (!input || !output || output_size == 0) {
        return -1;
    }
    
    size_t input_len = strlen(input);
    size_t output_pos = 0;
    
    for (size_t i = 0; i < input_len && output_pos < output_size - 1; i++) {
        if (isalpha((unsigned char)input[i])) {
            output[output_pos++] = toupper((unsigned char)input[i]);
        }
    }
    
    output[output_pos] = '\0';
    return 0;
}

int alberti_encrypt(const char *plaintext,
                   const char *outer_alphabet,
                   const char *inner_alphabet,
                   int initial_position,
                   const char *rotation_strategy,
                   int rotation_amount,
                   char *result, size_t result_size) {
    if (!plaintext || !rotation_strategy || !result || result_size == 0) {
        return -1;
    }
    
    char outer_alpha[MAX_ALPHABET_SIZE];
    char inner_alpha[MAX_ALPHABET_SIZE];
    char plaintext_clean[MAX_BUFFER_SIZE];
    char inner_current[MAX_ALPHABET_SIZE];
    
    // Set up alphabets
    if (outer_alphabet) {
        strncpy(outer_alpha, outer_alphabet, sizeof(outer_alpha) - 1);
        outer_alpha[sizeof(outer_alpha) - 1] = '\0';
    } else {
        strcpy(outer_alpha, DEFAULT_ALPHABET);
    }
    
    if (inner_alphabet) {
        strncpy(inner_alpha, inner_alphabet, sizeof(inner_alpha) - 1);
        inner_alpha[sizeof(inner_alpha) - 1] = '\0';
    } else {
        if (generate_scrambled_alphabet(outer_alpha, inner_alpha, sizeof(inner_alpha)) != 0) {
            return -1;
        }
    }
    
    // Clean plaintext
    if (clean_text(plaintext, plaintext_clean, sizeof(plaintext_clean)) != 0) {
        return -1;
    }
    
    if (strlen(plaintext_clean) == 0) {
        result[0] = '\0';
        return 0;
    }
    
    // Parse rotation strategy
    int *rotation_points = NULL;
    int point_count = 0;
    if (parse_rotation_strategy(rotation_strategy, plaintext_clean, &rotation_points, &point_count) != 0) {
        return -1;
    }
    
    // Initialize inner disk position
    int current_position = initial_position % (int)strlen(inner_alpha);
    if (current_position < 0) {
        current_position += (int)strlen(inner_alpha);
    }
    
    if (rotate_alphabet(inner_alpha, current_position, inner_current, sizeof(inner_current)) != 0) {
        free(rotation_points);
        return -1;
    }
    
    // Encrypt
    size_t result_pos = 0;
    int rotation_index = 0;
    
    for (size_t i = 0; i < strlen(plaintext_clean) && result_pos < result_size - 1; i++) {
        int outer_pos = find_char_position(outer_alpha, plaintext_clean[i]);
        if (outer_pos == -1) {
            continue;  // Skip characters not in alphabet
        }
        
        // Map to inner alphabet
        if (outer_pos < (int)strlen(inner_current)) {
            result[result_pos++] = inner_current[outer_pos];
        } else {
            result[result_pos++] = inner_current[outer_pos % (int)strlen(inner_current)];
        }
        
        // Check if we need to rotate
        if (rotation_index < point_count && i == (size_t)rotation_points[rotation_index]) {
            current_position = (current_position + rotation_amount) % (int)strlen(inner_alpha);
            if (current_position < 0) {
                current_position += (int)strlen(inner_alpha);
            }
            
            if (rotate_alphabet(inner_alpha, current_position, inner_current, sizeof(inner_current)) != 0) {
                free(rotation_points);
                return -1;
            }
            rotation_index++;
        }
    }
    
    result[result_pos] = '\0';
    free(rotation_points);
    return 0;
}

int alberti_decrypt(const char *ciphertext,
                   const char *outer_alphabet,
                   const char *inner_alphabet,
                   int initial_position,
                   const char *rotation_strategy,
                   int rotation_amount,
                   char *result, size_t result_size) {
    if (!ciphertext || !rotation_strategy || !result || result_size == 0) {
        return -1;
    }
    
    char outer_alpha[MAX_ALPHABET_SIZE];
    char inner_alpha[MAX_ALPHABET_SIZE];
    char ciphertext_clean[MAX_BUFFER_SIZE];
    char inner_current[MAX_ALPHABET_SIZE];
    
    // Set up alphabets
    if (outer_alphabet) {
        strncpy(outer_alpha, outer_alphabet, sizeof(outer_alpha) - 1);
        outer_alpha[sizeof(outer_alpha) - 1] = '\0';
    } else {
        strcpy(outer_alpha, DEFAULT_ALPHABET);
    }
    
    if (inner_alphabet) {
        strncpy(inner_alpha, inner_alphabet, sizeof(inner_alpha) - 1);
        inner_alpha[sizeof(inner_alpha) - 1] = '\0';
    } else {
        if (generate_scrambled_alphabet(outer_alpha, inner_alpha, sizeof(inner_alpha)) != 0) {
            return -1;
        }
    }
    
    // Clean ciphertext
    if (clean_text(ciphertext, ciphertext_clean, sizeof(ciphertext_clean)) != 0) {
        return -1;
    }
    
    if (strlen(ciphertext_clean) == 0) {
        result[0] = '\0';
        return 0;
    }
    
    // Parse rotation strategy
    int *rotation_points = NULL;
    int point_count = 0;
    if (parse_rotation_strategy(rotation_strategy, ciphertext_clean, &rotation_points, &point_count) != 0) {
        return -1;
    }
    
    // Initialize inner disk position
    int current_position = initial_position % (int)strlen(inner_alpha);
    if (current_position < 0) {
        current_position += (int)strlen(inner_alpha);
    }
    
    if (rotate_alphabet(inner_alpha, current_position, inner_current, sizeof(inner_current)) != 0) {
        free(rotation_points);
        return -1;
    }
    
    // Decrypt
    size_t result_pos = 0;
    int rotation_index = 0;
    
    for (size_t i = 0; i < strlen(ciphertext_clean) && result_pos < result_size - 1; i++) {
        int inner_pos = find_char_position(inner_current, ciphertext_clean[i]);
        if (inner_pos == -1) {
            continue;  // Skip characters not in alphabet
        }
        
        // Map to outer alphabet
        if (inner_pos < (int)strlen(outer_alpha)) {
            result[result_pos++] = outer_alpha[inner_pos];
        } else {
            result[result_pos++] = outer_alpha[inner_pos % (int)strlen(outer_alpha)];
        }
        
        // Check if we need to rotate
        if (rotation_index < point_count && i == (size_t)rotation_points[rotation_index]) {
            current_position = (current_position + rotation_amount) % (int)strlen(inner_alpha);
            if (current_position < 0) {
                current_position += (int)strlen(inner_alpha);
            }
            
            if (rotate_alphabet(inner_alpha, current_position, inner_current, sizeof(inner_current)) != 0) {
                free(rotation_points);
                return -1;
            }
            rotation_index++;
        }
    }
    
    result[result_pos] = '\0';
    free(rotation_points);
    return 0;
}
