/**
 * @file hill.c
 * @brief Hill Cipher implementation
 */

#include "cryptology/classical/substitution/polygraphic/hill.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_TEXT_SIZE 1024
#define MAX_MATRIX_SIZE 10

static int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

static int mod_inverse(int a, int m) {
    a = a % m;
    for (int x = 1; x < m; x++) {
        if ((a * x) % m == 1) {
            return x;
        }
    }
    return -1; // No inverse exists
}

static int matrix_determinant(int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE], int n) {
    if (n == 1) {
        return matrix[0][0];
    }
    
    if (n == 2) {
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    }
    
    int det = 0;
    int temp[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
    
    for (int fc = 0; fc < n; fc++) {
        int sign = (fc % 2 == 0) ? 1 : -1;
        
        // Create submatrix
        for (int i = 1; i < n; i++) {
            int col = 0;
            for (int j = 0; j < n; j++) {
                if (j != fc) {
                    temp[i-1][col] = matrix[i][j];
                    col++;
                }
            }
        }
        
        det += sign * matrix[0][fc] * matrix_determinant(temp, n - 1);
    }
    
    return det;
}

static int matrix_inverse(int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE], 
                         int inverse[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE], int n) {
    int det = matrix_determinant(matrix, n);
    det = ((det % 26) + 26) % 26;
    
    if (det == 0) {
        return -1; // Matrix is singular
    }
    
    if (gcd(det, 26) != 1) {
        return -1; // Determinant is not coprime with 26
    }
    
    int det_inv = mod_inverse(det, 26);
    if (det_inv == -1) {
        return -1;
    }
    
    // Calculate adjugate matrix
    int adj[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int temp[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
            int sub_i = 0, sub_j = 0;
            
            // Create submatrix
            for (int row = 0; row < n; row++) {
                if (row != i) {
                    sub_j = 0;
                    for (int col = 0; col < n; col++) {
                        if (col != j) {
                            temp[sub_i][sub_j] = matrix[row][col];
                            sub_j++;
                        }
                    }
                    sub_i++;
                }
            }
            
            int cofactor = matrix_determinant(temp, n - 1);
            adj[j][i] = cofactor; // Transpose for adjugate
        }
    }
    
    // Calculate inverse
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            inverse[i][j] = ((adj[i][j] * det_inv) % 26 + 26) % 26;
        }
    }
    
    return 0;
}

static int prepare_text(const char *input, char *output, size_t output_size, int n) {
    if (!input || !output || output_size == 0) {
        return -1;
    }
    
    size_t input_len = strlen(input);
    size_t output_pos = 0;
    
    for (size_t i = 0; i < input_len && output_pos < output_size - 1; i++) {
        char c = tolower((unsigned char)input[i]);
        if (c >= 'A' && c <= 'Z') {
            output[output_pos++] = c;
        }
    }
    
    // Add X padding to make length divisible by n
    while (output_pos % n != 0) {
        if (output_pos < output_size - 1) {
            output[output_pos++] = 'X';
        } else {
            break;
        }
    }
    
    output[output_pos] = '\0';
    return 0;
}

static int char_to_num(char c) {
    return c - 'A';
}

static char num_to_char(int num) {
    return ((num % 26) + 26) % 26 + 'A';
}

static int encrypt_ngram(int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE], 
                        const char *ngram, char *result, int n) {
    int vector[MAX_MATRIX_SIZE];
    int result_vector[MAX_MATRIX_SIZE];
    
    // Convert characters to numbers
    for (int i = 0; i < n; i++) {
        vector[i] = char_to_num(ngram[i]);
    }
    
    // Matrix multiplication
    for (int i = 0; i < n; i++) {
        result_vector[i] = 0;
        for (int j = 0; j < n; j++) {
            result_vector[i] += matrix[i][j] * vector[j];
        }
        result_vector[i] = result_vector[i] % 26;
    }
    
    // Convert back to characters
    for (int i = 0; i < n; i++) {
        result[i] = num_to_char(result_vector[i]);
    }
    
    return 0;
}

static int decrypt_ngram(int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE], 
                        const char *ngram, char *result, int n) {
    int inverse[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
    
    if (matrix_inverse(matrix, inverse, n) != 0) {
        return -1;
    }
    
    int vector[MAX_MATRIX_SIZE];
    int result_vector[MAX_MATRIX_SIZE];
    
    // Convert characters to numbers
    for (int i = 0; i < n; i++) {
        vector[i] = char_to_num(ngram[i]);
    }
    
    // Matrix multiplication with inverse
    for (int i = 0; i < n; i++) {
        result_vector[i] = 0;
        for (int j = 0; j < n; j++) {
            result_vector[i] += inverse[i][j] * vector[j];
        }
        result_vector[i] = result_vector[i] % 26;
    }
    
    // Convert back to characters
    for (int i = 0; i < n; i++) {
        result[i] = num_to_char(result_vector[i]);
    }
    
    return 0;
}

int hill_encrypt(const char *plaintext, const int *key_matrix, int matrix_size,
                 char *result, size_t result_size) {
    if (!plaintext || !key_matrix || !result || result_size == 0 || matrix_size < 2) {
        return -1;
    }
    
    if (matrix_size > MAX_MATRIX_SIZE) {
        return -1;
    }
    
    int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
    
    // Convert 1D array to 2D matrix
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            matrix[i][j] = key_matrix[i * matrix_size + j];
        }
    }
    
    char prepared_text[MAX_TEXT_SIZE];
    if (prepare_text(plaintext, prepared_text, sizeof(prepared_text), matrix_size) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += matrix_size) {
        char ngram[MAX_MATRIX_SIZE + 1];
        char result_ngram[MAX_MATRIX_SIZE + 1];
        
        // Extract n-gram
        for (int j = 0; j < matrix_size; j++) {
            ngram[j] = prepared_text[i + j];
        }
        ngram[matrix_size] = '\0';
        
        if (encrypt_ngram(matrix, ngram, result_ngram, matrix_size) != 0) {
            return -1;
        }
        
        // Copy result
        for (int j = 0; j < matrix_size; j++) {
            result[i + j] = result_ngram[j];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}

int hill_decrypt(const char *ciphertext, const int *key_matrix, int matrix_size,
                 char *result, size_t result_size) {
    if (!ciphertext || !key_matrix || !result || result_size == 0 || matrix_size < 2) {
        return -1;
    }
    
    if (matrix_size > MAX_MATRIX_SIZE) {
        return -1;
    }
    
    int matrix[MAX_MATRIX_SIZE][MAX_MATRIX_SIZE];
    
    // Convert 1D array to 2D matrix
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            matrix[i][j] = key_matrix[i * matrix_size + j];
        }
    }
    
    char prepared_text[MAX_TEXT_SIZE];
    if (prepare_text(ciphertext, prepared_text, sizeof(prepared_text), matrix_size) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += matrix_size) {
        char ngram[MAX_MATRIX_SIZE + 1];
        char result_ngram[MAX_MATRIX_SIZE + 1];
        
        // Extract n-gram
        for (int j = 0; j < matrix_size; j++) {
            ngram[j] = prepared_text[i + j];
        }
        ngram[matrix_size] = '\0';
        
        if (decrypt_ngram(matrix, ngram, result_ngram, matrix_size) != 0) {
            return -1;
        }
        
        // Copy result
        for (int j = 0; j < matrix_size; j++) {
            result[i + j] = result_ngram[j];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}
