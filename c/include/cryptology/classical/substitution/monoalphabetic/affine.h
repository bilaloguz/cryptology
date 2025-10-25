/**
 * @file affine.h
 * @brief Affine Cipher implementation
 * 
 * The Affine cipher is a monoalphabetic substitution cipher that uses modular arithmetic.
 * It is the general form of all linear monoalphabetic substitution ciphers.
 * 
 * Encryption: E(x) = (ax + b) mod m
 * Decryption: D(y) = a^(-1) * (y - b) mod m
 */

#ifndef CRYPTOLOGY_AFFINE_H
#define CRYPTOLOGY_AFFINE_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Affine cipher
 * 
 * @param plaintext The text to encrypt (will be converted to lowercase)
 * @param a The multiplicative key (must be coprime with alphabet length)
 * @param b The additive key
 * @param alphabet The alphabet to use for encryption
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int affine_encrypt(const char *plaintext, int a, int b, const char *alphabet,
                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Affine cipher
 * 
 * @param ciphertext The text to decrypt (will be converted to lowercase)
 * @param a The multiplicative key that was used for encryption
 * @param b The additive key that was used for encryption
 * @param alphabet The alphabet that was used for encryption
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int affine_decrypt(const char *ciphertext, int a, int b, const char *alphabet,
                   char *result, size_t result_size);

/**
 * @brief Produce an affine-transformed alphabet
 * 
 * This function creates a custom alphabet by applying an affine transformation
 * to the base alphabet. The produced alphabet can be used with polygraphic 
 * ciphers for enhanced security.
 * 
 * @param a The multiplicative key (must be coprime with alphabet length)
 * @param b The additive key
 * @param alphabet The base alphabet to transform
 * @param result Buffer to store the transformed alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int affine_produce_alphabet(int a, int b, const char *alphabet, char *result, size_t result_size);

#endif /* CRYPTOLOGY_AFFINE_H */

