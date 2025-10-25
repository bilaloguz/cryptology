/**
 * @file four_square.h
 * @brief Four Square Cipher header
 * 
 * The Four Square cipher uses four 5x5 key squares to encrypt digrams.
 * It provides even more security than Two Square by using four different key squares.
 */

#ifndef CRYPTOLOGY_FOUR_SQUARE_H
#define CRYPTOLOGY_FOUR_SQUARE_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Four Square cipher
 * 
 * @param plaintext Input text to encrypt
 * @param key1 First keyword for generating the first 5x5 key square
 * @param key2 Second keyword for generating the second 5x5 key square
 * @param key3 Third keyword for generating the third 5x5 key square
 * @param key4 Fourth keyword for generating the fourth 5x5 key square
 * @param result Output buffer for encrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int four_square_encrypt(const char *plaintext, const char *key1, const char *key2,
                        const char *key3, const char *key4,
                        char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Four Square cipher
 * 
 * @param ciphertext Input text to decrypt
 * @param key1 First keyword for generating the first 5x5 key square
 * @param key2 Second keyword for generating the second 5x5 key square
 * @param key3 Third keyword for generating the third 5x5 key square
 * @param key4 Fourth keyword for generating the fourth 5x5 key square
 * @param result Output buffer for decrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int four_square_decrypt(const char *ciphertext, const char *key1, const char *key2,
                        const char *key3, const char *key4,
                        char *result, size_t result_size);

#endif // CRYPTOLOGY_FOUR_SQUARE_H
