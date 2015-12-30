import webnotes

def get_context():
	word_count = dict(webnotes.conn.sql("""select name, `count` from tabWord order by `count` desc limit 50"""))
	words = word_count.keys()
	words.sort()
	xmin = min(word_count.values())
	word_size = {}
	for word, count in word_count.iteritems():
		word_size[word] = int(float(count-xmin) / 40) + 12
	return {
		"words": words,
		"word_count": word_count,
		"word_size": word_size
	}