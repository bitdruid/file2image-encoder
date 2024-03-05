import base64
import sys
import os
import math
import zlib
import PIL.Image

# all grey scale colors with 8 bit depth and very light
B64_RGB_DICT = {
    "A": (188, 188, 188),
    "B": (189, 189, 189),
    "C": (190, 190, 190),
    "D": (191, 191, 191),
    "E": (192, 192, 192),
    "F": (193, 193, 193),
    "G": (194, 194, 194),
    "H": (195, 195, 195),
    "I": (196, 196, 196),
    "J": (197, 197, 197),
    "K": (198, 198, 198),
    "L": (199, 199, 199),
    "M": (200, 200, 200),
    "N": (201, 201, 201),
    "O": (202, 202, 202),
    "P": (203, 203, 203),
    "Q": (204, 204, 204),
    "R": (205, 205, 205),
    "S": (206, 206, 206),
    "T": (207, 207, 207),
    "U": (208, 208, 208),
    "V": (209, 209, 209),
    "W": (210, 210, 210),
    "X": (211, 211, 211),
    "Y": (212, 212, 212),
    "Z": (213, 213, 213),
    "a": (214, 214, 214),
    "b": (215, 215, 215),
    "c": (216, 216, 216),
    "d": (217, 217, 217),
    "e": (218, 218, 218),
    "f": (219, 219, 219),
    "g": (220, 220, 220),
    "h": (221, 221, 221),
    "i": (222, 222, 222),
    "j": (223, 223, 223),
    "k": (224, 224, 224),
    "l": (225, 225, 225),
    "m": (226, 226, 226),
    "n": (227, 227, 227),
    "o": (228, 228, 228),
    "p": (229, 229, 229),
    "q": (230, 230, 230),
    "r": (231, 231, 231),
    "s": (232, 232, 232),
    "t": (233, 233, 233),
    "u": (234, 234, 234),
    "v": (235, 235, 235),
    "w": (236, 236, 236),
    "x": (237, 237, 237),
    "y": (238, 238, 238),
    "z": (239, 239, 239),
    "0": (240, 240, 240),
    "1": (241, 241, 241),
    "2": (242, 242, 242),
    "3": (243, 243, 243),
    "4": (244, 244, 244),
    "5": (245, 245, 245),
    "6": (246, 246, 246),
    "7": (247, 247, 247),
    "8": (248, 248, 248),
    "9": (249, 249, 249),
    "+": (250, 250, 250),
    "/": (251, 251, 251),
    "=": (252, 252, 252),
    "\n": (253, 253, 253),
    "\r": (254, 254, 254),
    " ": (255, 255, 255)
}

def encode_hex(filepath):
    try:
        filename = os.path.basename(filepath) + "\n\r"
        #filename_b64 = base64.b64encode(filename.encode("utf-8")).decode("utf-8")
        filename_b64_hex = filename.hex()
        with open(filepath, "rb") as file:
            file_content = file.read()
            file_content_compressed = zlib.compress(file_content, 9)
            #file_content_compressed_b64 = base64.b64encode(file_content_compressed).decode("utf-8")
            file_content_compressed_b64_hex = file_content_compressed.hex()
            encoded_file = filename_b64_hex + file_content_compressed_b64_hex
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")

    return encoded_file

def create_image_content_hex(encoded_content):
    # end recognized by: \n\r and one 0x00 byte
    # \n = 0x0a, \r = 0x0d
    # append end delimiter
    encoded_content += "0a0d"
    rest = (6 - len(encoded_content) % 6) // 2
    # append 0x00 bytes to fill up the last 6 byte block
    if rest != 6:
        encoded_content += "00" * rest
    # split encoded content into 6 byte blocks
    hex_pixel_matrix = [encoded_content[i:i+6] for i in range(0, len(encoded_content), 6)]
    # append 0x00 bytes until the length of the hex pixel matrix is a perfect square
    hex_pixel_matrix_root = math.sqrt(len(hex_pixel_matrix))
    if not hex_pixel_matrix_root.is_integer():
        hex_pixel_matrix += ["000000"] * (int(hex_pixel_matrix_root + 1) ** 2 - len(hex_pixel_matrix))
    print(hex_pixel_matrix)
    return hex_pixel_matrix

def create_image_hex(hex_pixel_matrix):
    rgb_pixel_matrix = [tuple(int(hex_pixel[i:i+2], 16) for i in (0, 2, 4)) for hex_pixel in hex_pixel_matrix]
    image_size = math.sqrt(len(rgb_pixel_matrix))
    image = PIL.Image.new("RGB", (int(image_size), int(image_size)))
    image.putdata(rgb_pixel_matrix)
    image.save("encoded.png")

def main():
    if len(sys.argv) != 2:
        print("Usage: python encode.py <filepath>")
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        encoded_content = encode_hex(filepath)
        image_content = create_image_content_hex(encoded_content)
        create_image_hex(image_content)
        # encoded_file = encode(filepath)
        # image_content = create_image_content(encoded_file)
        # create_image(image_content)
        # print("File encoded.")

if __name__ == "__main__":
    main()
