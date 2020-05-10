import tkinter as tk
import os
from pyshard.shard import Shard
from tkinter import filedialog, Button, Entry, Label, BooleanVar, Checkbutton, messagebox, StringVar


class ShardMenu(object):
    """Main GUI window"""

    def __init__(self, root):
        root.geometry('370x200')
        root.title('PyShard')

        self.package_label = Label(root, text="Entrypoint")
        self.package_label.grid(column=0, row=0, pady=(10, 0), padx=(10, 0))
        self.package_entry = Entry(root)
        self.package_entry.grid(column=1, row=0, pady=(10, 0), padx=(10, 0))
        self.package_button = Button(root, text='Browse', command=self.get_package_path)
        self.package_button.grid(column=2, row=0, pady=(10, 0), padx=(10, 0))
        self.output_label = Label(root, text="Output Location")
        self.output_label.grid(column=0, row=1, pady=(10, 0), padx=(10, 0))
        self.output_entry = Entry(root)
        self.output_entry.grid(column=1, row=1, pady=(10, 0), padx=(10, 0))
        self.output_button = Button(root, text='Browse', command=self.get_output_path)
        self.output_button.grid(column=2, row=1, pady=(10, 0), padx=(10, 0))
        self.one_file = BooleanVar()
        self.one_file_flag = Checkbutton(
            root, 
            text="One-file Bundle", 
            variable=self.one_file, 
            onvalue=True, 
            offvalue=False
        )
        self.one_file_flag.grid(row=2, pady=(10, 0), padx=(20, 0))
        self.noconsole = BooleanVar()
        self.noconsole_flag = Checkbutton(
            root, 
            text="No-Console", 
            variable=self.noconsole, 
            onvalue=True, 
            offvalue=False
        )
        self.noconsole_flag.grid(row=2, column=1, pady=(10, 0), padx=(10, 0))
        self.nowindowed = BooleanVar()
        self.nowindowed_flag = Checkbutton(
            root, 
            text="No-Windowed", 
            variable=self.nowindowed, 
            onvalue=True, 
            offvalue=False
        )
        self.nowindowed_flag.grid(row=3, pady=(10, 0), padx=(15, 0))
        self.elevation = BooleanVar()
        self.elevation_flag = Checkbutton(
            root, 
            text="Run as Admin", 
            variable=self.elevation, 
            onvalue=True, 
            offvalue=False
        )
        self.elevation_flag.grid(row=3, column=1, pady=(10, 0), padx=(20, 0))

        self.feedback = StringVar()
        self.feedback.set('Choose a package to freeze')
        self.feedback_label = Label(root, textvariable=self.feedback, fg="steel blue")
        self.feedback_label.grid(row=4, column=1, pady=(15, 0))
        
        self.freeze_button = Button(root, text='Freeze Package', command=self.freeze)
        self.freeze_button.grid(row=4, pady=(10, 0), padx=(10, 0))


    def freeze(self):
        output_dir = self.output_entry.get()
        entrypoint = self.package_entry.get()
        if os.path.isdir(output_dir) and os.path.isfile(entrypoint):
            shard = Shard()
            args, kwargs = [], {}
            args.extend(['--clean', '--noconfirm'])
            if self.one_file.get():
                args.append('--onefile')
            if self.noconsole.get():
                args.append('--noconsole')
            if self.nowindowed.get():
                args.append('--nowindowed')
            if self.elevation.get():
                args.append('--uac-admin')
            kwargs['--distpath'] = output_dir
            self.feedback.set('Freezing Package...')
            self.feedback_label.update()
            shard.freeze(entrypoint, *args, **kwargs)
            self.feedback.set('Done Freezing!')
            self.feedback_label.update()
        else:
            messagebox.showerror(
                title='Invalid Input/Output', 
                message='You must provide valid input/output values'
            )

    def get_package_path(self):
        package_name = filedialog.askopenfilename(
            defaultextension='.txt',
            filetypes=[('Python Files', '*.py')],
        )
        current_entry = self.package_entry.get()
        self.package_entry.delete(0, len(current_entry))
        self.package_entry.insert(0, package_name)

    def get_output_path(self):
        output_path = filedialog.askdirectory(mustexist=True)
        current_entry = self.output_entry.get()
        self.output_entry.delete(0, len(current_entry))
        self.output_entry.insert(0, output_path)


if __name__ == "__main__":
    root = tk.Tk()
    pt = ShardMenu(root)
    root.mainloop()

#  TODO: add user feedback