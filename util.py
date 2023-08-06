def string_to_bytes(data: str) -> bytes:
    b = bytearray()

    for i in range(0, len(data), 8):
        b.append(int(data[i : i + 8], 2))

    return bytes(b)


def bytes_to_string(bytes: bytes) -> str:
    return "".join(f"{n:08b}" for n in bytes)
