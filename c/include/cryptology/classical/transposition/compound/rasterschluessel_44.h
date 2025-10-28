/**
 * @file rasterschluessel_44.h
 * @brief Rasterschlüssel 44 (RS44) Cipher
 * 
 * Rasterschlüssel 44 (Grid Key 44) was a German cipher used during WWII.
 * It combines a Polybius square (6x6) with coordinate-based substitution.
 * 
 * The name "44" refers to the grid system. Uses a 6x6 square with 
 * 26 letters + 10 digits = 36 characters.
 */

#ifndef CRYPTOLOGY_RASTERSCHLUESSEL_44_H
#define CRYPTOLOGY_RASTERSCHLUESSEL_44_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Encrypt plaintext using Rasterschlüssel 44 cipher.
 * 
 * @param plaintext  Input text to encrypt (case-insensitive)
 * @param keyword    Key for Polybius square generation
 * @param output     Output buffer for encrypted text (must be large enough)
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int rasterschluessel_44_encrypt(const char *plaintext, const char *keyword, 
                                 char *output, size_t max_len);

/**
 * Decrypt ciphertext using Rasterschlüssel 44 cipher.
 * 
 * @param ciphertext Input encrypted text (should be digits)
 * @param keyword    Key for Polybius square generation
 * @param output     Output buffer for decrypted text (must be large enough)
 * @param max_len    Maximum length of output buffer
 * @return           0 on success, -1 on error
 */
int rasterschluessel_44_decrypt(const char *ciphertext, const char *keyword, 
                                 char *output, size_t max_len);

/**
 * Generate a Polybius square for Rasterschlüssel 44.
 * 
 * Creates a 6x6 square with keyword + remaining alphabet + digits.
 * 
 * @param keyword    Key for square generation
 * @param square     Output 6x6 square (36 characters)
 */
void rasterschluessel_44_produce_square(const char *keyword, char square[6][6]);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_RASTERSCHLUESSEL_44_H

