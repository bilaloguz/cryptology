/**
 * @file reihenschieber.h
 * @brief Reihenschieber Cipher Implementation
 * 
 * A mechanical polyalphabetic substitution cipher that uses shifting strips.
 * Essentially a mechanical Vigenère cipher with progressive shifting capabilities.
 * 
 * Features:
 * - Multiple shift modes: fixed, progressive, custom
 * - Shift directions: forward (default), backward
 * - Custom alphabets support (English, Turkish, etc.)
 * - Random key generation
 * - Self-reciprocal encryption/decryption
 */

#ifndef REIHENSHIEBER_H
#define REIHENSHIEBER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Encrypt text using the Reihenschieber cipher
 * 
 * @param plaintext Text to encrypt
 * @param key Encryption key (repeats as needed)
 * @param alphabet Custom alphabet (NULL for default English)
 * @param shift_mode "fixed", "progressive", or "custom"
 * @param shift_direction "forward" or "backward"
 * @param shift_amount Amount to shift (for fixed/progressive modes)
 * @param custom_shifts Array of custom shift values (for custom mode)
 * @param custom_shifts_count Number of custom shift values
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
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
);

/**
 * @brief Decrypt text using the Reihenschieber cipher
 * 
 * @param ciphertext Text to decrypt
 * @param key Decryption key (repeats as needed)
 * @param alphabet Custom alphabet (NULL for default English)
 * @param shift_mode "fixed", "progressive", or "custom"
 * @param shift_direction "forward" or "backward"
 * @param shift_amount Amount to shift (for fixed/progressive modes)
 * @param custom_shifts Array of custom shift values (for custom mode)
 * @param custom_shifts_count Number of custom shift values
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
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
);

/**
 * @brief Generate a random key for Reihenschieber cipher
 * 
 * @param length Length of the key to generate
 * @param key Buffer to store generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int reihenschieber_generate_random_key(int length, char* key, size_t key_size);

/**
 * @brief Generate a key of appropriate length for the given text
 * 
 * @param text_length Length of the text to encrypt
 * @param key Buffer to store generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int reihenschieber_generate_key_for_text(int text_length, char* key, size_t key_size);

/**
 * @brief Encrypt text with a randomly generated key
 * 
 * @param plaintext Text to encrypt
 * @param key_length Length of key to generate (0 for auto)
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @param generated_key Buffer to store generated key
 * @param key_size Size of generated_key buffer
 * @return 0 on success, -1 on error
 */
int reihenschieber_encrypt_with_random_key(
    const char* plaintext,
    int key_length,
    char* result,
    size_t result_size,
    char* generated_key,
    size_t key_size
);

/**
 * @brief Produce custom shift patterns for Reihenschieber cipher
 * 
 * @param pattern_type Type of pattern ("alternating", "fibonacci", "prime", "random")
 * @param pattern_length Length of the pattern
 * @param shifts Buffer to store shift values
 * @param shifts_size Size of shifts buffer
 * @return 0 on success, -1 on error
 */
int reihenschieber_produce_custom_shifts(
    const char* pattern_type,
    int pattern_length,
    int* shifts,
    size_t shifts_size
);

/**
 * @brief Encrypt Turkish text using Reihenschieber cipher
 * 
 * @param plaintext Turkish text to encrypt
 * @param key Encryption key
 * @param shift_mode "fixed", "progressive", or "custom"
 * @param shift_direction "forward" or "backward"
 * @param shift_amount Amount to shift
 * @param custom_shifts Array of custom shift values (for custom mode)
 * @param custom_shifts_count Number of custom shift values
 * @param result Buffer to store encrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
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
);

/**
 * @brief Decrypt Turkish text using Reihenschieber cipher
 * 
 * @param ciphertext Turkish text to decrypt
 * @param key Decryption key
 * @param shift_mode "fixed", "progressive", or "custom"
 * @param shift_direction "forward" or "backward"
 * @param shift_amount Amount to shift
 * @param custom_shifts Array of custom shift values (for custom mode)
 * @param custom_shifts_count Number of custom shift values
 * @param result Buffer to store decrypted text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
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
);

#ifdef __cplusplus
}
#endif

#endif /* REIHENSHIEBER_H */
