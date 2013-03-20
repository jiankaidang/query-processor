//
//  QueryProcessor.cpp
//  Query Processor
//
//  Created by Jiankai Dang on 3/20/13.
//  Copyright (c) 2013 NYU-Poly. All rights reserved.
//

#include "QueryProcessor.h"
#include <string>
using namespace std;
struct list_pointer {
    //the number of docs containing word t.
    int f_t;
    //the docID of “current” posting in the list
    int did;
    //- information about the list
    //pointers to the “current” posting in the list
    //- info about whether the current chunk has already been uncompressed
};
//open the inverted list for term t for reading
list_pointer openList(string t)
{
    list_pointer lp;
    return lp;
}
//close the inverted list for term t
void closeList(list_pointer lp)
{
    
}
//find the next posting in list lp with docID >= k and return its docID. Return value > MAXDID if none exists.
int nextGEQ(list_pointer lp, int k)
{
    return 0;
}
//get the frequency of the current posting in list lp
int getFreq(list_pointer lp)
{
    return 0;
}