import sys
import os
import markdown 
from fileio import read_txt_file_content, save_str_to_file 

EXTENSIONS=['fenced_code', 'tables']
MDX_HTML_HEADER = """
<header>
    <script id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-chtml.js">
    </script>
    <script>
    MathJax = {
      tex: {
          inlineMath: [['$', '$'], ['\(', '\)']]
           }
    };
    </script>
    <link rel="stylesheet" href="styles.css">
</header>
<body>
"""
HTML_FOOTER = """
</body>
"""

def _parse_args(argv:list)->list:
    usage_str = 'usage: python md2html.py <input.md> <output_dir>'
    n_args=len(argv)
    expected_n_args = 3
    if not(n_args==expected_n_args):
        print(f'Error: Arguments Incorrect:\n    {usage_str}')
        return []
    md_file_exisits = os.path.isfile(argv[1])
    md_file_valid = os.path.splitext(argv[1])[1]=='.md'
    if not(md_file_exisits): 
        print(f'Error: {argv[1]} md file does not exist:\n    {usage_str}')
        return []
    if not(md_file_valid):
        print(f'Error: {argv[1]} is not a md file:\n    {usage_str}')
        return []
    # make sure the html dir is valid and exists already
    html_dir_exists = os.path.isdir(argv[2])
    if not(html_dir_exists):
        print(f'Error: {argv[2]} is not an existing directory :\n    {usage_str}')
        return []
    #If we make it here we know both arguments are good
    md_file_str = argv[1]
    html_dir_str = argv[2]
    return [md_file_str, html_dir_str]

def md2html(md_file_path:str, html_dir:str)->None:
    md_content_str = read_txt_file_content(md_file_path)
    html_content_str = markdown.markdown(md_content_str, extensions=EXTENSIONS)
    html_content_str = MDX_HTML_HEADER + html_content_str + HTML_FOOTER
    html_file_name = os.path.splitext(os.path.basename(md_file_path))[0]
    html_file_path = html_dir + html_file_name + '.html'
    save_str_to_file(html_file_path, html_content_str)
    
def main(argv:list)->None:
    arg_list = _parse_args(argv)
    if arg_list == []: 
        print('Error while parsing input arguments')
        return 
    md_file_path = arg_list[0]
    html_dir = arg_list[1]
    md2html(md_file_path, html_dir)

if __name__=='__main__':
    main(sys.argv)
