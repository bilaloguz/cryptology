/**
 * @file example.c
 * @brief Example usage of the cryptology library
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
    
    printf("==================================================\n");
    printf("CAESAR CIPHER - English\n");
    printf("==================================================\n");
    
    const char *plaintext1 = "Hello World";
    int shift = 3;
    
    caesar_encrypt(plaintext1, shift, NULL, encrypted, BUFFER_SIZE);
    caesar_decrypt(encrypted, shift, NULL, decrypted, BUFFER_SIZE);
    
    printf("Original:  %s\n", plaintext1);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n\n", decrypted);
    
    printf("==================================================\n");
    printf("ROT13 CIPHER - English\n");
    printf("==================================================\n");
    
    const char *message = "This is a Secret Message!";
    
    rot13_encrypt(message, NULL, encrypted, BUFFER_SIZE);
    rot13_decrypt(encrypted, NULL, decrypted, BUFFER_SIZE);
    
    printf("Original: %s\n", message);
    printf("Encoded:  %s\n", encrypted);
    printf("Decoded:  %s\n\n", decrypted);
    
    printf("==================================================\n");
    printf("ATBASH CIPHER - English\n");
    printf("==================================================\n");
    
    const char *atbash_text = "Hello World";
    
    atbash_encrypt(atbash_text, NULL, encrypted, BUFFER_SIZE);
    atbash_decrypt(encrypted, NULL, decrypted, BUFFER_SIZE);
    
    printf("Original:  %s\n", atbash_text);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n\n", decrypted);
    
    printf("==================================================\n");
    printf("KEYWORD CIPHER - English\n");
    printf("==================================================\n");
    
    const char *keyword_text = "Hello World";
    const char *key = "secret";
    
    keyword_encrypt(keyword_text, key, NULL, encrypted, BUFFER_SIZE);
    keyword_decrypt(encrypted, key, NULL, decrypted, BUFFER_SIZE);
    
    printf("Keyword:   %s\n", key);
    printf("Original:  %s\n", keyword_text);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n\n", decrypted);
    
    printf("==================================================\n");
    printf("AFFINE CIPHER - English\n");
    printf("==================================================\n");
    
    const char *affine_text = "Hello World";
    int a = 5, b = 8;
    
    affine_encrypt(affine_text, a, b, NULL, encrypted, BUFFER_SIZE);
    affine_decrypt(encrypted, a, b, NULL, decrypted, BUFFER_SIZE);
    
    printf("Keys: a=%d, b=%d\n", a, b);
    printf("Original:  %s\n", affine_text);
    printf("Encrypted: %s\n", encrypted);
    printf("Decrypted: %s\n\n", decrypted);
    
    printf("==================================================\n");
    printf("AFFINE - General Form Demonstration\n");
    printf("==================================================\n");
    
    const char *demo_text = "cryptology";
    
    printf("Original text: %s\n\n", demo_text);
    
    // Caesar is Affine with a=1
    caesar_encrypt(demo_text, 3, NULL, encrypted, BUFFER_SIZE);
    printf("Caesar (shift=3):  %s\n", encrypted);
    
    affine_encrypt(demo_text, 1, 3, NULL, encrypted, BUFFER_SIZE);
    printf("Affine (a=1, b=3): %s\n", encrypted);
    printf("(Same result - Caesar is Affine with a=1)\n\n");
    
    printf("Different affine keys produce different results:\n");
    affine_encrypt(demo_text, 5, 8, NULL, encrypted, BUFFER_SIZE);
    printf("Affine (a=5, b=8):  %s\n", encrypted);
    
    affine_encrypt(demo_text, 7, 3, NULL, encrypted, BUFFER_SIZE);
    printf("Affine (a=7, b=3):  %s\n", encrypted);
    
    affine_encrypt(demo_text, 11, 15, NULL, encrypted, BUFFER_SIZE);
    printf("Affine (a=11, b=15): %s\n", encrypted);
    
    return 0;
}

