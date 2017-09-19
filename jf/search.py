import re

_nottitle = "-title"
_nottags = "-tags"
_nottext = "-text"


def search(search_string, entries):
	keywords = search_string.split(" ")

	# Should title or tag be skipped?
	search_title = True
	search_tags = True
	search_text = True

	if _nottitle in keywords:
		keywords.remove(_nottitle)
		search_title = False

	if _nottags in keywords:
		keywords.remove(_nottags)
		search_tags = False

	if _nottext in keywords:
		keywords.remove(_nottext)
		search_text = False

	searched_entries = []

	# Actual search
	for entry in entries:
		score = 0
		for keyword in keywords:
			# Appends + to each char
			key = "+".join([c for c in keyword.lower()]) + "+"

			# Text
			if search_text:
				match_text = re.findall(key, entry.text.lower())
				score += len(match_text)

			# Tags
			if search_tags:
				for tag in entry.tags:
					if re.match(key, tag.lower()):
						score += 2

			# Title
			if search_title:
				match_title = re.findall(key, entry.title.lower())
				score += len(match_title) * 3

		if score:
			searched_entries.append([entry, score])

	# Sort and return
	sorted_searched_entries = sorted(searched_entries, key=lambda l: l[1])
	return [l[0] for l in sorted_searched_entries][::-1]
