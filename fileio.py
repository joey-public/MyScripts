import os
import subprocess as sbp

def _get_file_name_from_path(path:str)->str:
    return os.path.splittext(os.path.basename(path))[0]

def read_txt_file_content(path:str)->str:
    with open(path, 'r', encoding='utf-8') as input_file:
        txt_str=input_file.read()
    return txt_str

def save_str_to_file(path:str, content:str)->None:
    with open(path, 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
        output_file.write(content)

def create_pdf_file_from_tex(tex_path:str, out_dir:str, 
                     tex_eng='pdflatex', latex_timeout=1.0)->None:
    cmd = ['pdflatex', f'-output-directory', f'{pdf_dir}', f'{tex_path}']
    out = sbp.run(cmd, capture_output='True', timeout=latex_timeout)
    e = out.stderr
    if e!=b'': return False
    temp_str = out_dir + _get_file_name_from_path(tex_path)
    os.remove(temp_str + '.aux')
    os.remove(temp_str + '.log')
    os.remove(temp_str + '.tex')
    return True

