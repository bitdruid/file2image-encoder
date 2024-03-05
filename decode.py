import sys
import zlib
import PIL.Image

def decode(encoded_file, output=None):
    try:
        decoded_filename = bytes.fromhex(encoded_file.split("0a0d")[0]).decode("utf-8")
        decoded_content = bytes.fromhex(encoded_file.split("0a0d")[1])
        with open("decoded_" + decoded_filename, "wb") as file:
            decoded_content = zlib.decompress(decoded_content)
            file.write(decoded_content)
    except Exception as e:
        stacktrace = e.with_traceback(e.__traceback__)
        line = e.__traceback__.tb_lineno
        print(f"An error occurred: {e}")
        print(f"Line: {line}")
        print(f"Stacktrace: {stacktrace}")


def read_image_content(hex_pixel_matrix: list) -> str:
    encoded_file = ""
    for hex_pixel in hex_pixel_matrix:
        encoded_file += hex_pixel
    encoded_file = encoded_file.rsplit("0a0d", 1)[0]
    return encoded_file
    

def read_image(filepath):
    hex_pixel_matrix = []
    try:
        image = PIL.Image.open(filepath)
        pixel_matrix = list(image.getdata())
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
    for pixel in pixel_matrix:
        hex_pixel_matrix.append("".join([f"{hex(color)[2:].zfill(2)}" for color in pixel]))
    return hex_pixel_matrix
        


def main():
    if len(sys.argv) != 2:
        print("Usage: python decode.py <filepath>")
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        hex_pixel_matrix = read_image(filepath)
        encoded_file = read_image_content(hex_pixel_matrix)
        decode(encoded_file)
        print("File decoded.")

if __name__ == "__main__":
    main()
