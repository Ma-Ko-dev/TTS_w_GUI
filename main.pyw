from tkinter import *
from tkinter import filedialog
from gtts import gTTS
import gtts.lang
import os


# constants
WIDTH = 600
HEIGHT = 500
PADDINGX = 20
PADDINGY = 20
# TODO: Add a config file to save the last Save location and maybe other stuff.
FILE_PATH = "Not set"
# TODO: Add a Version Check once the initial release is out.
# OWNER = " Ma-Ko-dev"
# REPO = "TTS_w_GUI"
# URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
#
# version_check = requests.get(URL)
# print(version_check)
tts_langs = gtts.tts.tts_langs()


# Button functions
def set_location():
    global FILE_PATH
    folder_name = filedialog.askdirectory()
    save_label.config(text=folder_name)
    FILE_PATH = f'"{folder_name}"'


def open_dir():
    global FILE_PATH
    os.startfile(FILE_PATH)


def text_to_speech():
    # TODO: Add a file name with current date and time.
    global FILE_PATH
    text = text_value.get(1.0, "end-1c")
    tts_lang = [k for k, v in tts_langs.items() if v == lang.get()][0]
    tts_slow = slow.get()
    tts_obj = gTTS(text=text, lang=tts_lang, slow=tts_slow)
    tts_obj.save(f"{FILE_PATH}/text_to_speech.mp3".replace('"', ""))
    # TODO: Add a notification when the files was created.


# GUI CREATION
root = Tk()
root.minsize(WIDTH, HEIGHT)
root.config(padx=PADDINGX, pady=PADDINGY)
root.resizable(width=False, height=False)
root.title("Text to Speech")

# labels
save_label = Label(text=FILE_PATH)
save_label.grid(row=2, column=0, columnspan=2, padx=2, pady=10, sticky="w")

# option menu
lang = StringVar()
lang.set("German")
dropdown = OptionMenu(root, lang, *tts_langs.values())
dropdown.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

# checkbutton
slow = BooleanVar()
check_slow = Checkbutton(root, text="Slow?", variable=slow)
check_slow.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

# button
location_button = Button(text="Set Save Location", command=set_location)
location_button.grid(row=1, column=0, padx=2, sticky="ew")
open_button = Button(text="Open Folder", command=open_dir)
open_button.grid(row=1, column=1, padx=2, sticky="ew")
convert_button = Button(text="Convert", command=text_to_speech)
convert_button.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")

# text
text_value = Text(root, height=20, width=70)
text_value.grid(row=3, columnspan=3, sticky="ew")


root.mainloop()
