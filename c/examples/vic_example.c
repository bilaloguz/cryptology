#include <stdio.h>
#include <string.h>
#include "../include/cryptology/classical/substitution/composite/vic.h"

int main() {
    printf("=== VIC Cipher Example ===\n\n");
    
    const char* plaintext = "HELLO";
    const char* polybius_key = "SECRET";
    const char* checkerboard_key = "KEYWORD";
    const char* transposition_key = "CIPHER";
    const char* numeric_key = "123456";
    
    printf("Plaintext: %s\n", plaintext);
    printf("Polybius Key: %s\n", polybius_key);
    printf("Checkerboard Key: %s\n", checkerboard_key);
    printf("Transposition Key: %s\n", transposition_key);
    printf("Numeric Key: %s\n", numeric_key);
    printf("\n");
    
    // Test basic VIC encryption/decryption
    char encrypted[1024];
    char decrypted[1024];
    
    printf("1. Basic English VIC:\n");
    if (vic_encrypt(plaintext, polybius_key, checkerboard_key, transposition_key, numeric_key,
                   "keyword", NULL, "english", NULL, 1, 0, encrypted, sizeof(encrypted)) == 0) {
        printf("   Encrypted: %s\n", encrypted);
        
        if (vic_decrypt(encrypted, polybius_key, checkerboard_key, transposition_key, numeric_key,
                       "keyword", NULL, "english", NULL, 1, 0, decrypted, sizeof(decrypted)) == 0) {
            printf("   Decrypted: %s\n", decrypted);
            printf("   Success: %s\n", strcmp(decrypted, plaintext) == 0 ? "Yes" : "No");
        } else {
            printf("   Decryption failed\n");
        }
    } else {
        printf("   Encryption failed\n");
    }
    printf("\n");
    
    // Test different square types
    printf("2. Square Generation:\n");
    char square[1024];
    
    printf("   Standard Square:\n");
    if (vic_produce_polybius_square("standard", NULL, NULL, NULL, "english", square, sizeof(square)) == 0) {
        printf("     %s\n", square);
    } else {
        printf("     Failed to generate standard square\n");
    }
    
    printf("   Keyword Square:\n");
    if (vic_produce_polybius_square("keyword", "SECRET", NULL, NULL, "english", square, sizeof(square)) == 0) {
        printf("     %s\n", square);
    } else {
        printf("     Failed to generate keyword square\n");
    }
    
    printf("   Caesar Square:\n");
    if (vic_produce_polybius_square("caesar", NULL, NULL, "{\"shift\": 3}", "english", square, sizeof(square)) == 0) {
        printf("     %s\n", square);
    } else {
        printf("     Failed to generate caesar square\n");
    }
    printf("\n");
    
    // Test checkerboard generation
    printf("3. Checkerboard Generation:\n");
    char checkerboard[1024];
    if (vic_produce_checkerboard("KEYWORD", NULL, "english", checkerboard, sizeof(checkerboard)) == 0) {
        printf("   %s\n", checkerboard);
    } else {
        printf("   Failed to generate checkerboard\n");
    }
    printf("\n");
    
    // Test random key generation
    printf("4. Random Key Generation:\n");
    char random_keys[4][32];
    if (vic_generate_keys_for_text(6, 6, 6, 6, random_keys[0], random_keys[1], random_keys[2], random_keys[3], sizeof(random_keys[0])) == 0) {
        printf("   Generated keys:\n");
        printf("     Polybius: %s\n", random_keys[0]);
        printf("     Checkerboard: %s\n", random_keys[1]);
        printf("     Transposition: %s\n", random_keys[2]);
        printf("     Numeric: %s\n", random_keys[3]);
        
        char random_encrypted[1024];
        char random_decrypted[1024];
        if (vic_encrypt(plaintext, random_keys[0], random_keys[1], random_keys[2], random_keys[3],
                       "standard", NULL, "english", NULL, 1, 0, random_encrypted, sizeof(random_encrypted)) == 0) {
            printf("   Encrypted with generated keys: %s\n", random_encrypted);
            
            if (vic_decrypt(random_encrypted, random_keys[0], random_keys[1], random_keys[2], random_keys[3],
                           "standard", NULL, "english", NULL, 1, 0, random_decrypted, sizeof(random_decrypted)) == 0) {
                printf("   Decrypted: %s\n", random_decrypted);
                printf("   Success: %s\n", strcmp(random_decrypted, plaintext) == 0 ? "Yes" : "No");
            }
        }
    } else {
        printf("   Failed to generate random keys\n");
    }
    printf("\n");
    
    // Test Turkish alphabet
    printf("5. Turkish Alphabet:\n");
    const char* plaintext_tr = "MERHABA";
    char encrypted_tr[1024];
    char decrypted_tr[1024];
    
    if (vic_encrypt(plaintext_tr, polybius_key, checkerboard_key, transposition_key, numeric_key,
                   "keyword", NULL, "turkish", NULL, 1, 0, encrypted_tr, sizeof(encrypted_tr)) == 0) {
        printf("   Turkish encrypted: %s\n", encrypted_tr);
        
        if (vic_decrypt(encrypted_tr, polybius_key, checkerboard_key, transposition_key, numeric_key,
                       "keyword", NULL, "turkish", NULL, 1, 0, decrypted_tr, sizeof(decrypted_tr)) == 0) {
            printf("   Turkish decrypted: %s\n", decrypted_tr);
            printf("   Success: %s\n", strcmp(decrypted_tr, plaintext_tr) == 0 ? "Yes" : "No");
        } else {
            printf("   Turkish decryption failed\n");
        }
    } else {
        printf("   Turkish encryption failed\n");
    }
    printf("\n");
    
    // Test multiple transposition passes
    printf("6. Multiple Transposition Passes:\n");
    char multi_encrypted[1024];
    char multi_decrypted[1024];
    
    if (vic_encrypt(plaintext, polybius_key, checkerboard_key, transposition_key, numeric_key,
                   "keyword", NULL, "english", NULL, 3, 0, multi_encrypted, sizeof(multi_encrypted)) == 0) {
        printf("   Encrypted with 3 passes: %s\n", multi_encrypted);
        
        if (vic_decrypt(multi_encrypted, polybius_key, checkerboard_key, transposition_key, numeric_key,
                       "keyword", NULL, "english", NULL, 3, 0, multi_decrypted, sizeof(multi_decrypted)) == 0) {
            printf("   Decrypted: %s\n", multi_decrypted);
            printf("   Success: %s\n", strcmp(multi_decrypted, plaintext) == 0 ? "Yes" : "No");
        } else {
            printf("   Decryption failed\n");
        }
    } else {
        printf("   Encryption failed\n");
    }
    printf("\n");
    
    // Test chain addition
    printf("7. Chain Addition:\n");
    char chain_encrypted[1024];
    char chain_decrypted[1024];
    
    if (vic_encrypt(plaintext, polybius_key, checkerboard_key, transposition_key, numeric_key,
                   "keyword", NULL, "english", NULL, 1, 1, chain_encrypted, sizeof(chain_encrypted)) == 0) {
        printf("   Encrypted with chain addition: %s\n", chain_encrypted);
        
        if (vic_decrypt(chain_encrypted, polybius_key, checkerboard_key, transposition_key, numeric_key,
                       "keyword", NULL, "english", NULL, 1, 1, chain_decrypted, sizeof(chain_decrypted)) == 0) {
            printf("   Decrypted: %s\n", chain_decrypted);
            printf("   Success: %s\n", strcmp(chain_decrypted, plaintext) == 0 ? "Yes" : "No");
        } else {
            printf("   Decryption failed\n");
        }
    } else {
        printf("   Encryption failed\n");
    }
    printf("\n");
    
    printf("=== VIC Example Complete ===\n");
    
    return 0;
}
