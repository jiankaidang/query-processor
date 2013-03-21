import os,hashlib,heapq
import string
import gzip
import gc
import sys
from datetime import datetime

def sort(w,hashlist):
    """
    sort: for each intermediate posting file, the items sorted by <word docId postion> returned
    """
    listdir = os.listdir(w)
    length = len(listdir)
    for i in range(length):
        #bug in python garbage collector!
        #appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        
        try:
            f = open(w + '/' + listdir[i], 'r')
        except:
            print "can not open posting."
        termList = []
        for line in f:
            word = line.split()
            if len(word) == 3:
                term = word[0]
                if term.isdigit():
                    continue
                #print term
                if stopwords(term,hashlist):
                    continue
            
                docId = int(word[2])
                position = int(word[1])          
           
                termList.append((term,docId,position))
            
        f.close()
        
        dir = 'sorted/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        filetowrite = open(dir + str(i),"wb")
        for f in sorted(set(termList)):
            filetowrite.write(f[0] + ' ' + str(f[1]) + ' ' + str(f[2]) + '\n')
        filetowrite.close()


##def base62encode(number):
##    if not isinstance(number, (int, long)):
##        raise TypeError('number must be an integer')
##    if number < 0:
##        raise ValueError('number must be positive')
##    
##    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
##    re
##    base62 = ''
##    while number:
##        number, i = divmod(number, 62)
##        base62 = alphabet[i] + base62
##
##    return base62 or alphabet[0]
##
##def base62decode(str):
##    return int(str,62)


def decode7bit(bytes):
    bytes = list(bytes)
    value = 0
    shift = 0
    while True:
        byteval = ord(bytes.pop(0))
        if(byteval & 128) == 0: break
        value |= ((byteval & 0x7F) << shift)
        shift += 7
    return (value | (byteval << shift))


def encode7bit(value):
    temp = value
    bytes = ""
    while temp >= 128:
        bytes += chr(0x000000FF & (temp | 0x80))
        temp >>= 7
    bytes += chr(temp)
    return bytes

   
 
def createIndex(input_path, output_path, lexicon):
    """
    createIndex: build index structure  dict(term) = [ [doc_1, [p1, p2]], [doc_2, [p1]], [doc_3, [p1]] ]
    """
    termDoc = {}
    
    f = open(input_path, 'r')
    
    for line in f:
        if line[0] <= 'z' and line[0] >= 'a':
            key_ = line.split()[0] + ' ' + line.split()[1]
        
            value_ = line.split()[2]
            if termDoc.has_key(key_):
                termDoc[key_].append(int(value_))
            else:
                termDoc[key_] = [int(value_)]
    
    f.close()
    
    term = {}
    for record in termDoc:
    
        occ = len(termDoc[record])
        key_ = record.split()[0]        
        value_ = int(record.split()[1])
        
        if term.has_key(key_):            
            term[key_].append([value_,occ])
            i = term[key_].pop(0)
            term[key_].insert(0,i + 1)
        else:
            term[key_] = [1,[value_,occ]]
            
    
##    x = encode7bit(1000)
##    print x
##    print decode7bit(x)    
    f = gzip.open(output_path,'wb')
    for k in term.keys():
        start = f.tell()
##        for t in term[k]:
##            print t
##        print term[k][1:]
        str_ = ''
        doc_freq_list = term[k][1:]
        base = 0
        for i in sorted(doc_freq_list, key = lambda x: x[0]):            
            str_ = str_ + str(i[0] - base) + ' ' + str(i[1]) + ' '
            base = i[0]
        f.write(str_)
        end = f.tell()
        length = end - start
        term[k].insert(1,start)
        term[k].insert(2,length)    
    f.close()

    f = open(lexicon,'wb')
    for k in sorted(term):
        f.write(str(k) + ' ' + str(term[k][0]) + ' ' + str(term[k][1]) + ' ' + str(term[k][2]) + '\n')
    f.close()
    
    

def stopwords(w,hashlist):
    """
    stopwords: not index the word in stopwords list
    """    
    if hashlist.count(w) > 0:
        return 1
    else:
        return 0

    
def qsort1(list):
    """
    Quicksort using list comprehensions
    >>> qsort1<<docstring test numeric input>>
    <<docstring test numeric output>>
    >>> qsort1<<docstring test string input>>
    <<docstring test string output>>
    """
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = qsort1([x for x in list[1:] if x < pivot])
        greater = qsort1([x for x in list[1:] if x >= pivot])
        return lesser + [pivot] + greater
    
def decorated_file(f, key):
    """ Yields an easily sortable tuple. 
    """
    for line in f:
        yield (key(line), line)

def standard_keyfunc(line):
    """ The standard key function in my application.
    """
    
    return line

def saveUrlTable(paths, output_path):
    """ merge the urltables and save to file
    """
    filelist = os.listdir(paths)
    filelist = [paths + '/' + x for x in filelist]
    files = map(open,filelist)
    
    f = open(output_path, 'wb')
    for tempfile in files:
        f.write(tempfile.read())

def mergeSortedFiles(paths, output_path, dedup=True, keyfunc=standard_keyfunc):
    """ merge multiple sorted files 
    """
    
    listdir = os.listdir(paths)
    
    listdir = ['sorted/' + x for x in listdir]
    files = map(open, listdir) #open defaults to mode='r'
    
    output_file = open(output_path, 'wb')
    lines_written = 0
    previous_comparable = ''
    for line in heapq.merge(*[decorated_file(f, keyfunc) for f in files]):
        comparable = line[0]
        if previous_comparable != comparable:
            output_file.write(line[1])
            lines_written += 1
        previous_comparable = comparable
    return lines_written
    

def init():
    
    str_dir = os.path.abspath('.')
    datafolder = raw_input("Please enter the data folder:")
    print "Data folder:",datafolder
    stoplist = []
    try:
        f = open(str_dir + '/' + 'stopwords.txt', 'r')
    except:
        print "can not open stopwords."

    for line in f:        
        stoplist.append(line.strip())
    print datetime.now()
    print "Sorting..."
    sort(str_dir + '/' + datafolder + '\posting',stoplist)
    print "Merging..."
    mergeSortedFiles(str_dir + '\sorted', 'merged')
    print "Create Index and Save Index..."
    createIndex('merged','index','lexicon')
    print "Save URL table..."
    saveUrlTable(str_dir + '/' + datafolder + '\url','urlTable')
    print datetime.now()

if __name__ == '__main__':
    init()
