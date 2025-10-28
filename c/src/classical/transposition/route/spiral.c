#include "cryptology/classical/transposition/route/spiral.h"
#include "cryptology/classical/transposition/route/boustrophedon.h"

/**
 * Spiral Route currently uses Boustrophedon as a simplified implementation.
 */
int spiral_encrypt(const char *plaintext, char *output, size_t max_len) {
    return boustrophedon_encrypt(plaintext, output, max_len);
}

int spiral_decrypt(const char *ciphertext, char *output, size_t max_len) {
    return boustrophedon_decrypt(ciphertext, output, max_len);
}

