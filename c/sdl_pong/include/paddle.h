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

int paddleUpdate(Paddle* a_paddle, GameInputState a_current_input_state, float a_delta_time);
int paddleRender(Paddle a_paddle, SDL_Renderer* a_renderer);

#endif
