#include "../../../../include/cryptology/classical/substitution/composite/vic.h"
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
            output[j++] = tolower(input[i]);
        }
        i++;
    }
    output[j] = '\0';
}

// Helper function to create standard Polybius square
static int create_standard_polybius_square(const char* alphabet, char* result, size_t result_size) {
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

// Helper function to create keyword-based Polybius square
static int create_keyword_polybius_square(const char* keyword, const char* alphabet, char* result, size_t result_size) {
    if (!keyword || !alphabet || !result) return -1;
    
    size_t char_len = utf8_strlen(alphabet);
    if (char_len < 36) return -1;
    
    // Remove duplicates from keyword while preserving order
    char keyword_unique[37] = {0};
    int unique_pos = 0;
    int seen[256] = {0};
    
    for (size_t i = 0; keyword[i] && unique_pos < 36; i++) {
        char c = tolower(keyword[i]);
        if (strchr(alphabet, c) && !seen[(unsigned char)c]) {
            keyword_unique[unique_pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Add remaining alphabet characters
    for (size_t i = 0; alphabet[i] && unique_pos < 36; i++) {
        char c = alphabet[i];
        if (!seen[(unsigned char)c]) {
            keyword_unique[unique_pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Format as 6x6 grid
    int pos = 0;
    for (int row = 0; row < 6 && pos < result_size - 1; row++) {
        for (int col = 0; col < 6 && pos < result_size - 1; col++) {
            int char_index = row * 6 + col;
            if (char_index < unique_pos) {
                result[pos++] = keyword_unique[char_index];
            }
        }
        if (row < 5 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to create straddling checkerboard
static int create_straddling_checkerboard(const char* keyword, const char* alphabet, char* result, size_t result_size) {
    if (!keyword || !alphabet || !result) return -1;
    
    size_t char_len = utf8_strlen(alphabet);
    if (char_len < 30) return -1;
    
    // Remove duplicates from keyword while preserving order
    char keyword_unique[31] = {0};
    int unique_pos = 0;
    int seen[256] = {0};
    
    for (size_t i = 0; keyword[i] && unique_pos < 30; i++) {
        char c = tolower(keyword[i]);
        if (strchr(alphabet, c) && !seen[(unsigned char)c]) {
            keyword_unique[unique_pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Add remaining alphabet characters
    for (size_t i = 0; alphabet[i] && unique_pos < 30; i++) {
        char c = alphabet[i];
        if (!seen[(unsigned char)c]) {
            keyword_unique[unique_pos++] = c;
            seen[(unsigned char)c] = 1;
        }
    }
    
    // Format as 3x10 checkerboard
    int pos = 0;
    for (int row = 0; row < 3 && pos < result_size - 1; row++) {
        for (int col = 0; col < 10 && pos < result_size - 1; col++) {
            int char_index = row * 10 + col;
            if (char_index < unique_pos) {
                result[pos++] = keyword_unique[char_index];
            }
        }
        if (row < 2 && pos < result_size - 1) {
            result[pos++] = '\n';
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to find character position in Polybius square (UTF-8 aware)
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

// Helper function to get character from Polybius square at given position (UTF-8 aware)
static int get_char_from_square(const char* square, int row, int col, char* result, size_t result_size) {
    if (!square || !result || result_size == 0) return -1;
    
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
            for (int i = 0; i < bytes && i < result_size - 1; i++) {
                result[i] = utf8_char[i];
            }
            result[bytes] = '\0';
            return bytes;
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
    
    return -1; // Position not found
}

// Helper function to substitute text to Polybius pairs (UTF-8 aware)
static int substitute_to_polybius(const char* text, const char* square, char* result, size_t result_size) {
    if (!text || !square || !result) return -1;
    
    const char* vic_chars = VIC_LETTERS;
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
            result[pos++] = vic_chars[row];
            result[pos++] = vic_chars[col];
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to substitute Polybius pairs back to text (UTF-8 aware)
static int substitute_from_polybius(const char* pairs, const char* square, char* result, size_t result_size) {
    if (!pairs || !square || !result) return -1;
    
    const char* vic_chars = VIC_LETTERS;
    int pos = 0;
    
    for (size_t i = 0; pairs[i] && pairs[i+1] && pos < result_size - 1; i += 2) {
        char row_char = pairs[i];
        char col_char = pairs[i+1];
        
        int row = -1, col = -1;
        for (int j = 0; j < 6; j++) {
            if (vic_chars[j] == row_char) row = j;
            if (vic_chars[j] == col_char) col = j;
        }
        
        if (row >= 0 && col >= 0) {
            char utf8_char[5];
            int bytes = get_char_from_square(square, row, col, utf8_char, sizeof(utf8_char));
            if (bytes > 0) {
                for (int k = 0; k < bytes && pos < result_size - 1; k++) {
                    result[pos++] = utf8_char[k];
                }
            }
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to convert Polybius pairs to digits
static int pairs_to_digits(const char* pairs, char* result, size_t result_size) {
    if (!pairs || !result) return -1;
    
    const char* vic_chars = VIC_LETTERS;
    int pos = 0;
    
    for (size_t i = 0; pairs[i] && pos < result_size - 1; i++) {
        if (strchr(vic_chars, pairs[i])) {
            int index = strchr(vic_chars, pairs[i]) - vic_chars;
            result[pos++] = '0' + index;
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to convert digits to Polybius pairs
static int digits_to_pairs(const char* digits, char* result, size_t result_size) {
    if (!digits || !result) return -1;
    
    const char* vic_chars = VIC_LETTERS;
    int pos = 0;
    
    for (size_t i = 0; digits[i] && pos < result_size - 1; i++) {
        if (isdigit(digits[i])) {
            int index = digits[i] - '0';
            if (0 <= index && index < 6) {
                result[pos++] = vic_chars[index];
            }
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to convert digits to letters using straddling checkerboard
static int digits_to_letters(const char* digits, const char* checkerboard, char* result, size_t result_size) {
    if (!digits || !checkerboard || !result) return -1;
    
    const char* lines[3];
    int line_count = 0;
    char checkerboard_copy[1024];
    strcpy(checkerboard_copy, checkerboard);
    
    // Split checkerboard into lines
    char* token = strtok(checkerboard_copy, "\n");
    while (token && line_count < 3) {
        lines[line_count++] = token;
        token = strtok(NULL, "\n");
    }
    
    int pos = 0;
    size_t i = 0;
    
    while (digits[i] && pos < result_size - 1) {
        // Try two-digit lookup first (rows 1-2)
        if (i + 1 < strlen(digits)) {
            int row = digits[i] - '0';
            int col = digits[i + 1] - '0';
            if (1 <= row && row < line_count && 0 <= col && col < strlen(lines[row])) {
                result[pos++] = lines[row][col];
                i += 2;
                continue;
            }
        }
        
        // Single digit lookup (row 0)
        int digit = digits[i] - '0';
        if (0 <= digit && digit < strlen(lines[0])) {
            result[pos++] = lines[0][digit];
        }
        i++;
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function to convert letters to digits using straddling checkerboard
static int letters_to_digits(const char* letters, const char* checkerboard, char* result, size_t result_size) {
    if (!letters || !checkerboard || !result) return -1;
    
    const char* lines[3];
    int line_count = 0;
    char checkerboard_copy[1024];
    strcpy(checkerboard_copy, checkerboard);
    
    // Split checkerboard into lines
    char* token = strtok(checkerboard_copy, "\n");
    while (token && line_count < 3) {
        lines[line_count++] = token;
        token = strtok(NULL, "\n");
    }
    
    int pos = 0;
    
    for (size_t i = 0; letters[i] && pos < result_size - 1; i++) {
        int found = 0;
        for (int row = 0; row < line_count && !found; row++) {
            for (int col = 0; col < strlen(lines[row]) && !found; col++) {
                if (lines[row][col] == letters[i]) {
                    if (row == 0) {
                        // Single digit (first row)
                        result[pos++] = '0' + col;
                    } else {
                        // Two digits (other rows)
                        result[pos++] = '0' + row;
                        result[pos++] = '0' + col;
                    }
                    found = 1;
                }
            }
        }
        
        if (!found) {
            // Character not found in checkerboard, skip it
            continue;
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

// Helper function for numeric key addition
static int numeric_addition(const char* text, const char* numeric_key, const char* alphabet, int encrypt, char* result, size_t result_size) {
    if (!text || !numeric_key || !alphabet || !result) return -1;
    
    int pos = 0;
    size_t key_len = strlen(numeric_key);
    
    for (size_t i = 0; text[i] && pos < result_size - 1; i++) {
        const char* char_pos = strchr(alphabet, text[i]);
        if (char_pos) {
            int char_index = char_pos - alphabet;
            int key_digit = numeric_key[i % key_len] - '0';
            
            int new_index;
            if (encrypt) {
                new_index = (char_index + key_digit) % strlen(alphabet);
            } else {
                new_index = (char_index - key_digit + strlen(alphabet)) % strlen(alphabet);
            }
            
            result[pos++] = alphabet[new_index];
        } else {
            result[pos++] = text[i];
        }
    }
    result[pos] = '\0';
    
    return 0;
}

// Helper function for chain addition encryption
static int chain_addition_encrypt(const char* text, const char* numeric_key, const char* alphabet, char* result, size_t result_size) {
    if (!text || !numeric_key || !alphabet || !result) return -1;
    
    int pos = 0;
    size_t key_len = strlen(numeric_key);
    char* current_key = malloc(key_len + 1);
    if (!current_key) return -1;
    strcpy(current_key, numeric_key);
    
    for (size_t i = 0; text[i] && pos < result_size - 1; i++) {
        const char* char_pos = strchr(alphabet, text[i]);
        if (char_pos) {
            int char_index = char_pos - alphabet;
            int key_digit = current_key[i % key_len] - '0';
            
            int new_index = (char_index + key_digit) % strlen(alphabet);
            result[pos++] = alphabet[new_index];
            
            // Update key for next character
            memmove(current_key, current_key + 1, key_len - 1);
            current_key[key_len - 1] = '0' + new_index;
        } else {
            result[pos++] = text[i];
        }
    }
    result[pos] = '\0';
    
    free(current_key);
    return 0;
}

// Helper function for chain addition decryption
static int chain_addition_decrypt(const char* text, const char* numeric_key, const char* alphabet, char* result, size_t result_size) {
    if (!text || !numeric_key || !alphabet || !result) return -1;
    
    int pos = 0;
    size_t key_len = strlen(numeric_key);
    char* current_key = malloc(key_len + 1);
    if (!current_key) return -1;
    strcpy(current_key, numeric_key);
    
    for (size_t i = 0; text[i] && pos < result_size - 1; i++) {
        const char* char_pos = strchr(alphabet, text[i]);
        if (char_pos) {
            int char_index = char_pos - alphabet;
            int key_digit = current_key[i % key_len] - '0';
            
            int new_index = (char_index - key_digit + strlen(alphabet)) % strlen(alphabet);
            result[pos++] = alphabet[new_index];
            
            // Update key for next character
            memmove(current_key, current_key + 1, key_len - 1);
            current_key[key_len - 1] = '0' + new_index;
        } else {
            result[pos++] = text[i];
        }
    }
    result[pos] = '\0';
    
    free(current_key);
    return 0;
}

// Main VIC functions

int vic_encrypt(
    const char* plaintext,
    const char* polybius_key,
    const char* checkerboard_key,
    const char* transposition_key,
    const char* numeric_key,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size
) {
    if (!plaintext || !polybius_key || !checkerboard_key || !transposition_key || !numeric_key || !result) {
        return -1;
    }
    
    // Determine alphabet to use
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_VIC_ALPHABET;
        if (language && strcmp(language, "turkish") == 0) {
            use_alphabet = TURKISH_VIC_ALPHABET;
        }
    }
    
    // Step 1: Generate Polybius square
    char polybius_square[1024];
    if (vic_produce_polybius_square(square_type, polybius_key, use_alphabet, mono_params, language, polybius_square, sizeof(polybius_square)) != 0) {
        return -1;
    }
    
    // Step 2: Substitute to Polybius pairs
    char polybius_pairs[1024];
    if (substitute_to_polybius(plaintext, polybius_square, polybius_pairs, sizeof(polybius_pairs)) != 0) {
        return -1;
    }
    
    // Step 3: Convert pairs to digits
    char digits[1024];
    if (pairs_to_digits(polybius_pairs, digits, sizeof(digits)) != 0) {
        return -1;
    }
    
    // Step 4: Generate straddling checkerboard
    char checkerboard[1024];
    if (vic_produce_checkerboard(checkerboard_key, use_alphabet, language, checkerboard, sizeof(checkerboard)) != 0) {
        return -1;
    }
    
    // Step 5: Convert digits to letters using checkerboard
    char letters[1024];
    if (digits_to_letters(digits, checkerboard, letters, sizeof(letters)) != 0) {
        return -1;
    }
    
    // Step 6: Apply columnar transposition (multiple passes)
    char transposed[1024];
    strcpy(transposed, letters);
    for (int pass = 0; pass < transposition_passes; pass++) {
        char temp[1024];
        if (columnar_transposition(transposed, transposition_key, 1, temp, sizeof(temp)) != 0) {
            return -1;
        }
        strcpy(transposed, temp);
    }
    
    // Step 7: Apply numeric key addition
    if (use_chain_addition) {
        return chain_addition_encrypt(transposed, numeric_key, use_alphabet, result, result_size);
    } else {
        return numeric_addition(transposed, numeric_key, use_alphabet, 1, result, result_size);
    }
}

int vic_decrypt(
    const char* ciphertext,
    const char* polybius_key,
    const char* checkerboard_key,
    const char* transposition_key,
    const char* numeric_key,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size
) {
    if (!ciphertext || !polybius_key || !checkerboard_key || !transposition_key || !numeric_key || !result) {
        return -1;
    }
    
    // Determine alphabet to use
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_VIC_ALPHABET;
        if (language && strcmp(language, "turkish") == 0) {
            use_alphabet = TURKISH_VIC_ALPHABET;
        }
    }
    
    // Step 1: Reverse numeric key addition
    char letters[1024];
    if (use_chain_addition) {
        if (chain_addition_decrypt(ciphertext, numeric_key, use_alphabet, letters, sizeof(letters)) != 0) {
            return -1;
        }
    } else {
        if (numeric_addition(ciphertext, numeric_key, use_alphabet, 0, letters, sizeof(letters)) != 0) {
            return -1;
        }
    }
    
    // Step 2: Reverse columnar transposition (multiple passes)
    char transposed[1024];
    strcpy(transposed, letters);
    for (int pass = 0; pass < transposition_passes; pass++) {
        char temp[1024];
        if (columnar_transposition(transposed, transposition_key, 0, temp, sizeof(temp)) != 0) {
            return -1;
        }
        strcpy(transposed, temp);
    }
    
    // Step 3: Generate straddling checkerboard
    char checkerboard[1024];
    if (vic_produce_checkerboard(checkerboard_key, use_alphabet, language, checkerboard, sizeof(checkerboard)) != 0) {
        return -1;
    }
    
    // Step 4: Convert letters to digits using checkerboard
    char digits[1024];
    if (letters_to_digits(transposed, checkerboard, digits, sizeof(digits)) != 0) {
        return -1;
    }
    
    // Step 5: Convert digits to Polybius pairs
    char polybius_pairs[1024];
    if (digits_to_pairs(digits, polybius_pairs, sizeof(polybius_pairs)) != 0) {
        return -1;
    }
    
    // Step 6: Generate Polybius square
    char polybius_square[1024];
    if (vic_produce_polybius_square(square_type, polybius_key, use_alphabet, mono_params, language, polybius_square, sizeof(polybius_square)) != 0) {
        return -1;
    }
    
    // Step 7: Substitute from Polybius pairs
    return substitute_from_polybius(polybius_pairs, polybius_square, result, result_size);
}

int vic_produce_polybius_square(
    const char* square_type,
    const char* keyword,
    const char* alphabet,
    const char* mono_params,
    const char* language,
    char* result,
    size_t result_size
) {
    if (!square_type || !result || result_size == 0) return -1;
    
    // Determine alphabet to use
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_VIC_ALPHABET;
        if (language && strcmp(language, "turkish") == 0) {
            use_alphabet = TURKISH_VIC_ALPHABET;
        }
    }
    
    // Check if alphabet has enough characters (UTF-8 aware)
    size_t char_len = utf8_strlen(use_alphabet);
    if (char_len < 36) {
        return -1; // Not enough characters for 6x6 square
    }
    
    if (strcmp(square_type, "standard") == 0) {
        return create_standard_polybius_square(use_alphabet, result, result_size);
    } else if (strcmp(square_type, "caesar") == 0 || 
               strcmp(square_type, "atbash") == 0 || 
               strcmp(square_type, "affine") == 0) {
        // Use shared monoalphabetic square generation
        return create_monoalphabetic_square(square_type, use_alphabet, mono_params, result, result_size);
    } else if (strcmp(square_type, "keyword") == 0) {
        return create_keyword_polybius_square(keyword ? keyword : "SECRET", use_alphabet, result, result_size);
    } else {
        // Unsupported square type
        return -1;
    }
}

int vic_produce_checkerboard(
    const char* keyword,
    const char* alphabet,
    const char* language,
    char* result,
    size_t result_size
) {
    if (!keyword || !result || result_size == 0) return -1;
    
    // Determine alphabet to use
    const char* use_alphabet = alphabet;
    if (!use_alphabet) {
        use_alphabet = DEFAULT_VIC_ALPHABET;
        if (language && strcmp(language, "turkish") == 0) {
            use_alphabet = TURKISH_VIC_ALPHABET;
        }
    }
    
    return create_straddling_checkerboard(keyword, use_alphabet, result, result_size);
}

int vic_generate_random_key(
    size_t length,
    char* result,
    size_t result_size
) {
    if (!result || result_size == 0 || length >= result_size) return -1;
    
    srand(time(NULL));
    
    for (size_t i = 0; i < length; i++) {
        result[i] = 'A' + (rand() % 26);
    }
    result[length] = '\0';
    
    return 0;
}

int vic_generate_random_numeric_key(
    size_t length,
    char* result,
    size_t result_size
) {
    if (!result || result_size == 0 || length >= result_size) return -1;
    
    srand(time(NULL));
    
    for (size_t i = 0; i < length; i++) {
        result[i] = '0' + (rand() % 10);
    }
    result[length] = '\0';
    
    return 0;
}

int vic_generate_keys_for_text(
    size_t polybius_key_length,
    size_t checkerboard_key_length,
    size_t transposition_key_length,
    size_t numeric_key_length,
    char* polybius_key,
    char* checkerboard_key,
    char* transposition_key,
    char* numeric_key,
    size_t key_size
) {
    if (!polybius_key || !checkerboard_key || !transposition_key || !numeric_key || key_size == 0) {
        return -1;
    }
    
    if (vic_generate_random_key(polybius_key_length, polybius_key, key_size) != 0 ||
        vic_generate_random_key(checkerboard_key_length, checkerboard_key, key_size) != 0 ||
        vic_generate_random_key(transposition_key_length, transposition_key, key_size) != 0 ||
        vic_generate_random_numeric_key(numeric_key_length, numeric_key, key_size) != 0) {
        return -1;
    }
    
    return 0;
}

int vic_encrypt_with_random_keys(
    const char* plaintext,
    const char* square_type,
    const char* alphabet,
    const char* language,
    const char* mono_params,
    int transposition_passes,
    int use_chain_addition,
    char* result,
    size_t result_size,
    char* generated_keys,
    size_t keys_size
) {
    if (!plaintext || !result || !generated_keys) return -1;
    
    char polybius_key[32];
    char checkerboard_key[32];
    char transposition_key[32];
    char numeric_key[32];
    
    if (vic_generate_keys_for_text(6, 6, 6, 6, polybius_key, checkerboard_key, transposition_key, numeric_key, sizeof(polybius_key)) != 0) {
        return -1;
    }
    
    if (vic_encrypt(plaintext, polybius_key, checkerboard_key, transposition_key, numeric_key, square_type, alphabet, language, mono_params, transposition_passes, use_chain_addition, result, result_size) != 0) {
        return -1;
    }
    
    // Format generated keys as JSON-like string
    snprintf(generated_keys, keys_size, 
        "{\"polybius_key\":\"%s\",\"checkerboard_key\":\"%s\",\"transposition_key\":\"%s\",\"numeric_key\":\"%s\"}",
        polybius_key, checkerboard_key, transposition_key, numeric_key);
    
    return 0;
}
