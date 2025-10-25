/**
 * @file playfair.h
 * @brief Playfair Cipher header
 * 
 * The Playfair cipher is a digraphic substitution cipher that uses a 5x5 key square.
 * It encrypts pairs of letters (digrams) using special rules for positioning.
 */

#ifndef CRYPTOLOGY_PLAYFAIR_H
#define CRYPTOLOGY_PLAYFAIR_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Playfair cipher with default English alphabet
 * 
 * @param plaintext Input text to encrypt
 * @param key Keyword for generating the key square
 * @param result Output buffer for encrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int playfair_encrypt(const char *plaintext, const char *key, 
                     char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Playfair cipher with default English alphabet
 * 
 * @param ciphertext Input text to decrypt
 * @param key Keyword for generating the key square
 * @param result Output buffer for decrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int playfair_decrypt(const char *ciphertext, const char *key,
                     char *result, size_t result_size);

/**
 * @brief Encrypt plaintext using Playfair cipher with custom alphabet
 * 
 * @param plaintext Input text to encrypt
 * @param key Keyword for generating the key square
 * @param alphabet Custom alphabet to use
 * @param result Output buffer for encrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int playfair_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Playfair cipher with custom alphabet
 * 
 * @param ciphertext Input text to decrypt
 * @param key Keyword for generating the key square
 * @param alphabet Custom alphabet to use
 * @param result Output buffer for decrypted text
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int playfair_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                   char *result, size_t result_size);

#endif // CRYPTOLOGY_PLAYFAIR_H
