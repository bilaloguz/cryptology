/**
 * @file caesar.h
 * @brief Caesar Cipher implementation
 * 
 * The Caesar cipher is one of the simplest and most widely known encryption techniques.
 * It is a type of substitution cipher where each letter in the plaintext is shifted
 * a certain number of places down the alphabet.
 */

#ifndef CRYPTOLOGY_CAESAR_H
#define CRYPTOLOGY_CAESAR_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Caesar cipher
 * 
 * @param plaintext The text to encrypt (will be converted to lowercase)
 * @param shift The number of positions to shift
 * @param alphabet The alphabet to use for encryption
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int caesar_encrypt(const char *plaintext, int shift, const char *alphabet, 
                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Caesar cipher
 * 
 * @param ciphertext The text to decrypt (will be converted to lowercase)
 * @param shift The number of positions that were shifted
 * @param alphabet The alphabet that was used for encryption
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int caesar_decrypt(const char *ciphertext, int shift, const char *alphabet,
                   char *result, size_t result_size);

#endif /* CRYPTOLOGY_CAESAR_H */

