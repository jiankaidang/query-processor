#
#comand list:
#quit
#search
#glance
#open
#glanceall

top = 10

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
        self.total
        self.pr = -1

    def display(self):
        print self.url, str(self.id), str(self.total), str(self.pr)


def build_lexicon(path):
    global lexicon_list
    global word_list
    is_init = False
    for line in open(path):
        w = line.split()
        if len(w) == 1 and is_init == False:
            t = lexicon_node()
            for i in range(0, int(w[0])):
                lexicon_list.append(t)
        elif len(w) == 6:
            id = int(w[1])
            word_list[w(0)] = id
            lexicon_node[id].start = w[4]
            lexicon_node[id].length = w[5]
            lexicon_node[id].total = w[3]
            lexicon_node[id].file_name = w[2]
        else:
            continue
    return

def build_doc_meta_data(path):
    global doc_list
    global doc_meta
    is_init = False
    for line in open(path):
        w = line.split()
        if len(w) == 1 and is_init == False:
            t = lexicon_node()
            for i in range(0, int(w[0])):
                doc_meta.append(t)
        elif len(w) == 4:
            id = int(w[0])
            doc_list[w[1]] = id
            doc_meta[id].url = w[1]
            doc_meta[id].total = w[2]
            doc_meta[id].pr = 3
        else:
            continue
    return

#DaaT functions begin
def open(query_word):
    return
def openList(term):
    return
def closeList(term):
    return
def nextGEQ(list_posting, k_docID):
    return
def getFreq(list_posting):
    return

#DaaT functions end



def display_result_glance():
    """to do
    """
    return

def display_result_open():
    """to do
    """
    return

def search_query(query):
    """to do
    """
    return



#main function
doc_list = {}
doc_meta = []
lexicon_list = []
word_list = {}

build_doc_meta_data()
build_lexicon()
result_set = []
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