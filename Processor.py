from heapq import heappush, heappop
from math import log
import random
from encode import decode7bit
from getPageRank import getPageRank, getAlexaRank
from checkResult import check_result
from queryParser import parse

#
#comand list:
#quit
#search
#glance
#open
#glanceall

################## Initialize Lexicon and Doc meta data part######################
class lexicon_node:
#    lexicon class
    def __init__(self):
        self.start = -1 # line number in lexicon file
        self.total = -1
        self.did = -1
        self.length = -1
        #        self.number = -1

    def display(self):
        print self.file_name, str(self.total), str(self.start), str(self.length)

class doc_node:
#    doc meta class
    def __init__(self):
        self.url = -1
        self.id = -1
        self.total = -1
        self.pr = -1
        self.ar = -1
        # self.number = -1

    def display(self):
        print self.url, str(self.id), str(self.total), str(self.pr)

# hard code here
lexicon_file_line_number = 3091675

def build_lexicon(path):
#    read in lexicon file into memory
    global lexicon_list
    global word_list
    global d_avg
    is_init = False
    for i in range(0, lexicon_file_line_number):
        lexicon_list.append(lexicon_node())
    for line in open(path):
        w = line.split()
        if len(w) == 7:
            id = int(w[1])
            word_list[w[0]] = id
            lexicon_list[id].start = w[4]
            lexicon_list[id].total = w[3]
            lexicon_list[id].did = w[2]
            lexicon_list[id].length = w[6]
            d_avg += float(w[5])
        else:
            continue
    d_avg /= float(lexicon_file_line_number)
    return

def build_doc_meta_data(path):
#    read in doc meta data file into memory
    global doc_list
    global doc_meta
    is_init = False
    for line in open(path):
        w = line.split()
        if len(w) == 1 and is_init == False:
            t = doc_node()
            for i in range(0, int(w[0])):
                doc_meta.append(t)
        elif len(w) == 4:
            id = int(w[0])
            doc_list[w[1]] = id
            doc_meta[id].url = w[1]
            doc_meta[id].total = w[2]
            doc_meta[id].pr = float(getPageRank(w[1]))
            doc_meta[id].ar = float(getAlexaRank(w[1]))
        else:
            continue
    return

# basic variables initialization here
top = 10
d_avg = 0.0
#main function
doc_list = {}
doc_meta = []
lexicon_list = []
word_list = {}

pwd = "/Users/charnugagoo/Documents/Workspace/InvertedIndexLargeDataSet/LargeDateset/"
build_doc_meta_data(pwd + "DocMetaData_large_set.txt")
build_lexicon(pwd + "LexiconMetaData_large_set.txt")
result_set = []
max_doc_id = len(doc_list)
################## Initialize Lexicon and Doc meta data part######################

################## Basic Search APIs ######################

#DaaT functions begin

def openList(term, getCache = False):

    if getCache:
        if is_cached(term):
            return get_cache_data(term)

    print term
    lexicon_node_obj = lexicon_list[term]
    print lexicon_node_obj.did
    print lexicon_node_obj.start
    print lexicon_node_obj.total
    list_posting = {
        "current_posting_index": 0,
        "postings": []
    }
    list_file = open("IndexCompression/LargeDateset/inverted_index_new/" + str(lexicon_node_obj.did), "rb")
    list_file.seek(int(lexicon_node_obj.start))
    list_data_str = list_file.read(int(lexicon_node_obj.length))
    print "lexicon_node_obj.start:" + str(lexicon_node_obj.start)
    print "lexicon_node_obj.len:" + str(lexicon_node_obj.length)
    list_data = decode7bit(list_data_str)
    list_file.close()
    print "len(list_data):---" + str(len(list_data))
    for i in range(0, len(list_data), 2):
        if i != 0:
            list_data[i] = list_data[i - 2] + list_data[i]
        list_posting["postings"].append({
            "did": list_data[i],
            "freq": list_data[i + 1]
        })
    return list_posting
def closeList(term):
    return
def nextGEQ(list_posting, k_docID):
    current_posting_index = list_posting["current_posting_index"]
    if list_posting["postings"][current_posting_index]["did"] == k_docID:
        return k_docID
    current_posting_index += 1
    if current_posting_index >= len(list_posting["postings"]):
        return max_doc_id
    list_posting["current_posting_index"] = current_posting_index
    return list_posting["postings"][current_posting_index]["did"]
def getFreq(list_posting):
    return list_posting["postings"][list_posting["current_posting_index"]]["freq"]

#DaaT functions end
################## Basic Search APIs ######################

################## Search APIs######################

def compute_BM25(terms, did, freq):
#    function to calculate BM25 score
    global max_doc_id
    global d_avg
    res = 0.0
    if did < 0 or did >= max_doc_id or len(terms) == 0 or len(freq) == 0:
        return -1.0
    if len(terms) != len(freq):
        print "error: len(terms) != len(freq)\n"
    n = float(len(terms))
    d = float(doc_meta[did].length)
    k1 = 1.2
    b = 0.75
    K = k1*(1 - b + b * d / d_avg)
    for i in range(0, len(terms)):
        ft = float(   lexicon_list[word_list[terms[i]]].total )
        fdt = float(freq[i])
        res += log((n - ft + 0.5)/(ft + 0.5)) * (k1 + 1.0) * fdt / (K + fdt)
    return res

def compute_score(terms, did, freq):
#    compute score based on BM25,
    BM25 = compute_BM25(terms, did, freq)
    k1 = 1.0
    PageRank = doc_meta[did].pr
    AlexRank = doc_meta[did].ar
    res = BM25
    if PageRank < 0:
        res *= k1*1.0
    else:
        res *= k1*PageRank
    if AlexRank < 0:
        res *= 1.0
    else:
        res *= (1.0 + 1.0/AlexRank)
    return res

def search_query(query, complex = False):
    global max_doc_id
    global top
    res = []
    # query = query.split()
    query = parse(query)
    if len(query) == 0:
        return res
    ip = []
    d = []
    for q in query:
        ip.append(openList(word_list[q]))
    if len(ip) == 0:
        return res

    res_q = [] # heap of #top results
    num = len(ip)
    did = 0

    while(did < max_doc_id):
        # get next post from shortest list
        did = nextGEQ(ip[0], did)

        # see if you find entries with same docID in other lists
        # for (i=1; (i<num) && ((d=nextGEQ(lp[i], did)) == did); i++);
        d = -1
        for i in range(1, num):
            d = nextGEQ(ip[i], did)
            if d != did:
                break
                # not in intersection
        if d > did:
            did = d
        else:
            # docID is in intersection; now get all frequencies
            # for (i=0; i<num; i++)  f[i] = getFreq(lp[i], did);
            f = []
            for i in range(0, num):
                f.append(getFreq(ip[i]))

            # compute BM25 score from frequencies and other data
            temp = compute_score(query, did, f)
            if len(res_q) < top:
                heappush(res_q, (temp, did))
            elif res_q[0][0] < temp:
                heappop(res_q)
                heappush(res_q, (temp, did))
                # to do top10, using priority queue

            # and increase did to search for next post
            did = did+1

    for i in range(0, num):
        closeList(ip[i])
    for i in reversed(range(0, len(res_q))):
        url = doc_meta[ res_q[i][0] ].url
        res.append(  (res_q[i][0], url, res_q[i][1])  )

    display_simple_result(res)
    if complex:
        res = display_complex_result(res, query)

    return res

################## Search APIs######################

################## Display APIs######################

def display_simple_result(result_set):
    print "There are " + str(len(result_set)) + " querries.\n Simple Result:\n"
    for i in range(0, len(result_set)):
        print "Result #" + str(i)
        r = result_set[i]
        print r[0], r[1], r[2]
        print result_set[i][1]
    return

def display_complex_result(result_set, query):
    print "There are " + str(len(result_set)) + " querries.\n Complex Result:\n"
    # check duplicate and none-visitable result
    result_set = check_result(query, result_set)
    for i in range(0, len(result_set)):
        print "Result #" + str(i)
        r = result_set[i][0]
        print r[0], r[1], r[2]
        print result_set[i][1]
    return result_set
################## Display APIs######################


################## Cache APIs######################

def make_decision_and_do_cache(cache_num = 500000, path = "EnglishWordFrequency2.txt"):
#    This function selects terms to do cache
#    This function read a bag of words with frequency in common English. In decending order of this frequency, do cache.
    cached_num = 0
    for line in open(path):
        line = line.split()
        if len(line) == 3:
            word = line[0]
            freq = int(line[1])
            if do_cache(word):
                cached_num += 1
            if cached_num == cache_num:
                break
        else:
            pass
    if cached_num < cache_num:
        for i in range(cache_num, cache_num):
            do_cache("")

def do_cache(word):
#    this function fo cache of selected word
#    if no word as input, do cache of a random word not cached
#    return true if cache successfully
#    return false if not
    #if word == "", do random
    if word != "":
        if word in word_list:
            # do cache
            cached_data[word_list[word]] = openList(word_list[word]) # to do waiting for Jiankai's API
        else:
            # could not cache
            return False
    else:
        while True:
            t = random.uniform(0, 3091674)
            if not is_cached(t):
                cached_data[t] = openList(word_list[word])
                break
    return True

def is_cached(word_id):
#    check if the word with this word id is cached
    return word_id in cached_data

def get_cache_data(word_id):
#    given a word_id, return the cached data
    if word_id in cached_data:
        return cached_data[word_id]

cached_data = {}
################## Cache APIs######################


################## Main Function######################
make_decision_and_do_cache()
while(True):
    input = raw_input("> input query: search, search-complex or quit\n")
    if(input == "quit"):
        break
    if input == "search":
        query = raw_input("your query: ")
        result_set = search_query(query)
    elif input == "search-complex":
        query = raw_input("your query: ")
        result_set = search_query(query, True)
    else:
        print "error: invalid command"
        ################## Main Function######################