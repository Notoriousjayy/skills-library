#include <stddef.h>
size_t capacity_for(size_t count) {
    return count * 32;  /* may wrap before allocation */
}
