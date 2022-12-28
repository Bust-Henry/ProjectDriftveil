from PIL import ImageOps, ImageEnhance, Image
import pytesseract

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

def readAll(img):
    # better readability options:
    # convert image to grayscale
    img = ImageOps.grayscale(img)
    # enhance contrast 10x
    img = ImageEnhance.Contrast(img).enhance(10)
    # remove alpha channel
    img = remove_transparency(img)
    return pytesseract.image_to_string(img) 

def readBoxes(img):
    # better readability options:
    # convert image to grayscale
    img = ImageOps.grayscale(img)
    # enhance contrast 10x
    img = ImageEnhance.Contrast(img).enhance(10)
    # remove alpha channel
    img = remove_transparency(img)
    return pytesseract.image_to_boxes(img) 