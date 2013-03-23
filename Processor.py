from heapq import heappush, heappop
from math import log
from getPageRank import getPageRank, 
from checkResult import check_result
#
#comand list:
#quit
#search
#glance
#open
#glanceall

################## Initialize Lexicon and Doc meta data part######################
class lexicon_node:
    def __init__(self):
        self.start = -1
        self.length = -1
        self.total = -1
        self.file_name = ""
#        self.number = -1

    def display(self):
        print self.file_name, str(self.total), str(self.start), str(self.length)

class doc_node:
    def __init__(self):
        self.url = -1
        self.id = -1
        self.total = -1
        self.pr = -1
        self.ar = -1
        # self.number = -1

    def display(self):
        print self.url, str(self.id), str(self.total), str(self.pr)


def build_lexicon(path):
    global lexicon_list
    global word_list
    global d_avg
    is_init = False
    l = 0
    for line in open(path):
        w = line.split()
        if len(w) == 1 and is_init == False:
            t = lexicon_node()
            l = int(w[0])
            for i in range(0, l):
                lexicon_list.append(t)
        elif len(w) == 6:
            id = int(w[1])
            word_list[w[0]] = id
            lexicon_list[id].start = w[4]
            lexicon_list[id].length = w[5]
            lexicon_list[id].total = w[3]
            lexicon_list[id].file_name = w[2]
            d_avg += float(w[5])
        else:
            continue
    d_avg /= float(l)
    return

def build_doc_meta_data(path):
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
# def open(query_word):
#     return
# def openList(term):
#     return
# def closeList(term):
#     return
# def nextGEQ(list_posting, k_docID):
#     return
# def getFreq(list_posting):
#     return

#DaaT functions end
################## Basic Search APIs ######################

################## Search APIs######################

def compute_BM25(terms, did, freq):
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
        fdt = float(f[i])
        res += log((n - ft + 0.5)/(ft + 0.5)) * (k1 + 1.0) * fdt / (K + fdt)
    return res

def compute_score(terms, did, freq):
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

def search_query(query):
    global max_doc_id
    global top
    res = []
    query = query.split()
    if len(query) == 0:
        return res
    ip = []
    d = []
    for q in query:
        ip = openList(word_list[q])
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
            d = nextGEQ(lp[i], did)
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
                f.append(getFreq(lp[i], did))

            # compute BM25 score from frequencies and other data
            temp = compute_score(query, did, f)
            if len(res_q) < top:
                heappush(res_q, (temp, did))
            else if res_q[0][0] < temp:
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


    # check duplicate and none-visitable result
    res = check_result(res)
    return res

################## Search APIs######################

################## Display APIs######################
# def display_result_glance():
#     """to do
#     """
#     return

# def display_result_open():
#     """to do
#     """
#     return

# def search_query(query):
#     """to do
#     """
#     return
################## Display APIs######################




while(True):
    input = raw_input(">")
    if(input == "quit"):
    	break
    if input == "search":
        query = raw_input("your query: ")
        result_set = search_query(query)
        print "There are " + str(len(result_set)) + " querries."
    elif input == "glance":
        number = int(raw_input("give me a doc number in result set"))
        if number >= len(result_set):
            print "error: out of result set number"
        else:
            display_result_glance(result_set[number])
    elif input == "glanceall":
        for i in range(0, min(top, len(result_set))):
            display_result_glance(result_set[i])
    elif input == "open":
        number = int(raw_input("give me a doc number in result set"))
        if number >= len(result_set):
            print "error: out of result set number"
        else:
            display_result_open(result_set[number])
    else:
        print "error: invalid command"