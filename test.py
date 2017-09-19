import jf

search_string = "doajoisdjoqjwoieioqioweioqjiowejio"
results = jf.search(search_string, jf.get_entries())

for result in results:
	print("{:>02} {}".format(result[1], result[0].title))
