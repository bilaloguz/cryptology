/**
 * Rail Fence Cipher implementation.
 *
 * The Rail Fence cipher is a transposition cipher that writes the message
 * in a zigzag pattern along multiple "rails" (rows), then reads it off
 * in a linear fashion.
 *
 * The pattern looks like a fence when viewed from the side, hence the name.
 *
 * Example with 3 rails:
 *   H . . . O . . . R . .
 *   . E . L . W . O . L .
 *   . . L . . . D . . . .
 *
 * Encryption: Write diagonally, read horizontally
 * Decryption: Write horizontally, read diagonally
 */

#ifndef CRYPTOLOGY_RAIL_FENCE_H
#define CRYPTOLOGY_RAIL_FENCE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Rail Fence cipher.
 *
 * @param plaintext Input text to encrypt (case-insensitive, removes non-alphabetic)
 * @param rails Number of rails (rows)
 * @param output Buffer to store encrypted text (must be at least strlen(plaintext) + 1)
 * @param output_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int rail_fence_encrypt(const char *plaintext, int rails, char *output, size_t output_size);

/**
 * Decrypt ciphertext using Rail Fence cipher.
 *
 * @param ciphertext Encrypted text
 * @param rails Number of rails (rows)
 * @param output Buffer to store decrypted text (must be at least strlen(ciphertext) + 1)
 * @param output_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int rail_fence_decrypt(const char *ciphertext, int rails, char *output, size_t output_size);

/**
 * Visualize the rail fence pattern (for debugging).
 *
 * @param text Text to visualize
 * @param rails Number of rails
 * @param output Buffer to store visualization (must be large enough)
 * @param output_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int rail_fence_visualize(const char *text, int rails, char *output, size_t output_size);

/**
 * Get the valid range of keys for a given text length.
 *
 * @param text_length Length of the text
 * @param min_key Output parameter for minimum key
 * @param max_key Output parameter for maximum key
 */
void rail_fence_get_key_range(size_t text_length, int *min_key, int *max_key);

#ifdef __cplusplus
}
#endif

#endif /* CRYPTOLOGY_RAIL_FENCE_H */
