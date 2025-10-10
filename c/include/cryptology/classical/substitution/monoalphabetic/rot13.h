/**
 * @file rot13.h
 * @brief ROT13 Cipher implementation
 * 
 * ROT13 is a special case of the Caesar cipher where the shift is always 13.
 * Since there are 26 letters in the alphabet, applying ROT13 twice returns the original text.
 */

#ifndef CRYPTOLOGY_ROT13_H
#define CRYPTOLOGY_ROT13_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using ROT13
 * 
 * @param plaintext The text to encrypt (will be converted to lowercase)
 * @param alphabet The alphabet to use for encryption
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int rot13_encrypt(const char *plaintext, const char *alphabet,
                  char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using ROT13
 * 
 * @param ciphertext The text to decrypt (will be converted to lowercase)
 * @param alphabet The alphabet that was used for encryption
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int rot13_decrypt(const char *ciphertext, const char *alphabet,
                  char *result, size_t result_size);

#endif /* CRYPTOLOGY_ROT13_H */

