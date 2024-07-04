import markdown

md_str = r"""# Title
hello world!
"""

html = markdown.markdown(md_str)
print(type(html))
print(html)
