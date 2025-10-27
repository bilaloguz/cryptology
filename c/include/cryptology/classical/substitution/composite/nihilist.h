/**
 * @file nihilist.h
 * @brief Nihilist Cipher Implementation
 * 
 * The Nihilist cipher is a composite cipher that combines:
 * 1. Polybius square substitution
 * 2. Numeric key addition with modular arithmetic
 * 
 * It converts letters to coordinates, adds a numeric key, and converts back to letters.
 */

#ifndef NIHILIST_H
#define NIHILIST_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Encrypt text using the Nihilist cipher
 * 
 * @param plaintext Text to encrypt
 * @param key Numeric or alphabetic key
 * @param square Polybius square (NULL for default standard square)
 * @param key_type "numeric" or "alphabetic"
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int nihilist_encrypt(
    const char* plaintext,
    const char* key,
    const char* square,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Decrypt text using the Nihilist cipher
 * 
 * @param ciphertext Text to decrypt
 * @param key Numeric or alphabetic key
 * @param square Polybius square (NULL for default standard square)
 * @param key_type "numeric" or "alphabetic"
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int nihilist_decrypt(
    const char* ciphertext,
    const char* key,
    const char* square,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Produce a Polybius square for Nihilist cipher
 * 
 * @param square_type Type of square ("standard", "frequency", "keyword", "custom", 
 *                    "caesar", "atbash", "affine")
 * @param keyword Keyword for keyword-based square (NULL if not needed)
 * @param alphabet Custom alphabet (NULL for default English)
 * @param result Buffer to store square
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int nihilist_produce_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a random key for Nihilist cipher
 * 
 * @param length Length of key to generate
 * @param key_type "numeric" or "alphabetic"
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int nihilist_generate_random_key(
    int length,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a key matching the length of the text
 * 
 * @param text Text to match key length
 * @param key_type "numeric" or "alphabetic"
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int nihilist_generate_key_for_text(
    const char* text,
    const char* key_type,
    char* result,
    size_t result_size
);

/**
 * @brief Encrypt text with a randomly generated key
 * 
 * @param plaintext Text to encrypt
 * @param key_length Length of key to generate
 * @param key_type "numeric" or "alphabetic"
 * @param square Polybius square (NULL for default standard square)
 * @param encrypted_result Buffer to store encrypted text
 * @param encrypted_size Size of encrypted result buffer
 * @param key_result Buffer to store generated key
 * @param key_size Size of key result buffer
 * @return 0 on success, -1 on error
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
);

#ifdef __cplusplus
}
#endif

#endif /* NIHILIST_H */
