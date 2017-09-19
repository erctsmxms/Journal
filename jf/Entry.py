import json
from datetime import datetime

from .config import config


class Entry():
	"""Loads entry json file, and presents a simple api to access and
	   save fields"""
	def __init__(self):
		d = datetime.now()
		self.datetime = {
			"year": d.year,
			"month": d.month,
			"day": d.day,
			"hour": d.hour,
			"minute": d.minute,
			"second": d.second,
		}
		self.tags = []
		self.title = ""
		self.text = ""
		self.__file_name = ""

	@classmethod
	def load(cls, file_name, directory=config.directory):
		"""Loads an entry json and returns an Entry object"""
		with open(f"{directory}/{file_name}", "r") as f:
			data = json.load(f)

		entry = cls()
		entry.datetime = data["datetime"]
		entry.tags = data["tags"]
		entry.title = data["title"]
		entry.text = data["text"]
		entry.__file_name = file_name

		return entry

	def save(self):
		data = {
			"datetime": self.datetime,
			"tags": self.tags,
			"title": self.title,
			"text": self.text
		}

		file_name = "{}/{}".format(config.directory, self.file_name)
		with open(file_name, "w") as f:
			json.dump(data, f, ensure_ascii=True)

	###########################################################################

	@property
	def file_name(self):
		"""Generates or loads the filename to be used when saving
		"""
		if not self.__file_name:
			date = self.str_date
			time = self.str_time.replace(":", "-")
			self.__file_name = "{} - {}.json".format(date, time)

		return self.__file_name

	@property
	def str_date(self):
		return "{year}-{month:0>2}-{day:0>2}".format(**self.datetime)

	@property
	def str_time(self):
		return "{hour:0>2}:{minute:0>2}:{second:0>2}".format(**self.datetime)

	@property
	def str_time_short(self):
		return "{hour:0>2}:{minute:0>2}".format(**self.datetime)

	def __str__(self):
		if self.title:
			return "{} - {} - {}".format(self.str_date, self.str_time, self.title)
		else:
			return "{} - {}".format(self.str_date, self.str_time)

	###########################################################################

	@staticmethod
	def sort_key(entry):
		"""To be used in sorted(list, key=Entry.sort_key)"""
		return "{}T{}-{}".format(entry.str_date, entry.str_time, entry.title)
