from __future__ import annotations
import heapq
from typing import Type


class node:
    def __init__(
        self,
        freq: int,
        char: str = "",
        left: Type[node] = None,
        right: Type[node] = None,
    ):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, nxt: node):
        return self.freq < nxt.freq


def huffman_tree(freqs: dict):
    nodes: list[node] = []

    keys = list(freqs)

    for i in range(len(keys)):
        heapq.heappush(nodes, node(freqs[keys[i]], keys[i]))

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        newNode = node(left.freq + right.freq, "", left, right)

        heapq.heappush(nodes, newNode)

    return nodes[0]


def huffman_codes(
    node: node,
    codes: dict[str, str] = {},
    code: str = "",
    shape: str = "",
    chars: str = "",
):
    if not node.left and not node.right:
        codes[node.char] = code
        return (codes, shape + "1", chars + node.char)

    shape += "0"

    info_left = huffman_codes(node.left, codes, code + "0", shape, chars)
    info_right = huffman_codes(
        node.right, codes, code + "1", info_left[1], info_left[2]
    )

    return (codes, info_right[1], info_right[2])


def calc_freqs(string: str):
    freqs = {}

    for char in string:
        if char not in freqs:
            freqs[char] = 0

        freqs[char] += 1

    return freqs


def huffman_code(string: str):
    freqs = calc_freqs(string)
    root = huffman_tree(freqs)

    (dict, shape, chars) = huffman_codes(root)

    encoded = ""
    binary_chars = ""

    for char in string:
        encoded += dict[char]

    for char in chars:
        binary_chars += format(ord(char), "08b")

    final = shape + binary_chars + encoded

    extra = format(8 - ((len(final) + 4) % 8), "04b")

    return extra + shape + binary_chars + encoded


def tree_from_shape(code: str, i: int, currentNode: node):
    if code[i] == "1":
        return i

    currentNode.left = node(-1)
    i = tree_from_shape(code, i + 1, currentNode.left)

    currentNode.right = node(-1)
    i = tree_from_shape(code, i + 1, currentNode.right)

    return i


def fill_leaves(code, currentNode: node, i: int = 0):
    if not currentNode.left and not currentNode.right:
        currentNode.char = chr(int(code[i : i + 8], 2))
        return i + 8

    i = fill_leaves(code, currentNode.left, i)
    return fill_leaves(code, currentNode.right, i)


def char_from_tree(code: str, i, root: node):
    currentNode = root
    for j in range(i, len(code) + 1):
        if currentNode.char:
            return (currentNode.char, j)
        if code[j] == "0":
            currentNode = currentNode.left
        if code[j] == "1":
            currentNode = currentNode.right


def string_from_tree(code: str, root: node):
    i = 0
    string = ""

    while i < len(code):
        (char, j) = char_from_tree(code, i, root)
        i = j
        string += char

    return string


def printNodes(node: node, val=""):
    if node.left:
        printNodes(node.left, val + "0")
    if node.right:
        printNodes(node.right, val + "1")

    if not node.left and not node.right:
        print(f"{node.char} -> {val}")


def huffman_decode(code: str):
    extra = int(code[:4], 2)
    rest = code[4:]
    root = node(-1)
    index = tree_from_shape(rest, 0, root)
    rest = rest[index + 1 :]
    x = fill_leaves(rest, root)
    rest = rest[x:]
    rest = rest[: len(rest) - 8] + rest[len(rest) - 8 + extra :]
    return string_from_tree(rest, root)


def to_bytes(data):
    b = bytearray()
    for i in range(0, len(data), 8):
        b.append(int(data[i : i + 8], 2))
    return bytes(b)


s = "test string"

encoded = huffman_code(s)

with open("test.bin", "wb") as f:
    f.write(to_bytes(encoded))

with open("test.txt", "w") as f:
    f.write(s)

encoded = "".join(f"{n:08b}" for n in open("test.bin", "rb").read())
print(huffman_decode(encoded))
