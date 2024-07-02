run:
	python md2html.py /home/joey/Notes/temp.md /home/joey/Notes/html/temp.html
	firefox /home/joey/Notes/html/temp.html &
debug:
	python -m pdb md2html.py /home/joey/Notes/temp.md /home/joey/Notes/html/temp.html
clean:
	rm *.aux
	rm *.pdf
	rm *.log
