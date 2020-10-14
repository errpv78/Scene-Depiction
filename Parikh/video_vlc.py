import os
import sys
from functools import partial
import time
import pathlib

import vlc
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename


class PyPlayer(tk.Frame):
    def __init__(self, container, container_instance, title=None):
        tk.Frame.__init__(self, container_instance)
        self.container = container
        self.container_instance = container_instance
        self.initial_directory = pathlib.Path(os.path.expanduser("~"))
        self.menu_font = Font(family="Verdana", size=20)
        self.default_font = Font(family="Times New Roman", size=16)

        # create vlc instance
        self.vlc_instance, self.vlc_media_player_instance = self.create_vlc_instance()

        # main menubar
        self.menubar = tk.Menu(self.container_instance)
        self.menubar.config(font=self.menu_font)

        # cascading file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.create_file_menu()

        # cascading list menu
        self.list_menu = tk.Menu(self.menubar, tearoff=0)
        self.create_list_menu()

        # other menus
        self.menubar.add_command(label="More", command=None)
        self.menubar.add_command(label="Debug", command=self._debug)
        self.menubar.add_command(label="Quit", command=self.close)
        self.container_instance.config(menu=self.menubar)

        # vlc video frame
        self.video_panel = ttk.Frame(self.container_instance)
        self.canvas = tk.Canvas(self.video_panel, background='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

        # controls
        self.create_control_panel()

    def _debug(self):
        """Debugging."""
        import pdb;
        pdb.set_trace()
        pass

    def create_control_panel(self):
        """Add control panel."""
        control_panel = ttk.Frame(self.container_instance)
        pause = ttk.Button(control_panel, text="Pause", command=self.pause)
        play = ttk.Button(control_panel, text="Play", command=self.play)
        stop = ttk.Button(control_panel, text="Stop", command=self.stop)
        volume = ttk.Button(control_panel, text="Volume", command=None)
        pause.pack(side=tk.LEFT)
        play.pack(side=tk.LEFT)
        stop.pack(side=tk.LEFT)
        volume.pack(side=tk.LEFT)
        control_panel.pack(side=tk.BOTTOM)

    def create_vlc_instance(self):
        """Create a vlc instance; `https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html`"""
        vlc_instance = vlc.Instance()
        vlc_media_player_instance = vlc_instance.media_player_new()
        self.container_instance.update()
        return vlc_instance, vlc_media_player_instance

    def get_handle(self):
        return self.video_panel.winfo_id()

    def play(self):
        """Play a file."""
        if not self.vlc_media_player_instance.get_media():
            self.open()
        else:
            if self.vlc_media_player_instance.play() == -1:
                pass

    def close(self):
        """Close the window."""
        self.container.delete_window()

    def pause(self):
        """Pause the player."""
        self.vlc_media_player_instance.pause()

    def stop(self):
        """Stop the player."""
        self.vlc_media_player_instance.stop()

    def open(self):
        """New window allowing user to select a file and play."""
        file = askopenfilename(
            initialdir=self.initial_directory,
            filetypes=(
                ("Audio Video Interleave", "*.avi"),
                ("Matroska", "*.mkv"),
            )
        )
        if isinstance(file, tuple):
            return
        if os.path.isfile(file):
            self.play_film(file)

    def play_film(self, file):
        """Invokes the `play` method on the vlc instance for the current file."""
        directory_name = os.path.dirname(file)
        file_name = os.path.basename(file)
        self.Media = self.vlc_instance.media_new(
            str(os.path.join(directory_name, file_name))
        )
        self.Media.get_meta()
        self.vlc_media_player_instance.set_media(self.Media)
        self.vlc_media_player_instance.set_xwindow(self.get_handle())
        self.play()

    @staticmethod
    def get_film_name(film) -> str:
        """Removes directory from film name."""
        return film.split('/')[-1]

    def create_file_menu(self):
        """Create file menu."""
        self.file_menu.add_command(label="Open", command=self.open, font=self.default_font, accelerator="ctrl + o")
        self.file_menu.add_command(label="Search", command=None, font=self.default_font, accelerator="ctrl + s")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.close, font=("Verdana", 14, "bold"),
                                   accelerator="ctrl + q")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def create_film_entry(self, film):
        """Adds an entry to the `list_menu` for a given film."""
        self.list_menu.add_command(
            label=self.get_film_name(film),
            command=partial(self.play_film, film),
            font=self.default_font
        )

    def create_list_menu(self):
        """List all films present on system."""
        films = []
        try:
            for root, dirs, files in os.walk(str(self.initial_directory)):
                for file in files:
                    if file.endswith(('.mkv', '.avi')) and not file.endswith(('.sample.mkv', '.sample.avi')):
                        films.append(os.path.join(root, file))
        except TypeError:
            raise ("Error")
        films.sort(key=lambda s: s.lower().split('/')[-1])
        [self.create_film_entry(film) for film in films]
        self.menubar.add_cascade(label="All Films", menu=self.list_menu)


class BaseTkContainer:
    def __init__(self):
        self.tk_instance = tk.Tk()
        self.tk_instance.title("py player")
        self.tk_instance.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.tk_instance.geometry("1920x1080")  # default to 1080p
        self.tk_instance.configure(background='black')
        self.theme = ttk.Style()
        self.theme.theme_use("alt")

    def delete_window(self):
        tk_instance = self.tk_instance
        tk_instance.quit()
        tk_instance.destroy()
        os._exit(1)

    def __repr__(self):
        return "Base tk Container"


root = BaseTkContainer()
player = PyPlayer(root, root.tk_instance, title="pyplayer")
root.tk_instance.mainloop()