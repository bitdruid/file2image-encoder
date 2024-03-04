import base64
import sys
import zlib
import PIL.Image

# all grey scale colors with 8 bit depth and very light
B64_RGB_DICT = {
    (188, 188, 188): "A",
    (189, 189, 189): "B",
    (190, 190, 190): "C",
    (191, 191, 191): "D",
    (192, 192, 192): "E",
    (193, 193, 193): "F",
    (194, 194, 194): "G",
    (195, 195, 195): "H",
    (196, 196, 196): "I",
    (197, 197, 197): "J",
    (198, 198, 198): "K",
    (199, 199, 199): "L",
    (200, 200, 200): "M",
    (201, 201, 201): "N",
    (202, 202, 202): "O",
    (203, 203, 203): "P",
    (204, 204, 204): "Q",
    (205, 205, 205): "R",
    (206, 206, 206): "S",
    (207, 207, 207): "T",
    (208, 208, 208): "U",
    (209, 209, 209): "V",
    (210, 210, 210): "W",
    (211, 211, 211): "X",
    (212, 212, 212): "Y",
    (213, 213, 213): "Z",
    (214, 214, 214): "a",
    (215, 215, 215): "b",
    (216, 216, 216): "c",
    (217, 217, 217): "d",
    (218, 218, 218): "e",
    (219, 219, 219): "f",
    (220, 220, 220): "g",
    (221, 221, 221): "h",
    (222, 222, 222): "i",
    (223, 223, 223): "j",
    (224, 224, 224): "k",
    (225, 225, 225): "l",
    (226, 226, 226): "m",
    (227, 227, 227): "n",
    (228, 228, 228): "o",
    (229, 229, 229): "p",
    (230, 230, 230): "q",
    (231, 231, 231): "r",
    (232, 232, 232): "s",
    (233, 233, 233): "t",
    (234, 234, 234): "u",
    (235, 235, 235): "v",
    (236, 236, 236): "w",
    (237, 237, 237): "x",
    (238, 238, 238): "y",
    (239, 239, 239): "z",
    (240, 240, 240): "0",
    (241, 241, 241): "1",
    (242, 242, 242): "2",
    (243, 243, 243): "3",
    (244, 244, 244): "4",
    (245, 245, 245): "5",
    (246, 246, 246): "6",
    (247, 247, 247): "7",
    (248, 248, 248): "8",
    (249, 249, 249): "9",
    (250, 250, 250): "+",
    (251, 251, 251): "/",
    (252, 252, 252): "=",
    (253, 253, 253): "\n",
    (254, 254, 254): "\r",
    (255, 255, 255): " "
}

def decode(encoded_filename, encoded_content):
    try:
        decoded_filename = base64.b64decode(encoded_filename).decode("utf-8")
        with open(decoded_filename, "wb") as file:
            decoded_content = zlib.decompress(base64.b64decode(encoded_content))
            #decoded_content = base64.b64decode(encoded_content)
            file.write(decoded_content)
    except Exception as e:
        print(e)

def read_image_content(filepath):
    pixel_matrix = []
    try:
        image = PIL.Image.open(filepath)
        pixel_matrix = list(image.getdata())
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
    encoded_content = ""
    encoded_filename_found = False
    encoded_filename_delimiter = False
    encoded_filename = ""
    for pixel in pixel_matrix:
        if pixel == (255, 255, 255):
            continue
        if not encoded_filename_found:    
            if not encoded_filename_delimiter:
                if pixel == (253, 253, 253):
                    encoded_filename_delimiter = True
                    continue
                encoded_filename += B64_RGB_DICT[pixel]
            if encoded_filename_delimiter:
                if pixel == (254, 254, 254):
                    encoded_filename_found = True
                    continue
                encoded_filename_delimiter = False
        if encoded_filename_found:
            encoded_content += B64_RGB_DICT[pixel]
    return encoded_filename, encoded_content
        


def main():
    if len(sys.argv) != 2:
        print("Usage: python decode.py <filepath>")
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        encoded_filename, encoded_content = read_image_content(filepath)
        decode(encoded_filename, encoded_content)
        print("File decoded.")

if __name__ == "__main__":
    main()
