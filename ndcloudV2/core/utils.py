from enum import Enum
import os, zipfile

class ProjectStatus(Enum):
    submit = 0
    success = 1
    fail = 2

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