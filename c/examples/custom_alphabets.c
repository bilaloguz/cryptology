/**
 * @file custom_alphabets.c
 * @brief Examples of using custom alphabets with various ciphers
 */

#include <stdio.h>
#include <string.h>
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/rot13.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"

#define BUFFER_SIZE 1024

int main() {
    char encrypted[BUFFER_SIZE];
    char decrypted[BUFFER_SIZE];
    
    printf("============================================================\n");
    printf("DIGITS ALPHABET\n");
    printf("============================================================\n");
    
    const char *alphabet_digits = "0123456789";
    const char *plaintext = "20231015";
    
    caesar_encrypt(plaintext, 3, alphabet_digits, encrypted, BUFFER_SIZE);
    printf("Original:   %s\n", plaintext);
    printf("Caesar(3):  %s\n", encrypted);
    
    atbash_encrypt(plaintext, alphabet_digits, encrypted, BUFFER_SIZE);
    printf("Atbash:     %s\n", encrypted);
    
    affine_encrypt(plaintext, 3, 7, alphabet_digits, encrypted, BUFFER_SIZE);
    printf("Affine(3,7): %s\n\n", encrypted);
    
    printf("============================================================\n");
    printf("HEXADECIMAL ALPHABET\n");
    printf("============================================================\n");
    
    const char *alphabet_hex = "0123456789abcdef";
    const char *hex_text = "deadbeef";
    
    caesar_encrypt(hex_text, 7, alphabet_hex, encrypted, BUFFER_SIZE);
    caesar_decrypt(encrypted, 7, alphabet_hex, decrypted, BUFFER_SIZE);
    
    printf("Original:  %s\n", hex_text);
    printf("Caesar(7): %s\n", encrypted);
    printf("Decrypted: %s\n\n", decrypted);
    
    printf("============================================================\n");
    printf("AFFINE CIPHER - Coprime Requirement\n");
    printf("============================================================\n");
    
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    const char *test_text = "test";
    
    printf("Alphabet length: 26\n");
    printf("Valid 'a' values (coprime with 26): 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25\n\n");
    
    int valid_a_values[] = {1, 3, 5, 7, 9};
    for (int i = 0; i < 5; i++) {
        int a = valid_a_values[i];
        if (affine_encrypt(test_text, a, 0, alphabet, encrypted, BUFFER_SIZE) == 0) {
            printf("a=%2d, b=0: %s -> %s\n", a, test_text, encrypted);
        }
    }
    
    printf("\nInvalid 'a' values (not coprime with 26):\n");
    int invalid_a_values[] = {2, 4, 6};
    for (int i = 0; i < 3; i++) {
        int a = invalid_a_values[i];
        if (affine_encrypt(test_text, a, 0, alphabet, encrypted, BUFFER_SIZE) != 0) {
            printf("a=%2d: ❌ Error - not coprime with 26\n", a);
        }
    }
    
    return 0;
}

