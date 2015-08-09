from PIL import Image
from operator import itemgetter
import hashlib
import time
import math
import os

class ImageDecoder(object):
    WHITE_COLOR = 255
    _in_image = None
    _out_image = None  
    DASH_LEN = 4  
    def __init__(self, settings, comparator):
        self._path = settings['icons_path']        
        self._iconset = settings['iconset']
        self._comparator = comparator
    
    def _get_color_index(self, im):       
        his = im.histogram()
        values = {}
        for i in range(256):
            values[i] = his[i]        
        result = sorted(values.items(), key=itemgetter(1), reverse=True)[:2]  
        return result[1][0] 
    
    def _set_in_image(self, file_name):
        if not self._in_image:
            self._in_image = Image.open(file_name)
            self._in_image = self._in_image.convert("P")
            self._color_index = self._get_color_index(self._in_image)
        
    def _get_out_image(self):
        if not self._out_image:
            self._out_image = Image.new('P', self._in_image.size, self.WHITE_COLOR)
            temp = {}            
            for x in range(self._in_image.size[1]):
                for y in range(self._in_image.size[0]):
                    pix = self._in_image.getpixel((y,x))
                    temp[pix] = pix
                    if pix == self._color_index:
                        self._out_image.putpixel((y,x),0)            
            self._clear_dashes(self._out_image)
        return self._out_image
    
    def _clear_dashes(self, im):
        pixdata = im.load()
        dash = []       
        for x in range(self._in_image.size[0]): #width
            pix_in_vline = []
            for y in range(self._in_image.size[1]): #height
                if pixdata[x, y] == self._color_index:
                    pix_in_vline.append((x, y))            
            if len(pix_in_vline) == 1:
                if dash and dash[-1][1] != pix_in_vline[0][1]:
                    del dash[:]
                dash.append(pix_in_vline[0])
            else:
                del dash[:]
            if len(dash) == self.DASH_LEN:
                for pix in dash:
                    pixdata[pix[0], pix[1]] = self.WHITE_COLOR
                del dash[:]
        
    def _prepare_letters(self, max_len=6):  
        inletter = foundletter = False        
        start = end = 0  
        letters = []    
        for y in range(self._get_out_image().size[0]):    # slice across
            for x in range(self._get_out_image().size[1]):    # slice down
                pix = self._get_out_image().getpixel((y, x))
                if pix != self.WHITE_COLOR:
                    inletter = True
            if foundletter == False and inletter == True:
                foundletter = True
                start = y        
            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                line_len = end - start
                if line_len <= max_len:            
                    letters.append((start, end))
                else:
                    steps = line_len // max_len
                    new_start = start
                    for x in range(1, steps+1):                
                        new_end = start + x * max_len
                        new_end = new_end if new_end < end-1 else end
                        letters.append((new_start, new_end))
                        new_start = new_end
            inletter = False        
        if max_len==1000:            
            l = [letter[1]-letter[0] for letter in letters]             
            return self._prepare_letters(int(sum(l) / len(l)))
        return letters 
    
    def split_image(self, image_file):
        self._set_in_image(image_file)
        count = 0
        for letter in self._prepare_letters():
            m = hashlib.md5()
            croped_image = self._get_out_image().crop(( letter[0] ,0, letter[1], self._get_out_image().size[1] ))
            m.update("%s%s"%(time.time(), count))
            file_name = "%s.png" % count             
            croped_image.save(os.path.join(self._path, file_name))
            count += 1
    
    def buildvector(self, image):
        d1 = {}
        count = 0
        for i in image.getdata():
            d1[count] = i
            count += 1    
        return d1
       
    def _imageset(self):
        imageset = []
        for letter in self._iconset:
            temp = []             
            for img in os.listdir(os.path.join(self._path, letter)):                      
                temp.append(self.buildvector(Image.open(os.path.join(self._path, letter, img))))
            imageset.append({letter:temp})
        return imageset
    
    def _get_result(self):
        result = []
        probabilities = []                
        for letter in self._prepare_letters():    
            croped_image = self._get_out_image().crop((letter[0], 0, letter[1], self._get_out_image().size[1]))
            guess = []
            for image in self._imageset():
                for letter,incons in image.iteritems():
                    for icon in incons:
                        guess.append((self._comparator.relation(icon, self.buildvector(croped_image)), letter))
            guess.sort(reverse=True)   
#             print "",guess[0] 
            result.append(guess[0][1])
            probabilities.append(guess[0][0])
        probability = sum(probabilities) / len(probabilities)
        return (result, probability)
    
    def decode(self, file_name):
        self._set_in_image(file_name)
        return self._get_result()


class VectorCompare(object):
    def magnitude(self,concordance):
        total = 0
        for count in concordance.itervalues():
            total += count ** 2
        return math.sqrt(total)

    def relation(self,concordance1, concordance2):        
        topvalue = 0
        for word in concordance1.iterkeys():
            if concordance2.has_key(word):                
                topvalue += concordance1[word] * concordance2[word]
        relevance = topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))        
        return round(relevance, 2)

