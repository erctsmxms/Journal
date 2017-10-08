import tkinter as tk
import tkinter.ttk
import tkinter.font
import tkinter.messagebox

import jf


class Journal_tk(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self, None)
		#self.parent = parent
		self.entries = []
		self.initialize()
		self.load_entries()

	####################################################################
	# Initialize
	def initialize(self):
		padding = {"padx": 2, "pady": 2}
		self.var_search_input = tk.StringVar()
		self.var_preview_label = tk.StringVar()
		self.var_preview_label.set("No entry selected")
		self.var_tags_label = tk.StringVar()
		self.var_tags_label.set("Tags: ")

		# Frames
		frame_search = tk.Frame(self, height=10, width=128)
		frame_entrylist = tk.Frame(self, height=128, width=64)
		frame_preview = tk.Frame(self, height=128, width=64)

		frame_search.grid(column=0, row=0, sticky="we", columnspan=2)
		frame_entrylist.grid(column=0, row=1, sticky="nswe")
		frame_preview.grid(column=1, row=1, sticky="nswe")

		self.columnconfigure(1, weight=1)
		self.rowconfigure(1, weight=1)

		frame_search.columnconfigure(0, weight=1)
		frame_entrylist.columnconfigure(0, weight=1)
		frame_entrylist.rowconfigure(0, weight=1)
		frame_preview.columnconfigure(0, weight=1)
		frame_preview.rowconfigure(1, weight=1)

		#########
		# Search
		self.search_input = tk.Entry(frame_search,
		                             textvariable=self.var_search_input,
		                             font=jf.config.font_label)
		self.search_button = tk.Button(frame_search, text="Search",
		                               font=jf.config.font_label)

		self.search_input.bind("<Return>", self.on_search_input_enter)
		self.search_button.bind("<ButtonRelease-1>", self.on_search_button_click)

		self.search_input.grid(column=0, row=0, sticky="we", padx=2)
		self.search_button.grid(column=1, row=0, padx=2, pady=2)

		##########
		# Entries
		entry_scroll = tk.Scrollbar(frame_entrylist)
		self.entry_list = tk.Listbox(frame_entrylist,
		                             yscrollcommand=entry_scroll.set,
		                             selectmode="browse",
		                             font=jf.config.font_label,
		                             width=40,
		                             highlightthickness=0,
		                             activestyle="none")
		entry_scroll.config(command=self.entry_list.yview)

		self.entry_list.grid(column=0, row=0, sticky="ns")
		entry_scroll.grid(column=1, row=0, sticky="ns")

		self.entry_list.bind("<ButtonRelease-1>", self.on_entry_list_select)
		self.entry_list.bind("<Double-Button-1>", self.on_entry_list_doubleclick)
		self.entry_list.bind("<Delete>", self.on_entry_delete)

		##########
		# Preview
		self.preview_label = tk.Label(frame_preview,
		                              anchor="w",
		                              textvariable=self.var_preview_label,
		                              font=jf.config.font_label)

		preview_scroll = tk.Scrollbar(frame_preview)
		self.preview_text = tk.Text(frame_preview, width=40, height=20,
		                            wrap="word", state="disabled",
		                            yscrollcommand=preview_scroll.set,
		                            font=jf.config.font_content)
		preview_scroll.config(command=self.preview_text.yview)
		self.tags_label = tk.Label(frame_preview,
		                           anchor="w",
		                           textvariable=self.var_tags_label,
		                           font=jf.config.font_label)

		self.preview_label.grid(column=0, row=0, sticky="we", columnspan=2)
		self.preview_text.grid(column=0, row=1, sticky="nswe")
		preview_scroll.grid(column=1, row=1, sticky="ns")
		self.tags_label.grid(column=0, row=2, sticky="we", columnspan=2)

		self.update()
		self.minsize(self.winfo_width(), self.winfo_height())

	def load_entries(self, entry_list=None):
		self.entry_list.delete(0, "end")

		if entry_list is None:
			self.entries = jf.get_entries()
		else:
			self.entries = entry_list

		# Insert all entries
		for i in range(len(self.entries)):
			entry = self.entries[i]
			text = f"{entry.str_date} {entry.str_time_short}"
			if entry.title:
				text += f" {entry.title}"

			self.entry_list.insert("end", text)

	def search_result_update(self):
		search_string = self.var_search_input.get().strip()
		if search_string:
			results = jf.search(search_string, jf.get_entries())
			self.load_entries(results)
		else:
			self.load_entries()

	####################################################################
	# Events
	def on_entry_list_select(self, event):
		index = self.entry_list.curselection()[0]
		entry = self.entries[index]

		label = f"{entry.str_date} {entry.str_time_short}"
		if entry.title:
			label += f" {entry.title}"
		self.var_preview_label.set(label)
		# Have to switch the text box on and off to write to it
		#self.preview_label.config(text=str(entry))
		self.preview_text.config(state="normal")
		self.preview_text.delete("1.0", "end")
		self.preview_text.insert("end", entry.text)
		self.preview_text.config(state="disable")
		self.var_tags_label.set("Tags: " + ", ".join(entry.tags))

	def on_entry_list_doubleclick(self, event):
		# TODO: This doesn't work. The new window doesn't contain the
		# entry's info. Focus can also be given back to master window,
		# which ideally shouldn't happen.
		index = self.entry_list.curselection()[0]
		entry = self.entries[index]
		app = journalentry.Journalentry_tk(self.__repr__(), entry)
		app.title("Journal - Edit")
		app.iconbitmap("media/icon.ico")
		app.mainloop()

	def on_entry_delete(self, event):
		index = self.entry_list.curselection()[0]
		entry = self.entries[index]
		name = f"{entry.str_date} {entry.str_time_short}"
		if entry.title:
			name += f" {entry.title}"
		title = "Delete entry"
		message = f"Are you sure you wish to delete entry \"{name}\"?\n" + \
		           "This action cannot be undone."
		should_delete = tk.messagebox.askyesno(title, message, icon="warning")

		if should_delete:
			try:
				index = self.entry_list.curselection()[0]
				self.entries[index].delete()
				self.var_preview_label.set("")
				self.preview_text.config(state="normal")
				self.preview_text.delete("1.0", "end")
				self.preview_text.config(state="disable")
				self.var_tags_label.set("")
				self.load_entries()
			except Exception as e:
				e = f"Could no delete entry.\n" + str(e)
				tk.messagebox.showwarning("Exception", e)

	def on_search_input_enter(self, event):
		self.search_result_update()

	def on_search_button_click(self, event):
		self.search_result_update()


if __name__ == "__main__":
	app = Journal_tk()
	app.title("Journal - Viewer")
	app.iconbitmap("media/icon.ico")
	app.mainloop()
