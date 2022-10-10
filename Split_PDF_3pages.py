import copy
import math
from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse
import re

import string
printable = set(string.printable)
def clean_text(text):
    """
    Removes non keyboard specific characters.
    Converts string to lower, removes sepecial characters, 
    removes numbers and strips off any extra whitespaces.
    Input : str
    output : str    
    """
    text = ''.join(filter(lambda x: x in printable, text)) 
    text=text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text=text.strip()
    return text

def split_pages2(src, dst):
    src_f = src
    dst_f = dst

    input = PdfFileReader(src_f)
    output = PdfFileWriter()

    for i in range(input.getNumPages()):
        # make three copies of the input page
        pp = input.getPage(i)
        p = copy.copy(pp)
        q = copy.copy(pp)
        r = copy.copy(pp)
        # extracting text from page
        content = pp.extractText()
        splits_cont_3_space = re.split('\s{3,}',content)
        splits_cont_2_space = re.split('\s{2,}',content)
        splits_cont_1_space = re.split('\s{1,}',content)
        # the new media boxes are the previous crop boxes
        p.mediaBox = copy.copy(p.cropBox)
        q.mediaBox = copy.copy(p.cropBox)
        r.mediaBox = copy.copy(p.cropBox)
        x1, x2 = p.mediaBox.lowerLeft
        x3, x4 = p.mediaBox.upperRight
        x1, x2 = math.floor(x1), math.floor(x2)
        x3, x4 = math.floor(x3), math.floor(x4)
        x5, x6 = x1+math.floor((x3-x1)/2), x2+math.floor((x4-x2)/2)
        x7 = x1+math.floor((x3-x1)/3)
        x8 = x7+math.floor((x3-x1)/3)
        #Splitting 3 columns into three pages
        if (len(splits_cont_3_space) == 2 and len(splits_cont_2_space) == 6) or ((len(splits_cont_2_space) == 6 or len(splits_cont_2_space) == 4) and len(clean_text(content))>8000) or (len(splits_cont_2_space) == 1 and len(splits_cont_1_space)>2000 and len(clean_text(content))>9000):
            q.mediaBox.upperRight = (x7, x4)
            q.mediaBox.lowerLeft = (x1, x2)

            p.mediaBox.upperRight = (x8, x4)
            p.mediaBox.lowerLeft = (x7, x2)

            r.mediaBox.upperRight = (x3, x4)
            r.mediaBox.lowerLeft = (x8, x2)
            p.artBox = p.mediaBox
            p.bleedBox = p.mediaBox
            p.cropBox = p.mediaBox

            q.artBox = q.mediaBox
            q.bleedBox = q.mediaBox
            q.cropBox = q.mediaBox
            
            r.artBox = r.mediaBox
            r.bleedBox = r.mediaBox
            r.cropBox = r.mediaBox

            output.addPage(q)
            output.addPage(p)
            output.addPage(r)
        #Splitting 2 columns into two pages
        elif (len(clean_text(content))>1000 and len(splits_cont_3_space)<25) or (len(splits_cont_1_space)>700 and len(clean_text(content))>1000):
            print(x1,x2,x3,x4,x5)
            q.mediaBox.upperRight = (x5, x4)
            q.mediaBox.lowerLeft = (x1, x2)

            p.mediaBox.upperRight = (x3, x4)
            p.mediaBox.lowerLeft = (x5, x2)

            p.artBox = p.mediaBox
            p.bleedBox = p.mediaBox
            p.cropBox = p.mediaBox

            q.artBox = q.mediaBox
            q.bleedBox = q.mediaBox
            q.cropBox = q.mediaBox

            output.addPage(q)
            output.addPage(p)
        else:
            p.artBox = p.mediaBox
            p.bleedBox = p.mediaBox
            p.cropBox = p.mediaBox                
            output.addPage(p)

    output.write(dst_f)

if __name__ == "__main__":
    input_file = 'Axium prime_M008876CDOC2_D_eng.pdf'
    output_file = 'Axium prime_M008876CDOC2_D_eng_modified.pdf'
    split_pages2(input_file,output_file)
