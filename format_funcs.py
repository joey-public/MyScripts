import re
import os
import subprocess as sbp
from pdf2image import convert_from_path

LATEX_TIMEOUT = 1.0
#'''Create a path to an image 
#arguments: 
#    n -- The nth math image in the file
#    md_file_name -- The name of the markdown file (this is used when generating the image link)
#    img_dir -- The directory the generated image will be stored 
#    img_fmt -- The format of the generated image
#returns:
#     img_path -- the path to the image 
#'''
def _create_image_path(n:str, md_file_name:str, img_dir:str, img_fmt:str)->str:
    return f'{img_dir}{md_file_name}_math_{n}{img_fmt}'

def _save_latex_file(latex_str:str, file_path:str)->None:
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

#NOTE: you need to use pdflatex not pdftex to generate the file with this string
#       for example you can use os.system('pdflatex'+latex_string)
#NOTE: it works best to just create a .tex file write to it and then call 
#       'pdflatex file_path.tex'
def _gen_pdf_from_latex_str(latex_str:str, pdf_path:str)->bool:
    pdf_file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    temp_str = os.path.splitext(pdf_path)[0]
    tex_path = temp_str + '.tex'
    pdf_dir = os.path.dirname(pdf_path)
    with open(tex_path, 'w', encoding='utf-8') as output_file:
        output_file.write(latex_str)
#    cmd = f'pdflatex -output-directory {pdf_dir} '+tex_path
    cmd = ['pdflatex', f'-output-directory', f'{pdf_dir}', f'{tex_path}']
    out = sbp.run(cmd, capture_output='True', timeout=LATEX_TIMEOUT)
    e = out.stderr
    if e!=b'': return False
    os.remove(temp_str + '.aux')
    os.remove(temp_str + '.log')
    os.remove(temp_str + '.tex')
    return True

#given a latex_style math str generate a png image of the math and save it 
#    to the passed png_path
def _gen_png_from_latex_str(math_str:str, png_path:str)->bool: 
    temp_str = os.path.splitext(png_path)[0]
    pdf_path = temp_str + '.pdf'
    if not(_gen_pdf_from_latex_str(math_str, pdf_path)): return False 
    image = convert_from_path(pdf_path)[0]
    image.save(png_path, 'SVG')
    os.remove(pdf_path)
    return True

#'''Convert a markdown style math string to latex style.
#arguments:
#    md_math_str -- a markdown string in the following style:
#    $$
#    a+b=c
#    $$
#returns: 
#    latex_str -- a latex style math strin in the following stlye:
#    \documentclass[preview]{standalone}\usepackage{amsmath}\begin{document}\begin{align*}a+b=c\end{align*}\end{document}
#'''
def _convert_md_math_to_latex_math(md_math_str:str)->str:
    regex_pattern = r'(\$\$\n)'
    header_str = r'\documentclass[preview]{standalone}\usepackage{amsmath}\begin{document}\begin{align*}'
    math_str = re.sub(regex_pattern, '', md_math_str, count=1, flags=re.M)
    regex_pattern = r'\n\$\$'
    math_str = re.sub(regex_pattern, '', math_str, count=1, flags=re.M)
    end_str = r'\end{align*}\end{document}'
    latex_str = header_str + math_str + end_str
    return header_str + math_str + end_str


#'''Loop through a md_file_str and replace all math block with image links
#arguments: 
#    md_file_str -- The contents of the markdown file to be converted
#    md_file_name -- The name of the markdown file (this is used when generating the image link)
#    img_dir -- The directory the generated image will be stored 
#    img_fmt -- The format of the generated image
#returns:
#    result_str -- A new string that replaces all the markdown style math with image links
#'''
def replace_md_math_with_img_links(md_file_str:str, md_file_name, img_dir:str, img_fmt:str)->str:
    MD_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
    p_obj = re.compile(MD_MATH_PATTERN)
    result_str = md_file_str
    cnt = 0
    while(True):
        match = p_obj.search(result_str)
        if match==None:
            break
        match_str = match.group(0)
        img_path = _create_image_path(str(cnt), md_file_name, img_dir, img_fmt)
        img_link = f'![math_{cnt}]({img_path})'
        result_str = p_obj.sub(img_link, result_str, count = 1) 
        cnt += 1
    return result_str


#'''Seach through md_file_str and generate a png image for each match block
#arguments:
#    md_file_str -- The contents of the markdown file to be converted
#    md_file_name -- The name of the markdown file (this is used when generating the image link)
#    img_dir -- The directory the generated image will be stored 
#    img_fmt -- The format of the generated image
#returns:
#    True/False -- suscessful/failed
#'''
def gen_math_images_from_md_str(md_file_str:str, md_file_name, img_dir:str, img_fmt:str)->bool:
    MD_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
    MAX_CNT = 25 
    p_obj = re.compile(MD_MATH_PATTERN)
    result_str = md_file_str
    cnt = 0
    while(True):
        match = p_obj.search(result_str)
        if match==None:
            break
        if cnt > MAX_CNT: 
            print(f'Over {MAX_CNT} images...stopping')
        match_str = match.group(0)
        latex_str = _convert_md_math_to_latex_math(match_str)
        img_path = _create_image_path(cnt, md_file_name, img_dir, img_fmt) 
        result_str = p_obj.sub('', result_str, count=1)
        _gen_png_from_latex_str(latex_str, img_path)
        cnt += 1
