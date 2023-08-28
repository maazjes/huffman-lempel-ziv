import unittest
import huffman
from util import tree_to_string
import unittest
from Node import Node
from BitReader import BitReader
import os
import filecmp


class TestHuffman(unittest.TestCase):
    def test_create_tree(self) -> None:
        inputs = [
            {"a": 0, "b": 3, "c": 5},
            {"k": 1001, "d": 10, "l": 50},
            {"x": 214312, "m": 2212, "l": 1032, "s": 24101, "o": 800},
        ]

        outputs = ["00a1b1c", "00d1l1k", "0000o1l1m1s1x"]

        for i in range(len(inputs)):
            self.assertEqual(tree_to_string(huffman.create_tree(inputs[i])), outputs[i])

    def test_huffman_codes(self) -> None:
        inputs = [
            Node(
                left=Node(left=Node(char="a"), right=Node(char="b")),
                right=Node(left=Node(char="c"), right=Node(char="d")),
            ),
            Node(
                left=Node(
                    left=Node(left=Node(char="x"), right=Node(char="?")),
                    right=Node(char="w"),
                ),
                right=Node(char="f"),
            ),
        ]

        outputs = [
            ({"a": "00", "b": "01", "c": "10", "d": "11"}, "0011011", "abcd"),
            ({"x": "000", "?": "001", "w": "01", "f": "1"}, "0001111", "x?wf"),
        ]

        for i in range(len(inputs)):
            self.assertEqual(huffman.huffman_codes(inputs[i], {}), outputs[i])

    def test_calc_freqs(self) -> None:
        outputs = [
            {
                "w": 10,
                "e": 9,
                "f": 4,
                "k": 10,
                "o": 10,
                "p": 11,
                "g": 6,
                "a": 4,
                "r": 4,
                "d": 2,
                "q": 2,
                "l": 4,
                "å": 2,
                "`": 2,
                "!": 3,
                "#": 1,
                "0": 5,
                "3": 3,
                "?": 5,
                "=": 1,
                "1": 1,
                "2": 5,
                "+": 5,
                ",": 1,
                "v": 1,
                " ": 2,
                "´": 2,
                "\n": 1,
            },
            {"a": 1, "s": 1, "d": 1, "\n": 1},
        ]

        for i in range(2):
            with open("assets/huffman/test_calc_freqs" + str(i) + ".txt", "r") as f:
                freqs = huffman.calc_freqs(f)
                self.assertEqual(freqs, outputs[i])

    def test_tree_from_shape(self) -> None:
        outputs = ["0010110101", "00110101"]

        for i in range(2):
            with open(
                "assets/huffman/test_tree_from_shape" + str(i) + ".bin", "rb"
            ) as fb:
                root = Node()
                huffman.tree_from_shape(BitReader(fb, 4000), root)
                self.assertEqual(outputs[i], tree_to_string(root))

    def test_fill_leaves(self) -> None:
        inputs = [
            Node(
                left=Node(left=Node(), right=Node()),
                right=Node(left=Node(), right=Node()),
            ),
            Node(
                left=Node(
                    left=Node(left=Node(), right=Node()),
                    right=Node(),
                ),
                right=Node(),
            ),
        ]

        outputs = ["00a1b10c1d", "000x1?1w1f"]

        for i in range(2):
            with open("assets/huffman/test_fill_leaves" + str(i) + ".bin", "rb") as fb:
                huffman.fill_leaves(BitReader(fb, 4000), inputs[i])
                self.assertEqual(tree_to_string(inputs[i]), outputs[i])

    def test_encode(self) -> None:
        outputs = [
            b"\x016\x00\xee\x00\xe4\x00\xde\x00\xd6'",
            b"\x03-`\x05\xc0\x04 \x05\x80\x07\xe0\x0c\xa0\x0c\xd2\x99\x1e",
        ]

        for i in range(2):
            huffman.encode("assets/huffman/test_encode" + str(i) + ".txt")

        for i in range(2):
            path = "assets/huffman/test_encode" + str(i) + ".bin"

            with open(path, "rb") as fb:
                self.assertEqual(fb.read(), outputs[i])

            os.remove(path)

    def test_decode(self) -> None:
        outputs = ["work", "?!?,.fe"]

        for i in range(2):
            huffman.decode("assets/huffman/test_decode" + str(i) + ".bin")

        for i in range(2):
            path = "assets/huffman/test_decode" + str(i) + ".txt"

            with open(path, "r") as f:
                self.assertEqual(f.read(), outputs[i])

            os.remove(path)

    def test_encode_decode(self) -> None:
        huffman.encode("assets/test.txt", "assets/test_encoded.bin")
        huffman.decode("assets/test_encoded.bin", "assets/test_decoded.txt")

        self.assertTrue(
            filecmp.cmp(
                "assets/test.txt",
                "assets/test_decoded.txt",
                shallow=False,
            )
        )

        self.assertTrue(
            os.path.getsize("assets/test_encoded.bin")
            < os.path.getsize("assets/test.txt")
        )

        os.remove("assets/test_decoded.txt")
        os.remove("assets/test_encoded.bin")
