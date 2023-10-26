import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import borders
import re
import os


class GUI:
    def __init__(self):
        self.start()

    def start(self):
        # Start tk with title
        self.app = TkinterDnD.Tk()
        self.app.title("Henry's Photo Finishing Tools")

        # Create a listbox to display the dropped files
        self.listbox = tk.Listbox(self.app, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Create a button to trigger the export action
        self.export_button = tk.Button(
            self.app, text="Export All with Borders", command=self.export_with_borders
        )
        self.export_button.pack()

        # Create a button to clear the listbox
        self.clear_button = tk.Button(
            self.app, text="Clear", command=self.clear_listbox
        )
        self.clear_button.pack()

        # Allow dropping files into the listbox
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.add_files)

        self.app.mainloop()

    def add_files(self, event):
        # Get the list of files from the event
        files = re.split("{([^{]*?)}", event.data)
        # remove empty strings from list and remove whitespace on ends
        files = [s.strip() for s in files if s]
        files = [s for s in files if s]
        # Add the files to the listbox
        for file in files:
            self.listbox.insert(tk.END, file)

    def export_with_borders(self):
        # Iterate through the list of files and add borders
        for file in self.listbox.get(0, tk.END):
            abspath = os.path.abspath(file)
            dir = os.path.dirname(abspath) + "/"
            # name = os.path.basename(abspath).split(".")[0]
            ext = os.path.splitext(abspath)[-1]
            name = os.path.basename(abspath)[0 : -len(ext)]
            print(f"dir: {dir}\nname: {name}\next: {ext}")
            borders.add_white_border(file, dir + name + "_border" + ext)

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)


def main():
    gui = GUI()


if __name__ == "__main__":
    main()
