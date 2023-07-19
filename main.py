# import all the libraries
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL.ExifTags import TAGS
from tkinter import filedialog
from tkinter import Tk

root = Tk()
root.withdraw()

filename = filedialog.askopenfilename(initialdir='/Users/ian/Documents/GitHub/photo-timestamp')
print(filename)

def add_watermark(img, text):
    canvas = Image.open(img)
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas)
    font_size = int(width / 8)
    font = ImageFont.truetype('arial.ttf', font_size)
    x, y = int(width/2), int(height/2)
    draw.text((x,y), text, font=font, fill='#FFF', stroke_width=5, stroke_fill='#222', anchor='ms')

    canvas.show()

def get_metadata(img):
    canvas = Image.open(img)
    info_dict = {
        "Filename": canvas.filename,
        "Image Size": canvas.size,
        "Image Height": canvas.height,
        "Image Width": canvas.width,
        "Image Format": canvas.format,
        "Image Mode": canvas.mode,
        "Image is Animated": getattr(canvas, "is_animated", False),
        "Frames in Image": getattr(canvas, "n_frames", 1)
    }
    for label,value in info_dict.items():
        print(f"{label:25}: {value}")
    
    exifdata = canvas.getexif()
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")


get_metadata(filename)
# add_watermark(filename, 'meow')
