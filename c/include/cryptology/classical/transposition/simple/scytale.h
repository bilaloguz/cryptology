/**
 * Scytale (Spartan Stick) Cipher implementation.
 *
 * The Scytale cipher is one of the oldest known transposition ciphers,
 * used by the ancient Spartans around 400 BC. It involves wrapping a
 * leather strip around a cylindrical rod, writing the message along
 * the length of the rod, and then unwrapping it to reveal the cipher.
 *
 * Modern implementation uses a matrix approach where we:
 * 1. Write text in rows based on key (wrapping around rod)
 * 2. Read it column by column (unwrapping from rod)
 */

#ifndef CRYPTOLOGY_SCYTALE_H
#define CRYPTOLOGY_SCYTALE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Scytale cipher.
 *
 * @param plaintext Input text to encrypt (case-insensitive, removes non-alphabetic)
 * @param key Number of columns (diameter of the rod)
 * @param output Buffer to store encrypted text (must be at least strlen(plaintext) + 1)
 * @param output_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int scytale_encrypt(const char *plaintext, int key, char *output, size_t output_size);

/**
 * Decrypt ciphertext using Scytale cipher.
 *
 * @param ciphertext Encrypted text
 * @param key Number of columns (diameter of the rod)
 * @param output Buffer to store decrypted text (must be at least strlen(ciphertext) + 1)
 * @param output_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int scytale_decrypt(const char *ciphertext, int key, char *output, size_t output_size);

/**
 * Get the valid range of keys for a given text length.
 *
 * @param text_length Length of the text
 * @param min_key Output parameter for minimum key
 * @param max_key Output parameter for maximum key
 */
void scytale_get_key_range(size_t text_length, int *min_key, int *max_key);

#ifdef __cplusplus
}
#endif

#endif /* CRYPTOLOGY_SCYTALE_H */
