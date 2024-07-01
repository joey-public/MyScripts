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

def save_html_to_file(path:str, html):
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

def read_txt_file(path:str)->str:
    with open(path, 'r', encoding='utf-8') as input_file:
        txt_str=input_file.read()
    return txt_str

def is_valid_path(path:str):
    return True

#--TODO: make sure argv paths are valid...
def parse_args(argv):
    n_args=len(argv)
    md_path=''
    html_path=''
    if  n_args==2: 
        md_path = argv[1]
        html_path = argv[1][0:-3] + '.html'
        print(f'No html file given, saving as:\n\t{html_path}')
    elif  n_args==3: 
        md_path = argv[1]
        html_path = argv[2]
    else: 
        print(USAGE_STR) 
    return (md_path, html_path)

# TODO: error checking 
#       - make sure pdftex is on the system
#       - make sure md_path is valid
#       - make sure html_path is valid
#       - make sure image_dir is valid

def main(argv):
    md_path, html_path = parse_args(argv)
    md_file_name = md_path[0:-3]
    print(md_file_name)
    md_file_str = read_txt_file(md_path)
    img_dir = DEFAULT_IMG_DIR
    img_fmt = '.png' 
    gen_math_images_from_md_str(md_file_str,md_file_name,img_dir,img_fmt)
    result_str = replace_md_math_with_img_links(md_file_str,md_file_name,img_dir,img_fmt)
    html_obj = markdown.markdown(result_str, extensions=EXTENSIONS)
    save_html_to_file(html_path, html_obj)

if __name__=='__main__':
    main(sys.argv)
