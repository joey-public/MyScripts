import sys
import os 
import re

def renumberMdTables(md_file_str:str)->str:
    regex_pattern = r'\*\*Table [0-9]+:\*\*'
    md_file_str = re.sub(regex_pattern, '**Table #:**', md_file_str)
    regex_pattern = r'\*\*Table #:\*\*'
    matches = re.finditer(regex_pattern, md_file_str)
    for i, m in enumerate(matches)
        r_str = f'**Table {i}:**'
        md_file_str = md_file_str[0:m.start()] + r_str + md_file_str[m.end():]
    return md_file_str

def _parse_args(argv:list)->str:
    usage_str = 'usage: python renumberMdTables.py <md_file_path>'
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
    md_file_str = renumberMdTables(md_file_str)
    formatted_md_file_path = os.path.splittext(md_file_path)[0] + '_formatted.md'
    with open(formatted_md_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(md_file_str)
    output_file.close()

if __name__=='__main__':
    _main(sys.argv)
