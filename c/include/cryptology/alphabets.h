/**
 * @file alphabets.h
 * @brief Centralized Alphabet Definitions
 * 
 * This module provides standardized alphabet definitions for all ciphers.
 * All alphabets are lowercase and support UTF-8 for Turkish characters.
 * 
 * Alphabet Standards:
 * 1. All alphabets use lowercase letters
 * 2. All input is converted to lowercase before encryption
 * 3. Turkish uses 29 letters + 7 digits (0-6) for 6x6 squares
 * 4. English uses 26 letters + 10 digits (0-9) for 6x6 squares
 * 5. All alphabets support UTF-8 encoding
 */

#ifndef ALPHABETS_H
#define ALPHABETS_H

#include <stddef.h>
#include <stdbool.h>

// Standard Alphabets (lowercase)

// English Alphabets
#define ENGLISH_ALPHABET "abcdefghijklmnopqrstuvwxyz"  // 26 letters
#define ENGLISH_WITH_DIGITS "abcdefghijklmnopqrstuvwxyz0123456789"  // 36 chars (for 6x6 squares)

// Turkish Alphabets
#define TURKISH_ALPHABET "abcçdefgğhıijklmnoöprsştuüvyz"  // 29 letters  
#define TURKISH_WITH_DIGITS "abcçdefgğhıijklmnoöprsştuüvyz0123456"  // 36 chars (29 letters + 7 digits 0-6)

// Digits
#define DIGITS "0123456789"  // 10 digits

/**
 * @brief Get alphabet by language and digit inclusion
 * 
 * @param language "english" or "turkish"
 * @param include_digits Whether to include digits in alphabet
 * @param result Buffer to store alphabet
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int get_alphabet(const char* language, bool include_digits, char* result, size_t result_size);

/**
 * @brief Normalize text to lowercase for consistent processing
 * 
 * @param text Text to normalize
 * @param result Buffer to store normalized text
 * @param result_size Size of result buffer
 * @return 0 on success, -1 on error
 */
int normalize_text(const char* text, char* result, size_t result_size);

/**
 * @brief Validate alphabet has no duplicate characters
 * 
 * @param alphabet Alphabet to validate
 * @return true if valid, false otherwise
 */
bool validate_alphabet(const char* alphabet);

/**
 * @brief Get alphabet length in UTF-8 characters (not bytes)
 * 
 * @param alphabet Alphabet string
 * @return Number of UTF-8 characters
 */
size_t get_alphabet_length(const char* alphabet);

#endif // ALPHABETS_H
