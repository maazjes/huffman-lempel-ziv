import heapq
from util import string_to_bytes
from BitReader import BitReader
import typing
from Node import Node
import os


CHUNK_SIZE = 4 * 10**8


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
    codes: dict[str, str],
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
def encode(file: str, target: str = "") -> None:
    with open(file, "r") as f:
        freqs = calc_freqs(f)
        f.seek(0)
        root = create_tree(freqs)

        (dict, shape, chars) = huffman_codes(root, {})

        binary_chars = ""

        # Convert leaf characters to binary.
        for char in chars:
            binary_chars += format(ord(char), "016b")

        encoded = 8 * "0" + shape + binary_chars

        filename = target

        if not filename:
            filename = file.split(".")[0] + ".bin"

        with open(filename, "wb") as fb:
            while True:
                chars = f.read(CHUNK_SIZE)

                if not chars:
                    # Count how many extra 0's will be added when writing to file.
                    extra = 8 - (len(encoded) % 8)

                    if extra == 8:
                        extra = 0

                    fb.write(string_to_bytes(encoded))
                    fb.seek(0)
                    fb.write(string_to_bytes(format(extra, "08b")))

                    break

                for char in chars:
                    encoded += dict[char]

                if len(encoded) >= CHUNK_SIZE:
                    fb.write(string_to_bytes(encoded))


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
def fill_leaves(br: BitReader, currentNode: Node) -> None:
    if not currentNode.left or not currentNode.right:
        code = int(br.read(16), 2)
        currentNode.char = chr(code)
        return

    fill_leaves(br, currentNode.left)
    fill_leaves(br, currentNode.right)


# Decode a text file encoded with Huffman coding.
def decode(file: str, target: str = "") -> None:
    with open(file, "rb") as fb:
        root = Node()
        br = BitReader(fb, CHUNK_SIZE)
        extra = int(br.read(8), 2)

        tree_from_shape(br, root)
        fill_leaves(br, root)

        decoded = ""
        currentNode = root

        filename = target

        if not filename:
            filename = file.split(".")[0] + ".txt"

        filesize = os.path.getsize(file) * 8

        with open(filename, "w") as f:
            while br.index < filesize:
                # Skip extra 0's.
                if filesize - br.index == 8:
                    br.read(extra)

                next_bit = br.read(1)

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

            f.write(decoded)
