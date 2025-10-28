#include <stdio.h>
#include <string.h>
#include "cryptology/classical/transposition/compound/rasterschluessel_44.h"

int main() {
    printf("============================================================\n");
    printf("RASTERSCHLÜSSEL 44 CIPHER - C IMPLEMENTATION\n");
    printf("============================================================\n");
    
    const char *plaintexts[] = {
        "HELLO",
        "HELLO WORLD",
        "CRYPTOGRAPHY",
        "ATTACK AT DAWN",
        "THE QUICK BROWN FOX"
    };
    
    const char *keyword = "SECRET";
    
    char encrypted[512];
    char decrypted[512];
    
    for (int i = 0; i < 5; i++) {
        printf("\nTest %d:\n", i + 1);
        printf("Plaintext:  %s\n", plaintexts[i]);
        printf("Keyword:    %s\n", keyword);
        
        if (rasterschluessel_44_encrypt(plaintexts[i], keyword, encrypted, sizeof(encrypted)) == 0) {
            printf("Encrypted:  %s\n", encrypted);
            
            if (rasterschluessel_44_decrypt(encrypted, keyword, decrypted, sizeof(decrypted)) == 0) {
                printf("Decrypted:  %s\n", decrypted);
                
                // Clean plaintext for comparison
                char clean_plaintext[512];
                int pos = 0;
                for (int j = 0; plaintexts[i][j] != '\0' && pos < sizeof(clean_plaintext) - 1; j++) {
                    if ((plaintexts[i][j] >= 'A' && plaintexts[i][j] <= 'Z') ||
                        (plaintexts[i][j] >= 'a' && plaintexts[i][j] <= 'z')) {
                        clean_plaintext[pos++] = (plaintexts[i][j] >= 'A' && plaintexts[i][j] <= 'Z') 
                            ? plaintexts[i][j] - 'A' + 'a' 
                            : plaintexts[i][j];
                    }
                }
                clean_plaintext[pos] = '\0';
                
                int success = strcmp(decrypted, clean_plaintext) == 0;
                printf("Success:    %s\n\n", success ? "✓" : "✗");
            }
        }
    }
    
    printf("============================================================\n");
    printf("RASTERSCHLÜSSEL 44 CIPHER TESTS COMPLETE\n");
    printf("============================================================\n");
    
    return 0;
}

