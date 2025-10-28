/**
 * @file nihilist.c
 * @brief Nihilist Cipher Implementation
 * 
 * The Nihilist cipher is a composite cipher that combines:
 * 1. Polybius square substitution
 * 2. Numeric key addition with modular arithmetic
 */

#include "../../../../include/cryptology/classical/substitution/composite/nihilist.h"
#include "../../../../include/cryptology/classical/substitution/polygraphic/alphabet_utils.h"
#include "../../../../include/cryptology/classical/substitution/polygraphic/monoalphabetic_squares.h"
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define MAX_ALPHABET_SIZE 50
#define MAX_SQUARE_SIZE 1000
#define MAX_TEXT_SIZE 1000

// Default English alphabet
static const char DEFAULT_ALPHABET[] = "abcdefghijklmnopqrstuvwxyz";

/**
 * @brief Prepare text for processing (remove non-alphabetic characters, convert to uppercase)
 */
static void prepare_text(const char* text, char* result, size_t result_size) {
    if (!text || !result || result_size == 0) {
        return;
    }
    
    size_t pos = 0;
    for (int i = 0; text[i] && pos < result_size - 1; i++) {
        if ((text[i] >= 'A' && text[i] <= 'Z') || (text[i] >= 'a' && text[i] <= 'z')) {
            result[pos++] = (text[i] >= 'a' && text[i] <= 'z') ? text[i] - 32 : text[i];
        }
    }
    result[pos] = '\0';
}

/**
 * @brief Prepare key for processing based on key type
 */
static void prepare_key(const char* key, const char* key_type, char* result, size_t result_size) {
    if (!key || !key_type || !result || result_size == 0) {
        return;
    }
    
    size_t pos = 0;
    if (strcmp(key_type, "numeric") == 0) {
        for (int i = 0; key[i] && pos < result_size - 1; i++) {
            if (key[i] >= '0' && key[i] <= '9') {
                result[pos++] = key[i];
            }
        }
    } else if (strcmp(key_type, "alphabetic") == 0) {
        for (int i = 0; key[i] && pos < result_size - 1; i++) {
            if ((key[i] >= 'A' && key[i] <= 'Z') || (key[i] >= 'a' && key[i] <= 'z')) {
                result[pos++] = (key[i] >= 'a' && key[i] <= 'z') ? key[i] - 32 : key[i];
            }
        }
    }
    result[pos] = '\0';
}

/**
 * @brief Parse square string into coordinate lookup
 */
static int parse_square(const char* square, int* square_dict, int* square_size) {
    if (!square || !square_dict || !square_size) {
        return -1;
    }
    
    // Initialize square dictionary
    for (int i = 0; i < 26; i++) {
        square_dict[i] = -1;  // -1 means not found
    }
    
    int row = 1, col = 1;
    int max_row = 0;
    
    for (int i = 0; square[i]; i++) {
        if (square[i] == '\n') {
            row++;
            col = 1;
        } else if ((square[i] >= 'A' && square[i] <= 'Z') || 
                   (square[i] >= 'a' && square[i] <= 'z')) {
            char letter = (square[i] >= 'a' && square[i] <= 'z') ? square[i] - 32 : square[i];
            square_dict[letter - 'A'] = row * 10 + col;  // Store as row*10 + col
            col++;
            if (row > max_row) max_row = row;
        }
    }
    
    *square_size = max_row;
    return 0;
}

/**
 * @brief Convert letters to coordinates using the square
 */
static int letters_to_coordinates(const char* text, const int* square_dict, int* coordinates, int max_coords) {
    if (!text || !square_dict || !coordinates) {
        return -1;
    }
    
    int count = 0;
    for (int i = 0; text[i] && count < max_coords; i++) {
        char letter = text[i];
        if (letter >= 'A' && letter <= 'Z') {
            int coord = square_dict[letter - 'A'];
            if (coord == -1) {
                return -1;  // Letter not found in square
            }
            coordinates[count++] = coord;
        }
    }
    
    return count;
}

/**
 * @brief Convert key to numeric values
 */
static int key_to_values(const char* key, const char* key_type, int* values, int max_values) {
    if (!key || !key_type || !values) {
        return -1;
    }
    
    int count = 0;
    if (strcmp(key_type, "numeric") == 0) {
        for (int i = 0; key[i] && count < max_values; i++) {
            if (key[i] >= '0' && key[i] <= '9') {
                values[count++] = key[i] - '0';
            }
        }
    } else if (strcmp(key_type, "alphabetic") == 0) {
        for (int i = 0; key[i] && count < max_values; i++) {
            if (key[i] >= 'A' && key[i] <= 'Z') {
                values[count++] = key[i] - 'A' + 1;
            }
        }
    }
    
    return count;
}

/**
 * @brief Add key values to coordinates with modular arithmetic
 */
static int add_coordinates_and_key(const int* coordinates, int coord_count, 
                                  const int* key_values, int key_count, 
                                  int square_size, int* result) {
    if (!coordinates || !key_values || !result || coord_count <= 0 || key_count <= 0) {
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        int key_val = key_values[i % key_count];
        int coord = coordinates[i];
        int row = coord / 10;
        int col = coord % 10;
        
        // Add key value with modular arithmetic
        int new_row = ((row - 1 + key_val) % square_size) + 1;
        int new_col = ((col - 1 + key_val) % square_size) + 1;
        
        result[i] = new_row * 10 + new_col;
    }
    
    return coord_count;
}

/**
 * @brief Subtract key values from coordinates with modular arithmetic
 */
static int subtract_key_from_coordinates(const int* coordinates, int coord_count,
                                        const int* key_values, int key_count,
                                        int square_size, int* result) {
    if (!coordinates || !key_values || !result || coord_count <= 0 || key_count <= 0) {
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        int key_val = key_values[i % key_count];
        int coord = coordinates[i];
        int row = coord / 10;
        int col = coord % 10;
        
        // Subtract key value with modular arithmetic
        int new_row = ((row - 1 - key_val) % square_size) + 1;
        int new_col = ((col - 1 - key_val) % square_size) + 1;
        
        result[i] = new_row * 10 + new_col;
    }
    
    return coord_count;
}

/**
 * @brief Convert coordinates back to letters using the square
 */
static int coordinates_to_letters(const int* coordinates, int coord_count,
                                 const char* square, char* result, size_t result_size) {
    if (!coordinates || !square || !result || coord_count <= 0 || result_size == 0) {
        return -1;
    }
    
    size_t pos = 0;
    for (int i = 0; i < coord_count && pos < result_size - 1; i++) {
        int coord = coordinates[i];
        int row = coord / 10;
        int col = coord % 10;
        
        // Find the letter at this coordinate in the square
        int current_row = 1, current_col = 1;
        for (int j = 0; square[j]; j++) {
            if (square[j] == '\n') {
                current_row++;
                current_col = 1;
            } else if ((square[j] >= 'A' && square[j] <= 'Z') || 
                       (square[j] >= 'a' && square[j] <= 'z')) {
                if (current_row == row && current_col == col) {
                    char letter = (square[j] >= 'a' && square[j] <= 'z') ? square[j] - 32 : square[j];
                    result[pos++] = letter;
                    break;
                }
                current_col++;
            }
        }
    }
    
    result[pos] = '\0';
    return pos;
}

/**
 * @brief Create a standard alphabetical square
 */
static int create_standard_square(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    // Convert to uppercase manually
    for (int i = 0; alphabet_upper[i]; i++) {
        if (alphabet_upper[i] >= 'a' && alphabet_upper[i] <= 'z') {
            alphabet_upper[i] = alphabet_upper[i] - 32;
        }
    }
    
    // Handle I=J combination for English
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        // Remove J, use I for both I and J
        char temp[MAX_ALPHABET_SIZE];
        int pos = 0;
        for (int i = 0; alphabet_upper[i]; i++) {
            if (alphabet_upper[i] != 'J') {
                temp[pos++] = alphabet_upper[i];
            }
        }
        temp[pos] = '\0';
        strcpy(alphabet_upper, temp);
    }
    
    // Determine square size
    int size;
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        size = 5;  // English uses 5x5 (25 letters with I=J)
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        size = 6;  // Turkish uses 6x6 (29 letters)
    } else {
        size = (strlen(alphabet_upper) <= 25) ? 5 : 6;
    }
    
    // Pad alphabet if needed
    while (strlen(alphabet_upper) < size * size) {
        char temp[MAX_ALPHABET_SIZE];
        strcpy(temp, alphabet_upper);
        strcat(temp, alphabet_upper);
        strncpy(alphabet_upper, temp, size * size);
        alphabet_upper[size * size] = '\0';
    }
    
    // Create square
    size_t pos = 0;
    for (int i = 0; i < size && pos < result_size - 1; i++) {
        for (int j = 0; j < size && pos < result_size - 1; j++) {
            result[pos++] = alphabet_upper[i * size + j];
        }
        if (i < size - 1 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

/**
 * @brief Create a frequency-based square
 */
static int create_frequency_square(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    // Convert to uppercase manually
    for (int i = 0; alphabet_upper[i]; i++) {
        if (alphabet_upper[i] >= 'a' && alphabet_upper[i] <= 'z') {
            alphabet_upper[i] = alphabet_upper[i] - 32;
        }
    }
    
    char frequency_order[MAX_ALPHABET_SIZE];
    
    // Define frequency orders
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        // English frequency order (25 letters for 5x5 square)
        strcpy(frequency_order, "ETAOINSHRDLCUMWFGYPBVKXQZ");
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        // Turkish frequency order (29 letters for 6x6 square)
        strcpy(frequency_order, "AENRLDKMSUTOYBGHCÇPFVZŞĞÖÜJIİ");
    } else {
        // For other alphabets, use alphabetical order
        strcpy(frequency_order, alphabet_upper);
    }
    
    // Handle I=J combination for English
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        char temp[MAX_ALPHABET_SIZE];
        int pos = 0;
        for (int i = 0; frequency_order[i]; i++) {
            if (frequency_order[i] != 'J') {
                temp[pos++] = frequency_order[i];
            }
        }
        temp[pos] = '\0';
        strcpy(frequency_order, temp);
    }
    
    // Determine square size
    int size;
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        size = 5;  // English uses 5x5 (25 letters with I=J)
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        size = 6;  // Turkish uses 6x6 (29 letters)
    } else {
        size = (strlen(frequency_order) <= 25) ? 5 : 6;
    }
    
    // Pad if needed
    while (strlen(frequency_order) < size * size) {
        char temp[MAX_ALPHABET_SIZE];
        strcpy(temp, frequency_order);
        strcat(temp, frequency_order);
        strncpy(frequency_order, temp, size * size);
        frequency_order[size * size] = '\0';
    }
    
    // Create square
    size_t pos = 0;
    for (int i = 0; i < size && pos < result_size - 1; i++) {
        for (int j = 0; j < size && pos < result_size - 1; j++) {
            result[pos++] = frequency_order[i * size + j];
        }
        if (i < size - 1 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

/**
 * @brief Create a keyword-based square
 */
static int create_keyword_square(const char* keyword, const char* alphabet, char* result, size_t result_size) {
    if (!keyword || !alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    // Convert to uppercase manually
    for (int i = 0; alphabet_upper[i]; i++) {
        if (alphabet_upper[i] >= 'a' && alphabet_upper[i] <= 'z') {
            alphabet_upper[i] = alphabet_upper[i] - 32;
        }
    }
    
    char keyword_upper[MAX_ALPHABET_SIZE];
    strcpy(keyword_upper, keyword);
    // Convert to uppercase manually
    for (int i = 0; keyword_upper[i]; i++) {
        if (keyword_upper[i] >= 'a' && keyword_upper[i] <= 'z') {
            keyword_upper[i] = keyword_upper[i] - 32;
        }
    }
    
    // Remove duplicates from keyword while preserving order
    char seen[26] = {0};
    char keyword_unique[MAX_ALPHABET_SIZE] = {0};
    int unique_pos = 0;
    
    for (int i = 0; keyword_upper[i]; i++) {
        char c = keyword_upper[i];
        if (c >= 'A' && c <= 'Z' && !seen[c - 'A']) {
            keyword_unique[unique_pos++] = c;
            seen[c - 'A'] = 1;
        }
    }
    
    // Add remaining alphabet letters
    char remaining[MAX_ALPHABET_SIZE] = {0};
    int remaining_pos = 0;
    
    for (int i = 0; alphabet_upper[i]; i++) {
        char c = alphabet_upper[i];
        if (c >= 'A' && c <= 'Z' && !seen[c - 'A']) {
            remaining[remaining_pos++] = c;
        }
    }
    
    // Combine keyword and remaining letters
    char square_alphabet[MAX_ALPHABET_SIZE];
    strcpy(square_alphabet, keyword_unique);
    strcat(square_alphabet, remaining);
    
    // Handle I=J combination for English
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        char temp[MAX_ALPHABET_SIZE];
        int pos = 0;
        for (int i = 0; square_alphabet[i]; i++) {
            if (square_alphabet[i] != 'J') {
                temp[pos++] = square_alphabet[i];
            }
        }
        temp[pos] = '\0';
        strcpy(square_alphabet, temp);
    }
    
    // Determine square size
    int size;
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        size = 5;  // English uses 5x5 (25 letters with I=J)
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        size = 6;  // Turkish uses 6x6 (29 letters)
    } else {
        size = (strlen(square_alphabet) <= 25) ? 5 : 6;
    }
    
    // Pad if needed
    while (strlen(square_alphabet) < size * size) {
        char temp[MAX_ALPHABET_SIZE];
        strcpy(temp, square_alphabet);
        strcat(temp, square_alphabet);
        strncpy(square_alphabet, temp, size * size);
        square_alphabet[size * size] = '\0';
    }
    
    // Create square
    size_t pos = 0;
    for (int i = 0; i < size && pos < result_size - 1; i++) {
        for (int j = 0; j < size && pos < result_size - 1; j++) {
            result[pos++] = square_alphabet[i * size + j];
        }
        if (i < size - 1 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

/**
 * @brief Create a custom square based on alphabet
 */
static int create_custom_square(const char* alphabet, char* result, size_t result_size) {
    return create_standard_square(alphabet, result, result_size);
}

/**
 * @brief Produce a Polybius square for Nihilist cipher
 */
int nihilist_produce_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    char* result,
    size_t result_size
) {
    if (!square_type || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    if (strcmp(square_type, "standard") == 0) {
        return create_standard_square(alphabet, result, result_size);
    } else if (strcmp(square_type, "frequency") == 0) {
        return create_frequency_square(alphabet, result, result_size);
    } else if (strcmp(square_type, "keyword") == 0) {
        if (!keyword) {
            return -1;
        }
        return create_keyword_square(keyword, alphabet, result, result_size);
    } else if (strcmp(square_type, "custom") == 0) {
        return create_custom_square(alphabet, result, result_size);
    } else if (strcmp(square_type, "caesar") == 0 || 
               strcmp(square_type, "atbash") == 0 || 
               strcmp(square_type, "affine") == 0 || 
               strcmp(square_type, "keyword") == 0) {
        // Use shared monoalphabetic square generation
        // For now, use default parameters - in a full implementation,
        // we would parse mono_params from a JSON string
        return create_monoalphabetic_square(square_type, alphabet, NULL, result, result_size);
    } else {
        return -1; // Invalid square type
    }
}

/**
 * @brief Encrypt text using the Nihilist cipher
 */
int nihilist_encrypt(
    const char* plaintext,
    const char* key,
    const char* square,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!key_type) {
        key_type = "numeric";
    }
    
    char default_square[MAX_SQUARE_SIZE];
    if (!square) {
        if (nihilist_produce_square("standard", NULL, NULL, default_square, sizeof(default_square)) != 0) {
            return -1;
        }
        square = default_square;
    }
    
    // Prepare text and key
    char processed_text[MAX_TEXT_SIZE];
    char processed_key[MAX_TEXT_SIZE];
    prepare_text(plaintext, processed_text, sizeof(processed_text));
    prepare_key(key, key_type, processed_key, sizeof(processed_key));
    
    if (strlen(processed_text) == 0 || strlen(processed_key) == 0) {
        return -1;
    }
    
    // Parse square
    int square_dict[26];
    int square_size;
    if (parse_square(square, square_dict, &square_size) != 0) {
        return -1;
    }
    
    // Convert letters to coordinates
    int coordinates[MAX_TEXT_SIZE];
    int coord_count = letters_to_coordinates(processed_text, square_dict, coordinates, MAX_TEXT_SIZE);
    if (coord_count <= 0) {
        return -1;
    }
    
    // Convert key to numeric values
    int key_values[MAX_TEXT_SIZE];
    int key_count = key_to_values(processed_key, key_type, key_values, MAX_TEXT_SIZE);
    if (key_count <= 0) {
        return -1;
    }
    
    // Add coordinates and key with modular arithmetic
    int encrypted_coordinates[MAX_TEXT_SIZE];
    if (add_coordinates_and_key(coordinates, coord_count, key_values, key_count, square_size, encrypted_coordinates) != coord_count) {
        return -1;
    }
    
    // Convert back to letters
    if (coordinates_to_letters(encrypted_coordinates, coord_count, square, result, result_size) <= 0) {
        return -1;
    }
    
    return 0;
}

/**
 * @brief Decrypt text using the Nihilist cipher
 */
int nihilist_decrypt(
    const char* ciphertext,
    const char* key,
    const char* square,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!key_type) {
        key_type = "numeric";
    }
    
    char default_square[MAX_SQUARE_SIZE];
    if (!square) {
        if (nihilist_produce_square("standard", NULL, NULL, default_square, sizeof(default_square)) != 0) {
            return -1;
        }
        square = default_square;
    }
    
    // Prepare text and key
    char processed_text[MAX_TEXT_SIZE];
    char processed_key[MAX_TEXT_SIZE];
    prepare_text(ciphertext, processed_text, sizeof(processed_text));
    prepare_key(key, key_type, processed_key, sizeof(processed_key));
    
    if (strlen(processed_text) == 0 || strlen(processed_key) == 0) {
        return -1;
    }
    
    // Parse square
    int square_dict[26];
    int square_size;
    if (parse_square(square, square_dict, &square_size) != 0) {
        return -1;
    }
    
    // Convert letters to coordinates
    int coordinates[MAX_TEXT_SIZE];
    int coord_count = letters_to_coordinates(processed_text, square_dict, coordinates, MAX_TEXT_SIZE);
    if (coord_count <= 0) {
        return -1;
    }
    
    // Convert key to numeric values
    int key_values[MAX_TEXT_SIZE];
    int key_count = key_to_values(processed_key, key_type, key_values, MAX_TEXT_SIZE);
    if (key_count <= 0) {
        return -1;
    }
    
    // Subtract key from coordinates with modular arithmetic
    int decrypted_coordinates[MAX_TEXT_SIZE];
    if (subtract_key_from_coordinates(coordinates, coord_count, key_values, key_count, square_size, decrypted_coordinates) != coord_count) {
        return -1;
    }
    
    // Convert back to letters
    if (coordinates_to_letters(decrypted_coordinates, coord_count, square, result, result_size) <= 0) {
        return -1;
    }
    
    return 0;
}

/**
 * @brief Generate a random key for Nihilist cipher
 */
int nihilist_generate_random_key(
    int length,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (length <= 0 || !key_type || !result || result_size == 0) {
        return -1;
    }
    
    if ((size_t)length >= result_size) {
        return -1;
    }
    
    srand(time(NULL));
    
    if (strcmp(key_type, "numeric") == 0) {
        for (int i = 0; i < length; i++) {
            result[i] = '0' + (rand() % 10);
        }
    } else if (strcmp(key_type, "alphabetic") == 0) {
        for (int i = 0; i < length; i++) {
            result[i] = 'A' + (rand() % 26);
        }
    } else {
        return -1;
    }
    
    result[length] = '\0';
    return 0;
}

/**
 * @brief Generate a key matching the length of the text
 */
int nihilist_generate_key_for_text(
    const char* text,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!text || !key_type || !result || result_size == 0) {
        return -1;
    }
    
    char processed_text[MAX_TEXT_SIZE];
    prepare_text(text, processed_text, sizeof(processed_text));
    
    return nihilist_generate_random_key(strlen(processed_text), key_type, result, result_size);
}

/**
 * @brief Encrypt text with a randomly generated key
 */
int nihilist_encrypt_with_random_key(
    const char* plaintext,
    int key_length,
    const char* key_type,
    const char* square,
    char* encrypted_result,
    size_t encrypted_size,
    char* key_result,
    size_t key_size
) {
    if (!plaintext || key_length <= 0 || !key_type || !encrypted_result || !key_result) {
        return -1;
    }
    
    // Generate random key
    if (nihilist_generate_random_key(key_length, key_type, key_result, key_size) != 0) {
        return -1;
    }
    
    // Encrypt with generated key
    return nihilist_encrypt(plaintext, key_result, square, key_type, encrypted_result, encrypted_size);
}
