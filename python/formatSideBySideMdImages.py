import sys 
import os 
import re

def _mdImage2Html(md_image_str)->str:
    re_pat = r'\(.+\)'
    image_path = re.search(re_pat, md_image_str).group(0)[1:-1]
    re_pat = r'\[.+\]'
    alt_txt = re.search(re_pat, md_image_str).group(0)[1:-1]
    return fr'<img alt="{alt_txt}" src="{image_path}">'
    
## Will only wok with this patter 
#**side-by-side**
#
#![alttext](img_path)
#
#![alttext](img_path)
def formatSideBySideMdImages(md_file_str:str)->str:
    def _sub(match_obj)->str:
        m_str = match_obj.group(0)
        lines = m_str.splitlines()
        left_image_str = _mdImage2Html(lines[2])
        right_image_str = _mdImage2Html(lines[4])
        return fr'''
<div class="row">
  <div class="column">
    {left_image_str}
  </div>
  <div class="column">
    {right_image_str}
  </div>
</div>

'''
    regex_pattern = r'\*\*side-by-side\*\*\n\n!\[.+\]\(.+\)\n\n!\[.+\]\(.+\)\n\n'


def _parse_args(argv:list)->str:
    usage_str = 'usage: python formatSideBySideMdImages.py <md_file_path>'
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
    md_file_str = formatSideBySideMdImages(md_file_str)
    formatted_md_file_path = os.path.splittext(md_file_path)[0] + '_formatted.md'
    with open(formatted_md_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(md_file_str)
    output_file.close()

if __name__=='__main__':
    _main(sys.argv)
