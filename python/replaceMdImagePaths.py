import sys
import os 
import re

def replaceMdImagePaths(md_file_str:str)->str:
    def _sub(match_obj)->str:
        m_str = match_obj.group(0)
        re_pat = r'\(.+\)'
        img_path_str = re.search(re_pat, m_str).group(0)[1:-1]
        abs_img_path_str = os.path.abspath(img_path_str)
        m_str = re.search(re_pat, f'({os.path.abspath(abs_img_path_str)})', m_str)
        return m_str

def _parse_args(argv:list)->str:
    usage_str = 'usage: python replaceMdImagePaths.py <md_file_path>'
    if len(argv)!=2:
        printf(f'Error: Arguments Incorrect:\n    {usage_str}')
        return '' 
    md_file_is_valid = os.path.splittext(argv[1])[1]=='.md'
    if not(md_file_is_valid):
        printf(f'Error: <{argv[1]} is not a Markdown file>:\n    {usage_str}')
        return ''
    if not(os.path.isfile(argv[1])):
        printf(f'Error: Markdown file <{argv[1]} is not an existing file>:\n    {usage_str}')
        return '' 
    return md_file_path

def _main(argv:list)->None:
    md_file_path = _parse_args(argv)
    if md_file_path=='': return 
    with open(md_file_path, 'r', encoding='utf-8') as input_file:
        md_file_str = input_file.read()
    input_file.close()
    md_file_str = renumberMdFigures(md_file_str)
    formatted_md_file_path = os.path.splittext(md_file_path)[0] + '_formatted.md'
    with open(formatted_md_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(md_file_str)
    output_file.close()

if __name__=='__main__':
    _main(sys.argv)
