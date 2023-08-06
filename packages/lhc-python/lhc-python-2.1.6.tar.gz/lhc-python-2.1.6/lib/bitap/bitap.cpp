#include "bitap.h"

#include <stdlib.h>
#include <string.h>
#include <limits.h>


int bitap(const char *text, const char *pattern) {
    int m = strlen(pattern);
    unsigned long R;
    unsigned long pattern_mask[CHAR_MAX+1];
    int i;

    if (pattern[0] == '\0') return -1;
    if (m > 31) return -1; // Pattern too long

    /* Initialize the bit array R */
    R = ~1;

    /* Initialize the pattern bitmasks */
    for (i=0; i <= CHAR_MAX; ++i)
         pattern_mask[i] = ~0;
    for (i=0; i < m; ++i)
         pattern_mask[pattern[i]] &= ~(1UL << i);

    for (i=0; text[i] != '\0'; ++i) {
        /* Update the bit array */
        R |= pattern_mask[text[i]];
        R <<= 1;

        if (0 == (R & (1UL << m)))
            return i - m + 1;
    }

    return -1;
}

int fuzzy_bitap(const char *text, const char *pattern, int k) {
    int result = -1;
    int m = strlen(pattern);
    unsigned long *R;
    unsigned long pattern_mask[CHAR_MAX+1];
    int i, d;

    if (pattern[0] == '\0') return -1;
    if (m > 31) return -1; // Pattern too long

    /* Initialize the bit array R */
    R = new unsigned long[k+1];
    for (i=0; i <= k; ++i)
        R[i] = ~1;

    /* Initialize the pattern bitmasks */
    for (i=0; i <= CHAR_MAX; ++i)
        pattern_mask[i] = ~0;
    for (i=0; i < m; ++i)
        pattern_mask[pattern[i]] &= ~(1UL << i);

    for (i=0; text[i] != '\0'; ++i) {
        /* Update the bit arrays */
        unsigned long old_Rd1 = R[0];

        R[0] |= pattern_mask[text[i]];
        R[0] <<= 1;

        for (d=1; d <= k; ++d) {
            unsigned long tmp = R[d];
            /* Substitution is all we care about */
            R[d] = (old_Rd1 & (R[d] | pattern_mask[text[i]])) << 1;
            old_Rd1 = tmp;
        }

        if (0 == (R[k] & (1UL << m))) {
            result = i - m + 1;
            break;
        }
    }

    delete [] R;
    return result;
}
