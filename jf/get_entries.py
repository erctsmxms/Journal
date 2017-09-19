import os
import os.path

from .config import config
from .Entry import Entry


def get_entries():
	path = config.directory
	entries = []
	for item in os.listdir(path):
		entry = f"{path}/{item}"
		if os.path.isfile(entry):
			entries.append(Entry.load(item))

	return sorted(entries, key=Entry.sort_key)[::-1]
