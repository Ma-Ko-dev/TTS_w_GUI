from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from gtts import gTTS
import gtts.lang
import os
import datetime as dt
import requests
import webbrowser
import configparser

# constants
WIDTH = 600
HEIGHT = 500
PADDINGX = 20
PADDINGY = 20
BLUE = "#256D85"
DBLUE = "#06283D"
LBLUE = "#DFF6FF"
CONFIG_PATH = "config/config.ini"
VERSION = "v1.0.1"
HOMEPAGE = "https://github.com/Ma-Ko-dev/TTS_w_GUI/releases"
OWNER = "Ma-Ko-dev"
REPO = "TTS_w_GUI"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"

# globals
tts_langs = gtts.tts.tts_langs()
file_path = 'C:/'
last_file = ''

# version check
request_version = requests.get(API_URL).json()["tag_name"]
if request_version != VERSION:
    messagebox.showinfo(title="New Version", message="There is a new Version. Go check it out!")
    webbrowser.open(HOMEPAGE)

# config check
if not os.path.exists(CONFIG_PATH):
    # creating a default config file it none exists
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set("settings", "path", file_path)
    os.makedirs(os.path.dirname(CONFIG_PATH))
    with open(CONFIG_PATH, mode="w") as config_file:
        config.write(config_file)
else:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    file_path = config["settings"]["path"]


# Button functions
def set_location():
    """Sets the Path to save the mp3 files to. Also updates the config.ini. Needs no Arguments, returns nothing."""
    global file_path
    folder_name = filedialog.askdirectory()
    if folder_name == "":
        messagebox.showwarning("No folder selected", "Please choose a valid Folder!")
    else:
        save_label.config(text=f"Your files will be saved here: {folder_name}")
        file_path = f'{folder_name}'
        config.set("settings", "path", file_path)
        with open(CONFIG_PATH, mode="w") as file:
            config.write(file)


def open_dir():
    """Opens the current Location of the mp3 files. Needs no Arguments, returns nothing."""
    os.startfile(file_path)


def text_to_speech():
    """Takes the values from textfield, checkbox and optionmenu and puts everything together to create the Text to
       Speech Object. Then Saves it in FILE_PATH. Needs no Arguments, returns nothing."""
    global last_file
    text = text_value.get(1.0, "end-1c").strip()
    if len(text) > 0:
        file_name = dt.datetime.now().strftime("Text-To-Speech_%H%M%S")
        last_file = f"{file_path}/{file_name}.mp3"
        tts_lang = [k for k, v in tts_langs.items() if v == lang.get()][0]
        tts_slow = slow.get()
        tts_obj = gTTS(text=text, lang=tts_lang, slow=tts_slow)
        tts_obj.save(f"{file_path}/{file_name}.mp3")
        messagebox.showinfo("Success!", "File was successfully created.")
    else:
        messagebox.showinfo("Information", "The Textarea can't be empty. Please insert some text.")


def play_file():
    """Plays the last created mp3 file. Needs no arguments. Returns nothing."""
    if os.path.exists(last_file) and not last_file == "":
        os.startfile(last_file)
    else:
        messagebox.showerror("No file found.", "Couldn't find a file to play.")


# GUI CREATION
root = Tk()
root.minsize(WIDTH, HEIGHT)
root.config(padx=PADDINGX, pady=PADDINGY, bg=BLUE)
root.resizable(width=False, height=False)
root.title(f"Text to Speech - {VERSION}")

# labels
save_label = Label(text=f"Your files will be saved here: {file_path}", bg=BLUE, fg=LBLUE)
save_label.grid(row=2, column=0, columnspan=3, padx=2, pady=10, sticky="w")

# option menu
lang = StringVar()
lang.set("German")
dropdown = OptionMenu(root, lang, *tts_langs.values())
dropdown.config(bg=DBLUE, fg=LBLUE, highlightthickness=0, activebackground=DBLUE, activeforeground=LBLUE)
dropdown.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

# checkbutton
slow = BooleanVar()
check_slow = Checkbutton(root, text="Slow?", variable=slow, bg=BLUE, fg=LBLUE, activebackground=BLUE,
                         activeforeground=LBLUE, selectcolor=DBLUE)
check_slow.grid(row=0, column=1, padx=2, pady=2, sticky="w")

# button
location_button = Button(text="Set Save Location", command=set_location, bg=DBLUE, fg=LBLUE)
location_button.grid(row=1, column=0, padx=2, sticky="ew")
open_button = Button(text="Open Folder", command=open_dir, bg=DBLUE, fg=LBLUE)
open_button.grid(row=1, column=1, padx=2, sticky="ew")
convert_button = Button(text="Convert", command=text_to_speech, bg=DBLUE, fg=LBLUE)
convert_button.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")
play_button = Button(text="Play", command=play_file, bg=DBLUE, fg=LBLUE)
play_button.grid(row=1, column=2, padx=2, stick="ew")

# text
text_value = Text(root, height=20, width=70, bg=LBLUE)
text_value.grid(row=3, columnspan=3, sticky="ew")


root.mainloop()
