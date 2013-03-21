import nltk
import os
import fnmatch
import time
import sys
import gzip
import string
import re

def index_directory(directory):
# parses out the pages provided in NZ dataset with the format of *data and *index files
# and returns [term, term position, urlID] tuples
		file_index=[]
		file_data=[]
		for file_name in os.listdir(directory+"/datset"):
                        # read *_index files
			if fnmatch.fnmatch(file_name, '*index'):
				file_index.append(file_name)
			# read *_data files
			else:
				file_data.append(file_name)
 
                 
		urlIndex = 0
		# strip punctuation from a string
		identify = string.maketrans('', '')     
                delEStr = string.punctuation 
		for  i in range(len(file_index)):
			f_data = gzip.open(directory+"/datset/"+file_data[i], 'rb')
			sizecounter=0
			for line in gzip.open(directory+"/datset/"+file_index[i],"rb").readlines():
				linkval=[]
				chunk=open("temp.txt","w")
				linkval=line.split(' ')
				# read a certain length of data in *_data files. the length is specified in fourth integer in each line of the index file
				chunk1=f_data.read(int(linkval[3]))
				chunk.write(chunk1)
				# find the start positon of the next page's data
				sizecounter=sizecounter+int(linkval[3])
				position = f_data.seek(sizecounter, 0);
				# information to write into the urltable: urlId, url, page length
				hyperlink="".join([str(urlIndex),' ',linkval[0],' ',linkval[3]])
                                # append writing to the urlTable files
				f = open(directory+"/output/url/u"+str(i),"a")
				f.write(hyperlink + '\n')
				f.close()
##				if linkval[6]=="ok":
##                                        print "yes"
##					index_file(hyperlink)
				# clean the page data and tokenize it
				raw = nltk.clean_html(chunk1).lower()
                                tokens = nltk.word_tokenize(raw)
                                tokenId = 0
                                # write into posting files
                                f = open(directory+"/output/posting/p"+str(i),"a")
                                for token in tokens:
                                    if len(token.translate(identify, delEStr)) > 1:
                                        f.write(token.translate(identify, delEStr) + ' ' + str(tokenId) + ' ' + str(urlIndex) + '\n')
                                        tokenId += 1
                                f.close()
                                urlIndex += 1
    
                                
                                
                                
				
 

def main(argv):
    crawl_directory=os.curdir
    if len(argv) > 1:
        crawl_directory = argv[1]
 
       # Indexing starts
    index_directory(crawl_directory)
 


 

if __name__ == "__main__":
    main(sys.argv)
