/**
 * @file porta.h
 * @brief Porta Cipher implementation with custom pairing support
 * 
 * The Porta cipher is a self-reciprocal polyalphabetic substitution cipher that uses
 * alphabet pairs. Each letter in the keyword determines which alphabet pair to use
 * for encryption.
 * 
 * This implementation supports:
 * 
 * - Fixed alphabet pair system (default 13 pairs for English)
 * - Custom alphabet pairs with validation
 * - Turkish alphabet support with proper pairs
 * - Self-reciprocal encryption/decryption
 * - Keyword-based encryption (alphabetic keys)
 * - Random key generation for enhanced security
 * - Multiple pairing strategies (default, custom, turkish, balanced)
 */

#ifndef CRYPTOLOGY_PORTA_H
#define CRYPTOLOGY_PORTA_H

#include <stddef.h>

/**
 * @brief Alphabet pair structure
 */
typedef struct {
    char first;
    char second;
} porta_pair_t;

/**
 * @brief Produce alphabet pairs for the Porta cipher using different strategies
 * 
 * @param pair_type Type of pairs ("default", "custom", "turkish", "balanced")
 * @param alphabet The alphabet to create pairs from
 * @param pairs Buffer to store the generated pairs
 * @param pairs_count Number of pairs generated
 * @param custom_pairs User-defined pairs (required for "custom" type)
 * @param custom_pairs_count Number of custom pairs
 * @return 0 on success, -1 on error
 */
int porta_produce_pairs(const char *pair_type,
                       const char *alphabet,
                       porta_pair_t *pairs,
                       size_t *pairs_count,
                       const porta_pair_t *custom_pairs,
                       size_t custom_pairs_count);

/**
 * @brief Encrypt plaintext using Porta cipher
 * 
 * @param plaintext The text to encrypt
 * @param key The alphabetic key
 * @param alphabet The alphabet to use (NULL for default)
 * @param pairs Custom alphabet pairs (NULL for default)
 * @param pairs_count Number of pairs
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int porta_encrypt(const char *plaintext,
                 const char *key,
                 const char *alphabet,
                 const porta_pair_t *pairs,
                 size_t pairs_count,
                 char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Porta cipher
 * 
 * Note: Porta cipher is self-reciprocal, so decryption uses the same algorithm as encryption.
 * 
 * @param ciphertext The text to decrypt
 * @param key The alphabetic key
 * @param alphabet The alphabet to use (NULL for default)
 * @param pairs Custom alphabet pairs (NULL for default)
 * @param pairs_count Number of pairs
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int porta_decrypt(const char *ciphertext,
                 const char *key,
                 const char *alphabet,
                 const porta_pair_t *pairs,
                 size_t pairs_count,
                 char *result, size_t result_size);

/**
 * @brief Generate a cryptographically secure random alphabetic key
 * 
 * @param length Length of the key to generate
 * @param alphabet The alphabet to use for key generation (NULL for default)
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int porta_generate_random_key(int length, const char *alphabet,
                             char *result, size_t result_size);

/**
 * @brief Generate a random alphabetic key matching the plaintext length
 * 
 * @param plaintext The text to encrypt (determines key length)
 * @param alphabet The alphabet to use for key generation (NULL for default)
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int porta_generate_key_for_text(const char *plaintext, const char *alphabet,
                               char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using a randomly generated alphabetic key
 * 
 * @param plaintext Text to encrypt
 * @param alphabet The alphabet to use (NULL for default)
 * @param pairs Custom alphabet pairs (NULL for default)
 * @param pairs_count Number of pairs
 * @param key_length Length of random key (0 for auto-detect)
 * @param encrypted_result Buffer to store the encrypted text
 * @param encrypted_size Size of encrypted buffer
 * @param key_result Buffer to store the generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int porta_encrypt_with_random_key(const char *plaintext,
                                 const char *alphabet,
                                 const porta_pair_t *pairs,
                                 size_t pairs_count,
                                 int key_length,
                                 char *encrypted_result, size_t encrypted_size,
                                 char *key_result, size_t key_size);

#ifdef __cplusplus
}
#endif

#endif /* CRYPTOLOGY_PORTA_H */
