/**
 * @file chaocipher.h
 * @brief Chaocipher implementation for C
 * 
 * Chaocipher is a polyalphabetic substitution cipher that uses two rotating
 * alphabets (left and right) that are permuted after each character.
 * It is self-reciprocal, meaning encryption and decryption use the same algorithm.
 */

#ifndef CHAOCIPHER_H
#define CHAOCIPHER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Create custom alphabets using keywords
 * 
 * @param left_keyword Keyword for left alphabet
 * @param right_keyword Keyword for right alphabet
 * @param left_alphabet Output buffer for left alphabet
 * @param right_alphabet Output buffer for right alphabet
 * @param alphabet_size Size of the alphabet buffer
 * @return 0 on success, -1 on error
 */
int chaocipher_create_custom_alphabets(const char *left_keyword,
                                     const char *right_keyword,
                                     char *left_alphabet,
                                     char *right_alphabet,
                                     size_t alphabet_size);

/**
 * @brief Permute the right alphabet after processing a character
 * 
 * @param alphabet Right alphabet to permute (modified in place)
 * @param alphabet_size Size of the alphabet
 * @param plain_char Character that was processed
 */
void chaocipher_permute_right_alphabet(char *alphabet, size_t alphabet_size, char plain_char);

/**
 * @brief Permute the left alphabet after processing a character
 * 
 * @param alphabet Left alphabet to permute (modified in place)
 * @param alphabet_size Size of the alphabet
 * @param cipher_char Character that was processed
 */
void chaocipher_permute_left_alphabet(char *alphabet, size_t alphabet_size, char cipher_char);

/**
 * @brief Prepare text for Chaocipher processing
 * 
 * @param text Input text
 * @param alphabet Alphabet to check against
 * @param alphabet_size Size of the alphabet
 * @param output Output buffer for prepared text
 * @param output_size Size of output buffer
 * @return Length of prepared text, or -1 on error
 */
int chaocipher_prepare_text(const char *text, 
                           const char *alphabet, 
                           size_t alphabet_size,
                           char *output, 
                           size_t output_size);

/**
 * @brief Encrypt plaintext using Chaocipher
 * 
 * @param plaintext Text to encrypt
 * @param left_alphabet Left alphabet (ciphertext alphabet)
 * @param right_alphabet Right alphabet (plaintext alphabet)
 * @param alphabet_size Size of the alphabets
 * @param output Output buffer for encrypted text
 * @param output_size Size of output buffer
 * @return Length of encrypted text, or -1 on error
 */
int chaocipher_encrypt(const char *plaintext,
                      const char *left_alphabet,
                      const char *right_alphabet,
                      size_t alphabet_size,
                      char *output,
                      size_t output_size);

/**
 * @brief Decrypt ciphertext using Chaocipher
 * 
 * @param ciphertext Text to decrypt
 * @param left_alphabet Left alphabet (ciphertext alphabet)
 * @param right_alphabet Right alphabet (plaintext alphabet)
 * @param alphabet_size Size of the alphabets
 * @param output Output buffer for decrypted text
 * @param output_size Size of output buffer
 * @return Length of decrypted text, or -1 on error
 */
int chaocipher_decrypt(const char *ciphertext,
                      const char *left_alphabet,
                      const char *right_alphabet,
                      size_t alphabet_size,
                      char *output,
                      size_t output_size);

/**
 * @brief Decrypt ciphertext with provided alphabets
 * 
 * @param ciphertext Text to decrypt
 * @param left_alphabet Left alphabet used for encryption
 * @param right_alphabet Right alphabet used for encryption
 * @param alphabet_size Size of the alphabets
 * @param output Output buffer for decrypted text
 * @param output_size Size of output buffer
 * @return Length of decrypted text, or -1 on error
 */
int chaocipher_decrypt_with_alphabets(const char *ciphertext,
                                    const char *left_alphabet,
                                    const char *right_alphabet,
                                    size_t alphabet_size,
                                    char *output,
                                    size_t output_size);

/**
 * @brief Create custom alphabets using monoalphabetic substitution ciphers
 * 
 * This function creates custom alphabets by applying monoalphabetic cipher
 * transformations to a base alphabet. The produced alphabets can be used
 * with Chaocipher for enhanced security.
 * 
 * @param left_cipher Type of monoalphabetic cipher for left alphabet ("caesar", "atbash", "keyword", "affine")
 * @param left_params Parameters for the left cipher (JSON-like string, e.g., "{\"shift\":5}")
 * @param right_cipher Type of monoalphabetic cipher for right alphabet
 * @param right_params Parameters for the right cipher (JSON-like string, e.g., "{\"keyword\":\"SECRET\"}")
 * @param alphabet Base alphabet to use (NULL for default English uppercase with space)
 * @param left_alphabet Output buffer for left alphabet
 * @param right_alphabet Output buffer for right alphabet
 * @param alphabet_size Size of alphabet buffers
 * @return 0 on success, -1 on error
 */
int chaocipher_create_alphabets_with_mono_ciphers(const char *left_cipher,
                                                const char *left_params,
                                                const char *right_cipher,
                                                const char *right_params,
                                                const char *alphabet,
                                                char *left_alphabet,
                                                char *right_alphabet,
                                                size_t alphabet_size);

#ifdef __cplusplus
}
#endif

#endif /* CHAOCIPHER_H */
