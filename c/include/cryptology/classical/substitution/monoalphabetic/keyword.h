/**
 * @file keyword.h
 * @brief Keyword Cipher implementation
 * 
 * The keyword cipher is a monoalphabetic substitution cipher where a keyword is used
 * to create the cipher alphabet.
 */

#ifndef CRYPTOLOGY_KEYWORD_H
#define CRYPTOLOGY_KEYWORD_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Keyword cipher
 * 
 * @param plaintext The text to encrypt (will be converted to lowercase)
 * @param keyword The keyword to use for creating cipher alphabet
 * @param alphabet The alphabet to use for encryption
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int keyword_encrypt(const char *plaintext, const char *keyword, const char *alphabet,
                    char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Keyword cipher
 * 
 * @param ciphertext The text to decrypt (will be converted to lowercase)
 * @param keyword The keyword that was used for encryption
 * @param alphabet The alphabet that was used for encryption
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int keyword_decrypt(const char *ciphertext, const char *keyword, const char *alphabet,
                    char *result, size_t result_size);

#endif /* CRYPTOLOGY_KEYWORD_H */

