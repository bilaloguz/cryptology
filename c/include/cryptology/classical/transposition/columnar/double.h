/**
 * @file double.h
 * @brief Double Columnar Transposition Cipher
 * 
 * Applies columnar transposition twice, providing stronger security.
 * Can use same keyword twice or two different keywords.
 */

#ifndef CRYPTOLOGY_DOUBLE_COLUMNAR_H
#define CRYPTOLOGY_DOUBLE_COLUMNAR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Double Columnar Transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param keyword1   First column arrangement keyword
 * @param keyword2   Second column arrangement keyword (NULL to use keyword1)
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int double_columnar_encrypt(const char *plaintext, const char *keyword1, 
                            const char *keyword2, char *output, size_t max_len);

/**
 * Decrypt ciphertext using Double Columnar Transposition.
 * 
 * @param ciphertext Encrypted text
 * @param keyword1  First column arrangement keyword
 * @param keyword2  Second column arrangement keyword (NULL to use keyword1)
 * @param output    Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return          0 on success, -1 on error
 */
int double_columnar_decrypt(const char *ciphertext, const char *keyword1, 
                            const char *keyword2, char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_DOUBLE_COLUMNAR_H

