//
//  QueryProcessor.cpp
//  Query Processor
//
//  Created by Jiankai Dang on 3/20/13.
//  Copyright (c) 2013 NYU-Poly. All rights reserved.
//

#include "QueryProcessor.h"
#include <string>
#include <vector>

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
list_pointer* openList(string t)
{
    list_pointer* lp = nullptr;
    return lp;
}
//close the inverted list for term t
void closeList(list_pointer* lp)
{
    
}
//find the next posting in list lp and return its docID. Return value > MAXDID if none exists.
int decodeNext(list_pointer* lp)
{
    return 0;
}
//find the next posting in list lp with docID >= k and return its docID. Return value > MAXDID if none exists.
int nextGEQ(list_pointer* lp, int k)
{
    while (lp->did < k)
        lp->did = decodeNext(lp);
    return(lp->did);
}
//get the frequency of the current posting in list lp
int getFreq(list_pointer* lp)
{
    return 0;
}
//document-at-a-time query processing
//vector of query string. We implement conjunctive queries.
void DAAT(vector<string> q)
{
    size_t num = q.size();
    vector<list_pointer*> lp;
    vector<int> f;
    for (int i = 0; i < num; i++) lp[i] = openList(q[i]);
    int did = 0;
    int maxdocID = 0;
    while (did <= maxdocID)
    {
        /* get next post from shortest list */
        did = nextGEQ(lp[0], did);
        int d;
        /* see if you find entries with same docID in other lists */
        for (int i=1; (i<num) && ((d=nextGEQ(lp[i], did)) == did); i++);
        if (d > did) did = d; /* not in intersection */
        else
        {
            /* docID is in intersection; now get all frequencies */
            for (int i=0; i<num; i++) f[i] = getFreq(lp[i]);
            /* compute BM25 score from frequencies and other data */
            //computeScore(p, numterm);
            did++; /* and increase did to search for next post */
        } 
    } 
    for (int i = 0; i < num; i++) closeList(lp[i]);
}