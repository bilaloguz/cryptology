/**
 * @file alberti.h
 * @brief Alberti Cipher implementation
 * 
 * The Alberti cipher is the first polyalphabetic cipher, invented by Leon Battista Alberti in 1467.
 * It uses two concentric disks - an outer disk with the plaintext alphabet and an inner disk 
 * with a scrambled ciphertext alphabet. The inner disk rotates according to a specified strategy.
 */

#ifndef CRYPTOLOGY_ALBERTI_H
#define CRYPTOLOGY_ALBERTI_H

#include <stddef.h>

/**
 * @brief Encrypt plaintext using Alberti cipher
 * 
 * @param plaintext The text to encrypt
 * @param outer_alphabet The plaintext alphabet (NULL for default)
 * @param inner_alphabet The ciphertext alphabet (NULL for auto-generated)
 * @param initial_position Starting position of inner disk
 * @param rotation_strategy Rotation strategy string
 * @param rotation_amount How many positions to rotate
 * @param result Buffer to store the encrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int alberti_encrypt(const char *plaintext,
                   const char *outer_alphabet,
                   const char *inner_alphabet,
                   int initial_position,
                   const char *rotation_strategy,
                   int rotation_amount,
                   char *result, size_t result_size);

/**
 * @brief Decrypt ciphertext using Alberti cipher
 * 
 * @param ciphertext The text to decrypt
 * @param outer_alphabet The plaintext alphabet (NULL for default)
 * @param inner_alphabet The ciphertext alphabet (NULL for auto-generated)
 * @param initial_position Starting position of inner disk
 * @param rotation_strategy Rotation strategy string
 * @param rotation_amount How many positions to rotate
 * @param result Buffer to store the decrypted result
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int alberti_decrypt(const char *ciphertext,
                   const char *outer_alphabet,
                   const char *inner_alphabet,
                   int initial_position,
                   const char *rotation_strategy,
                   int rotation_amount,
                   char *result, size_t result_size);

#endif // CRYPTOLOGY_ALBERTI_H
