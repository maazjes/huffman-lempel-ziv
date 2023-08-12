from __future__ import annotations
import heapq
from util import string_to_bytes
from BitReader import BitReader
import typing


CHUNK_SIZE = 4000


class Node:
    def __init__(
        self,
        freq: int = -1,
        char: str = "",
        left: Node | None = None,
        right: Node | None = None,
    ):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, nxt: Node) -> bool:
        return self.freq < nxt.freq


# Utility function for printing leaf node values.
def print_nodes(node: Node, val: str = "") -> None:
    if node.left:
        print_nodes(node.left, val + "0")
    if node.right:
        print_nodes(node.right, val + "1")

    if not node.left and not node.right:
        print(f"{node.char} -> {val}")


# Create a new tree from given frequencies
# acccording to Huffman coding.
def create_tree(freqs: dict[str, int]) -> Node:
    nodes: list[Node] = []
    keys = list(freqs)

    for i in range(len(keys)):
        heapq.heappush(nodes, Node(freqs[keys[i]], keys[i]))

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        newNode = Node(left.freq + right.freq, "", left, right)
        heapq.heappush(nodes, newNode)

    return nodes[0]


# Return a dictionary containing symbols as keys
# and their corresponding codes as values. Also
# return the shape of the tree as 0's (regular node)
# and 1's (leaf node) and the characters corresponding
# to the 1's in the same order.
def huffman_codes(
    node: Node,
    codes: dict[str, str] = {},
    code: str = "",
    shape: str = "",
    chars: str = "",
) -> tuple[dict[str, str], str, str]:
    if not node.left or not node.right:
        codes[node.char] = code
        return (codes, shape + "1", chars + node.char)

    shape += "0"

    info_left = huffman_codes(node.left, codes, code + "0", shape, chars)
    info_right = huffman_codes(
        node.right, codes, code + "1", info_left[1], info_left[2]
    )

    return (codes, info_right[1], info_right[2])


# Calculate frequencies of characters in a given text file.
def calc_freqs(f: typing.TextIO) -> dict[str, int]:
    freqs = {}

    while True:
        chars = f.read(CHUNK_SIZE)

        if not chars:
            break

        for char in chars:
            if char not in freqs:
                freqs[char] = 0
            freqs[char] += 1

    return freqs


# Encode a text file with Huffman coding.
def encode(file: str) -> None:
    with open(file, "r", encoding="latin-1") as f:
        freqs = calc_freqs(f)
        f.seek(0)
        root = create_tree(freqs)

        (dict, shape, chars) = huffman_codes(root)

        binary_chars = ""

        # Convert leaf characters to binary.
        for char in chars:
            binary_chars += format(ord(char), "08b")

        encoded = 8 * "0" + shape + binary_chars
        encoded_bits = b""

        with open(file.split(".")[0] + ".bin", "wb") as fb:
            while True:
                chars = f.read(CHUNK_SIZE)

                if not chars:
                    # Count how many extra 0's will be added when writing to file.
                    extra = len(encoded) % 8

                    if len(encoded) > 8:
                        extra = 8 - extra

                    fb.write(encoded_bits)
                    fb.write(string_to_bytes(encoded))
                    fb.seek(0)
                    fb.write(string_to_bytes(format(extra, "08b")))

                    break

                for char in chars:
                    encoded += dict[char]

                # Convert strings to bytes when possible.
                if len(encoded) % 8 == 0:
                    encoded_bits += string_to_bytes(encoded)
                    encoded = ""

                if len(encoded_bits) >= CHUNK_SIZE:
                    fb.write(encoded_bits)
                    encoded_bits = b""


# Create a tree from a given shape consisting of 0's and 1's.
def tree_from_shape(br: BitReader, currentNode: Node) -> None:
    next_bit = br.read(1)

    if next_bit == "1":
        return

    currentNode.left = Node()
    tree_from_shape(br, currentNode.left)

    currentNode.right = Node()
    tree_from_shape(br, currentNode.right)

    return


# Fill the leaves of a tree with given 8-bit characters.
def fill_leaves(fb: BitReader, currentNode: Node) -> None:
    if not currentNode.left or not currentNode.right:
        bits = fb.read(8)
        currentNode.char = chr(int(bits, 2))
        return

    fill_leaves(fb, currentNode.left)
    fill_leaves(fb, currentNode.right)


# Decode a text file encoded with Huffman coding.
def decode(file: str) -> None:
    with open(file, "rb") as fb:
        root = Node()
        br = BitReader(fb, CHUNK_SIZE)
        extra = int(br.read(8), 2)

        tree_from_shape(br, root)
        fill_leaves(br, root)

        decoded = ""
        currentNode = root

        with open(file.split(".")[0] + "_encoded.txt", "w") as f:
            while True:
                # Skip extra 0's.
                if len(br.buffer) * 8 - br.index <= 8 and extra >= 0:
                    br.read(extra)
                    extra = -1

                next_bit = br.read(1)

                if not next_bit:
                    f.write(decoded)
                    break

                if next_bit == "0" and currentNode.left:
                    currentNode = currentNode.left

                if next_bit == "1" and currentNode.right:
                    currentNode = currentNode.right

                if not currentNode.left and not currentNode.right:
                    decoded += currentNode.char
                    currentNode = root

                if len(decoded) >= CHUNK_SIZE:
                    f.write(decoded)
                    decoded = ""


encode("testa.txt")
decode("testa.bin")
