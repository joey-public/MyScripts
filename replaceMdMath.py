import re
import os
import sys
from genImageFromLatex import gen_png_from_md_math_str

#DEFAULT_IMG_DIR = os.path.expanduser('~/Notes/images/math/')


def save_str_to_file(path:str, text_str:str)->None:
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(text_str)

def gen_image_link_from_md_math_str(md_file_name:str, n:int, image_dir:str, file_extension='png'):
    return f'![MMMM_{n}]({image_dir}{md_file_name}_math_{n}.{file_extension})'


def format_md_str_math(md_file_name, md_str:str, img_dir:str)->str:
    MATH_IMAGE_PATTERN = r'(!\[math_\d\]\(.+\d\.png\))'
    UNLABELED_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
    MATH_SECTION_PATTERN = r'### Math Blocks'
    #![math_n](path)
    #       7  
    #0123456789
    MATH_IMAGE_N_IDX = 7 
    MAX_CNT = 10
    result = (re.split(MATH_SECTION_PATTERN, md_str))
    math_block_str = ''
    if len(result)==1: 
        old_math_blocks = ''
        result_str = md_str
    else: 
        old_math_blocks = result[1]
        result_str = result[0]
    cnt = 0
    regex_pattern = re.compile(MATH_IMAGE_PATTERN + '|' + UNLABELED_MATH_PATTERN)
    while(True):
        match = regex_pattern.search(result_str)
        if(match==None or cnt>MAX_CNT):
            break
        match_str = match.group(0)
        if match_str[0]=='!': 
            n = int(match_str[MATH_IMAGE_N_IDX])
            math_scrap = re.search(f'math_{n}'+r'\n\$\$[^\$]+\$\$', old_math_blocks).group(0)        
            math_block_str += '\n'+re.sub(f'math_{n}', f'math_{cnt}', math_scrap)
            img_link = gen_image_link_from_md_math_str(md_file_name, cnt, img_dir)
            result_str = re.sub(MATH_IMAGE_PATTERN, img_link, result_str, count=1)
        else: 
            math_block_str += f'\nmath_{cnt}\n'+match_str
            img_link = gen_image_link_from_md_math_str(md_file_name, cnt, img_dir)
            result_str = re.sub(UNLABELED_MATH_PATTERN, img_link, result_str, count=1)
        cnt+=1
    result_str = result_str + '\n\n' + MATH_SECTION_PATTERN + '\n\n' + math_block_str
    result_str = re.sub(r'MMMM_', 'math_', result_str)
    return result_str

    
        
#md_path = 'tests1_in.md'
#md_file_name = md_path[0:-3]
#output='temp.md'
#md_str = read_txt_file(md_path)  
#result_str = format_md_str_math(md_file_name, md_str)
#gen_math_images(md_file_name, result_str, DEFAULT_IMG_DIR)
#save_str_to_file(output, result_str)
