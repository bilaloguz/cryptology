/**
 * @file alphabet_utils.c
 * @brief Alphabet utilities implementation for polygraphic substitution ciphers
 */

#include "cryptology/classical/substitution/polygraphic/alphabet_utils.h"
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdbool.h>

#define MAX_ALPHABET_SIZE 256
#define MAX_LANGUAGE_SIZE 32

// Turkish letter frequency data (approximate)
static const char* turkish_frequent_letters = "aeirnldkysbzgcfhjpvmotu";

// English letter frequency data (approximate)
static const char* english_frequent_letters = "etaoinshrdlcumwfgypbvkjxqz";

const char* detect_language(const char *alphabet) {
    if (!alphabet) {
        return "unknown";
    }
    
    // Check for Turkish indicators
    if (strstr(alphabet, "ç") || strstr(alphabet, "ğ") || strstr(alphabet, "ı") || 
        strstr(alphabet, "ö") || strstr(alphabet, "ş") || strstr(alphabet, "ü") ||
        strstr(alphabet, "Ç") || strstr(alphabet, "Ğ") || strstr(alphabet, "İ") || 
        strstr(alphabet, "Ö") || strstr(alphabet, "Ş") || strstr(alphabet, "Ü")) {
        return "turkish";
    }
    
    // Check for English (26 letters, all basic Latin)
    if (strlen(alphabet) == 26) {
        bool is_english = true;
        for (int i = 0; alphabet[i] != '\0'; i++) {
            char c = tolower((unsigned char)alphabet[i]);
            if (c < 'a' || c > 'z') {
                is_english = false;
                break;
            }
        }
        if (is_english) {
            return "english";
        }
    }
    
    return "unknown";
}

int get_square_size(int alphabet_length) {
    if (alphabet_length <= 0) {
        return 5; // Default to 5x5
    }
    
    return (int)ceil(sqrt((double)alphabet_length));
}

static int apply_turkish_combinations(const char *alphabet, char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t len = strlen(alphabet);
    if (len >= result_size) {
        return -1;
    }
    
    strcpy(result, alphabet);
    
    // Apply Turkish combination rules
    char *pos;
    while ((pos = strstr(result, "ç")) != NULL) {
        *pos = 'c';
    }
    while ((pos = strstr(result, "ğ")) != NULL) {
        *pos = 'g';
    }
    while ((pos = strstr(result, "ı")) != NULL) {
        *pos = 'i';
    }
    while ((pos = strstr(result, "ö")) != NULL) {
        *pos = 'o';
    }
    while ((pos = strstr(result, "ş")) != NULL) {
        *pos = 's';
    }
    while ((pos = strstr(result, "ü")) != NULL) {
        *pos = 'u';
    }
    
    // Handle uppercase versions
    while ((pos = strstr(result, "Ç")) != NULL) {
        *pos = 'C';
    }
    while ((pos = strstr(result, "Ğ")) != NULL) {
        *pos = 'G';
    }
    while ((pos = strstr(result, "İ")) != NULL) {
        *pos = 'I';
    }
    while ((pos = strstr(result, "Ö")) != NULL) {
        *pos = 'O';
    }
    while ((pos = strstr(result, "Ş")) != NULL) {
        *pos = 'S';
    }
    while ((pos = strstr(result, "Ü")) != NULL) {
        *pos = 'U';
    }
    
    return 0;
}

static int remove_duplicates(const char *alphabet, char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    bool seen[256] = {false};
    size_t pos = 0;
    
    for (size_t i = 0; alphabet[i] != '\0' && pos < result_size - 1; i++) {
        unsigned char c = (unsigned char)alphabet[i];
        if (!seen[c]) {
            result[pos++] = alphabet[i];
            seen[c] = true;
        }
    }
    
    result[pos] = '\0';
    return 0;
}

static int select_by_frequency(const char *alphabet, const char *frequent_letters, 
                               int target_size, char *result, size_t result_size) {
    if (!alphabet || !frequent_letters || !result || result_size == 0) {
        return -1;
    }
    
    bool used[256] = {false};
    size_t pos = 0;
    
    // First, add letters from frequent_letters that exist in alphabet
    for (int i = 0; frequent_letters[i] != '\0' && pos < target_size && pos < result_size - 1; i++) {
        char c = frequent_letters[i];
        if (strchr(alphabet, c) && !used[(unsigned char)c]) {
            result[pos++] = c;
            used[(unsigned char)c] = true;
        }
    }
    
    // If we still need more letters, add remaining letters from alphabet
    for (size_t i = 0; alphabet[i] != '\0' && pos < target_size && pos < result_size - 1; i++) {
        char c = alphabet[i];
        if (!used[(unsigned char)c]) {
            result[pos++] = c;
            used[(unsigned char)c] = true;
        }
    }
    
    result[pos] = '\0';
    return 0;
}

int combine_similar_letters(const char *alphabet, const char *language,
                           char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    char temp[MAX_ALPHABET_SIZE];
    char deduplicated[MAX_ALPHABET_SIZE];
    
    // Detect language if auto
    const char *detected_language = language;
    if (strcmp(language, "auto") == 0) {
        detected_language = detect_language(alphabet);
    }
    
    // Apply language-specific combinations
    if (strcmp(detected_language, "turkish") == 0) {
        if (apply_turkish_combinations(alphabet, temp, sizeof(temp)) != 0) {
            return -1;
        }
    } else {
        // For English or unknown, just copy
        strncpy(temp, alphabet, sizeof(temp) - 1);
        temp[sizeof(temp) - 1] = '\0';
    }
    
    // Remove duplicates
    if (remove_duplicates(temp, deduplicated, sizeof(deduplicated)) != 0) {
        return -1;
    }
    
    // If still too long, use frequency-based selection
    int target_size = 25; // For 5x5 square
    if (strlen(deduplicated) > target_size) {
        const char *frequent_letters = NULL;
        if (strcmp(detected_language, "turkish") == 0) {
            frequent_letters = turkish_frequent_letters;
        } else {
            frequent_letters = english_frequent_letters;
        }
        
        if (select_by_frequency(deduplicated, frequent_letters, target_size, result, result_size) != 0) {
            return -1;
        }
    } else {
        strncpy(result, deduplicated, result_size - 1);
        result[result_size - 1] = '\0';
    }
    
    return 0;
}

int create_square_alphabet(const char *alphabet, int square_size,
                          char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0 || square_size <= 0) {
        return -1;
    }
    
    int target_length = square_size * square_size;
    size_t alphabet_len = strlen(alphabet);
    
    if (alphabet_len == target_length) {
        strncpy(result, alphabet, result_size - 1);
        result[result_size - 1] = '\0';
        return 0;
    } else if (alphabet_len < target_length) {
        // Pad with X if too short
        strncpy(result, alphabet, result_size - 1);
        result[result_size - 1] = '\0';
        
        size_t current_len = strlen(result);
        for (int i = current_len; i < target_length && i < result_size - 1; i++) {
            result[i] = 'X';
        }
        result[target_length] = '\0';
        return 0;
    } else {
        // Truncate if too long
        strncpy(result, alphabet, target_length);
        result[target_length] = '\0';
        return 0;
    }
}

int create_caesared_alphabet(const char *base_alphabet, int shift,
                            char *result, size_t result_size) {
    if (!base_alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t len = strlen(base_alphabet);
    if (len >= result_size) {
        return -1;
    }
    
    shift = shift % (int)len;
    if (shift < 0) {
        shift += len;
    }
    
    strcpy(result, base_alphabet + shift);
    strncat(result, base_alphabet, shift);
    result[result_size - 1] = '\0';
    
    return 0;
}

const char* get_letter_combination_rules(const char *language) {
    if (!language) {
        return NULL;
    }
    
    if (strcmp(language, "turkish") == 0) {
        return "ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u";
    } else if (strcmp(language, "english") == 0) {
        return "No combination rules needed";
    }
    
    return "Unknown language";
}
