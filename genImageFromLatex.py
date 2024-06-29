import re
import sys
import os
from pdf2image import convert_from_path

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


#TODO: verify that pdf compilation was successful
#TODO: wait for os system call to finish 
#NOTE: you need to use pdflatex not pdftex to generate the file with this string
#       for example you can use os.system('pdflatex'+latex_string)
def gen_pdf_from_latex_str(latex_str:str, pdf_path:str)->bool:
    e = os.system('pdflatex '+latex_str)
    if e!=0 : return False
    os.rename('texput.pdf',pdf_path) 
    os.remove('texput.aux')
    os.remove('texput.log')
    return True

def gen_png_from_latex_str(math_str:str)->str: 
    return ''

def parse_args(argv):
    pass

def main(argv):
    pdf_path = 'latex_math.pdf'
    md_math = '$$\na^2+b^2=c^2\n$$'
    latex_math = format_latex_math(md_math) 
    success = gen_pdf_from_latex_str(latex_math, pdf_path)
    image = convert_from_path(pdf_path)[0]
    image.save('out.png', 'PNG')

if __name__=='__main__':
    print('Hello World!')
    args = parse_args(sys.argv)
    main(args)
