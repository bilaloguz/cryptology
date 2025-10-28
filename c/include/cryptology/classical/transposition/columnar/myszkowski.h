/**
 * @file myszkowski.h
 * @brief Myszkowski Transposition Cipher
 * 
 * The Myszkowski variant handles repeated letters in the keyword
 * by grouping them together rather than giving sequential positions.
 */

#ifndef CRYPTOLOGY_MYSZKOWSKI_COLUMNAR_H
#define CRYPTOLOGY_MYSZKOWSKI_COLUMNAR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Myszkowski Transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for encrypted text
 * @param max_len     Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int myszkowski_encrypt(const char *plaintext, const char *keyword, 
                      char *output, size_t max_len);

/**
 * Decrypt ciphertext using Myszkowski Transposition.
 * 
 * @param ciphertext Encrypted text
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for decrypted text
 * @param max_len     Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int myszkowski_decrypt(const char *ciphertext, const char *keyword, 
                      char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_MYSZKOWSKI_COLUMNAR_H

