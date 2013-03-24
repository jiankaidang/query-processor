from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

def parse(query):
	try:
		return wordpunct_tokenize(query)
	except Exception:
		return query.split()