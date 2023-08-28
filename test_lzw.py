import unittest
import lzw
import os
import filecmp


class TestLZW(unittest.TestCase):
    def test_encode(self) -> None:
        outputs = [
            b"\x04\x00;\x80\x1b\xc0\x0e@\x06\x0b",
            b"\x01\x00\x1f\x80\x08@\x07\xe0\x02\xc0\x01p\x01\x98\x00e",
        ]

        for i in range(2):
            lzw.encode("assets/lzw/test_encode" + str(i) + ".txt")
            path = "assets/lzw/test_encode" + str(i) + ".bin"

            with open(path, "rb") as fb:
                self.assertEqual(
                    fb.read(),
                    outputs[i],
                )

            os.remove(path)

    def test_decode(self) -> None:
        outputs = ["work", "?!?,.fe"]

        for i in range(2):
            lzw.decode("assets/lzw/test_decode" + str(i) + ".bin")
            path = "assets/lzw/test_decode" + str(i) + ".txt"

            with open(path, "r") as f:
                self.assertEqual(f.read(), outputs[i])

            os.remove(path)

    def test_encode_decode(self) -> None:
        lzw.encode("assets/test.txt", "assets/test_encoded.bin")
        lzw.decode("assets/test_encoded.bin", "assets/test_decoded.txt")

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
