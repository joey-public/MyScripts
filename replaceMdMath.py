import re
import os
import sys

USAGE_MSG = ''

MATH_IMAGE_PATTERN = r'(!\[math_\d\]\(.+\d\.png\))'
UNLABELED_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
LABELED_MATH_PATTERN = r'(math_\d\n\$\$[^$]+\$\$)'
MATH_SECTION_PATTERN = r'### Math Blocks'

DEFAULT_IMG_DIR = os.path.expanduser('~/Notes/images/math/')

def gen_image_link_from_md_math_str(md_file_name:str, n:int, image_dir:str=DEFAULT_IMG_DIR, file_extension='.png'):
    return f'![math_{n}]({image_dir}{md_file_name}_math_{n}.{file_extension})'

md_path = 'test.md'
with open(md_path, 'r', encoding='utf-8') as input_file:
    md_str=input_file.read()
cnt = 0

image_pattern = re.compile(MATH_IMAGE_PATTERN)
md_math_str_pattern = re.compile(UNLABELED_MATH_PATTERN)
result = (re.split(MATH_SECTION_PATTERN, md_str))
if len(result)==1: 
    result_str = md_str
else: 
    result_str = result[1]
math_block_str = ''
while(True):
    image_match = image_pattern.search(result_str)
    math_match = md_math_str_pattern.search(result_str)
    if(image_match==None and math_match==None):
        break
    elif math_match==None: #we muct have matched an image
        pass
    else: #we must have matched a math block
        img_link = gen_image_link_from_md_math_str(md_path[0:-4],  cnt)
        math_block_str += f'math_{cnt}\n'+math_match.group(0)+'\n'
        result_str = md_math_str_pattern.sub(img_link, result_str, count=1)
    cnt+=1

result_str = result_str + '\n' + MATH_SECTION_PATTERN + '\n' + math_block_str
print(result_str)
