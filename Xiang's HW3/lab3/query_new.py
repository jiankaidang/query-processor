
""" Query interface to analyze the user's query condition and get the results. """

import string
import re
import gzip
import sys
import math
import heapq
import collections
from datetime import datetime



class SimpleQuery:
	""" Simple query class. """
	QueryOp = ['and','or']
	def __init__(self):
                """ Sets up the object & the data directory. """
                self.op = 'and'
		self.res = []
                self.docs_ = self.loadUrls('urlTable')
                self.lexicon_ = self.loadLexicon('lexicon')
                
                self.docNum = len(self.docs_)
                self.avgDocLen = sum(self.docs_[k][1] for k in self.docs_)/self.docNum
                self.termDoc_ = {}
                self.itemScore_ = {}

        def query_op(self, s, t):
		""" Opearte the query condition. """
		if self.op == 'and':
			return s & t
		elif self.op == 'or':
			return s | t
		else:
			pass

        def loadUrls(self, urlFile):
                """ Load the URL table."""
                urlList = {}
                try:
                        f = open(urlFile, 'r')
                        for rawline in f:
                                key_ = int(rawline.split()[0])
                                value_ = rawline.split()[1]
                                length_ = int(rawline.split()[2])
                                urlList[key_] = [value_,length_]
                        f.close()
                except:
                        print "Load urlTable Error."
                return urlList
                
        def loadLexicon(self, lexiconFile):
                """ Load the lexicon. """
                lexiconList = {}
                try:
                        f = open(lexiconFile, 'r')
                        for rawline in f:
                                key_ = rawline.split()[0]
                                
                                lexiconList[key_] = [rawline.split()[1], rawline.split()[2], rawline.split()[3]]
                        f.close()
                except:
                        print "Load lexicon Error."
                return lexiconList
                
	def query(self, q, op='and'):
		""" Query the condition and return the results. """
		sets = []
		words = q.split()
		print words
		for word in words:
                        resultlist = self.geturllist(word.lower())
                        if len(resultlist) == 0:
                                print "no search result."
                                return []
##                        s = set()                                          
##                        for item in resultlist:
##				s.add(item)
			sets.append(resultlist)
		res = sets[0]
		""" intersect the set retrieved by each term """
		for i in range(1,len(sets)):
			res = [val for val in res if val in set(sets[i])]
		if len(res) == 0:
                        print "no search result."
                        return []
		self.res = list(res)
		self.rank(res,words)
                
                        

        def rank(self, res, words):
##                for item in res:
##                        self.itemScore_[item] = self.bm25_relevance(words,item)
##                for nrank in heapq.nlargest(10, self.itemScore_.items(), key=lambda(k,v):(v,k)):
##                        print self.docs_[int(nrank[0])][0] + ' ' + str(nrank[1])
###
                """ compute the score for candidate URL get the top 10 URLs with highest scores"""
                for nrank in heapq.nlargest(10, res, key = lambda x: self.bm25_relevance(words,x)):
                        print self.docs_[int(nrank)][0] + ' ' + str(self.bm25_relevance(words,nrank))
                
        def bm25_relevance(self, terms, docItem, b=0.75, k=1.2):
                """
                Given multiple inputs, performs a BM25 relevance calculation for a
                given document.

                ``terms`` should be a list of terms.

                ``total_docs`` should be an integer of the total docs in the index.

                Optionally accepts a ``b`` parameter, which is an integer specifying
                the length of the document. Since it doesn't vastly affect the score,
                the default is ``0``.

                Optionally accepts a ``k`` parameter. It accepts a float & is used to
                modify scores to fall into a given range. With the default of ``1.2``,
                scores typically range from ``0.4`` to ``1.0``.
                """
                score = 0

                for term in terms:

                    idf = math.log((int(self.docNum) - int(self.lexicon_[term][0]) + 0.5) / (int(self.lexicon_[term][0]) + 0.5)) *(k + 1)*int(self.termDoc_[term,docItem])
                    score = score + idf / (k*((1 - b) + b*int(self.docs_[int(docItem)][1])/int(self.avgDocLen)) + int(self.termDoc_[term,docItem]))

                return score

        def geturllist(self, q):
                """ Get [urlID, frequency] list given a word, reading the inverted index file"""
                resultList = []
                if self.lexicon_.has_key(str(q)):
                        startPos = int(self.lexicon_[q][1])
                        length = int(self.lexicon_[q][2])
                        f = gzip.open('index','rb')
                        f.seek(startPos)
                        indexContent = f.read(length)
                        indexs = indexContent.split()
                        sets = []
                        base = 0
                        for i,k in zip(indexs[0::2], indexs[1::2]):
##                                self.termDoc_[q,int(decode7bit(i)) + base] = int(k)
##                                sets.append(int(decode7bit(i)) + base)
                                self.termDoc_[q,int(i) + base] = int(k)
                                sets.append(int(i) + base)
                                base = base + int(i)
                        return sets
                else:
                        return []
 
        def decode7bit(self,bytes):
            """ integer decode algorithm similar to variable byte"""
            bytes = list(bytes)
            value = 0
            shift = 0
            while True:
                byteval = ord(bytes.pop(0))
                if(byteval & 128) == 0: break
                value |= ((byteval & 0x7F) << shift)
                shift += 7
            return (value | (byteval << shift))


        def encode7bit(self,value):
            """ integer encode algorithm similar to variable byte coding"""
            temp = value
            bytes = ""
            while temp >= 128:
                bytes += chr(0x000000FF & (temp | 0x80))
                temp >>= 7
            bytes += chr(temp)
            return bytes

if __name__ == "__main__":
    query = SimpleQuery()
    print "Enter the Query:",
    quary = raw_input()    
    while quary != "quit":
        print datetime.now()
        query.query(quary)
        print datetime.now()
        print ""
        print ""
        print "Enter the Query:",
        quary = raw_input()
    
		
