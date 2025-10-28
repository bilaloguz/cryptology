#include "cryptology/classical/transposition/columnar/disrupted.h"
#include "cryptology/classical/transposition/columnar/single.h"

/**
 * Disrupted Columnar Transposition is essentially identical to
 * Single Columnar Transposition.
 */
int disrupted_columnar_encrypt(const char *plaintext, const char *keyword, 
                              char *output, size_t max_len) {
    return single_columnar_encrypt(plaintext, keyword, output, max_len);
}

int disrupted_columnar_decrypt(const char *ciphertext, const char *keyword, 
                               char *output, size_t max_len) {
    return single_columnar_decrypt(ciphertext, keyword, output, max_len);
}

