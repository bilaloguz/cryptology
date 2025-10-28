/**
 * @file porta.c
 * @brief Porta Cipher implementation with custom pairing support
 */

#include "cryptology/classical/substitution/polyalphabetic/porta.h"
#include <time.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
#define MAX_PAIRS 20
#define MAX_BUFFER_SIZE 1000

// Helper function to validate alphabetic key
static int validate_alphabetic_key(const char* key) {
    if (!key || strlen(key) == 0) {
        return -1;
    }
    
    for (const char* p = key; *p; p++) {
        if (!isalpha(*p)) {
            return -1;
        }
    }
    
    return 0;
}

// Helper function to find character position in alphabet
static int find_char_position(const char* alphabet, char c) {
    char upper_c = tolower(c);
    const char* pos = strchr(alphabet, upper_c);
    if (pos) {
        return pos - alphabet;
    }
    return -1;
}

// Helper function to find which pair contains a letter
static int find_letter_pair(char letter, const porta_pair_t* pairs, size_t pairs_count) {
    char upper_letter = tolower(letter);
    
    for (size_t i = 0; i < pairs_count; i++) {
        if (tolower(pairs[i].first) == upper_letter || tolower(pairs[i].second) == upper_letter) {
            return i;
        }
    }
    
    return -1; // Letter not found in any pair
}

// Helper function to create default pairs
static int create_default_pairs(const char* alphabet, porta_pair_t* pairs, size_t* pairs_count) {
    size_t alphabet_len = strlen(alphabet);
    
    if (alphabet_len == 26) {
        // English alphabet: create 13 pairs
        *pairs_count = 13;
        for (size_t i = 0; i < 13; i++) {
            pairs[i].first = alphabet[i];
            pairs[i].second = alphabet[i + 13];
        }
    } else {
        // Other alphabets: create pairs based on length
        *pairs_count = alphabet_len / 2;
        for (size_t i = 0; i < *pairs_count; i++) {
            pairs[i].first = alphabet[i];
            pairs[i].second = alphabet[i + *pairs_count];
        }
    }
    
    return 0;
}

// Helper function to create Turkish pairs
static int create_turkish_pairs(const char* alphabet, porta_pair_t* pairs, size_t* pairs_count) {
    if (strlen(alphabet) != 29) {
        // Fall back to default if not Turkish alphabet
        return create_default_pairs(alphabet, pairs, pairs_count);
    }
    
    // Turkish-specific pairs (14 pairs)
    *pairs_count = 14;
    porta_pair_t turkish_pairs[] = {
        {'A', 'L'}, {'B', 'M'}, {'C', 'N'}, {'Ç', 'O'}, {'D', 'Ö'},
        {'E', 'P'}, {'F', 'R'}, {'G', 'S'}, {'Ğ', 'Ş'}, {'H', 'T'},
        {'I', 'U'}, {'İ', 'Ü'}, {'J', 'V'}, {'K', 'Y'}
    };
    
    // Validate that all pairs exist in the alphabet
    size_t valid_count = 0;
    for (size_t i = 0; i < 14; i++) {
        if (strchr(alphabet, turkish_pairs[i].first) && strchr(alphabet, turkish_pairs[i].second)) {
            pairs[valid_count] = turkish_pairs[i];
            valid_count++;
        }
    }
    
    *pairs_count = valid_count;
    return 0;
}

// Helper function to create balanced pairs
static int create_balanced_pairs(const char* alphabet, porta_pair_t* pairs, size_t* pairs_count) {
    size_t alphabet_len = strlen(alphabet);
    *pairs_count = alphabet_len / 2;
    
    for (size_t i = 0; i < *pairs_count; i++) {
        pairs[i].first = alphabet[i];
        pairs[i].second = alphabet[i + *pairs_count];
    }
    
    return 0;
}

// Helper function to validate custom pairs
static int validate_custom_pairs(const porta_pair_t* custom_pairs, size_t custom_pairs_count, 
                                const char* alphabet, porta_pair_t* validated_pairs) {
    if (custom_pairs_count == 0) {
        return -1;
    }
    
    char used_letters[256] = {0}; // Track used letters
    
    for (size_t i = 0; i < custom_pairs_count; i++) {
        char first = custom_pairs[i].first;
        char second = custom_pairs[i].second;
        
        // Check if letters are in alphabet
        if (!strchr(alphabet, first) || !strchr(alphabet, second)) {
            return -1;
        }
        
        // Check for duplicates
        if (used_letters[(unsigned char)first] || used_letters[(unsigned char)second]) {
            return -1;
        }
        
        used_letters[(unsigned char)first] = 1;
        used_letters[(unsigned char)second] = 1;
        
        validated_pairs[i] = custom_pairs[i];
    }
    
    return 0;
}

int porta_produce_pairs(const char *pair_type,
                       const char *alphabet,
                       porta_pair_t *pairs,
                       size_t *pairs_count,
                       const porta_pair_t *custom_pairs,
                       size_t custom_pairs_count) {
    if (!pair_type || !alphabet || !pairs || !pairs_count) {
        return -1;
    }
    
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_ALPHABET;
    }
    
    if (strcmp(pair_type, "default") == 0) {
        return create_default_pairs(use_alphabet, pairs, pairs_count);
    }
    else if (strcmp(pair_type, "custom") == 0) {
        if (!custom_pairs) {
            return -1;
        }
        if (validate_custom_pairs(custom_pairs, custom_pairs_count, use_alphabet, pairs) != 0) {
            return -1;
        }
        *pairs_count = custom_pairs_count;
        return 0;
    }
    else if (strcmp(pair_type, "turkish") == 0) {
        return create_turkish_pairs(use_alphabet, pairs, pairs_count);
    }
    else if (strcmp(pair_type, "balanced") == 0) {
        return create_balanced_pairs(use_alphabet, pairs, pairs_count);
    }
    
    return -1; // Unknown pair type
}

int porta_encrypt(const char *plaintext,
                 const char *key,
                 const char *alphabet,
                 const porta_pair_t *pairs,
                 size_t pairs_count,
                 char *result, size_t result_size) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    // Validate alphabetic key
    if (validate_alphabetic_key(key) != 0) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    const porta_pair_t* use_pairs = pairs;
    size_t use_pairs_count = pairs_count;
    
    // Create default pairs if none provided
    porta_pair_t default_pairs[MAX_PAIRS];
    if (!use_pairs) {
        if (create_default_pairs(use_alphabet, default_pairs, &use_pairs_count) != 0) {
            return -1;
        }
        use_pairs = default_pairs;
    }
    
    size_t key_index = 0;
    size_t result_pos = 0;
    
    for (const char* p = plaintext; *p && result_pos < result_size - 1; p++) {
        if (strchr(use_alphabet, tolower(*p))) {
            // Find which pair contains this letter
            int pair_index = find_letter_pair(*p, use_pairs, use_pairs_count);
            
            if (pair_index >= 0) {
                // Determine which letter in the pair to use based on key
                char key_letter = tolower(key[key_index % strlen(key)]);
                int key_pos = find_char_position(use_alphabet, key_letter);
                
                if (key_pos >= 0) {
                    // Use the pair based on key letter position
                    char encrypted_char;
                    if (key_pos % 2 == 0) {  // Even position (A, C, E, etc.)
                        if (tolower(*p) == tolower(use_pairs[pair_index].first)) {
                            encrypted_char = use_pairs[pair_index].second;
                        } else {
                            encrypted_char = use_pairs[pair_index].first;
                        }
                    } else {  // Odd position (B, D, F, etc.)
                        if (tolower(*p) == tolower(use_pairs[pair_index].first)) {
                            encrypted_char = use_pairs[pair_index].first;
                        } else {
                            encrypted_char = use_pairs[pair_index].second;
                        }
                    }
                    
                    // Preserve case
                    if (islower(*p)) {
                        encrypted_char = tolower(encrypted_char);
                    }
                    
                    result[result_pos++] = encrypted_char;
                    key_index++;
                } else {
                    // Key letter not in alphabet, keep original
                    result[result_pos++] = *p;
                }
            } else {
                // Letter not in any pair, keep as is
                result[result_pos++] = *p;
            }
        } else {
            // Preserve non-alphabetic characters
            result[result_pos++] = *p;
        }
    }
    
    result[result_pos] = '\0';
    return 0;
}

int porta_decrypt(const char *ciphertext,
                 const char *key,
                 const char *alphabet,
                 const porta_pair_t *pairs,
                 size_t pairs_count,
                 char *result, size_t result_size) {
    // Porta cipher is self-reciprocal, so decryption is identical to encryption
    return porta_encrypt(ciphertext, key, alphabet, pairs, pairs_count, result, result_size);
}

int porta_generate_random_key(int length, const char *alphabet,
                             char *result, size_t result_size) {
    if (length <= 0 || !result || result_size == 0) {
        return -1;
    }
    
    if (result_size < length + 1) {
        return -1;
    }
    
    const char* use_alphabet = alphabet ? alphabet : DEFAULT_ALPHABET;
    
    srand(time(NULL));
    
    for (int i = 0; i < length; i++) {
        int random_index = rand() % strlen(use_alphabet);
        result[i] = use_alphabet[random_index];
    }
    
    result[length] = '\0';
    return 0;
}

int porta_generate_key_for_text(const char *plaintext, const char *alphabet,
                               char *result, size_t result_size) {
    if (!plaintext || !result || result_size == 0) {
        return -1;
    }
    
    // Count alphabetic characters
    int alphabetic_chars = 0;
    for (const char* p = plaintext; *p; p++) {
        if (isalpha(*p)) {
            alphabetic_chars++;
        }
    }
    
    return porta_generate_random_key(alphabetic_chars, alphabet, result, result_size);
}

int porta_encrypt_with_random_key(const char *plaintext,
                                 const char *alphabet,
                                 const porta_pair_t *pairs,
                                 size_t pairs_count,
                                 int key_length,
                                 char *encrypted_result, size_t encrypted_size,
                                 char *key_result, size_t key_size) {
    if (!plaintext || !encrypted_result || !key_result || 
        encrypted_size == 0 || key_size == 0) {
        return -1;
    }
    
    // Generate random key
    int actual_key_length = key_length;
    if (actual_key_length <= 0) {
        // Count alphabetic characters
        actual_key_length = 0;
        for (const char* p = plaintext; *p; p++) {
            if (isalpha(*p)) {
                actual_key_length++;
            }
        }
    }
    
    if (porta_generate_random_key(actual_key_length, alphabet, key_result, key_size) != 0) {
        return -1;
    }
    
    // Encrypt using the generated key
    return porta_encrypt(plaintext, key_result, alphabet, pairs, pairs_count, 
                        encrypted_result, encrypted_size);
}
