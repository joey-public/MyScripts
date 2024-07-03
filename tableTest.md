# Table Test

I want to update my custom md script `md2html.py` to be capable of generating good looking tables in html. 

The ideas I looked into:
1. Using the pandas DataFrame's `to_latex()` function
2. Using the pandas DataFrame's `to_html()` function
3. Use inline html and custom parsing
4. Use inline lates and custom parsing
5. Hacking an array into md using mathjax and array fucntion

I ultumately may want to try to implement more of these, but the most useful place to start is with 

## Using Inline HTML
#### Syntax

Python markdown implements John Gruber's [Markdown](https://daringfireball.net/projects/markdown/syntax#html) so it should support inline html code by defulat.

For example here is a table in HTML syntax:

```
<table>
    <tr>
    <th> Company</th>
    <th> Contact</th>
    <th> Country</th>
    </tr>
    <tr>
    <th> Google </th>
    <th> John Doe</th>
    <th> USA </th>
    </tr>
```

And here is what it looks like when it is rendered 

<table>
    <tr>
    <th> Company</th>
    <th> Contact</th>
    <th> Country</th>
    </tr>
    <tr>
    <th> Google </th>
    <th> John Doe</th>
    <th> USA </th>

This is great, but when I view my markdown source file in a markdown viewer (like github, or Obsidian) I would prefer if the inline html were formatted to look like a code block. I want to write my inline html with syntax as shown below using `(```<inline html>)` 

```
(```<inline html>)
<table>
    <tr>
    <th> Company</th>
    <th> Contact</th>
    <th> Country</th>
    </tr>
    <tr>
    <th> Google </th>
    <th> John Doe</th>
    <th> USA </th>
    </tr>
```
