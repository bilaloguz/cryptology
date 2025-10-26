/**
 * @file vigenere.h
 * @brief Vigenère Cipher implementation
 * 
 * The Vigenère cipher is a polyalphabetic substitution cipher that uses a table
 * where each row is a different Caesar cipher. This implementation supports:
 * 
 * - Classical Vigenère table (tabula recta) as default
 * - Custom tables generated using monoalphabetic ciphers
 * - English (26x26) and Turkish (29x29) table sizes
 * - Composable system with produce_table() method
 * - On-the-fly table generation for efficiency
 */

#ifndef CRYPTOLOGY_VIGENERE_H
#define CRYPTOLOGY_VIGENERE_H

#include <stddef.h>

/**
 * @brief Produce a Vigenère table using different strategies
 * 
 * @param table_type Type of table ("classical", "caesar", "affine", "keyword", "atbash")
 * @param alphabet The alphabet to use for the table
 * @param table Buffer to store the generated table (alphabet_size x alphabet_size)
 * @param table_size Size of the table buffer
 * @param ... Additional parameters for specific table types
 * @return 0 on success, -1 on error
 */
int vigenere_produce_table(const char *table_type,
                          const char *alphabet,
                          char ***table,
                          size_t *table_size,
                          ...);

/**
 * @brief Encrypt plaintext using Vigenère cipher
 * 
 * @param plaintext The text to encrypt
 * @param key The Vigenère key
 * @param table Custom Vigenère table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int vigenere_encrypt(const char *plaintext,
                    const char *key,
                    char ***table,
                    const char *alphabet,
                    char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Vigenère cipher
 * 
 * @param ciphertext The text to decrypt
 * @param key The Vigenère key
 * @param table Custom Vigenère table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int vigenere_decrypt(const char *ciphertext,
                    const char *key,
                    char ***table,
                    const char *alphabet,
                    char *result, size_t result_size);

/**
 * @brief Generate a cryptographically secure random key
 * 
 * @param length Length of the key to generate
 * @param alphabet The alphabet to use for key generation (NULL for default)
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int vigenere_generate_random_key(int length, const char *alphabet,
                                char *result, size_t result_size);

/**
 * @brief Generate a random key matching the plaintext length
 * 
 * @param plaintext The text to encrypt (determines key length)
 * @param alphabet The alphabet to use for key generation (NULL for default)
 * @param result Buffer to store the generated key
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int vigenere_generate_key_for_text(const char *plaintext, const char *alphabet,
                                  char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using a randomly generated key
 * 
 * @param plaintext Text to encrypt
 * @param table Custom Vigenère table (NULL for classical)
 * @param alphabet The alphabet to use (NULL for default)
 * @param key_length Length of random key (0 for auto)
 * @param encrypted Buffer to store encrypted text
 * @param encrypted_size Size of encrypted buffer
 * @param generated_key Buffer to store generated key
 * @param key_size Size of key buffer
 * @return 0 on success, -1 on error
 */
int vigenere_encrypt_with_random_key(const char *plaintext, char ***table,
                                   const char *alphabet, int key_length,
                                   char *encrypted, size_t encrypted_size,
                                   char *generated_key, size_t key_size);

#endif // CRYPTOLOGY_VIGENERE_H
