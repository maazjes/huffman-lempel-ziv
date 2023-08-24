import tkinter
from tkinter import filedialog
import huffman
import lzw
import os

root = tkinter.Tk()
root.withdraw()

action = ""
algo = ""


while True:
    action = input("Would you like to compress or decompress (c/d)? ")

    if action != "c" and action != "d":
        continue

    algo = input("Would you like to use Huffman or LZW (h/l)? ")

    if algo != "h" and algo != "l":
        continue

    break

file_path = filedialog.askopenfilename()
file_path_raw = file_path

if file_path.endswith(".txt") or file_path.endswith(".bin"):
    file_path_raw = "".join(file_path.split(".")[:-1])

i = 0

if action == "c":
    if os.path.exists(f"{file_path_raw}.bin"):
        i += 1

    while os.path.exists(f"{file_path_raw}.bin ({i})"):
        i += 1

    target = ""

    if i != 0:
        target = f"{file_path_raw}.bin ({i})"

    if algo == "h":
        huffman.encode(file_path, target)
    else:
        lzw.encode(file_path, target)
else:
    if os.path.exists(f"{file_path_raw}.txt"):
        i += 1

    while os.path.exists(f"{file_path_raw}.txt ({i})"):
        i += 1

    target = ""

    if i != 0:
        target = f"{file_path_raw}.txt ({i})"

    if algo == "h":
        huffman.decode(file_path, target)
    else:
        lzw.decode(file_path, target)
