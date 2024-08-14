# SDL Rendering Function Calls

https://wiki.libsdl.org/SDL2/CategoryRender

## Bresenham Line Drawing 

Consider the equation of a line:

$$
y = \frac{dy}{dx}x + b 
$$

where 

$$
dy = y1-y0;
$$

$$
dx = x1-x0;
$$

We can write the implicit line formulat by moving all variables to one side of the equation

$$
f(x,y) = \frac{dy}{dx}x + y + b 
$$

Which simplifies into:

$$ \boxed{
f(x,y) = (dy)(x) - (dx)(y) + (dx)(b)}
$$

Where if:

- $f(x,y) = 0$ then the point $(x,y)$ lyes **on the line**
- $f(x,y) > 0$ then the point $(x,y)$ lyes **above the line**
- $f(x,y) < 0$ then the point $(x,y)$ lyes **below the line**

https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
http://members.chello.at/~easyfilter/bresenham.html

## Drawing a Circle with SDL

SDL only has a few very basic built in drawing functions. To draw a circle use the `SDL_DrawPoints()` function, and pass an array of `SDL_Point` structures that represent the circle.

Look up the midpoint circle algo

## Raycasting Wolfenstein Style

https://lodev.org/cgtutor/raycasting.html

https://lodev.org/cgtutor/index.html
