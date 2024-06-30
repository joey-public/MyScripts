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

def gen_image_link_from_md_math_str(md_file_name:str, n:int, image_dir:str=DEFAULT_IMG_DIR, file_extension='png'):
    return f'![math_{n}]({image_dir}{md_file_name}_math_{n}.{file_extension})'

md_path = 'temp.md'
with open(md_path, 'r', encoding='utf-8') as input_file:
    md_str=input_file.read()
cnt = 0
image_pattern = re.compile(MATH_IMAGE_PATTERN)
md_math_str_pattern = re.compile(UNLABELED_MATH_PATTERN)

result = (re.split(MATH_SECTION_PATTERN, md_str))
math_block_str = ''
math_scatchpad = ''
if len(result)==1: 
    result_str = md_str
else: 
    old_math_blocks = result[1]
    result_str = result[0]
#    re.sub(r'!\[math_', r'?x?[math_', result_str)
print(result_str)
#TODO: Numbering is off...both image and math_match will be true for  file with images and math
while(True):
    image_match = image_pattern.search(result_str)
    math_match = md_math_str_pattern.search(result_str)
    if(image_match==None and math_match==None):
        print('no match!')
        break
    elif math_match==None: #we muct have matched an image
        print('img match: '+image_match.group(0))
        n = int(image_match.group(0)[MATH_IMAGE_N_IDX])
        img_link = '?x?'+gen_image_link_from_md_math_str(md_path[0:-3],  cnt)
        result_str = md_math_str_pattern.sub(img_link, result_str, count=1)
        math_scratchpad = re.search(f'(math_{n})', old_math_blocks)
        math_block_str += re.sub(f'math_{n}', f'math_{cnt}', math_scratchpad.group(0)) 
        print(result_str)
    else: #we must have matched a math block
        print('math match: '+math_match.group(0))
        img_link = '?x?'+gen_image_link_from_md_math_str(md_path[0:-3],  cnt)
        math_block_str += f'math_{cnt}\n'+math_match.group(0)+'\n'
        result_str = md_math_str_pattern.sub(img_link, result_str, count=1)
    cnt+=1

result_str = result_str + '\n' + MATH_SECTION_PATTERN + '\n' + math_block_str
result_str = re.sub(r'\?x\?', '', result_str)
print(result_str)

def save_str_to_file(path:str, text_str:str)->None:
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(text_str)
#save_str_to_file(md_path, result_str)
