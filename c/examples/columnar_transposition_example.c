#include <stdio.h>
#include <string.h>
#include "cryptology/classical/transposition/columnar/single.h"

int main() {
    printf("============================================================\n");
    printf("SINGLE COLUMNAR TRANSPOSITION CIPHER - C IMPLEMENTATION\n");
    printf("============================================================\n");
    
    const char *plaintexts[] = {
        "HELLO WORLD",
        "ATTACK AT DAWN",
        "THE QUICK BROWN FOX",
        "CRYPTOGRAPHY IS FUN",
        "SIMPLE COLUMNAR CIPHER"
    };
    
    const char *keywords[] = {
        "KEY",
        "CIPHER",
        "SECRET",
        "ALPHA",
        "TRANSPOSE"
    };
    
    char encrypted[512];
    char decrypted[512];
    
    for (int i = 0; i < 5; i++) {
        printf("\nTest %d:\n", i + 1);
        printf("Plaintext:  %s\n", plaintexts[i]);
        printf("Keyword:    %s\n", keywords[i]);
        
        // Clean plaintext for comparison
        char clean_plaintext[512] = {0};
        int pos = 0;
        for (int j = 0; plaintexts[i][j] != '\0' && pos < sizeof(clean_plaintext) - 1; j++) {
            if ((plaintexts[i][j] >= 'A' && plaintexts[i][j] <= 'Z') ||
                (plaintexts[i][j] >= 'a' && plaintexts[i][j] <= 'z')) {
                clean_plaintext[pos++] = (plaintexts[i][j] >= 'A' && plaintexts[i][j] <= 'Z') 
                    ? plaintexts[i][j] - 'A' + 'a' 
                    : plaintexts[i][j];
            }
        }
        
        if (single_columnar_encrypt(plaintexts[i], keywords[i], encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted:  %s\n", encrypted);
            
            if (single_columnar_decrypt(encrypted, keywords[i], decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
                
                int success = strcmp(decrypted, clean_plaintext) == 0;
                printf("Success:    %s\n", success ? "✓" : "✗");
            }
        }
    }
    
    printf("\n============================================================\n");
    printf("SINGLE COLUMNAR TRANSPOSITION TESTS COMPLETE\n");
    printf("============================================================\n");
    
    return 0;
}

