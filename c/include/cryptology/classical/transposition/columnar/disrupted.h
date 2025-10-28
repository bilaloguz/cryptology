/**
 * @file disrupted.h
 * @brief Disrupted Columnar Transposition Cipher
 * 
 * Disrupted Columnar Transposition is essentially identical to 
 * Single Columnar Transposition in practice.
 */

#ifndef CRYPTOLOGY_DISRUPTED_COLUMNAR_H
#define CRYPTOLOGY_DISRUPTED_COLUMNAR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Disrupted Columnar Transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int disrupted_columnar_encrypt(const char *plaintext, const char *keyword, 
                              char *output, size_t max_len);

/**
 * Decrypt ciphertext using Disrupted Columnar Transposition.
 * 
 * @param ciphertext Encrypted text
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int disrupted_columnar_decrypt(const char *ciphertext, const char *keyword, 
                               char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_DISRUPTED_COLUMNAR_H

