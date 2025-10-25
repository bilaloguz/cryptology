/**
 * @file two_square.h
 * @brief Two Square Cipher header
 * 
 * The Two Square cipher uses two 5x5 key squares to encrypt digrams.
 * It is more secure than Playfair as it uses two different key squares.
 */

#ifndef CRYPTOLOGY_TWO_SQUARE_H
#define CRYPTOLOGY_TWO_SQUARE_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Two Square cipher
 * 
 * @param plaintext Input text to encrypt
 * @param key1 First keyword for generating the first 5x5 key square
 * @param key2 Second keyword for generating the second 5x5 key square
 * @param result Output buffer for encrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int two_square_encrypt(const char *plaintext, const char *key1, const char *key2,
                       char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Two Square cipher
 * 
 * @param ciphertext Input text to decrypt
 * @param key1 First keyword for generating the first 5x5 key square
 * @param key2 Second keyword for generating the second 5x5 key square
 * @param result Output buffer for decrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int two_square_decrypt(const char *ciphertext, const char *key1, const char *key2,
                       char *result, size_t result_size);

#endif // CRYPTOLOGY_TWO_SQUARE_H
