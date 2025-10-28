/**
 * @file chaocipher.c
 * @brief Chaocipher implementation for C
 * 
 * Chaocipher is a polyalphabetic substitution cipher that uses two rotating
 * alphabets (left and right) that are permuted after each character.
 * It is self-reciprocal, meaning encryption and decryption use the same algorithm.
 */

#include "cryptology/classical/substitution/polyalphabetic/chaocipher.h"
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/**
 * @brief Default English alphabet with space
 */
static const char DEFAULT_ALPHABET[] = "abcdefghijklmnopqrstuvwxyz ";

/**
 * @brief Turkish alphabet with space
 */
static const char TURKISH_ALPHABET[] = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ";

/**
 * @brief Check if a character is in the alphabet
 */
static int is_in_alphabet(char c, const char *alphabet, size_t alphabet_size) {
    for (size_t i = 0; i < alphabet_size; i++) {
        if (alphabet[i] == c) {
            return 1;
        }
    }
    return 0;
}

/**
 * @brief Find position of character in alphabet
 */
static int find_char_position(char c, const char *alphabet, size_t alphabet_size) {
    for (size_t i = 0; i < alphabet_size; i++) {
        if (alphabet[i] == c) {
            return (int)i;
        }
    }
    return -1;
}

/**
 * @brief Remove duplicate characters from a string
 */
static void remove_duplicates(char *str) {
    size_t len = strlen(str);
    size_t write_pos = 0;
    
    for (size_t i = 0; i < len; i++) {
        int found = 0;
        for (size_t j = 0; j < write_pos; j++) {
            if (str[j] == str[i]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            str[write_pos++] = str[i];
        }
    }
    str[write_pos] = '\0';
}

int chaocipher_create_custom_alphabets(const char *left_keyword,
                                     const char *right_keyword,
                                     char *left_alphabet,
                                     char *right_alphabet,
                                     size_t alphabet_size) {
    if (!left_keyword || !right_keyword || !left_alphabet || !right_alphabet || alphabet_size == 0) {
        return -1;
    }
    
    // Copy base alphabet
    const char *base_alphabet = DEFAULT_ALPHABET;
    if (alphabet_size > 27) {
        base_alphabet = TURKISH_ALPHABET;
    }
    
    strncpy(left_alphabet, base_alphabet, alphabet_size);
    left_alphabet[alphabet_size] = '\0';
    
    strncpy(right_alphabet, base_alphabet, alphabet_size);
    right_alphabet[alphabet_size] = '\0';
    
    // Create left alphabet with keyword
    char temp_left[64];
    strcpy(temp_left, left_keyword);
    
    // Add remaining characters from base alphabet
    for (size_t i = 0; i < alphabet_size; i++) {
        if (!is_in_alphabet(base_alphabet[i], temp_left, strlen(temp_left))) {
            char temp_char[2] = {base_alphabet[i], '\0'};
            strcat(temp_left, temp_char);
        }
    }
    
    // Remove duplicates and copy to output
    remove_duplicates(temp_left);
    strncpy(left_alphabet, temp_left, alphabet_size);
    left_alphabet[alphabet_size] = '\0';
    
    // Create right alphabet with keyword
    char temp_right[64];
    strcpy(temp_right, right_keyword);
    
    // Add remaining characters from base alphabet
    for (size_t i = 0; i < alphabet_size; i++) {
        if (!is_in_alphabet(base_alphabet[i], temp_right, strlen(temp_right))) {
            char temp_char[2] = {base_alphabet[i], '\0'};
            strcat(temp_right, temp_char);
        }
    }
    
    // Remove duplicates and copy to output
    remove_duplicates(temp_right);
    strncpy(right_alphabet, temp_right, alphabet_size);
    right_alphabet[alphabet_size] = '\0';
    
    return 0;
}

void chaocipher_permute_right_alphabet(char *alphabet, size_t alphabet_size, char plain_char) {
    if (!alphabet || alphabet_size == 0) {
        return;
    }
    
    // Find position of plaintext character
    int plain_pos = find_char_position(plain_char, alphabet, alphabet_size);
    if (plain_pos == -1) {
        return;
    }
    
    // Step 1: Move plaintext character to position 0 (zenith)
    char temp = alphabet[plain_pos];
    memmove(&alphabet[plain_pos], &alphabet[plain_pos + 1], alphabet_size - plain_pos - 1);
    memmove(&alphabet[1], alphabet, alphabet_size - 1);
    alphabet[0] = temp;
    
    // Step 2: Move character at position 1 to position 13 (nadir)
    if (alphabet_size > 1) {
        temp = alphabet[1];
        memmove(&alphabet[1], &alphabet[2], alphabet_size - 2);
        memmove(&alphabet[14], &alphabet[13], alphabet_size - 14);
        alphabet[13] = temp;
    }
    
    // Steps 3 & 4: Shift remaining characters
    // Characters 2-13 shift left (positions 1-12)
    // Characters 15-26 shift right (positions 14-25)
    if (alphabet_size > 14) {
        // Move characters 15-26 (indices 14-25) to the right
        char temp_chars[32];
        size_t chars_15_26_len = alphabet_size - 14;
        memcpy(temp_chars, &alphabet[14], chars_15_26_len);
        memmove(&alphabet[14], &alphabet[13], alphabet_size - 13);
        memcpy(&alphabet[14], temp_chars, chars_15_26_len);
    }
}

void chaocipher_permute_left_alphabet(char *alphabet, size_t alphabet_size, char cipher_char) {
    if (!alphabet || alphabet_size == 0) {
        return;
    }
    
    // Find position of ciphertext character
    int cipher_pos = find_char_position(cipher_char, alphabet, alphabet_size);
    if (cipher_pos == -1) {
        return;
    }
    
    // Step 1: Move ciphertext character to position 0 (zenith)
    char temp = alphabet[cipher_pos];
    memmove(&alphabet[cipher_pos], &alphabet[cipher_pos + 1], alphabet_size - cipher_pos - 1);
    memmove(&alphabet[1], alphabet, alphabet_size - 1);
    alphabet[0] = temp;
    
    // Step 2: Move character at position 1 to position 13 (nadir)
    if (alphabet_size > 1) {
        temp = alphabet[1];
        memmove(&alphabet[1], &alphabet[2], alphabet_size - 2);
        memmove(&alphabet[14], &alphabet[13], alphabet_size - 14);
        alphabet[13] = temp;
    }
    
    // Steps 3 & 4: Shift remaining characters
    // Characters 2-13 shift left (positions 1-12)
    // Characters 15-26 shift right (positions 14-25)
    if (alphabet_size > 14) {
        // Move characters 15-26 (indices 14-25) to the right
        char temp_chars[32];
        size_t chars_15_26_len = alphabet_size - 14;
        memcpy(temp_chars, &alphabet[14], chars_15_26_len);
        memmove(&alphabet[14], &alphabet[13], alphabet_size - 13);
        memcpy(&alphabet[14], temp_chars, chars_15_26_len);
    }
}

int chaocipher_prepare_text(const char *text, 
                           const char *alphabet, 
                           size_t alphabet_size,
                           char *output, 
                           size_t output_size) {
    if (!text || !alphabet || !output || output_size == 0) {
        return -1;
    }
    
    size_t output_pos = 0;
    size_t text_len = strlen(text);
    
    for (size_t i = 0; i < text_len && output_pos < output_size - 1; i++) {
        char c = tolower(text[i]);
        
        if (is_in_alphabet(c, alphabet, alphabet_size)) {
            output[output_pos++] = c;
        }
    }
    
    output[output_pos] = '\0';
    return (int)output_pos;
}

int chaocipher_encrypt(const char *plaintext,
                      const char *left_alphabet,
                      const char *right_alphabet,
                      size_t alphabet_size,
                      char *output,
                      size_t output_size) {
    if (!plaintext || !left_alphabet || !right_alphabet || !output || 
        alphabet_size == 0 || output_size == 0) {
        return -1;
    }
    
    // Prepare text
    char prepared_text[1024];
    int prepared_len = chaocipher_prepare_text(plaintext, right_alphabet, alphabet_size, 
                                              prepared_text, sizeof(prepared_text));
    if (prepared_len < 0) {
        return -1;
    }
    
    // Create working copies of alphabets
    char working_left[64];
    char working_right[64];
    strncpy(working_left, left_alphabet, alphabet_size);
    working_left[alphabet_size] = '\0';
    strncpy(working_right, right_alphabet, alphabet_size);
    working_right[alphabet_size] = '\0';
    
    size_t output_pos = 0;
    
    for (int i = 0; i < prepared_len && output_pos < output_size - 1; i++) {
        char c = prepared_text[i];
        
        // Find position in right alphabet
        int right_pos = find_char_position(c, working_right, alphabet_size);
        if (right_pos == -1) {
            continue; // Skip characters not in alphabet
        }
        
        // Get corresponding character from left alphabet
        char cipher_char = working_left[right_pos];
        output[output_pos++] = cipher_char;
        
        // Permute both alphabets
        chaocipher_permute_left_alphabet(working_left, alphabet_size, cipher_char);
        chaocipher_permute_right_alphabet(working_right, alphabet_size, c);
    }
    
    output[output_pos] = '\0';
    return (int)output_pos;
}

int chaocipher_decrypt(const char *ciphertext,
                      const char *left_alphabet,
                      const char *right_alphabet,
                      size_t alphabet_size,
                      char *output,
                      size_t output_size) {
    if (!ciphertext || !left_alphabet || !right_alphabet || !output || 
        alphabet_size == 0 || output_size == 0) {
        return -1;
    }
    
    // Prepare text
    char prepared_text[1024];
    int prepared_len = chaocipher_prepare_text(ciphertext, left_alphabet, alphabet_size, 
                                              prepared_text, sizeof(prepared_text));
    if (prepared_len < 0) {
        return -1;
    }
    
    // Create working copies of alphabets
    char working_left[64];
    char working_right[64];
    strncpy(working_left, left_alphabet, alphabet_size);
    working_left[alphabet_size] = '\0';
    strncpy(working_right, right_alphabet, alphabet_size);
    working_right[alphabet_size] = '\0';
    
    size_t output_pos = 0;
    
    for (int i = 0; i < prepared_len && output_pos < output_size - 1; i++) {
        char c = prepared_text[i];
        
        // Find position in left alphabet
        int left_pos = find_char_position(c, working_left, alphabet_size);
        if (left_pos == -1) {
            continue; // Skip characters not in alphabet
        }
        
        // Get corresponding character from right alphabet
        char plain_char = working_right[left_pos];
        output[output_pos++] = plain_char;
        
        // Permute both alphabets (same as encryption - self-reciprocal)
        chaocipher_permute_left_alphabet(working_left, alphabet_size, c);
        chaocipher_permute_right_alphabet(working_right, alphabet_size, plain_char);
    }
    
    output[output_pos] = '\0';
    return (int)output_pos;
}

int chaocipher_decrypt_with_alphabets(const char *ciphertext,
                                    const char *left_alphabet,
                                    const char *right_alphabet,
                                    size_t alphabet_size,
                                    char *output,
                                    size_t output_size) {
    if (!ciphertext || !left_alphabet || !right_alphabet || !output || 
        alphabet_size == 0 || output_size == 0) {
        return -1;
    }
    
    return chaocipher_decrypt(ciphertext, left_alphabet, right_alphabet, 
                             alphabet_size, output, output_size);
}

/**
 * @brief Parse integer parameter from parameter string
 */
static int parse_int_param(const char *params, const char *key, int default_value) {
    if (!params || strlen(params) == 0) {
        return default_value;
    }
    
    // Simple parsing for "key:value" format
    char key_pattern[64];
    snprintf(key_pattern, sizeof(key_pattern), "%s:", key);
    
    char *pos = strstr(params, key_pattern);
    if (pos) {
        pos += strlen(key_pattern);
        return atoi(pos);
    }
    
    return default_value;
}

/**
 * @brief Parse string parameter from parameter string
 */
static int parse_string_param(const char *params, const char *key, char *result, size_t result_size) {
    if (!params || strlen(params) == 0) {
        return -1;
    }
    
    // Simple parsing for "key:value" format
    char key_pattern[64];
    snprintf(key_pattern, sizeof(key_pattern), "%s:", key);
    
    char *pos = strstr(params, key_pattern);
    if (pos) {
        pos += strlen(key_pattern);
        char *end = strchr(pos, ',');
        if (end) {
            size_t len = end - pos;
            if (len < result_size) {
                strncpy(result, pos, len);
                result[len] = '\0';
                return 0;
            }
        } else {
            if (strlen(pos) < result_size) {
                strcpy(result, pos);
                return 0;
            }
        }
    }
    
    return -1;
}

int chaocipher_create_alphabets_with_mono_ciphers(const char *left_cipher,
                                                const char *left_params,
                                                const char *right_cipher,
                                                const char *right_params,
                                                const char *alphabet,
                                                char *left_alphabet,
                                                char *right_alphabet,
                                                size_t alphabet_size) {
    if (!left_cipher || !right_cipher || !left_alphabet || !right_alphabet || alphabet_size == 0) {
        return -1;
    }
    
    // Use default alphabet if none provided
    const char *base_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    
    // Create left alphabet
    if (strcmp(left_cipher, "caesar") == 0) {
        int shift = parse_int_param(left_params, "shift", 3);
        if (caesar_produce_alphabet(shift, base_alphabet, left_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(left_cipher, "atbash") == 0) {
        if (atbash_produce_alphabet(base_alphabet, left_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(left_cipher, "keyword") == 0) {
        char keyword[64];
        if (parse_string_param(left_params, "keyword", keyword, sizeof(keyword)) != 0) {
            return -1;
        }
        if (keyword_produce_alphabet(keyword, base_alphabet, left_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(left_cipher, "affine") == 0) {
        int a = parse_int_param(left_params, "a", 1);
        int b = parse_int_param(left_params, "b", 0);
        if (affine_produce_alphabet(a, b, base_alphabet, left_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else {
        return -1; // Unsupported cipher
    }
    
    // Create right alphabet
    if (strcmp(right_cipher, "caesar") == 0) {
        int shift = parse_int_param(right_params, "shift", 3);
        if (caesar_produce_alphabet(shift, base_alphabet, right_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(right_cipher, "atbash") == 0) {
        if (atbash_produce_alphabet(base_alphabet, right_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(right_cipher, "keyword") == 0) {
        char keyword[64];
        if (parse_string_param(right_params, "keyword", keyword, sizeof(keyword)) != 0) {
            return -1;
        }
        if (keyword_produce_alphabet(keyword, base_alphabet, right_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else if (strcmp(right_cipher, "affine") == 0) {
        int a = parse_int_param(right_params, "a", 1);
        int b = parse_int_param(right_params, "b", 0);
        if (affine_produce_alphabet(a, b, base_alphabet, right_alphabet, alphabet_size + 1) != 0) {
            return -1;
        }
    } else {
        return -1; // Unsupported cipher
    }
    
    return 0;
}
