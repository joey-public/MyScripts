import re
import sys
import os
from pdf2image import convert_from_path

#NOTE: you need to use pdflatex not pdftex to generate the file with this string
#       for example you can use os.system('pdflatex'+latex_string)
def gen_pdf_from_latex_str(latex_str:str, pdf_path:str)->bool:
    e = os.system(f'pdflatex '+latex_str)
    if e!=0 : return False
    os.rename('texput.pdf',pdf_path) 
    os.remove('texput.aux')
    os.remove('texput.log')
    return True

#given a latex_style math str generate a png image of the math and save it 
#    to the passed png_path
def gen_png_from_latex_str(math_str:str, png_path:str)->bool: 
    pdf_path = png_path[0:-3] + 'pdf'
    if not(gen_pdf_from_latex_str(math_str, pdf_path)): return False 
    image = convert_from_path(pdf_path)[0]
    image.save(png_path, 'PNG')
    os.remove(pdf_path)
    return True


def gen_math_images(md_file_name, md_text, img_dir):
    cnt = 0
    while(True):
        LABELED_MATH_PATTERN = f'math_{cnt}'+r'\n\$\$[^$]+\$\$'
        match = re.search(LABELED_MATH_PATTERN, md_text)
        if(match==None):
            break
        match_str = match.group(0) 
        md_math_str = match_str[7:]
        img_path = f'{img_dir}{md_file_name}_math_{cnt}.png'
        gen_png_from_md_math_str(md_math_str, img_path)
        cnt+=1
