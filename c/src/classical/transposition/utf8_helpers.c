#include "cryptology/classical/transposition/utf8_helpers.h"
#include <string.h>
#include <ctype.h>

// Turkish lowercase letters: a-z, ş, ç, ğ, ö, ü, ı
// UTF-8 encoding for Turkish letters:
// ş = C5 9F (U+015F)
// ç = C3 A7 (U+00E7)
// ğ = C4 9F (U+011F)
// ö = C3 B6 (U+00F6)
// ü = C3 BC (U+00FC)
// ı = C4 B1 (U+0131)

// İ (capital dotted i) = C4 B0 (U+0130)
// lowercase: i = 69 (U+0069)

int utf8_is_letter(unsigned char byte, const unsigned char* bytes, int char_len) {
    // ASCII letters
    if (byte >= 'A' && byte <= 'Z') return 1;
    if (byte >= 'a' && byte <= 'z') return 1;

    // Turkish UTF-8 characters (2-byte UTF-8, starting with 0xC2-0xC6)
    if (char_len == 2 && bytes && bytes[0] >= 0xC0 && bytes[0] <= 0xDF) {
        unsigned char b1 = bytes[0];
        unsigned char b2 = bytes[1];

        // Turkish lowercase letters
        // ş (C5 9F), ç (C3 A7), ğ (C4 9F), ö (C3 B6), ü (C3 BC), ı (C4 B1)
        if (b1 == 0xC3 && (b2 == 0xA7 || b2 == 0xB6 || b2 == 0xBC)) return 1;  // ç, ö, ü
        if (b1 == 0xC4 && (b2 == 0x9F || b2 == 0xB1)) return 1;  // ğ, ı
        if (b1 == 0xC5 && b2 == 0x9F) return 1;  // ş
        if (b1 == 0xC4 && b2 == 0xB0) return 1;  // İ (capital dotted i)
    }

    return 0;
}

int utf8_to_lower(const unsigned char* bytes, int char_len, unsigned char* result, size_t result_size) {
    if (!bytes || !result || result_size < (size_t)char_len) return -1;

    // For ASCII uppercase, convert to lowercase
    if (char_len == 1 && bytes[0] >= 'A' && bytes[0] <= 'Z') {
        result[0] = bytes[0] - 'A' + 'a';
        return 1;
    }

    // For Turkish İ (capital dotted I), convert to i
    if (char_len == 2 && bytes[0] == 0xC4 && bytes[1] == 0xB0) {
        // İ -> i (ASCII lowercase i = 0x69)
        result[0] = 0x69;
        return 1;
    }

    // For all other characters, keep as is
    if (char_len <= (int)result_size) {
        memcpy(result, bytes, char_len);
        return char_len;
    }

    return -1;
}

int clean_utf8_text(const char* input, char* output, size_t output_size) {
    if (!input || !output || output_size == 0) return -1;

    const unsigned char* p = (const unsigned char*)input;
    size_t out_pos = 0;

    while (*p && out_pos < output_size - 1) {
        // Check if this is a UTF-8 character
        int char_len = 1;
        if ((*p & 0x80) == 0) {
            char_len = 1;
        } else if ((*p & 0xE0) == 0xC0) {
            char_len = 2;
        } else if ((*p & 0xF0) == 0xE0) {
            char_len = 3;
        } else if ((*p & 0xF8) == 0xF0) {
            char_len = 4;
        }

        // Check if this is a letter
        if (utf8_is_letter(*p, p, char_len)) {
            unsigned char lower[5];
            int result_len = utf8_to_lower(p, char_len, lower, 5);

            if (result_len > 0 && out_pos + result_len < output_size - 1) {
                memcpy(output + out_pos, lower, result_len);
                out_pos += result_len;
            }
        }

        p += char_len;
    }

    output[out_pos] = '\0';
    return 0;
}

