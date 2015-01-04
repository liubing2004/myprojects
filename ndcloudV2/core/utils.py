from enum import Enum
import os, zipfile

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