/**
 * @file monoalphabetic_squares.h
 * @brief Shared utilities for generating Polybius squares using monoalphabetic cipher transformations
 * 
 * This module provides shared utilities for generating Polybius squares using
 * monoalphabetic cipher transformations. This can be used by any cipher that
 * employs Polybius squares: Playfair, Two Square, Four Square, Bifid, Trifid, Nihilist.
 */

#ifndef MONOALPHABETIC_SQUARES_H
#define MONOALPHABETIC_SQUARES_H

#include <stddef.h>

/**
 * @brief Create a Polybius square using monoalphabetic cipher transformations
 * 
 * @param square_type Type of monoalphabetic transformation ("caesar", "atbash", "affine", "keyword")
 * @param alphabet Base alphabet (NULL for default English)
 * @param mono_params Parameters for the monoalphabetic transformation
 *                    - For "caesar": {"shift": int}
 *                    - For "affine": {"a": int, "b": int}
 *                    - For "keyword": {"keyword": str}
 * @param result Buffer to store the resulting square
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int create_monoalphabetic_square(
    const char *square_type,
    const char *alphabet,
    const char *mono_params,
    char *result,
    size_t result_size
);

/**
 * @brief Get list of available monoalphabetic square types
 * 
 * @param types Buffer to store comma-separated list of types
 * @param types_size Size of the types buffer
 * @return 0 on success, -1 on error
 */
int get_available_monoalphabetic_types(char *types, size_t types_size);

/**
 * @brief Validate monoalphabetic parameters for a given square type
 * 
 * @param square_type Type of monoalphabetic transformation
 * @param mono_params Parameters to validate (JSON string)
 * @return 1 if parameters are valid, 0 otherwise
 */
int validate_mono_params(const char *square_type, const char *mono_params);

/**
 * @brief Create a Caesar-shifted alphabet
 * 
 * @param alphabet Base alphabet
 * @param shift Shift amount
 * @param result Buffer to store the shifted alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int create_caesar_alphabet(const char *alphabet, int shift, char *result, size_t result_size);

/**
 * @brief Create an Atbash-reversed alphabet
 * 
 * @param alphabet Base alphabet
 * @param result Buffer to store the reversed alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int create_atbash_alphabet(const char *alphabet, char *result, size_t result_size);

/**
 * @brief Create an Affine-transformed alphabet
 * 
 * @param alphabet Base alphabet
 * @param a Affine parameter a
 * @param b Affine parameter b
 * @param result Buffer to store the transformed alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int create_affine_alphabet(const char *alphabet, int a, int b, char *result, size_t result_size);

/**
 * @brief Create a keyword-based alphabet
 * 
 * @param alphabet Base alphabet
 * @param keyword Keyword to use
 * @param result Buffer to store the keyword-based alphabet
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int create_keyword_alphabet(const char *alphabet, const char *keyword, char *result, size_t result_size);

/**
 * @brief Convert a transformed alphabet to a Polybius square
 * 
 * @param transformed_alphabet The transformed alphabet
 * @param original_alphabet The original alphabet (for size determination)
 * @param result Buffer to store the square
 * @param result_size Size of the result buffer
 * @return 0 on success, -1 on error
 */
int alphabet_to_square(const char *transformed_alphabet, const char *original_alphabet, char *result, size_t result_size);

#endif /* MONOALPHABETIC_SQUARES_H */
