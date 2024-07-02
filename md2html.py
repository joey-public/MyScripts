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

def _parse_args(argv):
    n_args=len(argv)
    md_path=''
    html_path=''
    if n_args == 1: 
        print('Error: No Markdown or HTML paths were given\n    '+USAGE_STR)
    elif  n_args==2: #TODO: we should be abel to autogenerate the html file in the same directory as the md file 
        valid_md_path = os.path.isfile(argv[1]) and os.path.splitext(argv[1])[1]=='.md'
        if valid_md_path:
            md_path = argv[1]
        else:
            print(f'Error: Invalid Markdown Path: <{argv[1]}> does not exist\n    '+USAGE_STR)
        print(f'Error: No HTML path given\n    '+USAGE_STR)
    elif  n_args==3: 
        valid_md_path = os.path.isfile(argv[1]) and os.path.splitext(argv[1])[1]=='.md'
        valid_html_path = os.path.isdir(os.path.dirname(argv[2])) and os.path.splitext(argv[2])[1]=='.html'
        if valid_md_path:
            md_path = argv[1]
        else:
            print(f'Error: Invalid Markdown Path: <{argv[1]}> does not exist\n    '+USAGE_STR)
        if valid_html_path:
            html_path = argv[2]
        else:
            print(f'Error: Invalid HTML Path: <{argv[2]}> does not exist\n    '+USAGE_STR)
    else: 
        print('Error: Too many arguments\n    '+USAGE_STR) 
    return (md_path, html_path)

# TODO: error checking 
#       - make sure pdftex is on the system
#       - make sure image_dir is valid
def main(argv):
    md_path, html_path = _parse_args(argv)
    if md_path=='' or html_path=='':
        print('Invalid arguments see messages above...')
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
