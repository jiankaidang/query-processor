from Processor import word_list, lexicon_list

def make_decistion(cache_num = 200000, path = "EnglishWord"):
	cached_num = 0
	for line in open(path):
		line = line.split()
		if len(line) == 3:
			word = line[0]
			freq = int(line[1])
			if do_cache(word):
				cached_num += 1
			if cached_num == cache_num:
				break
		else:
			pass

	return

def do_cache(word):
	#if word == "", do random 
	if word != "":
		if word in word_list:
			# do cache

		else:
			# could not cache
			return false
	else:

	return true

def is_cached(word_id):
	
	return
def get_cache_data():
	return

cached_word_list = {}
cached_data = {}