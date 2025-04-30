from pyzbar.pyzbar import decode
from PIL import Image

import string
import random
from hashlib import sha256


def read_input():
    input_data = input("give me your data:")
    if (
        any(not c in "01" for c in input_data)
        or len(input_data) != 21 * 21 * 21
        or input_data.count("1") >= 390
    ):
        raise ValueError("Invalid input")
    return input_data


def parse_data(input_str):
    data = [[[False] * 21 for _ in range(21)] for __ in range(21)]
    index = 0
    for z in range(21):
        for y in range(21):
            for x in range(21):
                if index < len(input_str):
                    data[x][y][z] = input_str[index] == "1"
                    index += 1
    return data


def create_image(matrix, module_size=10):
    size = len(matrix) * module_size
    img = Image.new("1", (size, size), 1)
    pixels = img.load()

    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y]:
                for dx in range(module_size):
                    for dy in range(module_size):
                        px = x * module_size + dx
                        py = y * module_size + dy
                        if px < size and py < size:
                            pixels[px, py] = 0
    return img


def decode_qr(image):
    decoded = decode(image)
    return decoded[0].data.decode("utf-8") if decoded else ""


def proof_of_work():
    proof = "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(20)]
    )
    digest = sha256(proof.encode()).hexdigest()
    print("sha256(XXXX+%s) == %s" % (proof[4:], digest))
    x = input("Give me XXXX:")
    if len(x) != 4 or sha256((x + proof[4:]).encode()).hexdigest() != digest:
        print("Sorry~ bye~")
        return False
    print("Right!")
    return True


def main():
    if not proof_of_work():
        exit(0)
    try:
        input_str = read_input()
        data = parse_data(input_str)
        front = [
            [any(data[x][y][z] for z in range(21)) for y in range(21)]
            for x in range(21)
        ]
        left = [
            [any(data[x][y][z] for x in range(21)) for z in range(21)]
            for y in range(21)
        ]
        top = [
            [any(data[x][y][z] for y in range(21)) for z in range(21)]
            for x in range(21)
        ]
        projections = [front, left, top]
        validation = ["Azure", "Assassin", "Alliance"]
        for projection, word in zip(projections, validation):
            content = decode_qr(create_image(projection))
            if content != word:
                raise ValueError("Invalid content")
    except Exception as e:
        print(f"Error: {e}")
        exit(0)

    with open("flag", "r") as f:
        print(f.read())


if __name__ == "__main__":
    main()