#include <stdio.h>
#include <string.h>
#include "cryptology/classical/transposition/simple/scytale.h"
#include "cryptology/classical/transposition/simple/rail_fence.h"

int main() {
    printf("============================================================\n");
    printf("CLASSICAL TRANSPOSITION CIPHERS - C IMPLEMENTATION\n");
    printf("============================================================\n");
    
    // Test Scytale cipher
    printf("\n============================================================\n");
    printf("SCYTALE CIPHER - Spartan Stick Cipher\n");
    printf("============================================================\n");
    
    const char *plaintext1 = "HELLO WORLD";
    int key1 = 3;
    char encrypted1[256];
    char decrypted1[256];
    
    printf("\nPlaintext:  %s\n", plaintext1);
    printf("Key:        %d\n", key1);
    
    if (scytale_encrypt(plaintext1, key1, encrypted1, sizeof(encrypted1)) == 0) {
        printf("Encrypted:  %s\n", encrypted1);
        
        if (scytale_decrypt(encrypted1, key1, decrypted1, sizeof(decrypted1)) == 0) {
            printf("Decrypted:  %s\n", decrypted1);
            printf("Success:    %s\n", strcmp(decrypted1, "helloworld") == 0 ? "True" : "False");
        }
    }
    
    // Test Rail Fence cipher
    printf("\n============================================================\n");
    printf("RAIL FENCE CIPHER\n");
    printf("============================================================\n");
    
    const char *plaintext2 = "HELLO WORLD";
    int rails2 = 3;
    char encrypted2[256];
    char decrypted2[256];
    char visualization[1024];
    
    printf("\nPlaintext:  %s\n", plaintext2);
    printf("Rails:      %d\n", rails2);
    
    if (rail_fence_encrypt(plaintext2, rails2, encrypted2, sizeof(encrypted2)) == 0) {
        printf("Encrypted:  %s\n", encrypted2);
        
        if (rail_fence_decrypt(encrypted2, rails2, decrypted2, sizeof(decrypted2)) == 0) {
            printf("Decrypted:  %s\n", decrypted2);
            printf("Success:    %s\n", strcmp(decrypted2, "helloworld") == 0 ? "True" : "False");
        }
        
        // Show visualization
        if (rail_fence_visualize(plaintext2, rails2, visualization, sizeof(visualization)) == 0) {
            printf("\nVisualization:\n%s\n", visualization);
        }
    }
    
    // Test with different parameters
    printf("\n============================================================\n");
    printf("ADDITIONAL TESTS\n");
    printf("============================================================\n");
    
    const char *plaintext3 = "CRYPTOGRAPHY";
    int key3 = 4;
    char encrypted3[256];
    char decrypted3[256];
    
    printf("\nPlaintext:  %s\n", plaintext3);
    printf("Key:        %d\n", key3);
    
    if (scytale_encrypt(plaintext3, key3, encrypted3, sizeof(encrypted3)) == 0) {
        printf("Encrypted:  %s\n", encrypted3);
        
        if (scytale_decrypt(encrypted3, key3, decrypted3, sizeof(decrypted3)) == 0) {
            printf("Decrypted:  %s\n", decrypted3);
            printf("Success:    %s\n", strcmp(decrypted3, "cryptography") == 0 ? "True" : "False");
        }
    }
    
    const char *plaintext4 = "ATTACK AT DAWN";
    int rails4 = 4;
    char encrypted4[256];
    char decrypted4[256];
    
    printf("\nPlaintext:  %s\n", plaintext4);
    printf("Rails:      %d\n", rails4);
    
    if (rail_fence_encrypt(plaintext4, rails4, encrypted4, sizeof(encrypted4)) == 0) {
        printf("Encrypted:  %s\n", encrypted4);
        
        if (rail_fence_decrypt(encrypted4, rails4, decrypted4, sizeof(decrypted4)) == 0) {
            printf("Decrypted:  %s\n", decrypted4);
            printf("Success:    %s\n", strcmp(decrypted4, "attackatdawn") == 0 ? "True" : "False");
        }
    }
    
    printf("\n============================================================\n");
    printf("C IMPLEMENTATION TESTS COMPLETE\n");
    printf("============================================================\n");
    
    return 0;
}
