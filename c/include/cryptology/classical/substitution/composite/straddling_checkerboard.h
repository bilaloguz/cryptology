/**
 * @file straddling_checkerboard.h
 * @brief Straddling Checkerboard Cipher Implementation
 * 
 * A composite cipher that combines substitution and fractionation techniques.
 * Uses a 10×3 grid to convert letters to digits, then applies numeric key addition.
 * 
 * Features:
 * - Custom checkerboard generation
 * - Multiple checkerboard types: standard, keyword-based, custom
 * - Numeric key support with random generation
 * - Turkish alphabet support (29 letters → 3×10 grid)
 * - Composite encryption: substitution + fractionation + key addition
 */

#ifndef STRADDLING_CHECKERBOARD_H
#define STRADDLING_CHECKERBOARD_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Encrypt text using the Straddling Checkerboard cipher
 * 
 * @param plaintext Text to encrypt
 * @param key Encryption key (numeric string for numeric keys)
 * @param checkerboard Custom checkerboard (NULL for standard)
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_encrypt(
    const char* plaintext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Decrypt text using the Straddling Checkerboard cipher
 * 
 * @param ciphertext Text to decrypt
 * @param key Decryption key (numeric string for numeric keys)
 * @param checkerboard Custom checkerboard (NULL for standard)
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_decrypt(
    const char* ciphertext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Produce a checkerboard for Straddling Checkerboard cipher
 * 
 * @param checkerboard_type Type of checkerboard ("standard", "frequency", "vowel_consonant", "keyword", "custom")
 * @param keyword Keyword for keyword-based checkerboard (NULL if not needed)
 * @param alphabet Custom alphabet (NULL for default English)
 * @param result Buffer to store checkerboard
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_produce_checkerboard(
    const char* checkerboard_type,
    const char* keyword,
    const char* alphabet,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a random key for Straddling Checkerboard cipher
 * 
 * @param length Length of the key to generate
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param key Buffer to store generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_generate_random_key(
    int length,
    const char* key_type,
    char* key,
    size_t key_size
);

/**
 * @brief Generate a key of appropriate length for the given text
 * 
 * @param text_length Length of the text to encrypt
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param key Buffer to store generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_generate_key_for_text(
    int text_length,
    const char* key_type,
    char* key,
    size_t key_size
);

/**
 * @brief Encrypt text with a randomly generated key
 * 
 * @param plaintext Text to encrypt
 * @param key_length Length of key to generate (0 for auto)
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @param generated_key Buffer to store generated key
 * @param key_size Size of generated_key buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_encrypt_with_random_key(
    const char* plaintext,
    int key_length,
    const char* key_type,
    char* result,
    size_t result_size,
    char* generated_key,
    size_t key_size
);

/**
 * @brief Encrypt Turkish text using Straddling Checkerboard cipher
 * 
 * @param plaintext Turkish text to encrypt
 * @param key Encryption key
 * @param checkerboard Custom checkerboard (NULL for Turkish default)
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_encrypt_turkish(
    const char* plaintext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Decrypt Turkish text using Straddling Checkerboard cipher
 * 
 * @param ciphertext Turkish text to decrypt
 * @param key Decryption key
 * @param checkerboard Custom checkerboard (NULL for Turkish default)
 * @param key_type Type of key ("numeric" or "alphabetic")
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int straddling_checkerboard_decrypt_turkish(
    const char* ciphertext,
    const char* key,
    const char* checkerboard,
    const char* key_type,
    char* result,
    size_t result_size
);

#ifdef __cplusplus
}
#endif

#endif /* STRADDLING_CHECKERBOARD_H */
