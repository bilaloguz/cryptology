#include "../../../../include/cryptology/classical/substitution/composite/adfgvx.h"
#include "../../../../include/cryptology/classical/substitution/polygraphic/monoalphabetic_squares.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

// Helper function to count UTF-8 characters (not bytes)
static size_t utf8_strlen(const char* str) {
    if (!str) return 0;
    
    size_t len = 0;
    const unsigned char* p = (const unsigned char*)str;
    
    while (*p) {
        if ((*p & 0x80) == 0) {
            // ASCII character (1 byte)
            len++;
            p++;
        } else if ((*p & 0xE0) == 0xC0) {
            // 2-byte UTF-8 character
            len++;
            p += 2;
        } else if ((*p & 0xF0) == 0xE0) {
            // 3-byte UTF-8 character
            len++;
            p += 3;
        } else if ((*p & 0xF8) == 0xF0) {
            // 4-byte UTF-8 character
            len++;
            p += 4;
        } else {
            // Invalid UTF-8, treat as single byte
            len++;
            p++;
        }
    }
    
    return len;
}

// Helper function to get UTF-8 character at index
static int utf8_char_at(const char* str, size_t index, char* result, size_t result_size) {
    if (!str || !result || result_size == 0) return -1;
    
    const unsigned char* p = (const unsigned char*)str;
    size_t current_index = 0;
    
    while (*p && current_index <= index) {
        if (current_index == index) {
            // Found the character at the desired index
            if ((*p & 0x80) == 0) {
                // ASCII character (1 byte)
                result[0] = *p;
                result[1] = '\0';
                return 1;
            } else if ((*p & 0xE0) == 0xC0) {
                // 2-byte UTF-8 character
                if (result_size >= 3) {
                    result[0] = p[0];
                    result[1] = p[1];
                    result[2] = '\0';
                    return 2;
                }
            } else if ((*p & 0xF0) == 0xE0) {
                // 3-byte UTF-8 character
                if (result_size >= 4) {
                    result[0] = p[0];
                    result[1] = p[1];
                    result[2] = p[2];
                    result[3] = '\0';
                    return 3;
                }
            } else if ((*p & 0xF8) == 0xF0) {
                // 4-byte UTF-8 character
                if (result_size >= 5) {
                    result[0] = p[0];
                    result[1] = p[1];
                    result[2] = p[2];
                    result[3] = p[3];
                    result[4] = '\0';
                    return 4;
                }
            }
            return -1;
        }
        
        // Move to next character
        if ((*p & 0x80) == 0) {
            p++;
        } else if ((*p & 0xE0) == 0xC0) {
            p += 2;
        } else if ((*p & 0xF0) == 0xE0) {
            p += 3;
        } else if ((*p & 0xF8) == 0xF0) {
            p += 4;
        } else {
            p++;
        }
        current_index++;
    }
    
    return -1; // Index out of bounds
}

// Helper function to clean text (remove spaces, convert to uppercase)
static void clean_text(const char* input, char* output, size_t output_size) {
    size_t i = 0, j = 0;
    while (input[i] && j < output_size - 1) {
        if (isalpha(input[i]) || isdigit(input[i])) {
            output[j++] = toupper(input[i]);
        }
        i++;
    }
    output[j] = '\0';
}

// Helper function to create standard ADFGVX square
static int create_standard_adfgvx_square(const char* alphabet, char* result, size_t result_size) {
    if (!alphabet || !result) return -1;
    
    size_t char_len = utf8_strlen(alphabet);
    if (char_len < 36) return -1;
    
    // Format as 6x6 grid using UTF-8 character indexing
    int pos = 0;
    for (int row = 0; row < 6 && pos < result_size - 1; row++) {
        for (int col = 0; col < 6 && pos < result_size - 1; col++) {
            int char_index = row * 6 + col;
            if (char_index < 36) {
                char utf8_char[5];
                int bytes = utf8_char_at(alphabet, char_index, utf8_char, sizeof(utf8_char));
                if (bytes > 0) {
                    for (int i = 0; i < bytes && pos < result_size - 1; i++) {
                        result[pos++] = utf8_char[i];
                    }
                }
            }
        }
        if (row < 5 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to find character position in square (UTF-8 aware)
static int find_char_in_square(const char* square, const char* target_char, int* row, int* col) {
    if (!square || !target_char || !row || !col) return -1;
    
    const char* p = square;
    int current_row = 0, current_col = 0;
    
    while (*p) {
        if (*p == '\n') {
            current_row++;
            current_col = 0;
            p++;
            continue;
        }
        
        // Check if this position matches the target character
        if (strncmp(p, target_char, strlen(target_char)) == 0) {
            *row = current_row;
            *col = current_col;
            return 0;
        }
        
        // Move to next character
        if ((*p & 0x80) == 0) {
            p++;
        } else if ((*p & 0xE0) == 0xC0) {
            p += 2;
        } else if ((*p & 0xF0) == 0xE0) {
            p += 3;
        } else if ((*p & 0xF8) == 0xF0) {
            p += 4;
        } else {
            p++;
        }
        current_col++;
    }
    
    return -1;
}

// Helper function to substitute text to ADFGVX pairs (UTF-8 aware)
static int substitute_to_adfgvx(const char* text, const char* square, char* result, size_t result_size) {
    if (!text || !square || !result) return -1;
    
    const char* adfgvx_chars = "ADFGVX";
    int pos = 0;
    
    const char* p = text;
    while (*p && pos < result_size - 1) {
        char utf8_char[5];
        int bytes = 0;
        
        // Extract current UTF-8 character
        if ((*p & 0x80) == 0) {
            // ASCII character (1 byte)
            utf8_char[0] = *p;
            utf8_char[1] = '\0';
            bytes = 1;
            p++;
        } else if ((*p & 0xE0) == 0xC0) {
            // 2-byte UTF-8 character
            utf8_char[0] = p[0];
            utf8_char[1] = p[1];
            utf8_char[2] = '\0';
            bytes = 2;
            p += 2;
        } else if ((*p & 0xF0) == 0xE0) {
            // 3-byte UTF-8 character
            utf8_char[0] = p[0];
            utf8_char[1] = p[1];
            utf8_char[2] = p[2];
            utf8_char[3] = '\0';
            bytes = 3;
            p += 3;
        } else if ((*p & 0xF8) == 0xF0) {
            // 4-byte UTF-8 character
            utf8_char[0] = p[0];
            utf8_char[1] = p[1];
            utf8_char[2] = p[2];
            utf8_char[3] = p[3];
            utf8_char[4] = '\0';
            bytes = 4;
            p += 4;
        } else {
            // Invalid UTF-8, treat as single byte
            utf8_char[0] = *p;
            utf8_char[1] = '\0';
            bytes = 1;
            p++;
        }
        
        int row, col;
        if (find_char_in_square(square, utf8_char, &row, &col) == 0) {
            result[pos++] = adfgvx_chars[row];
            result[pos++] = adfgvx_chars[col];
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to substitute ADFGVX pairs back to text (UTF-8 aware)
static int substitute_from_adfgvx(const char* adfgvx_pairs, const char* square, char* result, size_t result_size) {
    if (!adfgvx_pairs || !square || !result) return -1;
    
    const char* adfgvx_chars = "ADFGVX";
    int pos = 0;
    
    for (size_t i = 0; adfgvx_pairs[i] && adfgvx_pairs[i+1] && pos < result_size - 1; i += 2) {
        char row_char = adfgvx_pairs[i];
        char col_char = adfgvx_pairs[i+1];
        
        int row = -1, col = -1;
        for (int j = 0; j < 6; j++) {
            if (adfgvx_chars[j] == row_char) row = j;
            if (adfgvx_chars[j] == col_char) col = j;
        }
        
        if (row >= 0 && col >= 0) {
            // Find character at position (row, col) in square
            const char* p = square;
            int current_row = 0, current_col = 0;
            
            while (*p) {
                if (*p == '\n') {
                    current_row++;
                    current_col = 0;
                    p++;
                    continue;
                }
                
                if (current_row == row && current_col == col) {
                    // Found the character at the desired position
                    char utf8_char[5];
                    int bytes = 0;
                    
                    if ((*p & 0x80) == 0) {
                        // ASCII character (1 byte)
                        utf8_char[0] = *p;
                        utf8_char[1] = '\0';
                        bytes = 1;
                    } else if ((*p & 0xE0) == 0xC0) {
                        // 2-byte UTF-8 character
                        utf8_char[0] = p[0];
                        utf8_char[1] = p[1];
                        utf8_char[2] = '\0';
                        bytes = 2;
                    } else if ((*p & 0xF0) == 0xE0) {
                        // 3-byte UTF-8 character
                        utf8_char[0] = p[0];
                        utf8_char[1] = p[1];
                        utf8_char[2] = p[2];
                        utf8_char[3] = '\0';
                        bytes = 3;
                    } else if ((*p & 0xF8) == 0xF0) {
                        // 4-byte UTF-8 character
                        utf8_char[0] = p[0];
                        utf8_char[1] = p[1];
                        utf8_char[2] = p[2];
                        utf8_char[3] = p[3];
                        utf8_char[4] = '\0';
                        bytes = 4;
                    }
                    
                    // Copy UTF-8 character to result
                    for (int k = 0; k < bytes && pos < result_size - 1; k++) {
                        result[pos++] = utf8_char[k];
                    }
                    break;
                }
                
                // Move to next character
                if ((*p & 0x80) == 0) {
                    p++;
                } else if ((*p & 0xE0) == 0xC0) {
                    p += 2;
                } else if ((*p & 0xF0) == 0xE0) {
                    p += 3;
                } else if ((*p & 0xF8) == 0xF0) {
                    p += 4;
                } else {
                    p++;
                }
                current_col++;
            }
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function for columnar transposition (matches Python logic exactly)
static int columnar_transposition(const char* text, const char* key, int encrypt, char* result, size_t result_size) {
    if (!text || !key || !result) return -1;
    
    size_t key_len = strlen(key);
    size_t text_len = strlen(text);
    
    if (key_len == 0 || text_len == 0) return -1;
    
    // Create key order array (sorted by key letters, ascending)
    int* key_order = malloc(key_len * sizeof(int));
    if (!key_order) return -1;
    
    // Initialize key order
    for (size_t i = 0; i < key_len; i++) {
        key_order[i] = i;
    }
    
    // Sort key order by key characters (ascending)
    for (size_t i = 0; i < key_len - 1; i++) {
        for (size_t j = i + 1; j < key_len; j++) {
            if (key[key_order[i]] > key[key_order[j]]) {
                int temp = key_order[i];
                key_order[i] = key_order[j];
                key_order[j] = temp;
            }
        }
    }
    
    size_t cols = key_len;
    size_t rows = (text_len + cols - 1) / cols;  // Ceiling division
    
    if (encrypt) {
        // Encrypt: write by rows, read by columns
        // Create grid as array of strings
        char** grid = malloc(cols * sizeof(char*));
        if (!grid) {
            free(key_order);
            return -1;
        }
        
        // Initialize grid columns
        for (size_t i = 0; i < cols; i++) {
            grid[i] = malloc((rows + 1) * sizeof(char));
            if (!grid[i]) {
                for (size_t j = 0; j < i; j++) free(grid[j]);
                free(grid);
                free(key_order);
                return -1;
            }
            grid[i][0] = '\0';
        }
        
        // Write by rows into columns (grid[i % cols] += char)
        for (size_t i = 0; i < text_len; i++) {
            size_t col = i % cols;
            size_t row = i / cols;
            grid[col][row] = text[i];
            grid[col][row + 1] = '\0';
        }
        
        // Read columns in key order
        int pos = 0;
        for (size_t k = 0; k < cols && pos < result_size - 1; k++) {
            size_t col_idx = key_order[k];
            for (size_t row = 0; row < rows && pos < result_size - 1; row++) {
                size_t text_idx = row * cols + col_idx;
                if (text_idx < text_len) {
                    result[pos++] = grid[col_idx][row];
                }
            }
        }
        result[pos] = '\0';
        
        // Cleanup
        for (size_t i = 0; i < cols; i++) free(grid[i]);
        free(grid);
    } else {
        // Decrypt: write by columns, read by rows
        char** grid = malloc(cols * sizeof(char*));
        if (!grid) {
            free(key_order);
            return -1;
        }
        
        // Initialize grid columns
        for (size_t i = 0; i < cols; i++) {
            grid[i] = malloc((rows + 1) * sizeof(char));
            if (!grid[i]) {
                for (size_t j = 0; j < i; j++) free(grid[j]);
                free(grid);
                free(key_order);
                return -1;
            }
            grid[i][0] = '\0';
        }
        
        // Distribute text to columns in key order
        int text_pos = 0;
        for (size_t k = 0; k < cols; k++) {
            size_t col_idx = key_order[k];
            size_t col_len;
            
            // Calculate column length based on position in key order
            if (text_len % cols == 0) {
                // All columns have equal length
                col_len = rows;
            } else {
                // First (text_len % cols) columns get (rows) chars, rest get (rows-1) chars
                col_len = rows;
                if (col_idx >= text_len % cols) {
                    col_len = rows - 1;
                }
            }
            
            // Copy text segment to this column
            for (size_t i = 0; i < col_len && text_pos < text_len; i++) {
                grid[col_idx][i] = text[text_pos++];
            }
            grid[col_idx][col_len] = '\0';
        }
        
        // Read by rows
        int result_pos = 0;
        for (size_t row = 0; row < rows && result_pos < result_size - 1; row++) {
            for (size_t col = 0; col < cols && result_pos < result_size - 1; col++) {
                if (row < strlen(grid[col])) {
                    result[result_pos++] = grid[col][row];
                }
            }
        }
        result[result_pos] = '\0';
        
        // Cleanup
        for (size_t i = 0; i < cols; i++) free(grid[i]);
        free(grid);
    }
    
    free(key_order);
    return 0;
}

int adfgvx_encrypt(
    const char* plaintext,
    const char* key,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* result,
    size_t result_size
) {
    if (!plaintext || !key || !result || result_size == 0) return -1;
    
    // Clean plaintext
    char cleaned_text[1024];
    clean_text(plaintext, cleaned_text, sizeof(cleaned_text));
    
    if (strlen(cleaned_text) == 0) return -1;
    
    // Determine alphabet to use
    const char* use_alphabet = DEFAULT_ADFGVX_ALPHABET;
    if (alphabet && strcmp(alphabet, "turkish") == 0) {
        use_alphabet = TURKISH_ADFGVX_ALPHABET;
    }
    
    // Generate or use provided square
    char square_buffer[1024];
    if (square) {
        strncpy(square_buffer, square, sizeof(square_buffer) - 1);
        square_buffer[sizeof(square_buffer) - 1] = '\0';
    } else {
        if (create_standard_adfgvx_square(use_alphabet, square_buffer, sizeof(square_buffer)) != 0) {
            return -1;
        }
    }
    
    // Step 1: Substitution - convert letters to ADFGVX pairs
    char substituted[2048];
    if (substitute_to_adfgvx(cleaned_text, square_buffer, substituted, sizeof(substituted)) != 0) {
        return -1;
    }
    
    // Step 2: Columnar transposition
    if (columnar_transposition(substituted, key, 1, result, result_size) != 0) {
        return -1;
    }
    
    return 0;
}

int adfgvx_decrypt(
    const char* ciphertext,
    const char* key,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* result,
    size_t result_size
) {
    if (!ciphertext || !key || !result || result_size == 0) return -1;
    
    // Determine alphabet to use
    const char* use_alphabet = DEFAULT_ADFGVX_ALPHABET;
    if (alphabet && strcmp(alphabet, "turkish") == 0) {
        use_alphabet = TURKISH_ADFGVX_ALPHABET;
    }
    
    // Generate or use provided square
    char square_buffer[1024];
    if (square) {
        strncpy(square_buffer, square, sizeof(square_buffer) - 1);
        square_buffer[sizeof(square_buffer) - 1] = '\0';
    } else {
        if (create_standard_adfgvx_square(use_alphabet, square_buffer, sizeof(square_buffer)) != 0) {
            return -1;
        }
    }
    
    // Step 1: Reverse columnar transposition
    char substituted[2048];
    if (columnar_transposition(ciphertext, key, 0, substituted, sizeof(substituted)) != 0) {
        return -1;
    }
    
    // Step 2: Reverse substitution - convert ADFGVX pairs back to letters
    if (substitute_from_adfgvx(substituted, square_buffer, result, result_size) != 0) {
        return -1;
    }
    
    return 0;
}

int adfgvx_produce_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    char* result,
    size_t result_size
) {
    if (!square_type || !result || result_size == 0) return -1;
    
    // Determine alphabet to use
    const char* use_alphabet = DEFAULT_ADFGVX_ALPHABET;
    if (alphabet) {
        use_alphabet = alphabet;
    } else if (language && strcmp(language, "turkish") == 0) {
        use_alphabet = TURKISH_ADFGVX_ALPHABET;
    }
    
    // Check if alphabet has enough characters (UTF-8 aware)
    size_t char_len = utf8_strlen(use_alphabet);
    if (char_len < 36) {
        return -1; // Not enough characters for 6x6 square
    }
    
    if (strcmp(square_type, "standard") == 0) {
        return create_standard_adfgvx_square(use_alphabet, result, result_size);
    } else if (strcmp(square_type, "caesar") == 0 || 
               strcmp(square_type, "atbash") == 0 || 
               strcmp(square_type, "affine") == 0) {
        // Use shared monoalphabetic square generation
        return create_monoalphabetic_square(square_type, use_alphabet, mono_params, result, result_size);
    } else {
        // For now, only support standard and monoalphabetic types
        return -1;
    }
}

int adfgvx_generate_random_key(
    size_t length,
    char* result,
    size_t result_size
) {
    if (!result || result_size == 0 || length == 0) return -1;
    
    srand(time(NULL));
    
    for (size_t i = 0; i < length && i < result_size - 1; i++) {
        result[i] = 'A' + (rand() % 26);
    }
    result[length] = '\0';
    
    return 0;
}

int adfgvx_generate_key_for_text(
    const char* text,
    char* result,
    size_t result_size
) {
    if (!text || !result || result_size == 0) return -1;
    
    size_t text_len = strlen(text);
    return adfgvx_generate_random_key(text_len, result, result_size);
}

int adfgvx_encrypt_with_random_key(
    const char* plaintext,
    size_t key_length,
    const char* square,
    const char* alphabet,
    const char* mono_params,
    char* ciphertext,
    size_t ciphertext_size,
    char* generated_key,
    size_t key_size
) {
    if (!plaintext || !ciphertext || !generated_key) return -1;
    
    // Generate random key
    if (adfgvx_generate_random_key(key_length, generated_key, key_size) != 0) {
        return -1;
    }
    
    // Encrypt with generated key
    return adfgvx_encrypt(plaintext, generated_key, square, alphabet, mono_params, ciphertext, ciphertext_size);
}
