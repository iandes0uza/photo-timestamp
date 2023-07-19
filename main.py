# import all the libraries
from PIL import Image, ExifTags
from PIL import ImageFont
from PIL import ImageDraw
from PIL.ExifTags import TAGS, Base
from tkinter import filedialog
from tkinter import Tk

root = Tk()
root.withdraw()

filename = filedialog.askopenfilename(initialdir='/Users/ian/Documents/GitHub/photo-timestamp')
# print(filename)

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
    font_size = int(width / 20)
    font = ImageFont.truetype('seven_segment.ttf', font_size)
    x, y = int(width/3), int(height/3)
    draw.text((0,0), text, font=font, fill='#FFFF00', stroke_width=1, stroke_fill='#222', anchor='rs')
    img.show()

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
    # Open image 
    image = Image.open(filename)
    watermark = parse_metadata(image)
    add_watermark(image, watermark.format_dateAndTime())

if __name__ == "__main__":
    main()