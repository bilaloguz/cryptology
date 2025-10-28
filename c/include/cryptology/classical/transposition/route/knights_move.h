/**
 * @file knights_move.h
 * @brief Knight's Move Transposition Cipher
 * 
 * Knight's Move transposition uses the L-shaped movement pattern of a chess knight.
 */

#ifndef CRYPTOLOGY_KNIGHTS_MOVE_H
#define CRYPTOLOGY_KNIGHTS_MOVE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Knight's Move transposition.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param output     Output buffer for encrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int knights_move_encrypt(const char *plaintext, char *output, size_t max_len);

/**
 * Decrypt ciphertext using Knight's Move transposition.
 * 
 * @param ciphertext Encrypted text
 * @param output     Output buffer for decrypted text
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int knights_move_decrypt(const char *ciphertext, char *output, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_KNIGHTS_MOVE_H

