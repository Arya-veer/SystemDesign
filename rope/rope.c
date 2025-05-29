
#include <stdlib.h>
#include <stdio.h>
#include "rope.h"
#include <string.h>
#include <stdbool.h>

bool is_rope(rope_t root)
{
    /*
    • NULL is a valid rope. It represents the empty string.
    • A rope is a leaf if it is non-NULL, has a non-empty string data field, has left and right
    fields that are both NULL, and has a strictly positive len equal to the length of the
    string in the data field (according to the C0 string library function string_length).
    • A rope is a non-leaf if it has non-NULL left and right fields, both of which are valid
    ropes, and if it has a len field equal to the sum of the len fields of its children. The
    data field of a non-leaf is unspecified. We'll call these non-leaves concatenation nodes.
    */
    if (root == NULL)
    {
        return true;
    }
    if (root->left == NULL && 
        root->right == NULL && 
        root->length == strlen(root->data))
    {
        return true;
    }
    if (root->left != NULL &&
        root->right != NULL &&
        root->length == (root->left->length + root->right->length) &&
        root->data == NULL)
    {
        return is_rope(root->left) && is_rope(root->right);
    }
    return false;
}

int rope_length(rope_t R)
{
    if (R == NULL)
    {
        return 0;
    }
    return R->length;
}

rope_t _rope_new_util(string s)
{
    int len = strlen(s);
    rope_t new_rope = malloc(sizeof(struct RopeNode));
    if (len <= MAX_NODE_LENGTH)
    {
        new_rope->data = s;
        new_rope->length = len;
        new_rope->left = NULL;
        new_rope->right = NULL;
    }
    else
    {
        int half = len / 2;
        new_rope->data = NULL;
        new_rope->length = len;
        new_rope->left = _rope_new_util(strndup(s, half));
        new_rope->right = _rope_new_util(s + half);
    }
    return new_rope;
}

rope_t rope_new(string s)
{
    if (s == NULL)
    {
        return NULL;
    }
    return _rope_new_util(s);
}

rope_t rope_join(rope_t R, rope_t S)
{
    if (R == NULL)
    {
        return S;
    }
    if (S == NULL)
    {
        return R;
    }
    rope_t new_rope = malloc(sizeof(struct RopeNode));
    new_rope->left = R;
    new_rope->right = S;
    new_rope->length = R->length + S->length;
    new_rope->data = NULL;
    return new_rope;
}

char rope_charat(rope_t R, int i)
{
    if (R == NULL)
    {
        return '\0';
    }
    if (R->left == NULL && R->right == NULL)
    {
        return R->data[i];
    }
    if (i < R->left->length)
    {
        return rope_charat(R->left, i);
    }
    return rope_charat(R->right, i - R->left->length);
}

void rope_print(rope_t R)
{
    if (R == NULL)
    {
        return;
    }
    if (R->left == NULL && R->right == NULL)
    {
        printf("%s", R->data);
        return;
    }
    rope_print(R->left);
    rope_print(R->right);
}

string rope_tostring(rope_t R)
{
    if (R == NULL)
    {
        return NULL;
    }
    if (R->left == NULL && R->right == NULL)
    {
        return R->data;
    }
    string left = rope_tostring(R->left);
    string right = rope_tostring(R->right);
    string new_string = malloc(R->length + 1);
    strcpy(new_string, left);
    strcat(new_string, right);
    return new_string;
}