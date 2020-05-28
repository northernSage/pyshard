import os
import tkinter as tk
from tkinter import (BooleanVar, Button, Checkbutton, Entry, Label, StringVar,
                     filedialog, messagebox)
from typing import List, Tuple

from pyshard.shard import Shard


class ShardMenu(object):
    """Main GUI class"""

    def __init__(self, root):
        root.geometry('370x200')
        root.title('PyShard')

        self.package_label, self.package_entry, self.package_button = self._new_path_entry_group(
            label_text='Entrypoint', button_text='Browse', action=self.get_package_path)
        self.output_label, self.output_entry, self.output_button = self._new_path_entry_group(
            row=1, label_text='Output Location', button_text='Browse', action=self.get_output_path)

        self.one_file, self.one_file_flag = self._new_flag_group(
            text='One-file Bundle', r=2, px=(20, 0))
        self.noconsole, self.noconsole_flag = self._new_flag_group(
            text='No-Console', r=2, c=1)
        self.nowindowed, self.nowindowed_flag = self._new_flag_group(
            text='No-Windowed', r=3, px=(15, 0))
        self.elevation, self.elevation_flag = self._new_flag_group(
            text='Run as Admin', r=3, c=1, px=(20, 0))

        self.feedback = StringVar()
        self.feedback.set('Choose a package to freeze')

        self.feedback_label = Label(
            root, textvariable=self.feedback, fg="steel blue")
        self.feedback_label.grid(row=4, column=1, pady=(15, 0))

        self.freeze_button = Button(
            root, text='Freeze Package', command=self.freeze)
        self.freeze_button.grid(row=4, pady=(10, 0), padx=(10, 0))

    def _new_path_entry_group(self, row: int = 0, label_text: str = 'label', button_text: str = 'button', action=None) -> Tuple[Label, Entry, Button]:
        """Create widget group for file/dir path input"""
        label = Label(root, text=label_text)
        label.grid(column=0, row=row, pady=(10, 0), padx=(10, 0))
        entry = Entry(root)
        entry.grid(column=1, row=row, pady=(10, 0), padx=(10, 0))
        button = Button(root, text=button_text, command=action)
        button.grid(column=2, row=row, pady=(10, 0), padx=(10, 0))
        return label, entry, button

    def _new_flag_group(self, text: str = 'flag', r: int = 0, c: int = 0, px: Tuple[int, int] = (10, 0), py: Tuple[int, int] = (10, 0)) -> Tuple[BooleanVar, Checkbutton]:
        """Create flag input group for compiling specifications"""
        boolean = BooleanVar()
        flag = Checkbutton(root, text=text, variable=boolean,
                           onvalue=True, offvalue=False)
        flag.grid(row=r, column=c, pady=py, padx=px)
        return boolean, flag

    def _parse_flags(self) -> List[str]:
        """Parse flags to pyinstaller arguments"""
        args = []
        if self.one_file.get():
            messagebox.showwarning(
                title='One-file Bundle Restriction',
                message='Make sure all data files and '
                'assets are in your package\'s root directory. '
                'One-file bundling compression will flatten '
                'nested folders!'
            )
            args.append('--onefile')
        if self.noconsole.get():
            args.append('--noconsole')
        if self.nowindowed.get():
            args.append('--nowindowed')
        if self.elevation.get():
            args.append('--uac-admin')
        return args

    def _show_message(self, message: str) -> None:
        """Display message to user"""
        self.feedback.set(message)
        self.feedback_label.update()

    def get_package_path(self) -> None:
        """Get path to module entrypoint from user"""
        package_name = filedialog.askopenfilename(
            defaultextension='.py',
            filetypes=[('Python Files', '*.py')],
        )
        current_entry = self.package_entry.get()
        self.package_entry.delete(0, len(current_entry))
        self.package_entry.insert(0, package_name)

    def get_output_path(self) -> None:
        """Get path to directory where compiled package will be saved"""
        output_path = filedialog.askdirectory(mustexist=True)
        current_entry = self.output_entry.get()
        self.output_entry.delete(0, len(current_entry))
        self.output_entry.insert(0, output_path)

    def freeze(self) -> None:
        """Set up args and start shard freezing"""
        output_dir, entrypoint = self.output_entry.get(), self.package_entry.get()
        if os.path.isdir(output_dir) and os.path.isfile(entrypoint):
            args, kwargs = self._parse_flags() + \
                ['--clean',
                    '--noconfirm'], {'--distpath': output_dir, '--specpath': output_dir}
            self._show_message('Freezing Package...')
            Shard().freeze(entrypoint, *args, **kwargs)
            self._show_message('Done Freezing!')
        else:
            self._show_message('Invalid entry/output values!')


if __name__ == "__main__":
    root = tk.Tk()
    pt = ShardMenu(root)
    root.mainloop()
