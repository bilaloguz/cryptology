#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "cryptology/classical/transposition/compound/rasterschluessel_44.h"

#define ALPHABET_SIZE 36
#define SQUARE_SIZE 6

/**
 * Create a Polybius square using keyword.
 * For Rasterschlüssel 44, we use a 6x6 square (36 chars: 26 letters + 10 digits).
 */
static void create_square(const char *keyword, char square[6][6]) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz0123456789";
    char square_chars[36];
    int seen[256] = {0};
    int pos = 0;
    
    // Add keyword first
    for (int i = 0; keyword[i] != '\0'; i++) {
        char c = tolower((unsigned char)keyword[i]);
        if (strchr(alphabet, c) && !seen[(unsigned char)c] && pos < 36) {
            square_chars[pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Add rest of alphabet
    for (int i = 0; alphabet[i] != '\0'; i++) {
        char c = alphabet[i];
        if (!seen[(unsigned char)c] && pos < 36) {
            square_chars[pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Fill 6x6 square
    pos = 0;
    for (int row = 0; row < SQUARE_SIZE; row++) {
        for (int col = 0; col < SQUARE_SIZE; col++) {
            if (pos < 36) {
                square[row][col] = square_chars[pos++];
            }
        }
    }
}

/**
 * Find coordinates of a character in the square.
 * Returns -1 if not found.
 */
static int find_char_in_square(char c, const char square[6][6], int *row, int *col) {
    c = tolower((unsigned char)c);
    
    for (int r = 0; r < SQUARE_SIZE; r++) {
        for (int c2 = 0; c2 < SQUARE_SIZE; c2++) {
            if (tolower((unsigned char)square[r][c2]) == c) {
                *row = r;
                *col = c2;
                return 0;
            }
        }
    }
    return -1;
}

/**
 * Get character at coordinates in the square.
 */
static char get_char_at_coord(const char square[6][6], int row, int col) {
    if (row >= 0 && row < SQUARE_SIZE && col >= 0 && col < SQUARE_SIZE) {
        return square[row][col];
    }
    return '\0';
}

int rasterschluessel_44_encrypt(const char *plaintext, const char *keyword, 
                                 char *output, size_t max_len) {
    if (!plaintext || !keyword || !output || max_len == 0) {
        return -1;
    }
    
    // Clean and normalize text to lowercase
    char text[1024] = {0};
    int text_pos = 0;
    for (int i = 0; plaintext[i] != '\0' && text_pos < sizeof(text) - 1; i++) {
        if (isalpha((unsigned char)plaintext[i])) {
            text[text_pos++] = tolower((unsigned char)plaintext[i]);
        }
    }
    
    if (text_pos == 0) {
        output[0] = '\0';
        return 0;
    }
    
    // Create Polybius square
    char square[6][6];
    create_square(keyword, square);
    
    // Convert to coordinates
    int output_pos = 0;
    for (int i = 0; i < text_pos; i++) {
        int row, col;
        if (find_char_in_square(text[i], square, &row, &col) == 0) {
            if (output_pos < (int)max_len - 1) {
                output[output_pos++] = '0' + row;
            }
            if (output_pos < (int)max_len - 1) {
                output[output_pos++] = '0' + col;
            }
        }
    }
    output[output_pos] = '\0';
    
    return 0;
}

int rasterschluessel_44_decrypt(const char *ciphertext, const char *keyword, 
                                 char *output, size_t max_len) {
    if (!ciphertext || !keyword || !output || max_len == 0) {
        return -1;
    }
    
    // Extract digits
    char digits[2048] = {0};
    int digit_pos = 0;
    for (int i = 0; ciphertext[i] != '\0' && digit_pos < sizeof(digits) - 1; i++) {
        if (isdigit((unsigned char)ciphertext[i])) {
            digits[digit_pos++] = ciphertext[i];
        }
    }
    
    if (digit_pos == 0 || digit_pos % 2 != 0) {
        output[0] = '\0';
        return 0;
    }
    
    // Create square
    char square[6][6];
    create_square(keyword, square);
    
    // Convert coordinates back to characters
    int output_pos = 0;
    for (int i = 0; i < digit_pos; i += 2) {
        if (i + 1 < digit_pos) {
            int row = digits[i] - '0';
            int col = digits[i + 1] - '0';
            
            if (row < SQUARE_SIZE && col < SQUARE_SIZE && output_pos < (int)max_len - 1) {
                char c = get_char_at_coord(square, row, col);
                if (c != '\0') {
                    output[output_pos++] = c;
                }
            }
        }
    }
    output[output_pos] = '\0';
    
    return 0;
}

void rasterschluessel_44_produce_square(const char *keyword, char square[6][6]) {
    create_square(keyword, square);
}

