/**
 * @file straddling_checkerboard.c
 * @brief Straddling Checkerboard Cipher Implementation
 * 
 * A composite cipher that combines substitution and fractionation techniques.
 * Uses a 10×3 grid to convert letters to digits, then applies numeric key addition.
 */

#include "../../../../include/cryptology/classical/substitution/composite/straddling_checkerboard.h"
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>
#include <stdio.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
#define MAX_ALPHABET_SIZE 50
#define MAX_TEXT_SIZE 1000
#define MAX_CHECKERBOARD_SIZE 1000

/**
 * @brief Convert string to uppercase
 */
static void to_upper(char* str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

/**
 * @brief Create standard checkerboard
 */
static int create_standard_checkerboard(char* result, size_t result_size) {
    if (!result || result_size == 0) {
        return -1;
    }
    
    // Standard checkerboard mapping - corrected
    const char* mapping = 
        "0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,"
        "A:0,B:1,C:2,D:3,E:4,F:5,G:6,H:7,I:8,J:9,"
        "K:10,L:11,M:12,N:13,O:14,P:15,Q:16,R:17,S:18,T:19,"
        "U:20,V:21,W:22,X:23,Y:24,Z:25";
    
    if (strlen(mapping) >= result_size) {
        return -1;
    }
    
    strcpy(result, mapping);
    return 0;
}

/**
 * @brief Create keyword-based checkerboard
 */
static int create_keyword_checkerboard(const char* keyword, const char* alphabet, char* result, size_t result_size) {
    if (!keyword || !alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char keyword_upper[MAX_ALPHABET_SIZE];
    char alphabet_upper[MAX_ALPHABET_SIZE];
    
    strcpy(keyword_upper, keyword);
    strcpy(alphabet_upper, alphabet);
    to_upper(keyword_upper);
    to_upper(alphabet_upper);
    
    // Remove duplicates from keyword while preserving order
    char keyword_chars[MAX_ALPHABET_SIZE] = {0};
    int keyword_len = 0;
    int seen[256] = {0};
    
    for (int i = 0; keyword_upper[i]; i++) {
        char c = keyword_upper[i];
        if (strchr(alphabet_upper, c) && !seen[c]) {
            keyword_chars[keyword_len++] = c;
            seen[c] = 1;
        }
    }
    
    // Add remaining alphabet characters
    char all_chars[MAX_ALPHABET_SIZE] = {0};
    int all_len = keyword_len;
    strcpy(all_chars, keyword_chars);
    
    for (int i = 0; alphabet_upper[i]; i++) {
        char c = alphabet_upper[i];
        if (!seen[c]) {
            all_chars[all_len++] = c;
        }
    }
    
    // Build checkerboard string
    char checkerboard[MAX_CHECKERBOARD_SIZE] = {0};
    int pos = 0;
    
    // Row 0: digits
    for (int i = 0; i < 10; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%d:%d,", i, i);
    }
    
    // Row 1: first 10 letters
    for (int i = 0; i < 10 && i < all_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:%d,", all_chars[i], i);
    }
    
    // Row 2: next 10 letters
    for (int i = 10; i < 20 && i < all_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:1%d,", all_chars[i], i - 10);
    }
    
    // Row 3: remaining letters
    for (int i = 20; i < all_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:2%d,", all_chars[i], i - 20);
    }
    
    // Remove trailing comma
    if (pos > 0 && checkerboard[pos - 1] == ',') {
        checkerboard[pos - 1] = '\0';
    }
    
    if (strlen(checkerboard) >= result_size) {
        return -1;
    }
    
    strcpy(result, checkerboard);
    return 0;
}

/**
 * @brief Create custom checkerboard
 */
static int create_custom_checkerboard(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    to_upper(alphabet_upper);
    
    int alphabet_len = strlen(alphabet_upper);
    
    // Build checkerboard string
    char checkerboard[MAX_CHECKERBOARD_SIZE] = {0};
    int pos = 0;
    
    // Row 0: digits
    for (int i = 0; i < 10; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%d:%d,", i, i);
    }
    
    // Row 1: first 10 letters
    for (int i = 0; i < 10 && i < alphabet_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:%d,", alphabet_upper[i], i);
    }
    
    // Row 2: next 10 letters
    for (int i = 10; i < 20 && i < alphabet_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:1%d,", alphabet_upper[i], i - 10);
    }
    
    // Row 3: remaining letters
    for (int i = 20; i < alphabet_len; i++) {
        pos += snprintf(checkerboard + pos, sizeof(checkerboard) - pos, "%c:2%d,", alphabet_upper[i], i - 20);
    }
    
    // Remove trailing comma
    if (pos > 0 && checkerboard[pos - 1] == ',') {
        checkerboard[pos - 1] = '\0';
    }
    
    if (strlen(checkerboard) >= result_size) {
        return -1;
    }
    
    strcpy(result, checkerboard);
    return 0;
}

/**
 * @brief Find character mapping in checkerboard
 */
static int find_char_mapping(const char* checkerboard, char c, char* digits, size_t digits_size) {
    if (!checkerboard || !digits || digits_size == 0) {
        return -1;
    }
    
    char search_pattern[10];
    snprintf(search_pattern, sizeof(search_pattern), "%c:", c);
    
    const char* pos = strstr(checkerboard, search_pattern);
    if (!pos) {
        return -1;
    }
    
    // Find the colon
    const char* colon = strchr(pos, ':');
    if (!colon) {
        return -1;
    }
    
    // Find the comma or end
    const char* comma = strchr(colon + 1, ',');
    if (!comma) {
        comma = colon + strlen(colon);
    }
    
    int len = comma - (colon + 1);
    if (len >= digits_size) {
        return -1;
    }
    
    strncpy(digits, colon + 1, len);
    digits[len] = '\0';
    
    return 0;
}

/**
 * @brief Find digit mapping in checkerboard using reverse lookup
 */
static int find_digit_mapping(const char* checkerboard, const char* digits, char* c) {
    if (!checkerboard || !digits || !c) {
        return -1;
    }
    
    // Create reverse mapping by parsing the checkerboard string
    const char* pos = checkerboard;
    while (*pos) {
        // Find the colon
        const char* colon = strchr(pos, ':');
        if (!colon) break;
        
        // Find the comma or end
        const char* comma = strchr(colon + 1, ',');
        if (!comma) {
            comma = colon + strlen(colon);
        }
        
        // Extract character and digit
        char char_val = *pos;
        int digit_len = comma - (colon + 1);
        char digit_str[10];
        strncpy(digit_str, colon + 1, digit_len);
        digit_str[digit_len] = '\0';
        
        // Check if this digit matches what we're looking for
        // Skip digit-to-digit mappings (0-9), only use letter-to-digit mappings
        if (strcmp(digit_str, digits) == 0 && !(char_val >= '0' && char_val <= '9')) {
            *c = char_val;
            return 0;
        }
        
        // Move to next entry
        pos = comma;
        if (*pos == ',') pos++;
    }
    
    return -1;
}

/**
 * @brief Convert letters to digits using checkerboard
 */
static int letters_to_digits(const char* text, const char* checkerboard, char* result, size_t result_size) {
    if (!text || !checkerboard || !result || result_size == 0) {
        return -1;
    }
    
    char digits[MAX_TEXT_SIZE] = {0};
    int pos = 0;
    
    for (int i = 0; text[i] && pos < result_size - 1; i++) {
        char c = tolower(text[i]);
        char char_digits[10];
        
        if (find_char_mapping(checkerboard, c, char_digits, sizeof(char_digits)) == 0) {
            int len = strlen(char_digits);
            if (pos + len < result_size - 1) {
                strcpy(digits + pos, char_digits);
                pos += len;
            }
        }
    }
    
    if (strlen(digits) >= result_size) {
        return -1;
    }
    
    strcpy(result, digits);
    return 0;
}

/**
 * @brief Convert digits to letters using checkerboard
 */
static int digits_to_letters(const char* digits, const char* checkerboard, char* result, size_t result_size) {
    if (!digits || !checkerboard || !result || result_size == 0) {
        return -1;
    }
    
    char letters[MAX_TEXT_SIZE] = {0};
    int pos = 0;
    int i = 0;
    
    while (digits[i] && pos < result_size - 1) {
        char c;
        
        // Try 2-digit first (for straddling positions)
        if (digits[i + 1]) {
            char two_digit[3] = {digits[i], digits[i + 1], '\0'};
            if (find_digit_mapping(checkerboard, two_digit, &c) == 0) {
                letters[pos++] = c;
                i += 2;
                continue;
            }
        }
        
        // Try 1-digit
        char one_digit[2] = {digits[i], '\0'};
        if (find_digit_mapping(checkerboard, one_digit, &c) == 0) {
            letters[pos++] = c;
        }
        
        i++;
    }
    
    letters[pos] = '\0';
    
    if (strlen(letters) >= result_size) {
        return -1;
    }
    
    strcpy(result, letters);
    return 0;
}

/**
 * @brief Apply numeric key to digits
 */
static int apply_numeric_key(const char* digits, const char* key, int reverse, char* result, size_t result_size) {
    if (!digits || !key || !result || result_size == 0) {
        return -1;
    }
    
    char key_digits[MAX_TEXT_SIZE];
    strcpy(key_digits, key);
    
    char result_digits[MAX_TEXT_SIZE] = {0};
    int key_len = strlen(key_digits);
    int digits_len = strlen(digits);
    
    for (int i = 0; i < digits_len; i++) {
        int key_digit = key_digits[i % key_len] - '0';
        int digit_value = digits[i] - '0';
        
        int result_value;
        if (reverse) {
            result_value = (digit_value - key_digit + 10) % 10;
        } else {
            result_value = (digit_value + key_digit) % 10;
        }
        
        result_digits[i] = '0' + result_value;
    }
    
    if (strlen(result_digits) >= result_size) {
        return -1;
    }
    
    strcpy(result, result_digits);
    return 0;
}

/**
 * @brief Apply alphabetic key to digits
 */
static int apply_alphabetic_key(const char* digits, const char* key, const char* checkerboard, int reverse, char* result, size_t result_size) {
    if (!digits || !key || !checkerboard || !result || result_size == 0) {
        return -1;
    }
    
    char key_upper[MAX_TEXT_SIZE];
    strcpy(key_upper, key);
    to_upper(key_upper);
    
    char result_digits[MAX_TEXT_SIZE] = {0};
    int key_len = strlen(key_upper);
    
    for (int i = 0; digits[i]; i++) {
        char key_char = key_upper[i % key_len];
        char key_digits[10];
        
        if (find_char_mapping(checkerboard, key_char, key_digits, sizeof(key_digits)) == 0) {
            int key_digit = atoi(key_digits);
            int digit_value = digits[i] - '0';
            
            int result_value;
            if (reverse) {
                result_value = (digit_value - key_digit + 10) % 10;
            } else {
                result_value = (digit_value + key_digit) % 10;
            }
            
            result_digits[i] = '0' + result_value;
        } else {
            result_digits[i] = digits[i];
        }
    }
    
    if (strlen(result_digits) >= result_size) {
        return -1;
    }
    
    strcpy(result, result_digits);
    return 0;
}

/**
 * @brief Encrypt text using the Straddling Checkerboard cipher
 */
int straddling_checkerboard_encrypt(
    const char* plaintext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!checkerboard) {
        char default_checkerboard[MAX_CHECKERBOARD_SIZE];
        if (create_standard_checkerboard(default_checkerboard, sizeof(default_checkerboard)) != 0) {
            return -1;
        }
        checkerboard = default_checkerboard;
    }
    
    if (!key_type) {
        key_type = "numeric";
    }
    
    // Prepare text (remove spaces)
    char processed_text[MAX_TEXT_SIZE];
    int pos = 0;
    for (int i = 0; plaintext[i] && pos < sizeof(processed_text) - 1; i++) {
        if (plaintext[i] != ' ') {
            processed_text[pos++] = tolower(plaintext[i]);
        }
    }
    processed_text[pos] = '\0';
    
    // Step 1: Convert letters to digits
    char digits[MAX_TEXT_SIZE];
    if (letters_to_digits(processed_text, checkerboard, digits, sizeof(digits)) != 0) {
        return -1;
    }
    
    // Step 2: Apply key
    char encrypted_digits[MAX_TEXT_SIZE];
    if (strcmp(key_type, "numeric") == 0) {
        if (apply_numeric_key(digits, key, 0, encrypted_digits, sizeof(encrypted_digits)) != 0) {
            return -1;
        }
    } else {
        if (apply_alphabetic_key(digits, key, checkerboard, 0, encrypted_digits, sizeof(encrypted_digits)) != 0) {
            return -1;
        }
    }
    
    // Step 3: Convert digits back to letters
    if (digits_to_letters(encrypted_digits, checkerboard, result, result_size) != 0) {
        return -1;
    }
    
    return 0;
}

/**
 * @brief Decrypt text using the Straddling Checkerboard cipher
 */
int straddling_checkerboard_decrypt(
    const char* ciphertext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!checkerboard) {
        char default_checkerboard[MAX_CHECKERBOARD_SIZE];
        if (create_standard_checkerboard(default_checkerboard, sizeof(default_checkerboard)) != 0) {
            return -1;
        }
        checkerboard = default_checkerboard;
    }
    
    if (!key_type) {
        key_type = "numeric";
    }
    
    // Prepare text (remove spaces)
    char processed_text[MAX_TEXT_SIZE];
    int pos = 0;
    for (int i = 0; ciphertext[i] && pos < sizeof(processed_text) - 1; i++) {
        if (ciphertext[i] != ' ') {
            processed_text[pos++] = tolower(ciphertext[i]);
        }
    }
    processed_text[pos] = '\0';
    
    // Step 1: Convert letters to digits
    char digits[MAX_TEXT_SIZE];
    if (letters_to_digits(processed_text, checkerboard, digits, sizeof(digits)) != 0) {
        return -1;
    }
    
    // Step 2: Apply key (reverse)
    char decrypted_digits[MAX_TEXT_SIZE];
    if (strcmp(key_type, "numeric") == 0) {
        if (apply_numeric_key(digits, key, 1, decrypted_digits, sizeof(decrypted_digits)) != 0) {
            return -1;
        }
    } else {
        if (apply_alphabetic_key(digits, key, checkerboard, 1, decrypted_digits, sizeof(decrypted_digits)) != 0) {
            return -1;
        }
    }
    
    // Step 3: Convert digits back to letters
    if (digits_to_letters(decrypted_digits, checkerboard, result, result_size) != 0) {
        return -1;
    }
    
    return 0;
}

/**
 * @brief Create frequency-based checkerboard
 */
static int create_frequency_checkerboard(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    to_upper(alphabet_upper);
    
    char frequency_order[MAX_ALPHABET_SIZE];
    
    // Define frequency-based letter orders for English and Turkish
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        // English frequency order (most to least frequent)
        strcpy(frequency_order, "ETAOINSHRDLCUMWFGYPBVKJXQZ");
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        // Turkish frequency order (most to least frequent)
        strcpy(frequency_order, "AENRLDKMSUTOYBGHCÇPFVZŞĞÖÜJ");
    } else {
        // For other alphabets, use alphabetical order
        strcpy(frequency_order, alphabet_upper);
    }
    
    return create_custom_checkerboard(frequency_order, result, result_size);
}

/**
 * @brief Create vowel-consonant separation checkerboard
 */
static int create_vowel_consonant_checkerboard(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strcpy(alphabet_upper, alphabet);
    to_upper(alphabet_upper);
    
    char vowels[MAX_ALPHABET_SIZE] = {0};
    char consonants[MAX_ALPHABET_SIZE] = {0};
    
    // Define vowels and consonants
    if (strcmp(alphabet_upper, "abcdefghijklmnopqrstuvwxyz") == 0) {
        strcpy(vowels, "AEIOU");
        strcpy(consonants, "BCDFGHJKLMNPQRSTVWXYZ");
    } else if (strcmp(alphabet_upper, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        strcpy(vowels, "AEIOUÖÜ");
        strcpy(consonants, "BCÇDFGĞHJKLMNPQRSSŞTVWXYZ");
    } else {
        // For other alphabets, separate vowels and consonants
        strcpy(vowels, "AEIOU");
        int vowel_pos = 0;
        int consonant_pos = 0;
        for (int i = 0; alphabet_upper[i]; i++) {
            char c = alphabet_upper[i];
            if (strchr("AEIOU", c)) {
                vowels[vowel_pos++] = c;
            } else {
                consonants[consonant_pos++] = c;
            }
        }
    }
    
    // Combine vowels and consonants
    char combined_order[MAX_ALPHABET_SIZE];
    strcpy(combined_order, vowels);
    strcat(combined_order, consonants);
    
    return create_custom_checkerboard(combined_order, result, result_size);
}

/**
 * @brief Produce a checkerboard for Straddling Checkerboard cipher
 */
int straddling_checkerboard_produce_checkerboard(
    const char* checkerboard_type,
    const char* keyword,
    const char* alphabet,
    char* result,
    size_t result_size
) {
    if (!checkerboard_type || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    if (strcmp(checkerboard_type, "standard") == 0) {
        return create_standard_checkerboard(result, result_size);
    } else if (strcmp(checkerboard_type, "frequency") == 0) {
        return create_frequency_checkerboard(alphabet, result, result_size);
    } else if (strcmp(checkerboard_type, "vowel_consonant") == 0) {
        return create_vowel_consonant_checkerboard(alphabet, result, result_size);
    } else if (strcmp(checkerboard_type, "keyword") == 0) {
        if (!keyword) {
            return -1;
        }
        return create_keyword_checkerboard(keyword, alphabet, result, result_size);
    } else if (strcmp(checkerboard_type, "custom") == 0) {
        return create_custom_checkerboard(alphabet, result, result_size);
    } else {
        return -1;
    }
}

/**
 * @brief Generate a random key for Straddling Checkerboard cipher
 */
int straddling_checkerboard_generate_random_key(
    int length,
    const char* key_type,
    char* key,
    size_t key_size
) {
    if (length <= 0 || !key_type || !key || key_size == 0) {
        return -1;
    }
    
    if (length >= key_size) {
        return -1;
    }
    
    srand(time(NULL));
    
    if (strcmp(key_type, "numeric") == 0) {
        for (int i = 0; i < length; i++) {
            key[i] = '0' + (rand() % 10);
        }
    } else if (strcmp(key_type, "alphabetic") == 0) {
        for (int i = 0; i < length; i++) {
            key[i] = 'A' + (rand() % 26);
        }
    } else {
        return -1;
    }
    
    key[length] = '\0';
    return 0;
}

/**
 * @brief Generate a key of appropriate length for the given text
 */
int straddling_checkerboard_generate_key_for_text(
    int text_length,
    const char* key_type,
    char* key,
    size_t key_size
) {
    if (text_length <= 0 || !key_type || !key || key_size == 0) {
        return -1;
    }
    
    int key_length = 3 + (rand() % (text_length < 10 ? text_length - 2 : 8));
    return straddling_checkerboard_generate_random_key(key_length, key_type, key, key_size);
}

/**
 * @brief Encrypt text with a randomly generated key
 */
int straddling_checkerboard_encrypt_with_random_key(
    const char* plaintext,
    int key_length,
    const char* key_type,
    char* result,
    size_t result_size,
    char* generated_key,
    size_t key_size
) {
    if (!plaintext || !key_type || !result || !generated_key || result_size == 0 || key_size == 0) {
        return -1;
    }
    
    if (key_length <= 0) {
        key_length = 3 + (rand() % 8);
    }
    
    if (straddling_checkerboard_generate_random_key(key_length, key_type, generated_key, key_size) != 0) {
        return -1;
    }
    
    return straddling_checkerboard_encrypt(plaintext, generated_key, NULL, key_type, result, result_size);
}

/**
 * @brief Encrypt Turkish text using Straddling Checkerboard cipher
 */
int straddling_checkerboard_encrypt_turkish(
    const char* plaintext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!checkerboard) {
        char turkish_checkerboard[MAX_CHECKERBOARD_SIZE];
        if (create_custom_checkerboard(TURKISH_ALPHABET, turkish_checkerboard, sizeof(turkish_checkerboard)) != 0) {
            return -1;
        }
        return straddling_checkerboard_encrypt(plaintext, key, turkish_checkerboard, key_type, result, result_size);
    }
    
    return straddling_checkerboard_encrypt(plaintext, key, checkerboard, key_type, result, result_size);
}

/**
 * @brief Decrypt Turkish text using Straddling Checkerboard cipher
 */
int straddling_checkerboard_decrypt_turkish(
    const char* ciphertext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
) {
    if (!checkerboard) {
        char turkish_checkerboard[MAX_CHECKERBOARD_SIZE];
        if (create_custom_checkerboard(TURKISH_ALPHABET, turkish_checkerboard, sizeof(turkish_checkerboard)) != 0) {
            return -1;
        }
        return straddling_checkerboard_decrypt(ciphertext, key, turkish_checkerboard, key_type, result, result_size);
    }
    
    return straddling_checkerboard_decrypt(ciphertext, key, checkerboard, key_type, result, result_size);
}
