from Processor import word_list, lexicon_list, openList
import random

""" This file includes caching method
"""

def make_decision_and_do_cache(cache_num = 500000, path = "EnglishWordFrequency2.txt"):
#    This function selects terms to do cache
#    This function read a bag of words with frequency in common English. In decending order of this frequency, do cache.
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

def do_cache(word):
#    this function fo cache of selected word
#    if no word as input, do cache of a random word not cached
#    return true if cache successfully
#    return false if not
	#if word == "", do random 
	if word != "":
		if word in word_list:
			# do cache
			cached_data[word_list[word]] = openList(word_list[word]) # to do waiting for Jiankai's API
		else:
			# could not cache
			return False
	else:
		while True:
			t = random.uniform(0, 3091674)
			if not is_cached(t):
				cached_data[t] = openList(word_list[word])
				break
	return True

def is_cached(word_id):
#    check if the word with this word id is cached
	return word_id in cached_data

def get_cache_data(word_id):
#    given a word_id, return the cached data
	if word_id in cached_data:
	    return cached_data[word_id]

cached_data = {}