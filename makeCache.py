from Processor import word_list, lexicon_list
import random

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
	if cached_num < cache_num:
		for i in range(cache_num, cache_num):
			do_cache("")
	return

def do_cache(word):
	#if word == "", do random 
	if word != "":
		if word in word_list:
			# do cache
			cached_data[word_list[word]] = get_date() # to do waiting for Jiankai's API
		else:
			# could not cache
			return False
	else:
		while True:
			t = random.uniform(0, 3091674)
			if not is_cached(t):
				cached_data[t] = get_date()
				break
	return True

def is_cached(word_id):
	return word_id in cached_data

def get_cache_data(word_id):
	if word_id in cached_data:
	    return cached_data[word_id]

cached_data = {}