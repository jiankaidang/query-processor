from getPageRank import getPageRank, getAlexaRank
path = "/Users/charnugagoo/Documents/Workspace/InvertedIndexLargeDataSet/LargeDateset/"
file = open(path + "DocMetaData_large_set_with_pageRank_new.txt", 'w')
cnt = 0
for line in open(path + "DocMetaData_large_set_with_pageRank.txt"):
    print cnt
    cnt += 1
    w = line.split()
    if len(w) == 1:
        file.write(w[0] + "\n")
    elif len(w) == 4:
        file.write(w[0] + " ")
        file.write(w[1] + " ")
        file.write(w[2] + " ")
        pr = float(getPageRank(w[1]))
        ar = float(getAlexaRank(w[1]))
        file.write(str(pr) + " ")
        file.write(str(ar) + "\n")
    else:
        file.write(line + "\n")
file.close()