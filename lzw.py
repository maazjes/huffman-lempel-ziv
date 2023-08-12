from util import string_to_bytes
from BitReader import BitReader


CHUNK_SIZE = 4000


# Encode a text file with LZW.
def encode(file: str) -> None:
    dict = {}

    for i in range(256):
        dict[chr(i)] = i

    substr = ""
    encoded = 8 * "0"
    encoded_bits = b""

    with open(file, "r", encoding="latin-1") as f:
        with open(file.split(".")[0] + ".bin", "wb") as fb:
            while True:
                chars = f.read(CHUNK_SIZE)

                if not chars:
                    if len(substr) > 0:
                        encoded += format(
                            dict[substr],
                            "0" + str(len(format(len(dict) + 1, "b"))) + "b",
                        )

                    extra = len(encoded) % 8

                    if len(encoded) > 8:
                        extra = 8 - extra

                    fb.write(encoded_bits)
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

                if len(encoded) % 8 == 0:
                    encoded_bits += string_to_bytes(encoded)
                    encoded = ""

                if len(encoded_bits) >= CHUNK_SIZE:
                    fb.write(encoded_bits)
                    encoded_bits = b""


# Decode a text file encoded with LZW.
def decode(file: str) -> None:
    dict = {}

    for i in range(256):
        dict[i] = chr(i)

    with open(file, "rb") as fb:
        br = BitReader(fb, CHUNK_SIZE)
        extra = int(br.read(8), 2)
        bits = br.read(len(format(len(dict), "b")))
        substr = dict[int(bits, 2)]
        decoded = substr

        with open(file.split(".")[0] + "_encoded.txt", "w") as f:
            while True:
                nextBits = len(format(len(dict) + 1, "b"))
                lastByteBits = 8 - (len(br.buffer) * 8 - br.index - nextBits)

                next = ""

                if lastByteBits > 0 and extra >= 0:
                    next = br.read(nextBits - lastByteBits)
                    br.read(extra)
                    next += br.read(lastByteBits)
                    extra = -1
                else:
                    next = br.read(nextBits)

                if not next:
                    f.write(decoded)
                    break

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


encode("testa.txt")
decode("testa.bin")
