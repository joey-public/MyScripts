# Python Modules vs Packages

## Module

https://docs.python.org/3/tutorial/modules.html

A python file is any .py file containing definitions and statements.  

Basically any file you save with python code in it is a module. 

The statements and definitions from one module can be imported into anther python module/file, or even just imported int he interpreter. 

The name of a module is available with he `__name__` global variable. 

### Importing Modules Functions

You can directly import a function like this:
```
from MyFile import func1, func2

a = func1()
b = func2()
```

Or you can import the module and then access functions like this
```
import MyFile as f

a = f.func1()
b = f.func2()
```

By default the `import MyFile` call will search in the directly of the script and look for `MyFile.py`. You can import from other directories like this 
```
import .MyModules.Myfile as f
```

## Python Packaging

If you have a useful collection of python modules that all work together  it may be convenient to group them together into a package. 

A package is essentially a folder with a collection of python modules/files. This folder must have a python file named `__init__.py`. Even if you just make it an empty file it is best practice to always have this file in your package directory. 

For example consider a package with several classes for shapes. you make want to organize your project something like this:

```
ProjectRootDir
---main.py
------shapes
---------__init__.py
---------Point.py
---------Rect.py
---------math_funcs.py
```

You could make the `__init__.py` file look like this:

```
from .Point import Point #assuming Point.py just contains the Point class
from .Rect import Rect
import .math_funcs as calculator
```

Then in you `main.py` you might write something like this:

```
import shapes 

p = shapes.Point(1,1)
r = shapes.Rect(0,0,2,2)
point_in_rect = shapes.calculator.rect_contains_point(r, p)
```
