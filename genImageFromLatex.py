import re
import sys
import os
from pdf2image import convert_from_path


def get_dir_from_path(path:str)->str:
    return re.sub(r'[^/]+\.pdf', '', pdf_path)

#Takes in a mardown math string that looks something like this:
#   $$
#   a+b=c
#   $$
#Returns a latex equivalent lieke this:
#   \usepackage{amsmath}\begin{align*}a+b=c\end{align*}
def format_latex_math(math_str:str)->str:
    regex_pattern = r'(\$\$\n)'
    header_str = r'"\documentclass[preview]{standalone}\usepackage{amsmath}\begin{document}\begin{align*}'
    math_str = re.sub(regex_pattern, '', math_str, count=1, flags=re.M)
    regex_pattern = r'\n\$\$'
    math_str = re.sub(regex_pattern, '', math_str, count=1, flags=re.M)
    end_str = r'\end{align*}\end{document}"'
    return header_str + math_str + end_str

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

def gen_png_from_md_math_str(md_math_str, png_path)->bool:
    latex_str = format_latex_math(md_math_str)
    if not(gen_png_from_latex_str(latex_str, png_path)): return False
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

#md_math_str = '$$\na^2+b^2=c^2\n$$' 
#png_path = os.path.expanduser('~/Notes/images/test.png')
#gen_png_from_md_math_str(md_math_str, png_path)    
