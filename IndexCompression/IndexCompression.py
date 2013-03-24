from datetime import datetime
import gzip
import os
from encode import encode7bit

start = datetime.now()
print start


class lexicon_node:
    def __init__(self, term_id=-1, term="", file_name="", start=-1, data_num=-1, f_t=-1):
        self.start = start
        self.file_name = file_name
        self.term = term
        self.term_id = term_id
        self.f_t = f_t
        self.data_num = data_num


data_set_dir = "/Users/charnugagoo/Documents/Workspace/InvertedIndexLargeDataSet/LargeDateset/"
inverted_index_set_dir = data_set_dir + "InvertedIndex_large_set/"
gz_suffix = ".gz"
txt_suffix = ".txt"
inverted_index_dir = data_set_dir + "inverted_index_new"
if not os.path.exists(inverted_index_dir):
    os.mkdir(inverted_index_dir)
lexicon_file = open(data_set_dir + "LexiconMetaData_large_set.txt", "r")
lexicon_lines = lexicon_file.readlines()
lexicon_map = {}
for lexicon_line in lexicon_lines[1:]:
    print lexicon_line
    lexicon_data = lexicon_line.split()
    term = lexicon_data[0]
    term_id = lexicon_data[1]
    inverted_index_file = lexicon_data[2].split("/")[-1]
    f_t = lexicon_data[3]
    start_index = int(lexicon_data[4])
    data_num = int(lexicon_data[5])
    lexicon_node_obj = lexicon_node(term_id, term, inverted_index_file, start_index, data_num, f_t)
    lexicon_map[inverted_index_file + "-" + str(start_index)] = lexicon_node_obj
lexicon_file.close()
lexicon_info = []
for i in range(66):
    print "doc" + str(i)
    doc_start = datetime.now()
    print doc_start
    inverted_index_file = str(i)
    isGzipped = i < 41
    format_suffix = txt_suffix
    if isGzipped:
        format_suffix = gz_suffix
    data_file_suffix = "d" + format_suffix
    f_file_suffix = "f" + format_suffix
    if isGzipped:
        inverted_index_data_file = gzip.open(inverted_index_set_dir + inverted_index_file + data_file_suffix, "r")
        inverted_index_f_file = gzip.open(inverted_index_set_dir + inverted_index_file + f_file_suffix, "r")
    else:
        inverted_index_data_file = open(inverted_index_set_dir + inverted_index_file + data_file_suffix, "r")
        inverted_index_f_file = open(inverted_index_set_dir + inverted_index_file + f_file_suffix, "r")
    d_content_array = inverted_index_data_file.read().split()
    f_content_array = inverted_index_f_file.read().split()
    inverted_index_list = open(inverted_index_dir + "/" + inverted_index_file, "wb")
    index = 0
    line_num = 0
    d_array_len = len(d_content_array)
    print d_array_len
    while index < d_array_len:
        print inverted_index_file + "-" + str(index)
        lexicon_node_obj = lexicon_map[inverted_index_file + "-" + str(index)]
        lexicon_info.append(" ".join([
            lexicon_node_obj.term,
            lexicon_node_obj.term_id,
            lexicon_node_obj.file_name,
            lexicon_node_obj.f_t,
            str(line_num)
        ]) + "\n")
        start_index = lexicon_node_obj.start
        for i in range(start_index, start_index + lexicon_node_obj.data_num):
            d_content = d_content_array[i]
            if i == start_index:
                d_list = d_content
            else:
                d_list = int(d_content) - int(d_content_array[i - 1])
            inverted_index_list.write(encode7bit(int(d_list)) + " " + encode7bit(int(f_content_array[i])) + " ")
        inverted_index_list.write("\n")
        line_num += 1
        index += lexicon_node_obj.data_num
    inverted_index_list.close()
    inverted_index_data_file.close()
    inverted_index_f_file.close()
    doc_end = datetime.now()
    print "doc" + str(i) + "end time:" + str(doc_end)
    print "doc" + str(i) + "duration" + str(doc_end - doc_start)
lexicon = open("lexicon", "wb")
lexicon.write("".join(lexicon_info))
lexicon.close()
end = datetime.now()
print end
print end - start