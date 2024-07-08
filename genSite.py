import os 
import sys
import glob
from md2html import md2html

def _parse_args(argv:list)->list:
    usage_str = 'usage: python genSite.py <md_dir> <html_dir>'
    if not(len(argv)==3):
        print(f'Error: Arguments Incorrect:\n    {usage_str}')
        return []
    md_dir_exists = os.path.isdir(argv[1])
    html_dir_exists = os.path.isdir(argv[2])
    if not(md_dir_exists):
        print(f'Error: {argv[1]} is not an existing directory :\n    {usage_str}')
        return []
    if not(html_dir_exists):
        print(f'Error: {argv[2]} is not an existing directory :\n    {usage_str}')
        return []
    return argv[1:3]

def genSite(md_dir:str, html_dir:str)->None:
    for md_file_path in glob.glob(md_dir+'*.md'):
        md2html(md_file_path, html_dir)

def main(argv:list)->None:
    arg_list = _parse_args(argv)
    if arg_list == []: 
        print('Error: while parsing input arguments')
        return 
    md_dir, html_dir = arg_list
    genSite(md_dir, html_dir)

if __name__=='__main__':
    main(sys.argv)
