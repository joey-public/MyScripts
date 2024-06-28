import sys
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

BASE_URL = '~/Notes/html/'
USAGE_STR = 'python md2html.py <input.md> <output.html>'
OFFICIAL_EXT=['fenced_code', 'tables', WikiLinkExtension(base_url=BASE_URL, end_url='.html']
OTHER_EXT = ['mdx_math']
EXTENSIONS = OFFICIAL_EXT+OTHER_EXT 

def file_to_html(path:str):
    with open(path, 'r', encoding='utf-8') as input_file:
        text=input_file.read()
    return markdown.markdown(text, extensions=EXTENSIONS)

def save_html_to_file(path:str, html):
    with open(path, 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

def is_valid_path(path:str):
    return True
--TODO: make sure argv paths are valid...
def main(argv):
    n_args=len(argv)
    md_path=''
    html_path=''
    if  n_args==2: 
        md_path = argv[1]
        html_path = argv[1][0:-3] + '.html'
        print(f'No html file given, saving as:\n\t{html_path}'
    elif  n_args==3: 
        md_path = argv[1]
        html_path = argv[2]
    else: 
        print(USAGE_STR); return 
    html_obj = file_to_html(md_path)
    save_html_to_file(html_obj)

if __name__=='__main__':
    main(sys.argv)
