from __future__ import annotations
import heapq


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
def printNodes(node: Node, val: str = "") -> None:
    if node.left:
        printNodes(node.left, val + "0")
    if node.right:
        printNodes(node.right, val + "1")

    if not node.left and not node.right:
        print(f"{node.char} -> {val}")


# Creates a new tree from given frequencies
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


# Returns a dictionary containing symbols as keys
# and their corresponding codes as values. Also
# returns the shape of the tree as 0's (regular node)
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


# Calculate frequencies of characters in a given string.
def calc_freqs(string: str) -> dict[str, int]:
    freqs = {}

    for char in string:
        if char not in freqs:
            freqs[char] = 0
        freqs[char] += 1

    return freqs


# Main function for encoding a string with Huffman coding.
def encode(string: str) -> str:
    freqs = calc_freqs(string)
    root = create_tree(freqs)

    (dict, shape, chars) = huffman_codes(root)

    encoded = ""
    binary_chars = ""

    # Encode characters in the given string.
    for char in string:
        encoded += dict[char]

    # Convert leaf characters to binary.
    for char in chars:
        binary_chars += format(ord(char), "08b")

    final = shape + binary_chars + encoded

    # Count how many extra 0's will be added when writing to file.
    extra = format(8 - ((len(final) + 4) % 8), "04b")

    return extra + shape + binary_chars + encoded


# Creates a tree from a given shape consisting of 0's and 1's.
def tree_from_shape(shape: str, i: int, currentNode: Node) -> int:
    if shape[i] == "1":
        return i

    currentNode.left = Node()
    i = tree_from_shape(shape, i + 1, currentNode.left)

    currentNode.right = Node()
    i = tree_from_shape(shape, i + 1, currentNode.right)

    return i


# Fills the leaves of a tree with given 8-bit characters.
def fill_leaves(code: str, currentNode: Node, i: int = 0) -> int:
    if not currentNode.left or not currentNode.right:
        currentNode.char = chr(int(code[i : i + 8], 2))
        return i + 8

    i = fill_leaves(code, currentNode.left, i)
    return fill_leaves(code, currentNode.right, i)


# Decodes one character encoded with Huffman coding.
def char_from_code(code: str, i: int, root: Node) -> tuple[str, int]:
    currentNode = root

    for j in range(i, len(code) + 1):
        if not currentNode.left or not currentNode.right:
            return (currentNode.char, j)

        if currentNode.left and code[j] == "0":
            currentNode = currentNode.left
        if currentNode.right and code[j] == "1":
            currentNode = currentNode.right

    raise Exception("Incorrect code. Leaf node not reached.")


# Decodes a string encoded with Huffman coding.
def string_from_tree(code: str, root: Node) -> str:
    i = 0
    string = ""

    while i < len(code):
        (char, j) = char_from_code(code, i, root)
        i = j
        string += char

    return string


# Main function for decoding a string encoded with Huffman coding.
def decode(code: str) -> str:
    extra = int(code[:4], 2)
    rest = code[4:]
    root = Node()

    tree_size = tree_from_shape(rest, 0, root) + 1
    rest = rest[tree_size:]

    leaves = fill_leaves(rest, root)
    rest = rest[leaves:]

    # Delete extra zeros that were added when writing to file.
    rest = rest[: len(rest) - 8] + rest[len(rest) - 8 + extra :]

    return string_from_tree(rest, root)


def to_bytes(data: str) -> bytes:
    b = bytearray()

    for i in range(0, len(data), 8):
        b.append(int(data[i : i + 8], 2))

    return bytes(b)


s = "test string"

encoded = encode(s)

with open("test.bin", "wb") as f:
    f.write(to_bytes(encoded))

with open("test.txt", "w") as fs:
    fs.write(s)

encoded = "".join(f"{n:08b}" for n in open("test.bin", "rb").read())
print(decode(encoded))
