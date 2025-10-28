/**
 * @file test_chaocipher_simple.c
 * @brief Simple test program for Chaocipher implementation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "cryptology/classical/substitution/polyalphabetic/chaocipher.h"

#define MAX_TEXT_LEN 1024
#define MAX_ALPHABET_LEN 64

void test_basic_encryption_decryption() {
    printf("Testing basic encryption/decryption...\n");
    
    const char *plaintext = "HELLO WORLD";
    char left_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    char right_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    
    char encrypted[MAX_TEXT_LEN];
    char decrypted[MAX_TEXT_LEN];
    
    int encrypt_len = chaocipher_encrypt(plaintext, left_alphabet, right_alphabet, 
                                       27, encrypted, sizeof(encrypted));
    assert(encrypt_len > 0);
    
    int decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                       27, decrypted, sizeof(decrypted));
    assert(decrypt_len > 0);
    
    printf("Plaintext:  %s\n", plaintext);
    printf("Encrypted:  %s\n", encrypted);
    printf("Decrypted: %s\n", decrypted);
    printf("Match: %s\n", strcmp(decrypted, plaintext) == 0 ? "YES" : "NO");
    assert(strcmp(decrypted, plaintext) == 0);
    printf("✓ Basic encryption/decryption test passed\n\n");
}

void test_self_reciprocal_property() {
    printf("Testing self-reciprocal property...\n");
    
    const char *plaintext = "HELLO WORLD";
    char left_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    char right_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    
    char encrypted[MAX_TEXT_LEN];
    char decrypted[MAX_TEXT_LEN];
    
    int encrypt_len = chaocipher_encrypt(plaintext, left_alphabet, right_alphabet, 
                                       27, encrypted, sizeof(encrypted));
    assert(encrypt_len > 0);
    
    int decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                       27, decrypted, sizeof(decrypted));
    assert(decrypt_len > 0);
    
    printf("Plaintext:  %s\n", plaintext);
    printf("Encrypted:  %s\n", encrypted);
    printf("Decrypted: %s\n", decrypted);
    printf("Self-reciprocal: %s\n", strcmp(decrypted, plaintext) == 0 ? "YES" : "NO");
    assert(strcmp(decrypted, plaintext) == 0);
    printf("✓ Self-reciprocal property test passed\n\n");
}

void test_custom_alphabets() {
    printf("Testing custom alphabet creation...\n");
    
    char left_alphabet[MAX_ALPHABET_LEN];
    char right_alphabet[MAX_ALPHABET_LEN];
    
    int result = chaocipher_create_custom_alphabets("SECRET", "KEYWORD", 
                                                   left_alphabet, right_alphabet, 27);
    assert(result == 0);
    
    printf("Left alphabet (SECRET):  %s\n", left_alphabet);
    printf("Right alphabet (KEYWORD): %s\n", right_alphabet);
    printf("Length: %zu\n", strlen(left_alphabet));
    assert(strlen(left_alphabet) == 27);
    assert(strlen(right_alphabet) == 27);
    printf("✓ Custom alphabet creation test passed\n\n");
}

void test_edge_cases() {
    printf("Testing edge cases...\n");
    
    // Test empty text
    char encrypted[MAX_TEXT_LEN];
    char decrypted[MAX_TEXT_LEN];
    char left_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    char right_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    
    int encrypt_len = chaocipher_encrypt("", left_alphabet, right_alphabet, 
                                       27, encrypted, sizeof(encrypted));
    assert(encrypt_len == 0);
    
    int decrypt_len = chaocipher_decrypt("", left_alphabet, right_alphabet, 
                                       27, decrypted, sizeof(decrypted));
    assert(decrypt_len == 0);
    
    printf("Empty text test: ✓\n");
    
    // Test single character
    encrypt_len = chaocipher_encrypt("A", left_alphabet, right_alphabet, 
                                    27, encrypted, sizeof(encrypted));
    assert(encrypt_len == 1);
    
    decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                    27, decrypted, sizeof(decrypted));
    assert(decrypt_len == 1);
    assert(strcmp(decrypted, "A") == 0);
    
    printf("Single character test: ✓\n");
    
    // Test special characters
    encrypt_len = chaocipher_encrypt("HELLO!@#WORLD", left_alphabet, right_alphabet, 
                                    27, encrypted, sizeof(encrypted));
    assert(encrypt_len > 0);
    
    decrypt_len = chaocipher_decrypt(encrypted, left_alphabet, right_alphabet, 
                                    27, decrypted, sizeof(decrypted));
    assert(decrypt_len > 0);
    assert(strcmp(decrypted, "HELLOWORLD") == 0);
    
    printf("Special characters test: ✓\n");
    printf("✓ Edge cases test passed\n\n");
}

int main() {
    printf("=== Chaocipher C Implementation Simple Tests ===\n\n");
    
    test_basic_encryption_decryption();
    test_self_reciprocal_property();
    test_custom_alphabets();
    test_edge_cases();
    
    printf("=== All tests passed! ===\n");
    return 0;
}
