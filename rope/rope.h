#include <string.h>
#include <stdbool.h>

#define MAX_NODE_LENGTH 16

typedef char *string;
typedef struct RopeNode *rope_t;

enum NodeType
{
    LEAF,
    INTERNAL,
    ROOT
};

struct RopeNode
{
    string data;
    int length;
    rope_t left;
    rope_t right;
};

bool is_rope(rope_t root); // Check if a rope is a valid rope

int rope_length(rope_t R); // Get the length of a rope

rope_t rope_join(rope_t R, rope_t S); // Concatenate two ropes

char rope_charat(rope_t R, int i); // Get the character at index i

rope_t rope_new(string s); // Create a new rope from a string

string rope_tostring(rope_t R); // Convert a rope to a string

void rope_print(rope_t R); // Print a rope