import sys
import os
import math
import tqdm
import PIL.Image

# Global Variables
SILENT = False
ASPECT_RATIO = "1:1"

def main():

    if len(sys.argv) < 2:
        log("Usage: python encode.py <filepath>")
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "-q":
            global SILENT
            SILENT = True

        progress_bar = tqdm.tqdm(total=os.path.getsize(filepath), unit="byte", unit_scale=True)

        log(f">>> Preparing Filename: {filepath}")
        filename = os.path.basename(filepath)
        filename_hex = filename.encode("utf-8").hex()
        log(f"Filename Hex: {filename_hex}")
        log(f"Filename Hex Byte Count: {len(filename_hex) / 2}")
        log(f"Filename 6 Byte Blocks: {len(filename) / 6}")
        # calculate hex bytes for filename
        # append /r/n to filename and fill with 00 until full 6 byte block
        filename_hex += "0a0d"
        while len(filename_hex) / 2 % 6 != 0:
            filename_hex += "00"
        log(f"Optimized Filename Hex: {filename_hex}")
        log(f"Optimized Filename Hex Byte Count: {len(filename_hex) / 2}")
        log("")

        log(f">>> Preparing File: {filepath}")
        file_byte_count = os.path.getsize(filepath)
        filename_byte_count = len(filename_hex) / 2
        encoded_byte_count = filename_byte_count + file_byte_count
        log(f"File Byte Count: {encoded_byte_count}")
        log(f"File 6 Byte Blocks: {encoded_byte_count / 6}")
        while encoded_byte_count % 6 != 0:
            encoded_byte_count += 1
        log(f"Optimized File Byte Count: {encoded_byte_count}")
        log(f"Optimized File 6 Byte Blocks: {encoded_byte_count / 6}")
        log("")

        # open encoded image_file with the needed size to receive the encoded stream
        log(">>> Creating Image")
        encoded_image = open("encoded.png", "wb")
        encoded_image_size = int(math.ceil(math.sqrt(encoded_byte_count / 6)))
        encoded_image = PIL.Image.new("RGB", (encoded_image_size, encoded_image_size))
        log(f"Image Y Size: {encoded_image_size}")
        log(f"Image X Size: {encoded_image_size}")
        log(f"Image Pixel Size (1 Byte = 1 Pixel): {encoded_image_size * encoded_image_size}")

        # write filename to image
        log("")
        log(">>> Writing Filename to Image")
        filename_hex_bytes = bytes.fromhex(filename_hex)
        buffer = filename_hex_bytes
        pixel_max_x_pos = encoded_image_size - 1
        pixel_pos = (0, 0)
        sourcefile_byte_index = 0
        while buffer:
            pixel_pos = write_byte_buffer_to_image(encoded_image, buffer[:6], pixel_pos, pixel_max_x_pos, sourcefile_byte_index)
            sourcefile_byte_index += 6
            buffer = filename_hex_bytes[sourcefile_byte_index:]
            progress_bar.update(6)

        # write file to image
        log("")
        log(">>> Writing File to Image")
        file = open(filepath, "rb")
        buffer = file.read(6) # read 6 bytes at a time
        pixel_max_x_pos = encoded_image_size - 1
        pixel_pos = pixel_pos
        sourcefile_byte_index = 0
        while buffer:
            pixel_pos = write_byte_buffer_to_image(encoded_image, buffer, pixel_pos, pixel_max_x_pos, sourcefile_byte_index)
            sourcefile_byte_index += 6
            buffer = file.read(6)
            progress_bar.update(6)
        file.close()
        encoded_image.save("encoded.png")
        progress_bar.close()

def write_byte_buffer_to_image(image, buffer, pixel_pos, pixel_pos_max_x, byte_index):
    if len(buffer) < 6:
        log(f">>> Last Buffer: {len(buffer)} bytes - appending {6 - len(buffer)} null bytes")
        buffer_diff = 6 - len(buffer)
        buffer += b"\x00" * buffer_diff
    color = byte_block_into_color(buffer)
    image.putpixel(pixel_pos, color)
    # move to next pixel in pixel matrix
    if pixel_pos[0] == pixel_pos_max_x:
        pixel_pos = (0, pixel_pos[1] + 1)
    else:
        pixel_pos = (pixel_pos[0] + 1, pixel_pos[1])
    log(f"Byte: {byte_index} - Pixel Coordinate: {pixel_pos}- Hex: {buffer}")
    log(f"Byte: {byte_index} - Pixel Color: {color} - Hex: {buffer}")
    return pixel_pos

# convert 6 byte-block into rgb color
def byte_block_into_color(byte_block):
    byte_block_hex = byte_block.hex()
    color = tuple(int(byte_block_hex[i:i+2], 16) for i in (0, 2, 4))
    return color

def calculate_encoded_image_size(encoded_byte_count):
    if encoded_byte_count % 6 != 0:
        encoded_byte_count += 6 - encoded_byte_count % 6
    aspect_ratio = ASPECT_RATIO.split(":")
    aspect_ratio_x = int(aspect_ratio[0])
    aspect_ratio_y = int(aspect_ratio[1])
    width = int(math.sqrt(encoded_byte_count / (aspect_ratio_x / aspect_ratio_y)))
    height = int(width * (aspect_ratio_y / aspect_ratio_x))
    return width, height

def log(message):
    if SILENT:
        pass
    else:
        print(message)
    
if __name__ == "__main__":
    main()
