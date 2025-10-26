/**
 * @file gronsfeld.h
 * @brief Gronsfeld Cipher implementation
 * 
 * The Gronsfeld cipher is a polyalphabetic substitution cipher that uses numeric keys
 * instead of alphabetic keys like Vigenère. Each digit in the key specifies how many
 * positions to shift the corresponding character in the plaintext.
 * 
 * This implementation supports:
 * 
 * - Numeric key validation and handling
 * - Custom tables generated using monoalphabetic ciphers
 * - English (26x26) and Turkish (29x29) table sizes
 * - Composable system with produce_table() method
 * - On-the-fly table generation for efficiency
 * - Random numeric key generation for enhanced security
 */

#ifndef CRYPTOLOGY_GRONSFELD_H
#define CRYPTOLOGY_GRONSFELD_H

#include <stddef.h>

/**
 * @brief Produce a Gronsfeld table using different strategies
 * 
 * @param table_type Type of table ("classical", "caesar", "affine", "keyword", "atbash")
 * @param alphabet The alphabet to use for the table
 * @param table Buffer to store the generated table (alphabet_size x alphabet_size)
 * @param table_size Size of the table buffer
 * @param ... Additional parameters for specific table types
 * @return 0 on success, -1 on error
 */
int gronsfeld_produce_table(const char *table_type,
                           const char *alphabet,
                           char ***table,
                           size_t *table_size,
                           ...);

/**
 * @brief Encrypt plaintext using Gronsfeld cipher
 * 
 * @param plaintext The text to encrypt
 * @param key The numeric Gronsfeld key (digits only)
 * @param table Custom Gronsfeld table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int gronsfeld_encrypt(const char *plaintext,
                     const char *key,
                     char ***table,
                     const char *alphabet,
                     char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Gronsfeld cipher
 * 
 * @param ciphertext The text to decrypt
 * @param key The numeric Gronsfeld key (digits only)
 * @param table Custom Gronsfeld table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int gronsfeld_decrypt(const char *ciphertext,
                     const char *key,
                     char ***table,
                     const char *alphabet,
                     char *result, size_t result_size);

/**
 * @brief Generate a cryptographically secure random numeric key
 * 
 * @param length Length of the key to generate
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int gronsfeld_generate_random_numeric_key(int length,
                                         char *result, size_t result_size);

/**
 * @brief Generate a random numeric key matching the plaintext length
 * 
 * @param plaintext The text to encrypt (determines key length)
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int gronsfeld_generate_numeric_key_for_text(const char *plaintext,
                                           char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using a randomly generated numeric key
 * 
 * @param plaintext Text to encrypt
 * @param table Custom Gronsfeld table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param key_length Length of random key (0 for auto-detect)
 * @param encrypted_result Buffer to store the encrypted text
 * @param encrypted_size Size of encrypted buffer
 * @param key_result Buffer to store the generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int gronsfeld_encrypt_with_random_key(const char *plaintext,
                                     char ***table,
                                     const char *alphabet,
                                     int key_length,
                                     char *encrypted_result, size_t encrypted_size,
                                     char *key_result, size_t key_size);

#ifdef __cplusplus
}
#endif

#endif /* CRYPTOLOGY_GRONSFELD_H */
