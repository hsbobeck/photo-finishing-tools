import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import borders
import grain
import re
import os
from PIL import Image


class GUI:
    def __init__(self):
        self.start()

    def start(self):
        # Start tk with title
        self.app = TkinterDnD.Tk()
        self.app.title("Henry's Photo Finishing Tools")
        self.app.geometry("500x300")

        self.version_label = tk.Label(self.app, text="v0.1.2")
        self.version_label.pack()

        # Create a label for instructions
        self.instruction_label = tk.Label(self.app, text="Drag and drop files here")
        self.instruction_label.pack()

        # Create a listbox to display the dropped files
        self.listbox = tk.Listbox(self.app, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Create a button to trigger the export action
        self.export_with_borders_button = tk.Button(
            self.app, text="Export All with Borders", command=self.export_with_borders
        )
        self.export_with_borders_button.pack()

        # Create a button to trigger the export action
        self.export_with_grain_button = tk.Button(
            self.app, text="Export All with Grain", command=self.export_with_grain
        )
        self.export_with_grain_button.pack()

        # Create a button to clear the listbox
        self.clear_button = tk.Button(
            self.app, text="Clear", command=self.clear_listbox
        )
        self.clear_button.pack()

        # Allow dropping files into the listbox
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.add_files)

        self.app.mainloop()

    # adds files to the listbox given the drag and drop event
    # event.data is a single string of the filenames contained in the drag
    def add_files(self, event):
        # Get the list of files from the event
        if event.data[0] == "{":
            # when there is a space in the directory, it contains the filenames by {}
            files = re.split("{([^{]*?)}", event.data)
        else:
            # when there is no space in the directory, it separates filenames by only a space
            files = re.split(" ", event.data)
        # remove whitespace on ends of filenames and remove empty strings from list
        files = [s.strip() for s in files if s]
        files = [s for s in files if s]
        # Add the files to the listbox
        for file in files:
            self.listbox.insert(tk.END, file)

        # remove instruction label
        self.version_label.pack_forget()
        self.instruction_label.pack_forget()

    def export_with_borders(self):
        # Iterate through the list of files and export new versions in original folder
        for file in self.listbox.get(0, tk.END):
            abspath = os.path.abspath(file)
            dir = os.path.dirname(abspath) + "/"
            ext = os.path.splitext(abspath)[-1]
            name = os.path.basename(abspath)[0 : -len(ext)]
            print(f"dir: {dir}\nname: {name}\next: {ext}")
            borders.add_white_border(file, dir + name + "_border" + ext)

    def export_with_grain(self):
        # Iterate through the list of files and export new versions in original folder
        for file in self.listbox.get(0, tk.END):
            abspath = os.path.abspath(file)
            dir = os.path.dirname(abspath) + "/"
            ext = os.path.splitext(abspath)[-1]
            name = os.path.basename(abspath)[0 : -len(ext)]
            print(f"dir: {dir}\nname: {name}\next: {ext}")
            input_image = Image.open(file)
            output_image = grain.add_grain(input_image, "A", strength=1.0, scale=3)
            # Save the resulting image
            output_image.save(dir + name + "_grain" + ext)

    def clear_listbox(self):
        # clear all files in listbox
        self.listbox.delete(0, tk.END)


def main():
    gui = GUI()


if __name__ == "__main__":
    main()
