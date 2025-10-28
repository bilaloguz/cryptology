#include "cryptology/classical/transposition/route/knights_move.h"
#include "cryptology/classical/transposition/route/boustrophedon.h"

/**
 * Knight's Move currently uses Boustrophedon as a simplified implementation.
 */
int knights_move_encrypt(const char *plaintext, char *output, size_t max_len) {
    return boustrophedon_encrypt(plaintext, output, max_len);
}

int knights_move_decrypt(const char *ciphertext, char *output, size_t max_len) {
    return boustrophedon_decrypt(ciphertext, output, max_len);
}

