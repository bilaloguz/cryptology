/**
 * @file utf8_helpers.h
 * @brief UTF-8 Helper Functions for Turkish Character Support
 * 
 * These functions provide UTF-8 aware character handling for transposition ciphers,
 * specifically supporting Turkish characters (İ, ı, ş, ç, ğ, ö, ü).
 */

#ifndef CRYPTOLOGY_TRANSPOSITION_UTF8_HELPERS_H
#define CRYPTOLOGY_TRANSPOSITION_UTF8_HELPERS_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Check if a character is a letter (English or Turkish, including UTF-8 Turkish chars).
 * 
 * @param byte First byte of UTF-8 character
 * @param bytes Array of bytes representing the character
 * @param char_len Number of bytes in the character
 * @return 1 if letter, 0 otherwise
 */
int utf8_is_letter(unsigned char byte, const unsigned char* bytes, int char_len);

/**
 * Convert a UTF-8 character to lowercase (handles Turkish İ, I correctly).
 * 
 * @param bytes Array of bytes representing the character
 * @param char_len Number of bytes in the character
 * @param result Output buffer for lowercase character
 * @param result_size Size of result buffer
 * @return Number of bytes in result, or -1 on error
 */
int utf8_to_lower(const unsigned char* bytes, int char_len, unsigned char* result, size_t result_size);

/**
 * Clean text: keep only alphabetic characters and convert to lowercase.
 * Supports UTF-8 Turkish characters.
 * 
 * @param input Input text
 * @param output Output buffer
 * @param output_size Size of output buffer
 * @return 0 on success, -1 on error
 */
int clean_utf8_text(const char* input, char* output, size_t output_size);

#ifdef __cplusplus
}
#endif

#endif // CRYPTOLOGY_TRANSPOSITION_UTF8_HELPERS_H

