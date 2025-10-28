/**
 * @file single.h
 * @brief Single Columnar Transposition Cipher
 * 
 * The columnar transposition cipher writes plaintext in rows, then
 * reads it column by column in an order determined by a keyword.
 */

#ifndef CRYPTOLOGY_SINGLE_COLUMNAR_H
#define CRYPTOLOGY_SINGLE_COLUMNAR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Single Columnar Transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int single_columnar_encrypt(const char *plaintext, const char *keyword, 
                            char *output, size_t max_len);

/**
 * Decrypt ciphertext using Single Columnar Transposition.
 * 
 * @param ciphertext Encrypted text
 * @param keyword    The column arrangement keyword
 * @param output     Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int single_columnar_decrypt(const char *ciphertext, const char *keyword, 
                            char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_SINGLE_COLUMNAR_H

