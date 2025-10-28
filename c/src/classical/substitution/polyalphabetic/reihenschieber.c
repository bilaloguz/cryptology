/**
 * @file reihenschieber.c
 * @brief Reihenschieber Cipher Implementation
 * 
 * A mechanical polyalphabetic substitution cipher that uses shifting strips.
 * Essentially a mechanical Vigenère cipher with progressive shifting capabilities.
 */

#include "../../../../include/cryptology/classical/substitution/polyalphabetic/reihenschieber.h"
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
#define MAX_ALPHABET_SIZE 50
#define MAX_TEXT_SIZE 1000

/**
 * @brief Convert string to uppercase
 */
static void to_upper(char* str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

/**
 * @brief Find character index in alphabet
 */
static int find_char_index(const char* alphabet, char c) {
    for (int i = 0; alphabet[i]; i++) {
        if (alphabet[i] == c) {
            return i;
        }
    }
    return -1;
}

/**
 * @brief Validate that all characters in text are in alphabet
 */
static int validate_text(const char* text, const char* alphabet) {
    for (int i = 0; text[i]; i++) {
        if (find_char_index(alphabet, text[i]) == -1) {
            return -1;
        }
    }
    return 0;
}

/**
 * @brief Prepare text for processing
 */
static int prepare_text(const char* input, char* output, size_t output_size, const char* alphabet) {
    if (!input || !output || output_size == 0) {
        return -1;
    }
    
    size_t len = strlen(input);
    if (len >= output_size) {
        return -1;
    }
    
    strcpy(output, input);
    to_upper(output);
    
    // Remove characters not in alphabet
    int j = 0;
    for (int i = 0; output[i]; i++) {
        if (find_char_index(alphabet, output[i]) != -1) {
            output[j++] = output[i];
        }
    }
    output[j] = '\0';
    
    return 0;
}

/**
 * @brief Get shift value based on mode
 */
static int get_shift_value(
    const char* shift_mode,
    int shift_amount,
    int char_index,
    const int* custom_shifts,
    int custom_shifts_count,
    int* cumulative_shift
) {
    if (strcmp(shift_mode, "fixed") == 0) {
        return shift_amount;
    } else if (strcmp(shift_mode, "progressive") == 0) {
        *cumulative_shift += shift_amount;
        return *cumulative_shift;
    } else if (strcmp(shift_mode, "custom") == 0) {
        if (custom_shifts && char_index < custom_shifts_count) {
            return custom_shifts[char_index];
        }
        return 0;
    }
    return 0;
}

/**
 * @brief Encrypt text using the Reihenschieber cipher
 */
int reihenschieber_encrypt(
    const char* plaintext,
    const char* key,
    const char* alphabet,
    const char* shift_mode,
    const char* shift_direction,
    int shift_amount,
    const int* custom_shifts,
    int custom_shifts_count,
    char* result,
    size_t result_size
) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    if (!shift_mode) {
        shift_mode = "fixed";
    }
    
    if (!shift_direction) {
        shift_direction = "forward";
    }
    
    char processed_text[MAX_TEXT_SIZE];
    char processed_key[MAX_TEXT_SIZE];
    
    if (prepare_text(plaintext, processed_text, sizeof(processed_text), alphabet) != 0) {
        return -1;
    }
    
    if (prepare_text(key, processed_key, sizeof(processed_key), alphabet) != 0) {
        return -1;
    }
    
    if (strlen(processed_text) >= result_size) {
        return -1;
    }
    
    int alphabet_len = strlen(alphabet);
    int key_len = strlen(processed_key);
    int text_len = strlen(processed_text);
    
    int key_index = 0;
    int cumulative_shift = 0;
    
    for (int i = 0; i < text_len; i++) {
        char current_char = processed_text[i];
        char current_key = processed_key[key_index % key_len];
        key_index++;
        
        int char_index = find_char_index(alphabet, current_char);
        int key_index_pos = find_char_index(alphabet, current_key);
        
        if (char_index == -1 || key_index_pos == -1) {
            return -1;
        }
        
        int current_shift = get_shift_value(shift_mode, shift_amount, i, custom_shifts, custom_shifts_count, &cumulative_shift);
        
        if (strcmp(shift_direction, "backward") == 0) {
            current_shift = -current_shift;
        }
        
        int encrypted_index = (char_index + key_index_pos + current_shift) % alphabet_len;
        if (encrypted_index < 0) {
            encrypted_index += alphabet_len;
        }
        
        result[i] = alphabet[encrypted_index];
    }
    result[text_len] = '\0';
    
    return 0;
}

/**
 * @brief Decrypt text using the Reihenschieber cipher
 */
int reihenschieber_decrypt(
    const char* ciphertext,
    const char* key,
    const char* alphabet,
    const char* shift_mode,
    const char* shift_direction,
    int shift_amount,
    const int* custom_shifts,
    int custom_shifts_count,
    char* result,
    size_t result_size
) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    if (!shift_mode) {
        shift_mode = "fixed";
    }
    
    if (!shift_direction) {
        shift_direction = "forward";
    }
    
    char processed_text[MAX_TEXT_SIZE];
    char processed_key[MAX_TEXT_SIZE];
    
    if (prepare_text(ciphertext, processed_text, sizeof(processed_text), alphabet) != 0) {
        return -1;
    }
    
    if (prepare_text(key, processed_key, sizeof(processed_key), alphabet) != 0) {
        return -1;
    }
    
    if (strlen(processed_text) >= result_size) {
        return -1;
    }
    
    int alphabet_len = strlen(alphabet);
    int key_len = strlen(processed_key);
    int text_len = strlen(processed_text);
    
    int key_index = 0;
    int cumulative_shift = 0;
    
    for (int i = 0; i < text_len; i++) {
        char current_char = processed_text[i];
        char current_key = processed_key[key_index % key_len];
        key_index++;
        
        int char_index = find_char_index(alphabet, current_char);
        int key_index_pos = find_char_index(alphabet, current_key);
        
        if (char_index == -1 || key_index_pos == -1) {
            return -1;
        }
        
        int current_shift = get_shift_value(shift_mode, shift_amount, i, custom_shifts, custom_shifts_count, &cumulative_shift);
        
        if (strcmp(shift_direction, "backward") == 0) {
            current_shift = -current_shift;
        }
        
        int decrypted_index = (char_index - key_index_pos - current_shift) % alphabet_len;
        if (decrypted_index < 0) {
            decrypted_index += alphabet_len;
        }
        
        result[i] = alphabet[decrypted_index];
    }
    result[text_len] = '\0';
    
    return 0;
}

/**
 * @brief Generate a random key for Reihenschieber cipher
 */
int reihenschieber_generate_random_key(int length, char* key, size_t key_size) {
    if (length <= 0 || !key || key_size == 0) {
        return -1;
    }
    
    if (length >= key_size) {
        return -1;
    }
    
    srand(time(NULL));
    
    for (int i = 0; i < length; i++) {
        key[i] = 'A' + (rand() % 26);
    }
    key[length] = '\0';
    
    return 0;
}

/**
 * @brief Generate a key of appropriate length for the given text
 */
int reihenschieber_generate_key_for_text(int text_length, char* key, size_t key_size) {
    if (text_length <= 0 || !key || key_size == 0) {
        return -1;
    }
    
    int key_length = 3 + (rand() % (text_length < 10 ? text_length - 2 : 8));
    return reihenschieber_generate_random_key(key_length, key, key_size);
}

/**
 * @brief Encrypt text with a randomly generated key
 */
int reihenschieber_encrypt_with_random_key(
    const char* plaintext,
    int key_length,
    char* result,
    size_t result_size,
    char* generated_key,
    size_t key_size
) {
    if (!plaintext || !result || !generated_key || result_size == 0 || key_size == 0) {
        return -1;
    }
    
    if (key_length <= 0) {
        key_length = 3 + (rand() % 8);
    }
    
    if (reihenschieber_generate_random_key(key_length, generated_key, key_size) != 0) {
        return -1;
    }
    
    return reihenschieber_encrypt(plaintext, generated_key, NULL, "fixed", "forward", 1, NULL, 0, result, result_size);
}

/**
 * @brief Produce custom shift patterns for Reihenschieber cipher
 */
int reihenschieber_produce_custom_shifts(
    const char* pattern_type,
    int pattern_length,
    int* shifts,
    size_t shifts_size
) {
    if (!pattern_type || pattern_length <= 0 || !shifts || shifts_size == 0) {
        return -1;
    }
    
    if (pattern_length >= shifts_size) {
        return -1;
    }
    
    if (strcmp(pattern_type, "alternating") == 0) {
        for (int i = 0; i < pattern_length; i++) {
            shifts[i] = (i % 2 == 0) ? 1 : -1;
        }
    } else if (strcmp(pattern_type, "fibonacci") == 0) {
        if (pattern_length >= 1) shifts[0] = 1;
        if (pattern_length >= 2) shifts[1] = 1;
        for (int i = 2; i < pattern_length; i++) {
            shifts[i] = shifts[i-1] + shifts[i-2];
        }
    } else if (strcmp(pattern_type, "prime") == 0) {
        int primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
        int primes_count = sizeof(primes) / sizeof(primes[0]);
        for (int i = 0; i < pattern_length; i++) {
            shifts[i] = primes[i % primes_count];
        }
    } else if (strcmp(pattern_type, "random") == 0) {
        srand(time(NULL));
        for (int i = 0; i < pattern_length; i++) {
            shifts[i] = (rand() % 11) - 5; // -5 to 5
        }
    } else {
        return -1;
    }
    
    return 0;
}

/**
 * @brief Encrypt Turkish text using Reihenschieber cipher
 */
int reihenschieber_encrypt_turkish(
    const char* plaintext,
    const char* key,
    const char* shift_mode,
    const char* shift_direction,
    int shift_amount,
    const int* custom_shifts,
    int custom_shifts_count,
    char* result,
    size_t result_size
) {
    return reihenschieber_encrypt(plaintext, key, TURKISH_ALPHABET, shift_mode, shift_direction, shift_amount, custom_shifts, custom_shifts_count, result, result_size);
}

/**
 * @brief Decrypt Turkish text using Reihenschieber cipher
 */
int reihenschieber_decrypt_turkish(
    const char* ciphertext,
    const char* key,
    const char* shift_mode,
    const char* shift_direction,
    int shift_amount,
    const int* custom_shifts,
    int custom_shifts_count,
    char* result,
    size_t result_size
) {
    return reihenschieber_decrypt(ciphertext, key, TURKISH_ALPHABET, shift_mode, shift_direction, shift_amount, custom_shifts, custom_shifts_count, result, result_size);
}
