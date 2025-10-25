/**
 * @file polygraphic_example.c
 * @brief Example demonstrating polygraphic substitution ciphers
 */

#include <stdio.h>
#include <string.h>
#include "cryptology/classical/substitution/polygraphic/playfair.h"
#include "cryptology/classical/substitution/polygraphic/two_square.h"
#include "cryptology/classical/substitution/polygraphic/four_square.h"
#include "cryptology/classical/substitution/polygraphic/hill.h"

void demonstrate_playfair() {
    printf("=== Playfair Cipher ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "MONARCHY";
    char encrypted[1024];
    char decrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    
    if (playfair_encrypt(plaintext, key, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (playfair_decrypt(encrypted, key, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error decrypting\n");
        }
    } else {
        printf("Error encrypting\n");
    }
    printf("\n");
}

void demonstrate_two_square() {
    printf("=== Two Square Cipher ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key1 = "MONARCHY";
    const char *key2 = "PLAYFAIR";
    char encrypted[1024];
    char decrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key 1: %s\n", key1);
    printf("Key 2: %s\n", key2);
    
    if (two_square_encrypt(plaintext, key1, key2, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (two_square_decrypt(encrypted, key1, key2, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error decrypting\n");
        }
    } else {
        printf("Error encrypting\n");
    }
    printf("\n");
}

void demonstrate_four_square() {
    printf("=== Four Square Cipher ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key1 = "MONARCHY";
    const char *key2 = "PLAYFAIR";
    const char *key3 = "CIPHER";
    const char *key4 = "SECRET";
    char encrypted[1024];
    char decrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key 1: %s\n", key1);
    printf("Key 2: %s\n", key2);
    printf("Key 3: %s\n", key3);
    printf("Key 4: %s\n", key4);
    
    if (four_square_encrypt(plaintext, key1, key2, key3, key4, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (four_square_decrypt(encrypted, key1, key2, key3, key4, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error decrypting\n");
        }
    } else {
        printf("Error encrypting\n");
    }
    printf("\n");
}

void demonstrate_hill() {
    printf("=== Hill Cipher ===\n");
    
    const char *plaintext = "HELLO WORLD";
    int key_matrix[] = {3, 3, 2, 5}; // 2x2 matrix
    char encrypted[1024];
    char decrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key Matrix: [%d %d; %d %d]\n", key_matrix[0], key_matrix[1], key_matrix[2], key_matrix[3]);
    
    if (hill_encrypt(plaintext, key_matrix, 2, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (hill_decrypt(encrypted, key_matrix, 2, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error decrypting\n");
        }
    } else {
        printf("Error encrypting\n");
    }
    printf("\n");
}

void demonstrate_hill_3x3() {
    printf("=== Hill Cipher (3x3 Matrix) ===\n");
    
    const char *plaintext = "HELLO WORLD";
    int key_matrix[] = {1, 2, 3, 4, 5, 6, 7, 8, 10}; // 3x3 matrix
    char encrypted[1024];
    char decrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key Matrix: [%d %d %d; %d %d %d; %d %d %d]\n", 
           key_matrix[0], key_matrix[1], key_matrix[2],
           key_matrix[3], key_matrix[4], key_matrix[5],
           key_matrix[6], key_matrix[7], key_matrix[8]);
    
    if (hill_encrypt(plaintext, key_matrix, 3, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        if (hill_decrypt(encrypted, key_matrix, 3, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error decrypting\n");
        }
    } else {
        printf("Error encrypting\n");
    }
    printf("\n");
}

void demonstrate_security_comparison() {
    printf("=== Security Comparison ===\n");
    
    const char *plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    char playfair_encrypted[1024];
    char two_square_encrypted[1024];
    char four_square_encrypted[1024];
    char hill_encrypted[1024];
    
    printf("Plaintext: %s\n", plaintext);
    
    // Playfair
    if (playfair_encrypt(plaintext, "MONARCHY", playfair_encrypted, sizeof(playfair_encrypted)) == 0) {
        printf("Playfair:  %s\n", playfair_encrypted);
    }
    
    // Two Square
    if (two_square_encrypt(plaintext, "MONARCHY", "PLAYFAIR", two_square_encrypted, sizeof(two_square_encrypted)) == 0) {
        printf("Two Square: %s\n", two_square_encrypted);
    }
    
    // Four Square
    if (four_square_encrypt(plaintext, "MONARCHY", "PLAYFAIR", "CIPHER", "SECRET", 
                            four_square_encrypted, sizeof(four_square_encrypted)) == 0) {
        printf("Four Square: %s\n", four_square_encrypted);
    }
    
    // Hill
    int hill_matrix[] = {3, 3, 2, 5};
    if (hill_encrypt(plaintext, hill_matrix, 2, hill_encrypted, sizeof(hill_encrypted)) == 0) {
        printf("Hill:      %s\n", hill_encrypted);
    }
    
    printf("\n");
}

void demonstrate_error_handling() {
    printf("=== Error Handling ===\n");
    
    char result[1024];
    
    // Test invalid Playfair key
    if (playfair_encrypt("HELLO", "", result, sizeof(result)) == -1) {
        printf("✓ Correctly caught empty key error\n");
    }
    
    if (playfair_encrypt("HELLO", "123!@#", result, sizeof(result)) == -1) {
        printf("✓ Correctly caught non-letter key error\n");
    }
    
    // Test invalid Hill matrix
    int singular_matrix[] = {1, 2, 2, 4}; // Determinant = 0
    if (hill_encrypt("HELLO", singular_matrix, 2, result, sizeof(result)) == -1) {
        printf("✓ Correctly caught singular matrix error\n");
    }
    
    printf("\n");
}

int main() {
    printf("Polygraphic Substitution Ciphers Demo\n");
    printf("=====================================\n\n");
    
    demonstrate_playfair();
    demonstrate_two_square();
    demonstrate_four_square();
    demonstrate_hill();
    demonstrate_hill_3x3();
    demonstrate_security_comparison();
    demonstrate_error_handling();
    
    printf("Demo completed!\n");
    return 0;
}
