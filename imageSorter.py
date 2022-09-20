from ast import arg
from shutil import copyfile, move
from sys import argv
from PIL.ExifTags import TAGS
import PIL.Image
import os
from tkinter import *
from tkinter import filedialog
import re


def scan_dir(path):
    images = []
    for el in os.listdir(path):
        new_path = path + "/" + el
        if(os.path.isdir(new_path)):
            try:
                images = images + scan_dir(new_path)
            except Exception as e:
                continue
        if el.lower().endswith((".jpg", ".jpeg", ".png")):
            images += [new_path]
    return images


def get_datetime(exif):
    if exif:
        for (k, v) in exif.items():
            if TAGS.get(k) == "DateTime":
                return v
    return None


out_folder = None
if len(argv) == 2:
    print("Setting out_folder to", argv[1])
    out_folder = argv[1]

regex = re.compile("((20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))")
regex_dashed = re.compile(
    "((20)\d{2}(-|_)(0[1-9]|1[0-2])(-|_)(0[1-9]|[12]\d|3[01]))")

root = Tk()
root.withdraw()
base_folder = filedialog.askdirectory()


images = scan_dir(base_folder)

whatsapp_count = 0
other_string_count = 0
exif_count = 0
no_date_count = 0
regex_count = 0

dated_images = []
not_dated_images = []

print("Found", len(images), "Images")
for path in images:
    try:
        name = path.split("/")[-1]
        regex_result = regex.search(name)
        regex_dashed_result = regex_dashed.search(name)
        if regex_result:
            datetime = regex_result.group(1)
            datetime = datetime[:4] + ":" + datetime[4:6] + ":" + datetime[6:8]
            dated_images.append((path, datetime))
            regex_count += 1
        elif regex_dashed_result:
            datetime = regex_dashed_result.group(1)
            datetime = datetime[:4] + ":" + \
                datetime[5:7] + ":" + datetime[8:10]
            dated_images.append((path, datetime))
            regex_count += 1

        else:
            image = PIL.Image.open(path)
            exif = image._getexif()
            datetime = get_datetime(exif)
            if datetime:
                dated_images.append((path, datetime))
                exif_count += 1
            else:
                not_dated_images.append(path)
                no_date_count += 1

    except Exception as e:
        print(path, e)
        not_dated_images.append(path)
        no_date_count += 1
        continue

print("Len not dated:", len(not_dated_images))

print("Found", len(dated_images), "Images with DateTime (Regex:", regex_count,
      ", EXIF:", exif_count, ") and", no_date_count, "Images without DateTime")
if out_folder is None:
    out_folder = base_folder + "/output"
try:
    os.mkdir(out_folder)
except Exception as e:
    pass

no_date_folder = out_folder + "/no_date"
try:
    os.mkdir(no_date_folder)
except Exception as e:
    pass

print("Copying images with date")
percentage = 0
count = 0
percent = round(len(dated_images)/100)
for srcpath, date in dated_images:
    count += 1
    if count == percent:
        percentage += 1
        print(" ", percentage, end=" %\r", flush=True)
        count = 0

    try:
        dstpath = out_folder + "/" + date[0:4]
        try:
            os.mkdir(dstpath)
        except Exception as e:
            pass
        dstpath = dstpath + "/" + date[5:7]
        try:
            os.mkdir(dstpath)
        except Exception as e:
            pass
        dstpath = dstpath + "/" + srcpath.split("/")[-1]
        copyfile(srcpath, dstpath)

    except Exception as e:
        continue

print()
print("Copying images without date")
percentage = 0
count = 0
percent = round(len(not_dated_images)/100)
for path in not_dated_images:
    count += 1
    if count == percent:
        percentage += 1
        print(" ", percentage, end=" %\r", flush=True)
        count = 0
    try:
        copyfile(path, no_date_folder + "/" + path.split("/")[-1])
    except Exception as e:
        continue

print("")
