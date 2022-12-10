from PIL import ImageOps, ImageGrab, ImageEnhance
import pytesseract
import cv2
import win32gui
import re
import numpy

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)


def screenshotBluestack():
    bluestack = [(hwnd, title) for hwnd, title in winlist if 'bluestacks' in title.lower()]
    # just grab the hwnd for first window matching bluestack
    bluestack = bluestack[0]
    hwnd = bluestack[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    img = ImageEnhance.Contrast(ImageOps.grayscale(img)).enhance(10)
    return img

def quadrantImage(img) -> list:
    w, h = img.size
    split = []
    split.append(img.crop((20,300,w/3,h/2))) # top left
    split.append(img.crop((w/2.1,0,w-150,h/12))) # top right
    split.append(img.crop((0,h/2,w/2,h))) # bottom left
    split.append(img.crop((w/2,h/2,w,h))) # bottom right
    split[0].show()
    split[1].show()
    return split

def readBluestack():
    no = None
    lvl = None
    Stats = []
    gray = screenshotBluestack()
    w, h = gray.size
    pokenr = pytesseract.image_to_string(gray.crop((20, 350, w-350, h-435)))
    idNo = pytesseract.image_to_string(gray.crop((310, 770, w-40, h-20)))
    return pokenr, idNo

def readImage(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

def improveReadablility(img):
    cv_img = numpy.array(img)
    _,thresh1 = cv2.threshold(cv_img,100,255,cv2.THRESH_BINARY) 
    return thresh1

"""
@returns tuple of pokemon pokedex number, level
"""
def readPokemonStats():
    imageParts = quadrantImage(screenshotBluestack())
    # number is the only integer in the top left of the picture
    number = re.sub('\D','', pytesseract.image_to_string(imageParts[0]))
    level = re.sub('\D','', pytesseract.image_to_string(imageParts[1]))
    return number, level
    	


if __name__=="__main__":
    print(readPokemonStats())

"""
first no. =/= -> continue
lvl =/= -> continue
stats =/= -> continue

"""