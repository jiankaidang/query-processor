import zlib

data_set_dir = "LargeDateset/"
inverted_index_set_dir = data_set_dir + "InvertedIndex_large_set/"
gz_suffix = ".gz"
txt_suffix = ".txt"
data_file_suffix = "d"
f_file_suffix = "f"
lexicon_file = open(data_set_dir + "LexiconMetaData_large_set.txt", "r")
lexicon_lines = lexicon_file.readlines()
for lexicon_line in lexicon_lines[1:10]:
    lexicon_data = lexicon_line.split()
    term = lexicon_data[0]
    term_id = lexicon_data[1]
    inverted_index_file = lexicon_data[2].split("/")[-1]
    f_t = lexicon_data[3]
    start_index = lexicon_data[4]
    data_num = lexicon_data[5]
    isGzipped = inverted_index_file < 41
    if isGzipped:
        format_suffix = gz_suffix
    else:
        format_suffix = txt_suffix
    data_file_suffix += format_suffix
    f_file_suffix += format_suffix
    inverted_index_data_file = open(inverted_index_set_dir + inverted_index_file + data_file_suffix)
    inverted_index_f_file = open(inverted_index_set_dir + inverted_index_file + f_file_suffix)
    if isGzipped:
        inverted_index_data_file = zlib.decompress(inverted_index_data_file)
        inverted_index_f_file = zlib.decompress(inverted_index_f_file)

    inverted_index_data_file.close()
    inverted_index_f_file.close()
lexicon_file.close()