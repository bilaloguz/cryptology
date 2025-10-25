/**
 * @file fractionated_example.c
 * @brief Example demonstrating fractionated substitution ciphers
 * 
 * This example shows how Bifid and Trifid ciphers work with their fractionation
 * techniques, and how they can use custom alphabets for enhanced security.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Include fractionated cipher headers
#include "cryptology/classical/substitution/fractionated/bifid.h"
#include "cryptology/classical/substitution/fractionated/trifid.h"

// Include monoalphabetic cipher headers for composable system
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"

#define MAX_BUFFER_SIZE 1024
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define TURKISH_ALPHABET "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"

void demonstrate_bifid_cipher() {
    printf("=== Bifid Cipher Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "MONARCHY";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Encrypt
    if (bifid_encrypt(plaintext, key, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (bifid_decrypt(encrypted, key, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_trifid_cipher() {
    printf("=== Trifid Cipher Demo ===\n");
    
    const char *plaintext = "HELLO WORLD";
    const char *key = "MONARCHY";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Encrypt
    if (trifid_encrypt(plaintext, key, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (trifid_decrypt(encrypted, key, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_bifid_with_custom_alphabet() {
    printf("=== Bifid Cipher with Turkish Alphabet ===\n");
    
    const char *plaintext = "MERHABA DÜNYA";
    const char *key = "GİZLİ";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Turkish alphabet: %s\n", TURKISH_ALPHABET);
    printf("\n");
    
    // Encrypt
    if (bifid_encrypt_with_alphabet(plaintext, key, TURKISH_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (bifid_decrypt_with_alphabet(encrypted, key, TURKISH_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_trifid_with_custom_alphabet() {
    printf("=== Trifid Cipher with Turkish Alphabet ===\n");
    
    const char *plaintext = "MERHABA DÜNYA";
    const char *key = "GİZLİ";
    char encrypted[MAX_BUFFER_SIZE];
    char decrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Turkish alphabet: %s\n", TURKISH_ALPHABET);
    printf("\n");
    
    // Encrypt
    if (trifid_encrypt_with_alphabet(plaintext, key, TURKISH_ALPHABET, encrypted, sizeof(encrypted)) == 0) {
        printf("Encrypted: %s\n", encrypted);
        
        // Decrypt
        if (trifid_decrypt_with_alphabet(encrypted, key, TURKISH_ALPHABET, decrypted, sizeof(decrypted)) == 0) {
            printf("Decrypted: %s\n", decrypted);
        } else {
            printf("Error: Failed to decrypt\n");
        }
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_fractionation_technique() {
    printf("=== Fractionation Technique Explanation ===\n");
    
    const char *plaintext = "HELLO";
    const char *key = "MONARCHY";
    char encrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    printf("Step 1: Create 5x5 Polybius square\n");
    printf("M O N A R\n");
    printf("C H Y B D\n");
    printf("E F G I J\n");
    printf("K L P S T\n");
    printf("U V W X Z\n");
    printf("\n");
    
    printf("Step 2: Convert each letter to coordinates\n");
    printf("H -> (1,2), E -> (2,0), L -> (3,1), L -> (3,1), O -> (0,1)\n");
    printf("Rows: [1, 2, 3, 3, 0]\n");
    printf("Cols: [2, 0, 1, 1, 1]\n");
    printf("\n");
    
    printf("Step 3: Fractionation - write all rows, then all columns\n");
    printf("Fractionated: [1, 2, 3, 3, 0, 2, 0, 1, 1, 1]\n");
    printf("\n");
    
    printf("Step 4: Read pairs of coordinates to get new letters\n");
    printf("(1,2) -> H, (3,0) -> K, (0,1) -> O, (1,1) -> H\n");
    printf("\n");
    
    // Actual encryption
    if (bifid_encrypt(plaintext, key, encrypted, sizeof(encrypted)) == 0) {
        printf("Actual result: %s\n", encrypted);
    } else {
        printf("Error: Failed to encrypt\n");
    }
    printf("\n");
}

void demonstrate_security_benefits() {
    printf("=== Security Benefits of Fractionated Ciphers ===\n");
    
    const char *plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    const char *key = "SECRET";
    char bifid_encrypted[MAX_BUFFER_SIZE];
    char trifid_encrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("\n");
    
    // Bifid encryption
    if (bifid_encrypt(plaintext, key, bifid_encrypted, sizeof(bifid_encrypted)) == 0) {
        printf("Bifid encrypted: %s\n", bifid_encrypted);
    } else {
        printf("Error: Failed to encrypt with Bifid\n");
    }
    
    // Trifid encryption
    if (trifid_encrypt(plaintext, key, trifid_encrypted, sizeof(trifid_encrypted)) == 0) {
        printf("Trifid encrypted: %s\n", trifid_encrypted);
    } else {
        printf("Error: Failed to encrypt with Trifid\n");
    }
    printf("\n");
    
    printf("Security Benefits:\n");
    printf("1. Fractionation breaks letter frequency patterns\n");
    printf("2. Each letter affects multiple positions in ciphertext\n");
    printf("3. Trifid provides 3D fractionation (even more secure)\n");
    printf("4. Custom alphabets add another layer of security\n");
    printf("5. Resistant to frequency analysis attacks\n");
    printf("\n");
}

void demonstrate_composable_system() {
    printf("=== Composable System: Monoalphabetic + Fractionated ===\n");
    
    const char *plaintext = "COMPOSABLE CIPHER SYSTEM";
    const char *key = "FRACTIONATED";
    char caesar_alphabet[MAX_BUFFER_SIZE];
    char keyword_alphabet[MAX_BUFFER_SIZE];
    char bifid_encrypted[MAX_BUFFER_SIZE];
    char trifid_encrypted[MAX_BUFFER_SIZE];
    
    printf("Plaintext: %s\n", plaintext);
    printf("Fractionated key: %s\n", key);
    printf("\n");
    
    // Layer 1: Caesar-produced alphabet
    if (caesar_produce_alphabet(5, DEFAULT_ALPHABET, caesar_alphabet, sizeof(caesar_alphabet)) == 0) {
        printf("Caesar-produced alphabet: %s\n", caesar_alphabet);
        
        // Layer 2: Use Caesar alphabet with Bifid
        if (bifid_encrypt_with_alphabet(plaintext, key, caesar_alphabet, bifid_encrypted, sizeof(bifid_encrypted)) == 0) {
            printf("Bifid with Caesar alphabet: %s\n", bifid_encrypted);
        } else {
            printf("Error: Failed to encrypt with Bifid\n");
        }
        
        // Layer 3: Keyword-produced alphabet
        if (keyword_produce_alphabet("SECRET", caesar_alphabet, keyword_alphabet, sizeof(keyword_alphabet)) == 0) {
            printf("Keyword-produced alphabet: %s\n", keyword_alphabet);
            
            // Layer 4: Use keyword alphabet with Trifid
            if (trifid_encrypt_with_alphabet(plaintext, key, keyword_alphabet, trifid_encrypted, sizeof(trifid_encrypted)) == 0) {
                printf("Trifid with keyword alphabet: %s\n", trifid_encrypted);
            } else {
                printf("Error: Failed to encrypt with Trifid\n");
            }
        } else {
            printf("Error: Failed to produce keyword alphabet\n");
        }
    } else {
        printf("Error: Failed to produce Caesar alphabet\n");
    }
    printf("\n");
    
    printf("Multi-layer encryption provides:\n");
    printf("1. Caesar shift adds basic substitution\n");
    printf("2. Keyword rearrangement adds complexity\n");
    printf("3. Bifid fractionation breaks patterns\n");
    printf("4. Trifid 3D fractionation adds maximum security\n");
    printf("\n");
}

int main() {
    printf("Fractionated Substitution Ciphers Demo\n");
    printf("=====================================\n\n");
    
    demonstrate_bifid_cipher();
    demonstrate_trifid_cipher();
    demonstrate_bifid_with_custom_alphabet();
    demonstrate_trifid_with_custom_alphabet();
    demonstrate_fractionation_technique();
    demonstrate_security_benefits();
    demonstrate_composable_system();
    
    printf("Demo completed!\n\n");
    printf("Key Features:\n");
    printf("1. Bifid: 2D fractionation with 5x5 square\n");
    printf("2. Trifid: 3D fractionation with 3x3x3 cube\n");
    printf("3. Custom alphabet support for any language\n");
    printf("4. Composable with monoalphabetic ciphers\n");
    printf("5. Enhanced security through fractionation\n");
    
    return 0;
}
