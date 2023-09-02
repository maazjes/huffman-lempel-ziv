from util import string_to_bytes
from BitReader import BitReader
import os

CHUNK_SIZE = 4 * 10**8


# Encode a text file with LZW.
def encode(file: str, target: str = "") -> None:
    dict = {}

    for i in range(65536):
        dict[chr(i)] = i

    substr = ""
    encoded = 8 * "0"

    filename = target

    if not filename:
        filename = file.split(".")[0] + ".bin"

    with open(file, "r") as f:
        with open(filename, "wb") as fb:
            while True:
                chars = f.read(CHUNK_SIZE)

                if not chars:
                    if len(substr) > 0:
                        encoded += format(
                            dict[substr],
                            "0" + str(len(format(len(dict) + 1, "b"))) + "b",
                        )

                    extra = 8 - (len(encoded) % 8)

                    if extra == 8:
                        extra = 0

                    fb.write(string_to_bytes(encoded))
                    fb.seek(0)
                    fb.write(string_to_bytes(format(extra, "08b")))

                    break

                for char in chars:
                    newSubstr = substr + char

                    if newSubstr in dict:
                        substr = newSubstr
                    else:
                        encoded += format(
                            dict[substr],
                            "0" + str(len(format(len(dict), "b"))) + "b",
                        )
                        dict[newSubstr] = len(dict)
                        substr = char

                if len(encoded) >= CHUNK_SIZE:
                    fb.write(string_to_bytes(encoded))


# Decode a text file encoded with LZW.
def decode(file: str, target: str = "") -> None:
    dict = {}

    for i in range(65536):
        dict[i] = chr(i)

    with open(file, "rb") as fb:
        br = BitReader(fb, CHUNK_SIZE)
        extra = int(br.read(8), 2)
        bits = br.read(len(format(len(dict), "b")))
        substr = dict[int(bits, 2)]
        decoded = substr

        filename = target

        if not filename:
            filename = file.split(".")[0] + ".txt"

        filesize = os.path.getsize(file) * 8

        with open(filename, "w") as f:
            while br.index < filesize:
                next_bits = len(format(len(dict) + 1, "b"))
                last_bits = br.index + next_bits - (filesize - 8)
                next = ""

                if last_bits >= 0:
                    next = br.read(next_bits - last_bits)
                    br.read(extra)
                    next += br.read(last_bits)
                else:
                    next = br.read(next_bits)

                nextCode = int(next, 2)
                newSubstr = ""

                if nextCode in dict:
                    newSubstr = dict[nextCode]
                else:
                    newSubstr = substr + substr[0]

                decoded += newSubstr
                dict[len(dict)] = substr + newSubstr[0]
                substr = newSubstr

                if len(decoded) >= CHUNK_SIZE:
                    f.write(decoded)
                    decoded = ""

            f.write(decoded)
