/**
 * @file bifid.h
 * @brief Bifid Cipher implementation
 * 
 * The Bifid cipher is a fractionated substitution cipher that uses a 5x5 Polybius square.
 * It works by converting each letter to coordinates, fractionating them, then reading
 * new coordinates to get encrypted letters.
 */

#ifndef CRYPTOLOGY_BIFID_H
#define CRYPTOLOGY_BIFID_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Bifid cipher with default English alphabet
 * 
 * @param plaintext The text to encrypt
 * @param key The keyword for the Polybius square
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int bifid_encrypt(const char *plaintext, const char *key, 
                  char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Bifid cipher with default English alphabet
 * 
 * @param ciphertext The text to decrypt
 * @param key The keyword for the Polybius square
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int bifid_decrypt(const char *ciphertext, const char *key,
                  char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using Bifid cipher with custom alphabet
 * 
 * @param plaintext The text to encrypt
 * @param key The keyword for the Polybius square
 * @param alphabet Custom alphabet to use
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int bifid_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Bifid cipher with custom alphabet
 * 
 * @param ciphertext The text to decrypt
 * @param key The keyword for the Polybius square
 * @param alphabet Custom alphabet to use
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int bifid_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                char *result, size_t result_size);

#endif // CRYPTOLOGY_BIFID_H
