import re
import os
import sys


DEFAULT_IMG_DIR = os.path.expanduser('~/Notes/images/math/')

def read_txt_file(path:str)->str:
    with open(path, 'r', encoding='utf-8') as input_file:
        txt_str=input_file.read()
    return txt_str

def save_str_to_file(path:str, text_str:str)->None:
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(text_str)

def gen_image_link_from_md_math_str(md_file_name:str, n:int, image_dir:str=DEFAULT_IMG_DIR, file_extension='png'):
    return f'![math_{n}]({image_dir}{md_file_name}_math_{n}.{file_extension})'

def format_md_str_math(md_file_name, md_str:str)->str:
    MATH_IMAGE_PATTERN = r'([^\?][^x][^\?]!\[math_\d\]\(.+\d\.png\))'
    UNLABELED_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
    MATH_SECTION_PATTERN = r'### Math Blocks'
    MATH_IMAGE_N_IDX = 10
    MAX_CNT = 1000
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
        if match_str[3:10]=='![math_': 
            n = int(match_str[MATH_IMAGE_N_IDX])
            math_scrap = re.search(f'math_{n}'+r'\n\$\$[^\$]+\$\$', old_math_blocks).group(0)        
            math_block_str += '\n'+re.sub(f'math_{n}', f'math_{cnt}', math_scrap)
            img_link = '\n\n?x?'+gen_image_link_from_md_math_str(md_file_name, cnt)
            result_str = re.sub(MATH_IMAGE_PATTERN, img_link, result_str, count=1)
            print(f'----------------------{cnt}-----------------------')
            print(img_link)
            print(result_str)
        else: 
            math_block_str += f'math_{cnt}\n'+match_str
            img_link = '?x?'+gen_image_link_from_md_math_str(md_file_name, cnt)
            result_str = re.sub(UNLABELED_MATH_PATTERN, img_link, result_str, count=1)
        cnt+=1
    result_str = result_str + '\n' + MATH_SECTION_PATTERN + '\n' + math_block_str
    result_str = re.sub(r'\?x\?', '', result_str)
    return result_str


def main():
    md_path = 'tests1_in.md'
    print(md_path[0:-3])
    output='temp.md'
    md_str = read_txt_file(md_path)  
    result_str = format_md_str_math(md_path[0:-3], md_str)
    save_str_to_file(output, result_str)

main()
