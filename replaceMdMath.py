import re
import os
import sys

USAGE_MSG = ''

MATH_IMAGE_PATTERN = r'([^\?][^x][^\?]!\[math_\d\]\(.+\d\.png\))'
UNLABELED_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
LABELED_MATH_PATTERN = r'(math_\d\n\$\$[^$]+\$\$)'
MATH_SECTION_PATTERN = r'### Math Blocks'

DEFAULT_IMG_DIR = os.path.expanduser('~/Notes/images/math/')

MATH_IMAGE_N_IDX = 10
MAX_CNT = 10

def gen_image_link_from_md_math_str(md_file_name:str, n:int, image_dir:str=DEFAULT_IMG_DIR, file_extension='png'):
    return f'![math_{n}]({image_dir}{md_file_name}_math_{n}.{file_extension})'

md_path = 'tests1_in.md'
with open(md_path, 'r', encoding='utf-8') as input_file:
    md_str=input_file.read()

result = (re.split(MATH_SECTION_PATTERN, md_str))
math_block_str = ''
math_scatchpad = ''
if len(result)==1: 
    result_str = md_str
else: 
    old_math_blocks = result[1]
    result_str = result[0]

cnt = 0
regex_pattern = re.compile(MATH_IMAGE_PATTERN + '|' + UNLABELED_MATH_PATTERN)
#TODO: Numbering is off...both image and math_match will be true for  file with images and math
# if we match a math image link then 
#     0. Define n byt looking at the match string ![math_{n}]
#     1. find the md_math_string assosiated with it (by searching the old_math_blocks str)
#     2. math_scap = re.search(r'math_{n}\n\$\$[^\$]+\n\$\$'
#     3. math_block_str += re.sub(f'math_{n}', f'math_{cnt}', math_scrap)
#     4. replace the math block with the '?x?'+image link in result _str
# if we match a math block then 
#     0. math_block_str += f'math_{cnt}\n'+match_str`
#     1. replace the math block with the '?x?'+image link in result _str
while(True):
    match = regex_pattern.search(result_str)
    if(match==None or cnt>MAX_CNT):
        break
    match_str = match.group(0)
    if match_str[3:10]=='![math_': 
        n = int(match_str[MATH_IMAGE_N_IDX])
        math_scrap = re.search(f'math_{n}'+r'\n\$\$[^\$]+\$\$', old_math_blocks).group(0)        
        math_block_str += '\n'+re.sub(f'math_{n}', f'math_{cnt}', math_scrap)
        img_link = '\n\n?x?'+gen_image_link_from_md_math_str(md_path[0:-4], cnt)
        result_str = re.sub(MATH_IMAGE_PATTERN, img_link, result_str, count=1)
    else: 
        math_block_str += f'math_{cnt}\n'+match_str
        img_link = '?x?'+gen_image_link_from_md_math_str(md_path[0:-4], cnt)
        result_str = re.sub(UNLABELED_MATH_PATTERN, img_link, result_str, count=1)
    cnt+=1

result_str = result_str + '\n' + MATH_SECTION_PATTERN + '\n' + math_block_str
result_str = re.sub(r'\?x\?', '', result_str)

def save_str_to_file(path:str, text_str:str)->None:
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(text_str)

output='temp.md'
save_str_to_file(output, result_str)
