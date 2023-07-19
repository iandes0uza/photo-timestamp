# import all the libraries
from PIL import Image, ImageFont, ImageDraw
from PIL.ExifTags import TAGS
from tkinter import filedialog, Tk
import os, shutil

# Watermark object, stores values from parser and returns watermark string
class wmk:
    def __init__(self, d, m, y, hr, min, sec):
        self.d = d
        self.m = m
        self.y = y
        self.hr = hr
        self.min = min
        self.sec = sec

    def format_date(self):
        return (str(self.m) + "/" + str(self.d) + "/" + str(self.y))
    def format_dateAndTime(self):
        return (self.format_date() + " " +  str(self.hr) + ":" + str(self.min) + ":" + str(self.sec))

# This function adds the watermark to the photo
def add_watermark(img, text):
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('seven_segment.ttf', int(width / 30))
    textwidth, textheight = draw.textsize(text, font)
    x = width - textwidth - 45
    y = height - textheight - 25
    draw.text((x,y), text, font=font, fill='#FFFF00', stroke_width=1, stroke_fill='#222')

# This function grabs the timestamp from the image's EXIF data
def get_timestamp(img_exif):
    for (k,v) in img_exif.items():
        if TAGS.get(k) == 'DateTimeOriginal':
            return v

# This function splits timestamp into seperate sections (d/m/y etc). This portion changes based on how EXIF data is read        
def parse_metadata(img):
    exif = img._getexif()
    timestamp = str(get_timestamp(exif))
    date, time = timestamp.split(' ')
    y, m, d = date.split(':')
    hr, min, sec = time.split(':')
    return wmk(d, m, y, hr, min, sec)

def main():
    root = Tk()
    root.withdraw()
    filepath = filedialog.askdirectory(initialdir='/Users/ian/Documents/GitHub/photo-timestamp')
    files = list(filter(lambda f: f.lower().endswith(('.jpg', '.jpeg', '.png')), os.listdir(filepath)))
    dest_path = os.path.join(filepath, "Time_Stamped")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.makedirs(dest_path)
    print(files)
    # Open images 
    for imgpath in files:
        print(imgpath)
        image = Image.open(filepath+"/"+imgpath)
        watermark = parse_metadata(image)
        add_watermark(image, watermark.format_dateAndTime())
        image.save(f"{dest_path}/{imgpath}")

if __name__ == "__main__":
    main()