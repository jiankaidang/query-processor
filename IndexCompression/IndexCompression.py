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


data_set_dir = "/Users/charnugagoo/Documents/Workspace/InvertedIndexLargeDataSet/LargeDateset/"#"LargeDateset/"
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
    d_array_len = len(d_content_array)
    print d_array_len
    data_str = ""
    while index < d_array_len:
        print inverted_index_file + "-" + str(index)
        lexicon_node_obj = lexicon_map[inverted_index_file + "-" + str(index)]
        start_index = lexicon_node_obj.start
        chunk_content = ""
        chunks_data = ""
        meta_data = ""
        previous_chunk_did = 0
        for j in range(start_index, start_index + lexicon_node_obj.data_num):
            d_content = int(d_content_array[j])
            if j == start_index:
                d_list = d_content
            else:
                d_list = d_content - int(d_content_array[j - 1])
            chunk_content += encode7bit(int(d_list)) + encode7bit(int(f_content_array[j]))
            if (j - start_index + 1) % 128 == 0 or j == start_index + lexicon_node_obj.data_num - 1:
                chunk_did = d_content
                meta_data += encode7bit(chunk_did - previous_chunk_did) + encode7bit(len(chunk_content))
                previous_chunk_did = chunk_did
                chunks_data += chunk_content
                chunk_content = ""
        current_offset = len(data_str)
        print "current_offset:" + str(current_offset)
        lexicon_info.append([
            lexicon_node_obj.term,
            lexicon_node_obj.term_id,
            lexicon_node_obj.file_name,
            lexicon_node_obj.f_t,
            str(current_offset),
            str(lexicon_node_obj.data_num),
            str(len(meta_data))
        ])
        data_str += meta_data + chunks_data
        index += lexicon_node_obj.data_num
    inverted_index_list.write(data_str)
    inverted_index_list.close()
    inverted_index_data_file.close()
    inverted_index_f_file.close()
    doc_end = datetime.now()
    print "doc" + str(i) + "end time:" + str(doc_end)
    print "doc" + str(i) + "duration" + str(doc_end - doc_start)
lexicon = open(data_set_dir + "Lexicon_new", "wb")
lexicon_final = ""
for lexicon_data_content in lexicon_info:
    lexicon_final += " ".join(lexicon_data_content) + "\n"
lexicon.write(lexicon_final)
lexicon.close()
end = datetime.now()
print end
print end - start