from PIL import ImageOps, ImageEnhance, Image
import pytesseract
import calibrationGUI
import json
import os
import re

def calibrate(img):
    jsonpath = os.path.join(os.path.dirname(__file__), os.environ["calibration"])
    with open(jsonpath, "r") as jsonfile:
        calibration = json.load(jsonfile)
    with open(jsonpath, "w") as jsonfile:
        no, lvl,stats = calibrationGUI.run(img)
        calibration["lvl"] = list(lvl)
        calibration["no"] = list(no)
        calibration["stats"] = list(stats)
        json.dump(calibration, jsonfile, indent=4)

def getCalibration():
    jsonpath = os.path.join(os.path.dirname(__file__), os.environ["calibration"])
    with open(jsonpath, "r") as jsonfile:
        return json.load(jsonfile)

def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im

def readImage(img, calibration=False):
    # better readability options:
    # convert image to grayscale
    img = ImageOps.grayscale(img)
    # enhance contrast 10x
    img = ImageEnhance.Contrast(img).enhance(10)
    # remove alpha channel
    img = remove_transparency(img)
    # if calibration is needed, run calibrate function
    if calibration:
        calibrate(img)
    # fetch area calibration
    calibration = getCalibration()
    # crop the image in readable parts
    lvlimg = img.crop(tuple(calibration["lvl"]))
    # invert the lvlimg to get black text on white background
    lvlimg = ImageOps.invert(lvlimg)
    noimg = img.crop(tuple(calibration["no"]))
    statsimg = img.crop(tuple(calibration["stats"]))
    # read only digits in the 3 images
    no = re.sub('\D','', pytesseract.image_to_string(noimg))
    lvl = re.sub('\D','', pytesseract.image_to_string(lvlimg))
    stats = re.sub('\D','', pytesseract.image_to_string(statsimg))
    # return results
    return no, lvl, stats

def readBluestacks(calibration=False):
    path = os.path
    img = Image.open(path.join(path.dirname(__file__), "data", "screenshot", "screenshot.png"))
    return readImage(img, calibration)

def run(calibration=False):
    lvl, no, stats = readBluestacks(calibration=calibration)
    print("no: ", no, " lvl: ", lvl, " stats: ", stats)

if __name__=="__main__":
    run()
    

"""
first no. =/= -> continue
lvl =/= -> continue
stats =/= -> continue

"""