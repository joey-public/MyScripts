#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

//Point 
typedef struct Point{
    int32_t data[2];
}Point;

Point newPoint(int32_t x, int32_t y)
{
    Point p;
    p.data[0] = x;
    p.data[1] = y;
    return p;
}
int32_t getPointX(Point* p) 
{ 
    return p->data[0]; 
}
int32_t getPointY(Point* p) 
{ 
    return p->data[1]; 
}
void setPointX(Point* p, int32_t x) 
{ 
    p->data[0] = x; 
}
void setPointY(Point* p, int32_t y) 
{ 
    p->data[1] = y; 
}
void pointApplyXform(Point* p, int32_t xform[2][2]) 
{
    return;//need to implement this 
} 
void pointApplyXformAffine(Point* p, int32_t xform[3][3]) {}

// Linear Algebra Functions
int32_t la_dot(int32_t* v0, int32_t* v1, int32_t n)
{
    int32_t acc=0;
    for(int i = 0; i < n; i++)
    {
        acc += v0[i]*v1[i];
    }
    return acc;
}
int32_t la_matmul(Point* p, int32_t* v0, int32_t* v1, int32_t n)
{
    return 0;
}

int main()
{
    printf("Hello World!\n");
    Point p0 = newPoint(1,3);
    Point p1 = newPoint(2,5);
    int32_t k;
    k = la_dot(p0.data, p1.data , 2);
    printf("%d\n", k);

    printf("Goodbye World!\n");
    return 0;
}
