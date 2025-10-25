/**
 * @file hill.h
 * @brief Hill Cipher header
 * 
 * The Hill cipher uses matrix multiplication to encrypt n-grams.
 * It operates on groups of letters using modular arithmetic.
 */

#ifndef CRYPTOLOGY_HILL_H
#define CRYPTOLOGY_HILL_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Hill cipher
 * 
 * @param plaintext Input text to encrypt
 * @param key_matrix Encryption key matrix (n x n)
 * @param matrix_size Size of the matrix (n)
 * @param result Output buffer for encrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int hill_encrypt(const char *plaintext, const int *key_matrix, int matrix_size,
                 char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Hill cipher
 * 
 * @param ciphertext Input text to decrypt
 * @param key_matrix Encryption key matrix (n x n)
 * @param matrix_size Size of the matrix (n)
 * @param result Output buffer for decrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int hill_decrypt(const char *ciphertext, const int *key_matrix, int matrix_size,
                 char *result, size_t result_size);

#endif // CRYPTOLOGY_HILL_H
