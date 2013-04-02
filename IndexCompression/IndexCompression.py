import gzip
import os
from encode import encode7bit

# start = datetime.now()
# print start


class lexicon_node:
    def __init__(self, term_id=-1, term="", file_name="", start=-1, data_num=-1, f_t=-1):
        # The start offset of the lexicon.
        self.start = start
        # The file name in which the inverted list of this term is stored.
        self.file_name = file_name
        self.term = term
        self.term_id = term_id
        # The total frequencies of this term.
        self.f_t = f_t
        # The number of documents in which this term occurs.
        self.data_num = data_num

# The directory of the data set.
data_set_dir = "/Users/charnugagoo/Documents/Workspace/InvertedIndexLargeDataSet/LargeDateset/"
# The directory of inverted index files.
inverted_index_set_dir = data_set_dir + "InvertedIndex_large_set/"
gz_suffix = ".gz"
txt_suffix = ".txt"
# The directory in which the new inverted index files will be saved.
inverted_index_dir = data_set_dir + "inverted_index_new"
if not os.path.exists(inverted_index_dir):
    os.mkdir(inverted_index_dir)
# Read the lexicon file.
lexicon_file = open(data_set_dir + "LexiconMetaData_large_set.txt", "r")
lexicon_lines = lexicon_file.readlines()
# The dictionary to store the lexicon information.
lexicon_map = {}
# Skip the first line.
for lexicon_line in lexicon_lines[1:]:
    # print lexicon_line
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
# The array to store the lexicon information.
lexicon_info = []
# There're 66 files in total.
for i in range(66):
    # print "doc" + str(i)
    # doc_start = datetime.now()
    # print doc_start
    inverted_index_file = str(i)
    # The first 40 files are gzipped.
    isGzipped = i < 41
    format_suffix = txt_suffix
    if isGzipped:
        format_suffix = gz_suffix
    data_file_suffix = "d" + format_suffix
    f_file_suffix = "f" + format_suffix
    if isGzipped:
        # Read the data file.
        inverted_index_data_file = gzip.open(inverted_index_set_dir + inverted_index_file + data_file_suffix, "r")
        # Read the frequency file.
        inverted_index_f_file = gzip.open(inverted_index_set_dir + inverted_index_file + f_file_suffix, "r")
    else:
        inverted_index_data_file = open(inverted_index_set_dir + inverted_index_file + data_file_suffix, "r")
        inverted_index_f_file = open(inverted_index_set_dir + inverted_index_file + f_file_suffix, "r")
        # The data contents in an array.
    d_content_array = inverted_index_data_file.read().split()
    # The frequency contents in an array.
    f_content_array = inverted_index_f_file.read().split()
    # Open new inverted index file to write.
    inverted_index_list = open(inverted_index_dir + "/" + inverted_index_file, "wb")
    # The offset of current file.
    index = 0
    d_array_len = len(d_content_array)
    # print d_array_len
    # The string to store the data information.
    data_str = ""
    while index < d_array_len:
        # print inverted_index_file + "-" + str(index)
        lexicon_node_obj = lexicon_map[inverted_index_file + "-" + str(index)]
        start_index = lexicon_node_obj.start
        # The content of one chunk.
        chunk_content = ""
        # The content of all the chunks for one term.
        chunks_data = ""
        # The meta data information for this term.
        meta_data = ""
        previous_chunk_did = 0
        for j in range(start_index, start_index + lexicon_node_obj.data_num):
            # Document id.
            d_content = int(d_content_array[j])
            if j == start_index:
                # For the first document id, store its actual value.
                d_list = d_content
            else:
                # For the documents after the first one, store the gap information.
                d_list = d_content - int(d_content_array[j - 1])
                # V-Byte compression of chunk content.
            chunk_content += encode7bit(int(d_list)) + encode7bit(int(f_content_array[j]))
            # Chunk-wise compression. 128 postings per chunk.
            if (j - start_index + 1) % 128 == 0 or j == start_index + lexicon_node_obj.data_num - 1:
                chunk_did = d_content
                # V-Byte compression of meta data.
                meta_data += encode7bit(chunk_did - previous_chunk_did) + encode7bit(len(chunk_content))
                previous_chunk_did = chunk_did
                chunks_data += chunk_content
                chunk_content = ""
        current_offset = inverted_index_list.tell()
        # print "current_offset:" + str(current_offset)
        index += lexicon_node_obj.data_num
        # Write the meta data information.
        inverted_index_list.write(meta_data)
        chunks_data_offset = inverted_index_list.tell() - current_offset
        # Write the information of the chunks.
        inverted_index_list.write(chunks_data)
        # Build lexicon information.
        lexicon_info.append([
            lexicon_node_obj.term,
            lexicon_node_obj.term_id,
            lexicon_node_obj.file_name,
            lexicon_node_obj.f_t,
            # The offset of this inverted list.
            str(current_offset),
            str(lexicon_node_obj.data_num),
            # The offset of the chunks data.
            str(chunks_data_offset),
            # The total length of the inverted list for this term.
            str(inverted_index_list.tell() - current_offset)
        ])
    inverted_index_list.close()
    inverted_index_data_file.close()
    inverted_index_f_file.close()
    # doc_end = datetime.now()
    # print "doc" + str(i) + "end time:" + str(doc_end)
    # print "doc" + str(i) + "duration" + str(doc_end - doc_start)
# Open to write the new lexicon file.
lexicon = open(data_set_dir + "Lexicon_new", "wb")
lexicon_final = ""
for lexicon_data_content in lexicon_info:
    lexicon_final += " ".join(lexicon_data_content) + "\n"
lexicon.write(lexicon_final)
lexicon.close()
# end = datetime.now()
# print end
# print end - start