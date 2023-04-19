# Import needed librairy
import time, random
import PIL.Image

def print_ascii_art (file_path, scale, t):
    ASCII_CHARS = list()
    image = PIL.Image.open(file_path)
    width, height = image.size
    width = int(width/scale)
    height = int(height/scale)
    image = image.resize((width, height))
    image = image.convert("L")
    pixels = image.getdata()
    ascii_str = ""
    k = 0
    for pixel in pixels:
        if pixel < 50:
            ascii_str += chr(random.randint(33, 126))
            k += 1
            if k > 5:
                k = 0
        else:
            ascii_str += " "

    for i in range(height):
        for j in range(width):
             print(ascii_str[i*width + j], end=" ")
        print(" ")
        time.sleep(t)

def timed_print (file, t, end_time):
    with open(file, "r", encoding="utf-8") as f:
        s = f.readline()
        print(s)
        time.sleep(t)
        while s:
            s = f.readline()
            print(s)
            time.sleep(t)
    time.sleep(end_time)

def store_file_text (file):
    text = ""
    with open(file, "r") as f:
        text = f.readlines()
    return text