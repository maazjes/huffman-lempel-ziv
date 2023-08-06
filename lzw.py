from util import string_to_bytes, bytes_to_string


# Main function for encoding a string with LZW.
def encode(string: str) -> str:
    dict = {}
    for i in range(256):
        dict[chr(i)] = i

    substr = ""
    result = ""

    for char in string:
        newSubstr = substr + char

        if newSubstr in dict:
            substr = newSubstr
        else:
            result += format(
                dict[substr], "0" + str(len(format(len(dict) + 1, "b"))) + "b"
            )
            dict[newSubstr] = len(dict) + 1
            substr = char

    if len(substr) > 0:
        result += format(dict[substr], "0" + str(len(format(len(dict) + 1, "b"))) + "b")

    extra = format(8 - ((len(result) + 4) % 8), "04b")

    return extra + result


# Main function for decoding a string with LZW.
def decode(code: str) -> str:
    dict = {}
    for i in range(256):
        dict[i] = chr(i)

    extra = int(code[:4], 2)
    code = code[4 : len(code) - 8] + code[len(code) - 8 + extra :]

    bits = code[0 : len(format(len(dict) + 1, "b"))]
    substr = dict[int(bits, 2)]
    result = substr

    i = len(bits)
    while i < len(code):
        nextBits = len(format(len(dict) + 2, "b"))
        nextCode = int(code[i : i + nextBits], 2)
        newSubstr = ""

        if nextCode in dict:
            newSubstr = dict[nextCode]
        else:
            newSubstr = substr + substr[0]

        result += newSubstr
        dict[len(dict) + 1] = substr + newSubstr[0]
        substr = newSubstr

        i += nextBits

    return result


s = "testing"
encoded = encode(s)
print("encoded " + encoded)

with open("test1.bin", "wb") as f:
    f.write(string_to_bytes(encoded))

with open("test.txt", "w") as ft:
    ft.write(s)

encoded = bytes_to_string(open("test1.bin", "rb").read())
print("encoded " + encoded)
print(decode(encoded))
