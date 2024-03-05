import sys
import os
import math
import zlib
import PIL.Image

def encode_hex(filepath):
    try:
        filename = os.path.basename(filepath) + "\n\r"
        filename_b64_hex = filename.encode("utf-8").hex()
        with open(filepath, "rb") as file:
            file_content = file.read()
            file_content_compressed = zlib.compress(file_content, 9)
            file_content_compressed_b64_hex = file_content_compressed.hex()
            encoded_file = filename_b64_hex + file_content_compressed_b64_hex
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")

    return encoded_file

def create_image_content_hex(encoded_file):
    # end recognized by: \n\r and one 0x00 byte
    # \n = 0x0a, \r = 0x0d
    # append end delimiter
    encoded_file += "0a0d"
    rest = (6 - len(encoded_file) % 6) // 2
    # append 0x00 bytes to fill up the last 6 byte block
    if rest != 6:
        encoded_file += "00" * rest
    # split encoded content into 6 byte blocks
    hex_pixel_matrix = [encoded_file[i:i+6] for i in range(0, len(encoded_file), 6)]
    # append 0x00 bytes until the length of the hex pixel matrix is a perfect square
    hex_pixel_matrix_root = math.sqrt(len(hex_pixel_matrix))
    if not hex_pixel_matrix_root.is_integer():
        hex_pixel_matrix += ["000000"] * (int(hex_pixel_matrix_root + 1) ** 2 - len(hex_pixel_matrix))
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
        encoded_file = encode_hex(filepath)
        image_content = create_image_content_hex(encoded_file)
        create_image_hex(image_content)

if __name__ == "__main__":
    main()
