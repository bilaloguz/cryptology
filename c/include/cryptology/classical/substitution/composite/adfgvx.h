#ifndef ADFGVX_H
#define ADFGVX_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @file adfgvx.h
 * @brief ADFGVX/ADFGVZX cipher implementation
 * 
 * The ADFGVX cipher is a composite cipher that combines:
 * 1. Polybius square substitution (6x6 grid)
 * 2. Columnar transposition
 * 
 * Supports both English (26 letters + 10 digits) and Turkish (29 letters + 7 digits) alphabets.
 * Integrates with monoalphabetic square generation utilities.
 */

// Default alphabets
#define DEFAULT_ADFGVX_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#define TURKISH_ADFGVX_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456"

// ADFGVX characters
#define ADFGVX_LETTERS "ADFGVX"
#define ADFGVZX_LETTERS "ADFGVZX"

/**
 * @brief Encrypt text using the ADFGVX cipher
 * 
 * @param plaintext Text to encrypt
 * @param key Keyword for columnar transposition
 * @param square Optional 6x6 Polybius square (NULL for standard)
 * @param alphabet Alphabet to use ("english" or "turkish", NULL for "english")
 * @param mono_params Parameters for monoalphabetic square generation (JSON string)
 * @param result Buffer to store encrypted result
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_encrypt(
    const char* plaintext,
    const char* key,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* result,
    size_t result_size
);

/**
 * @brief Decrypt text using the ADFGVX cipher
 * 
 * @param ciphertext Text to decrypt
 * @param key Keyword for columnar transposition
 * @param square Optional 6x6 Polybius square (NULL for standard)
 * @param alphabet Alphabet to use ("english" or "turkish", NULL for "english")
 * @param mono_params Parameters for monoalphabetic square generation (JSON string)
 * @param result Buffer to store decrypted result
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_decrypt(
    const char* ciphertext,
    const char* key,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* result,
    size_t result_size
);

/**
 * @brief Produce a 6x6 Polybius square for ADFGVX cipher
 * 
 * @param square_type Type of square ("standard", "frequency", "keyword", 
 *                    "custom", "caesar", "atbash", "affine")
 * @param keyword Keyword for keyword-based square (NULL if not needed)
 * @param alphabet Custom alphabet (NULL for default)
 * @param language Language to use ("english" or "turkish", NULL for "english")
 * @param mono_params Parameters for monoalphabetic-based squares (JSON string)
 * @param result Buffer to store square result
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_produce_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a random key for ADFGVX cipher
 * 
 * @param length Desired key length
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_generate_random_key(
    size_t length,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a key matching the length of the given text
 * 
 * @param text Text to match length
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_generate_key_for_text(
    const char* text,
    char* result,
    size_t result_size
);

/**
 * @brief Encrypt with a randomly generated key
 * 
 * @param plaintext Text to encrypt
 * @param key_length Desired key length
 * @param square Optional 6x6 Polybius square (NULL for standard)
 * @param alphabet Alphabet to use ("english" or "turkish", NULL for "english")
 * @param mono_params Parameters for monoalphabetic square generation (JSON string)
 * @param ciphertext Buffer to store encrypted result
 * @param ciphertext_size Size of ciphertext buffer
 * @param generated_key Buffer to store generated key
 * @param key_size Size of generated_key buffer
 * @return 0 on success, -1 on error
 */
int adfgvx_encrypt_with_random_key(
    const char* plaintext,
    size_t key_length,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* ciphertext,
    size_t ciphertext_size,
    char* generated_key,
    size_t key_size
);

#ifdef __cplusplus
}
#endif

#endif // ADFGVX_H
