#include "constants.h"
#include <math.h>

int construct_pixel_line(int x0, int y0, int x1, int y1, 
                          int *points, int n_points)
{
   int dx, dy, sx, sy, err, e2, expected_n_points;
   dx = abs(x1 - x0);
   dy = -abs(y1 - y0); 
   sx = x0 < x1 ? 1 : -1;
   sy = y0 < y1 ? 1 : -1; 
   err = dx + dy; /* error value e_xy */
   expected_n_points = (dx > -dy ? dx : -dy) + 1;
   expected_n_points = 2*expected_n_points;
   if(n_points < expected_n_points)
   {
       return FALSE;
   }
   if (n_points % 2 != 0)
   {
       return FALSE;
   }
   for(int i = 0; i < expected_n_points/2; i++)
   {  /* loop */
       points[2*i] = x0;
       points[2*i+1] = y0;
       if (x0 == x1 && y0 == y1) break;
       e2 = 2 * err;
       if (e2 >= dy) { err += dy; x0 += sx; } /* e_xy+e_x > 0 */
       if (e2 <= dx) { err += dx; y0 += sy; } /* e_xy+e_y < 0 */
   }
   return TRUE;
}
