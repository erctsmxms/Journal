import tkinter as tk
import tkinter.ttk
import tkinter.font
import tkinter.messagebox

import jf


class Journalentry_tk(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self, None)
		#self.parent = parent
		self.entry = jf.Entry()
		self.initialize()

	def initialize(self):
		self.var_date_label = tk.StringVar()
		time = "{} {}".format(self.entry.str_date, self.entry.str_time_short)
		self.var_date_label.set(time)
		self.var_title_input = tk.StringVar()
		self.var_text_input = tk.StringVar()
		self.var_tags_input = tk.StringVar()

		#self.__var_date_input = tk.StringVar()  # Delete later

		# Frames
		frame_title = tk.Frame(self, height=10, width=256)
		frame_text = tk.Frame(self, height=128, width=256)
		frame_tags = tk.Frame(self, height=10, width=256)

		frame_title.grid(column=0, row=0, sticky="we", padx=2, pady=2)
		frame_text.grid(column=0, row=1, sticky="nswe")
		frame_tags.grid(column=0, row=2, sticky="we", padx=2, pady=2)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		frame_title.columnconfigure(1, weight=1)
		frame_text.columnconfigure(0, weight=1)
		frame_text.rowconfigure(0, weight=1)
		frame_tags.columnconfigure(1, weight=1)

		########
		# Title

		# Delete later
		#self.__date_input = tk.Entry(frame_title,
		#                             textvariable=self.__var_date_input,
		#                             font=jf.config.font_label,
		#                             width=24)
		#self.__date_input.grid(column=0, row=0, padx=2)
		# -----

		self.date_label = tk.Label(frame_title,
		                           anchor="w",
		                           textvariable=self.var_date_label,
		                           font=jf.config.font_label)
		self.title_input = tk.Entry(frame_title,
		                            textvariable=self.var_title_input,
		                            font=jf.config.font_label)

		self.date_label.grid(column=0, row=0, padx=2)
		self.title_input.grid(column=1, row=0, sticky="we", padx=2)

		#############
		# Text input
		text_scroll = tk.Scrollbar(frame_text)
		self.text_input = tk.Text(frame_text, width=80, height=20,
		                          wrap="word",
		                          yscrollcommand=text_scroll.set,
		                          font=jf.config.font_content)
		self.text_input.focus()
		text_scroll.config(command=self.text_input.yview)

		self.text_input.grid(column=0, row=0, sticky="nswe")
		text_scroll.grid(column=1, row=0, sticky="ns")

		#######
		# Tags
		self.tag_label = tk.Label(frame_tags,
		                          anchor="w",
		                          text="Tags:",
		                          font=jf.config.font_label)
		self.tags_input = tk.Entry(frame_tags,
		                           textvariable=self.var_tags_input,
		                           font=jf.config.font_label)
		self.save_button = tk.Button(frame_tags, text="Save and quit",
		                             font=jf.config.font_label)
		self.save_button.bind("<ButtonRelease-1>", self.on_save_click)

		self.tag_label.grid(column=0, row=0, padx=2)
		self.tags_input.grid(column=1, row=0, sticky="we", padx=2)
		self.save_button.grid(column=2, row=0, padx=2)

		self.update()
		self.minsize(self.winfo_width(), self.winfo_height())

	def on_save_click(self, event):
		try:
			# Delete this later
			#date, time = self.__var_date_input.get().split(" ")
			#date = [int(i) for i in date.split("-")]
			#time = [int(i) for i in time.split(":")]
			#datetime = {
			#	"year": date[0],
			#	"month": date[1],
			#	"day": date[2],
			#	"hour": time[0],
			#	"minute": time[1],
			#	"second": 0
			#}
			# -----

			title = self.var_title_input.get().strip()
			text = self.text_input.get("1.0", "end-1c")
			tags = self.var_tags_input.get().split(",")
			# Strips and removes empty tags
			tags = [i.strip() for i in tags if i.strip()]

			if text.strip() == "":
				tk.messagebox.showwarning("Oops",
				                          "There is nothing to save.\n" +
				                          "Did you forget body text?")
			else:
				self.entry.title = title
				self.entry.text = text
				self.entry.tags = tags
				#self.entry.datetime = datetime
				self.entry.save()

				self.destroy()
		except Exception as e:
			e = str(e) + "\nBackup your entry and fix the error, you lazy bum."
			tk.messagebox.showwarning("Exception", e)


if __name__ == "__main__":
	app = Journalentry_tk()
	app.title("Journal - Entry")
	app.iconbitmap("media/icon.ico")
	app.mainloop()
