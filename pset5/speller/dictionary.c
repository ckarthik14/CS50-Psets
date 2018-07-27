// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

#include "dictionary.h"

typedef struct node
{
    bool is_word;
    struct node* child[27];
}
node;

unsigned int dictionarySize;

node *rootDictionary;

node *getNode()
{
    node *temp = malloc(sizeof(node));
    temp -> is_word = false;

    for (int i = 0; i<27; i++)
    {
        temp -> child[i] = NULL;
    }

    return temp;
}

bool unloadUtil(node *root)
{
    for (int i = 0; i<27; i++)
    {
        if (root -> child[i] != NULL)
        {
            unloadUtil(root -> child[i]);
        }
    }

    free(root);

    return true;
}

bool insertWord(char *word)
{
    int i = 0;
    int pos;
    node *trav = rootDictionary;

    while (word[i])
    {
        if (word[i] == '\'')
        {
            pos = 26;
        }
        else
        {
            pos = tolower(word[i]) - 97;
        }

        if (trav -> child[pos] == NULL)
        {
            trav -> child[pos] = getNode();

            /*if (trav -> child[pos] == NULL)
            {
                return false;
            }*/
        }
        trav = trav -> child[pos];
        i++;
    }
    trav -> is_word = true;

    return true;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int i = 0;
    int pos;
    node *trav = rootDictionary;

    while (word[i] != 0)
    {
        if (word[i] == '\'')
        {
            pos = 26;
        }
        else
        {
            pos = tolower(word[i]) - 97;
        }

        if (trav -> child[pos] == NULL)
        {
            return false;
        }
        trav = trav -> child[pos];
        i++;
    }

    if (trav -> is_word == true)
    {
        return true;
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *dict = fopen (dictionary, "r");
    char word[46];

    rootDictionary = getNode();

    while (fscanf(dict, "%s", word) != EOF)
    {
        dictionarySize++;
        bool temp;
        temp = insertWord(word);

        /*if (!temp)
        {
            dictionarySize = 0;
            return temp;
        }*/
    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dictionarySize;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    bool temp = unloadUtil(rootDictionary);

    return temp;
}
