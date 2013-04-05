query-processor
===============

A program that uses the inverted index structure to answer queries typed in by a user.

About Programs: Files in details

a) Processor.py

Query Processor: index information loading, BM25 Score Computation, Ranking

b) IndexCompression/IndexCompression.py

Compress Inverted Index Files, using V-Byte and Chunk-wise Compression.

c) queryParser.py

query parser module

d) makeCache.py

cache module

e) checkResult.py

Check the result, if visit-able. Also give best sample content.

f) getPageRank.py

get PageRank and AlexaRank number by their APIs

g) EnglishWordFrequency.py

The English word frequency file

h) simHash.py

The similar hash function, the same as Assignment #1.


Search In Action: How to Run it

 Our program needs additional python packages, NLTK.

 In the folder of our program, type in the command line “python Processor.py”. The program would ask you to type in some commands.

 “quit” command: quit the program

 “search” command: type “search” and follow the instruction to type into your query (any format). Then the program would show you the result.

 “search-complex” command: the same as “search”. This time, program would show you a full result, with 140 chars sample content.
