/**
 * @file atbash.h
 * @brief Atbash Cipher implementation
 * 
 * The Atbash cipher is a monoalphabetic substitution cipher where the alphabet is reversed.
 * The first letter is replaced with the last, the second with the second-to-last, and so on.
 */

#ifndef CRYPTOLOGY_ATBASH_H
#define CRYPTOLOGY_ATBASH_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Atbash cipher
 * 
 * @param plaintext The text to encrypt (will be converted to lowercase)
 * @param alphabet The alphabet to use for encryption
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int atbash_encrypt(const char *plaintext, const char *alphabet,
                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Atbash cipher
 * 
 * @param ciphertext The text to decrypt (will be converted to lowercase)
 * @param alphabet The alphabet that was used for encryption
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int atbash_decrypt(const char *ciphertext, const char *alphabet,
                   char *result, size_t result_size);

/**
 * @brief Produce an Atbash-reversed alphabet
 * 
 * This function creates a custom alphabet by reversing the base alphabet.
 * The produced alphabet can be used with polygraphic ciphers for enhanced security.
 * 
 * @param alphabet The base alphabet to reverse
 * @param result Buffer to store the reversed alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int atbash_produce_alphabet(const char *alphabet, char *result, size_t result_size);

#endif /* CRYPTOLOGY_ATBASH_H */

