/**
 * @file alphabet_utils.h
 * @brief Alphabet utilities for polygraphic substitution ciphers
 * 
 * This module provides utilities for handling custom alphabets in polygraphic ciphers,
 * including letter combination strategies for English and Turkish.
 */

#ifndef CRYPTOLOGY_ALPHABET_UTILS_H
#define CRYPTOLOGY_ALPHABET_UTILS_H

#include <stddef.h>

/**
 * @brief Detect the language of an alphabet
 * 
 * @param alphabet Input alphabet string
 * @return Language code: "english", "turkish", or "unknown"
 */
const char* detect_language(const char *alphabet);

/**
 * @brief Get the appropriate square size for a given alphabet length
 * 
 * @param alphabet_length Number of letters in the alphabet
 * @return Square size (e.g., 5 for 25 letters, 6 for 36 letters)
 */
int get_square_size(int alphabet_length);

/**
 * @brief Combine similar letters in an alphabet to fit polygraphic cipher requirements
 * 
 * @param alphabet Input alphabet string
 * @param language Language hint for combination rules ("auto", "english", "turkish")
 * @param result Output buffer for combined alphabet
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int combine_similar_letters(const char *alphabet, const char *language,
                           char *result, size_t result_size);

/**
 * @brief Create a square-sized alphabet by combining letters if necessary
 * 
 * @param alphabet Input alphabet string
 * @param square_size Desired square size
 * @param result Output buffer for square-sized alphabet
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int create_square_alphabet(const char *alphabet, int square_size,
                          char *result, size_t result_size);

/**
 * @brief Create a 'Caesared' alphabet by shifting the base alphabet
 * 
 * @param base_alphabet Base alphabet to shift
 * @param shift Number of positions to shift
 * @param result Output buffer for shifted alphabet
 * @param result_size Size of the output buffer
 * @return 0 on success, -1 on error
 */
int create_caesared_alphabet(const char *base_alphabet, int shift,
                            char *result, size_t result_size);

/**
 * @brief Get letter combination rules for different languages
 * 
 * @param language Language code ("english", "turkish")
 * @return Pointer to combination rules string, NULL if not found
 */
const char* get_letter_combination_rules(const char *language);

#endif // CRYPTOLOGY_ALPHABET_UTILS_H
