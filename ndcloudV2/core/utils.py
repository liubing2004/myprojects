from enum import Enum
import os, zipfile, hashlib
import StringIO
from PIL import Image, ImageOps
import os
from django.core.files import File

class ProjectStatus(Enum):
    submit = 0
    success = 1
    fail = 2
    
class OrderStatus(Enum):
    submit = 0
    success = 1
    fail = 2
    
class Material(Enum):
    plastic = "plastic"
    resin = "resin"
    alumide = "alumide"
    multicolor = "multicolor"
    ceramic = "ceramic"
    
class SizeUnit(Enum):
    cm = "cm"
    mm = "mm"
    
class Color(Enum):
    white = "white"
    red = "red"
    black = "black"
    blue = "blue"
    green = "green"
    yellow = "yellow" 
    

def getColorHex(color):
    print "utils:", color, Color.white
    if color == Color.white:
        return "0xFFFFFF"
    elif color == Color.black:
        return "0x000000"
    elif color == Color.red:
        return "0xFF0000"
    elif color == Color.blue:
        return "0x0000FF"
    elif color == Color.green:
        return "0x00FF00"
    elif color == Color.yellow:
        return "0xFFFF00"
        
    
    
    
    

def isValidImageName(img_name):
    img_name = img_name.lower()
    return img_name.endswith("jpg") or img_name.endswith("png") \
            or img_name.endswith("jpeg") or img_name.endswith("bmp")
            
def getFileExtension(file_name):
    extension = os.path.splittext('tmpmodel.zip')[1][1:]
    return extension

def extractZipfile(zipfiles, outpath):
    z = zipfile.ZipFile(zipfiles, "r")
    for fn in z.namelist():
        bytes = z.read(fn)
        filename = fn.split("/")[-1]
        outf = open(outpath+filename, 'w')
        outf.write(bytes)
        outf.close()
        

def handle_uploaded_image(i, destdir, width, height):
    # read image from InMemoryUploadedFile
    image_str = ""
    for c in i.chunks():
        image_str += c
    

    # create PIL Image instance
    imagefile  = StringIO.StringIO(image_str)
    image = Image.open(imagefile)
    
    # if not RGB, convert
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    
    #define file output dimensions (ex 60x60)
    x = width
    y = height

    #get orginal image ratio
    img_ratio = float(image.size[0]) / image.size[1]

    # resize but constrain proportions?
    if x==0.0:
        x = y * img_ratio
    elif y==0.0:
        y = x / img_ratio

    # output file ratio
    resize_ratio = float(x) / y
    x = int(x); y = int(y)

    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * image.size[1] / y
        output_height = image.size[1]
        originX = image.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = image.size[0]
        output_height = y * image.size[0] / x
        originX = 0
        originY = image.size[1] / 2 - output_height / 2
    
    #crop
    cropBox = (originX, originY, originX + output_width, originY + output_height)
    image = image.crop(cropBox)
    # resize (doing a thumb)
    image.thumbnail([x, y], Image.ANTIALIAS)
    
    
    # re-initialize imageFile and set a hash (unique filename)
    m = hashlib.md5()
    m.update(i.name)
    filename =  m.hexdigest() +".jpg"

    #save to disk
    imagefile = open(os.path.join(destdir,filename), 'w')
    image.save(imagefile,'JPEG', quality=90)
    return filename
