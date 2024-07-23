#ifndef PADDLE_H
#define PADDLE_H
#include "custom_types.h"

extern const float PADDLE_SPEED; 
extern const int PADDLE_MIN_X;
extern const int PADDLE_MAX_X;
extern const int PADDLE_WIDTH;
extern const int PADDLE_HEIGHT;
extern const int PADDLE_Y_POS;

Paddle paddleSetup();

int paddleUpdate();
int paddleRender();

#endif
