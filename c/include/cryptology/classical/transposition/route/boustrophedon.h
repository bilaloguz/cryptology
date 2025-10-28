/**
 * @file boustrophedon.h
 * @brief Boustrophedon Transposition Cipher
 * 
 * Boustrophedon ("ox-turning") uses an alternating pattern:
 * Row 1: left to right →→→
 * Row 2: right to left ←←←
 * Row 3: left to right →→→
 * etc.
 */

#ifndef CRYPTOLOGY_BOUSTROPHEDON_H
#define CRYPTOLOGY_BOUSTROPHEDON_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Boustrophedon transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int boustrophedon_encrypt(const char *plaintext, char *output, size_t max_len);

/**
 * Decrypt ciphertext using Boustrophedon transposition.
 * 
 * @param ciphertext Encrypted text
 * @param output     Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int boustrophedon_decrypt(const char *ciphertext, char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_BOUSTROPHEDON_H

