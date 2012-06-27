#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except:
    import Image, ImageDraw, ImageFont, ImageEnhance

class ImpropertlyConfigured(Exception):
    pass



def ReduceOpacity(im, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def Imprint(im, inputtext, font=None, color=None, opacity=0.6, margin=(30,30)):
    """
    imprints a PIL image with the indicated text in lower-right corner
    """
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)
    textsize = textdraw.textsize(inputtext, font=font)
    textpos = [im.size[i]-textsize[i]-margin[i] for i in [0,1]]
    textdraw.text(textpos, inputtext, font=font, fill=color)
    if opacity != 1:
        textlayer = ReduceOpacity(textlayer,opacity)
    return Image.composite(textlayer, im, textlayer)

def watermark(image, text, font_path, font_scale=None, font_size=None, color=(0,0,0), opacity=0.6, margin=(30, 30)):
    """
    image - PIL Image instance
    text - text to add over image
    font_path - font that will be used
    font_scale - font size will be set as percent of image height
    """
    if font_scale and font_size:
        raise ImpropertlyConfigured("You should provide only font_scale or font_size option, but not both")
    elif font_scale:
        width, height = image.size
        font_size = int(font_scale*height)
    elif not (font_size or font_scale):
        raise ImpropertlyConfigured("You should provide font_scale or font_size option")
    font=ImageFont.truetype(font_path, font_size)
    im0 = Imprint(image, text, font=font, opacity=opacity, color=color, margin=margin)
    return im0