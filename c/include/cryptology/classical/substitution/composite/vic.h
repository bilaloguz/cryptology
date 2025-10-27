/**
 * @file vic.h
 * @brief VIC Cipher Implementation
 * 
 * The VIC cipher is a complex multi-stage encryption system that combines:
 * 1. Polybius square substitution (6x6)
 * 2. Fractionation (letters to digits)
 * 3. Straddling checkerboard (digits to letters)
 * 4. Columnar transposition (multiple passes)
 * 5. Numeric key addition (modular arithmetic)
 * 6. Chain addition (progressive key modification)
 * 
 * Supports both English and Turkish alphabets with UTF-8 handling.
 * Integrates with existing monoalphabetic square generation utilities.
 */

#ifndef VIC_H
#define VIC_H

#include <stddef.h>

// Default alphabets
#define DEFAULT_VIC_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#define TURKISH_VIC_ALPHABET "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456"

// VIC characters for substitution
#define VIC_LETTERS "ADFGVX"

/**
 * @brief Encrypt text using the VIC cipher
 * 
 * @param plaintext Text to encrypt
 * @param polybius_key Keyword for Polybius square generation
 * @param checkerboard_key Keyword for straddling checkerboard
 * @param transposition_key Keyword for columnar transposition
 * @param numeric_key Numeric key for addition operations
 * @param square_type Type of Polybius square ("standard", "caesar", "atbash", "affine", "keyword")
 * @param alphabet Custom alphabet (NULL for default)
 * @param language Language ("english" or "turkish")
 * @param mono_params Parameters for monoalphabetic transformations (JSON string)
 * @param transposition_passes Number of transposition passes (1-3)
 * @param use_chain_addition Whether to use chain addition
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_encrypt(
    const char* plaintext,
    const char* polybius_key,
    const char* checkerboard_key,
    const char* transposition_key,
    const char* numeric_key,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size
);

/**
 * @brief Decrypt text using the VIC cipher
 * 
 * @param ciphertext Text to decrypt
 * @param polybius_key Keyword for Polybius square generation
 * @param checkerboard_key Keyword for straddling checkerboard
 * @param transposition_key Keyword for columnar transposition
 * @param numeric_key Numeric key for addition operations
 * @param square_type Type of Polybius square ("standard", "caesar", "atbash", "affine", "keyword")
 * @param alphabet Custom alphabet (NULL for default)
 * @param language Language ("english" or "turkish")
 * @param mono_params Parameters for monoalphabetic transformations (JSON string)
 * @param transposition_passes Number of transposition passes (1-3)
 * @param use_chain_addition Whether to use chain addition
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_decrypt(
    const char* ciphertext,
    const char* polybius_key,
    const char* checkerboard_key,
    const char* transposition_key,
    const char* numeric_key,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size
);

/**
 * @brief Produce a Polybius square for VIC cipher
 * 
 * @param square_type Type of square ("standard", "caesar", "atbash", "affine", "keyword")
 * @param keyword Keyword for keyword-based squares
 * @param alphabet Custom alphabet (NULL for default)
 * @param mono_params Parameters for monoalphabetic transformations (JSON string)
 * @param language Language ("english" or "turkish")
 * @param result Buffer to store Polybius square
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_produce_polybius_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    const char* mono_params,
    const char* language,
    char* result,
    size_t result_size
);

/**
 * @brief Produce a straddling checkerboard for VIC cipher
 * 
 * @param keyword Keyword for checkerboard generation
 * @param alphabet Custom alphabet (NULL for default)
 * @param language Language ("english" or "turkish")
 * @param result Buffer to store checkerboard
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_produce_checkerboard(
    const char* keyword,
    const char* alphabet,
    const char* language,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a random alphabetic key for VIC cipher
 * 
 * @param length Length of key to generate
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_generate_random_key(
    size_t length,
    char* result,
    size_t result_size
);

/**
 * @brief Generate a random numeric key for VIC cipher
 * 
 * @param length Length of numeric key to generate
 * @param result Buffer to store generated key
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int vic_generate_random_numeric_key(
    size_t length,
    char* result,
    size_t result_size
);

/**
 * @brief Generate all required keys for VIC cipher
 * 
 * @param polybius_key_length Length of Polybius key
 * @param checkerboard_key_length Length of checkerboard key
 * @param transposition_key_length Length of transposition key
 * @param numeric_key_length Length of numeric key
 * @param polybius_key Buffer to store Polybius key
 * @param checkerboard_key Buffer to store checkerboard key
 * @param transposition_key Buffer to store transposition key
 * @param numeric_key Buffer to store numeric key
 * @param key_size Size of each key buffer
 * @return 0 on success, -1 on error
 */
int vic_generate_keys_for_text(
    size_t polybius_key_length,
    size_t checkerboard_key_length,
    size_t transposition_key_length,
    size_t numeric_key_length,
    char* polybius_key,
    char* checkerboard_key,
    char* transposition_key,
    char* numeric_key,
    size_t key_size
);

/**
 * @brief Encrypt text using VIC cipher with randomly generated keys
 * 
 * @param plaintext Text to encrypt
 * @param square_type Type of Polybius square
 * @param alphabet Custom alphabet (NULL for default)
 * @param language Language ("english" or "turkish")
 * @param mono_params Parameters for monoalphabetic transformations (JSON string)
 * @param transposition_passes Number of transposition passes
 * @param use_chain_addition Whether to use chain addition
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @param generated_keys Buffer to store generated keys (JSON string)
 * @param keys_size Size of generated keys buffer
 * @return 0 on success, -1 on error
 */
int vic_encrypt_with_random_keys(
    const char* plaintext,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size,
    char* generated_keys,
    size_t keys_size
);

#endif // VIC_H
