/**
 * @file spiral.h
 * @brief Spiral Route Transposition Cipher
 * 
 * Spiral Route transposition writes text in a spiral pattern.
 */

#ifndef CRYPTOLOGY_SPIRAL_ROUTE_H
#define CRYPTOLOGY_SPIRAL_ROUTE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Spiral Route transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int spiral_encrypt(const char *plaintext, char *output, size_t max_len);

/**
 * Decrypt ciphertext using Spiral Route transposition.
 * 
 * @param ciphertext Encrypted text
 * @param output     Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int spiral_decrypt(const char *ciphertext, char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_SPIRAL_ROUTE_H

