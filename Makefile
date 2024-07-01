run:
	python md2html.py temp.md temp.html
debug:
	python -m pdb md2html.py temp.md temp.html
run_repl_math:
	python replaceMdMath.py
debug_repl_math:
	python -m pdb replaceMdMath.py
