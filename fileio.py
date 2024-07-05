def read_txt_file_content(path:str)->str:
    with open(path, 'r', encoding='utf-8') as input_file:
        txt_str=input_file.read()
    return txt_str

def save_str_to_file(path:str, content:str)->None:
    with open(path, 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
        output_file.write(content)
