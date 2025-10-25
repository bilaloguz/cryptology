/**
 * @file trifid.h
 * @brief Trifid Cipher implementation
 * 
 * The Trifid cipher is a fractionated substitution cipher that uses a 3x3x3 cube.
 * It works by converting each letter to 3D coordinates, fractionating them, then reading
 * new coordinates to get encrypted letters.
 */

#ifndef CRYPTOLOGY_TRIFID_H
#define CRYPTOLOGY_TRIFID_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Trifid cipher with default English alphabet
 * 
 * @param plaintext The text to encrypt
 * @param key The keyword for the Trifid cube
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int trifid_encrypt(const char *plaintext, const char *key, 
                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Trifid cipher with default English alphabet
 * 
 * @param ciphertext The text to decrypt
 * @param key The keyword for the Trifid cube
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int trifid_decrypt(const char *ciphertext, const char *key,
                  char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using Trifid cipher with custom alphabet
 * 
 * @param plaintext The text to encrypt
 * @param key The keyword for the Trifid cube
 * @param alphabet Custom alphabet to use
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int trifid_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                 char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Trifid cipher with custom alphabet
 * 
 * @param ciphertext The text to decrypt
 * @param key The keyword for the Trifid cube
 * @param alphabet Custom alphabet to use
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int trifid_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                 char *result, size_t result_size);

#endif // CRYPTOLOGY_TRIFID_H
