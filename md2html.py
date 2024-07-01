import sys
import os
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from format_funcs import replace_md_math_with_img_links, gen_math_images_from_md_str


BASE_URL = '~/Notes/html/'
USAGE_STR = 'python md2html.py <input.md> <output.html>'
OFFICIAL_EXT=['fenced_code', 'tables', WikiLinkExtension(base_url=BASE_URL, end_url='.html')]
EXTENSIONS = OFFICIAL_EXT 

DEFAULT_IMG_DIR = os.path.expanduser('~/Notes/images/math/')

def _save_html_to_file(path:str, html):
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

def _read_txt_file(path:str)->str:
    with open(path, 'r', encoding='utf-8') as input_file:
        txt_str=input_file.read()
    return txt_str

#--TODO: make sure argv paths are valid...
def _parse_args(argv):
    n_args=len(argv)
    md_path=''
    html_path=''
    if  n_args==2: 
        md_path = argv[1]
#        html_path = argv[1][0:-3] + '.html'
#        print(f'No html file given, saving as:\n\t{html_path}')
    elif  n_args==3: 
        md_path = argv[1]
        html_path = argv[2]
    else: 
        print('Error: Missing one or more arguments\n    '+USAGE_STR) 
    return (md_path, html_path)

# TODO: error checking 
#       - make sure pdftex is on the system
#       - make sure image_dir is valid
def main(argv):
    md_path, html_path = _parse_args(argv)
    valid_md_path = os.path.isfile(md_path) and os.path.splitext(md_path)[1]=='.md'
    valid_html_path = os.path.isdir(os.path.dirname(html_path)) and os.path.splitext(html_path)[1]=='.html'
    if not(valid_md_path):
        print(f'Error: Invalid Markdown Path: <{md_path}> does not exist\n    '+USAGE_STR)
        return 
    if not(valid_html_path): 
        print(f'Error: Invalid HTML Path: <{html_path[0:-6]}> does not exits\n    '+USAGE_STR)
        return 
    md_file_name = os.path.splitext(os.path.basename(md_path))[0]
    md_file_str = _read_txt_file(md_path)
    
    img_dir = DEFAULT_IMG_DIR
    img_fmt = '.png' 
    result_str = replace_md_math_with_img_links(md_file_str,md_file_name,img_dir,img_fmt)
    if not(result_str==md_file_str): #only need to generate the images if there was acually math in the md_file
        gen_math_images_from_md_str(md_file_str,md_file_name,img_dir,img_fmt)
    html_obj = markdown.markdown(result_str, extensions=EXTENSIONS)
    _save_html_to_file(html_path, html_obj)

if __name__=='__main__':
    main(sys.argv)
