#include "./include/paddle.h"
#include "./include/constants.h"
#include "./include/custom_types.h"


//Paddle Constants
const float PADDLE_SPEED = 2000;
const int PADDLE_MIN_X = 0;
const int PADDLE_MAX_X = 640;
const int PADDLE_WIDTH = 80;
const int PADDLE_HEIGHT = 10;
const int PADDLE_Y_POS = 480-PADDLE_HEIGHT-10;

Paddle paddleSetup()
{
  Paddle paddle;
  paddle.sprite_box.x = PADDLE_WIDTH/2;
  paddle.sprite_box.y = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  return paddle;
}

int paddleUpdate(Paddle* a_paddle, GameInputState a_current_input_state, float a_delta_time)
{
//  (*a_paddle).sprite_box.x += PADDLE_SPEED * delta_time; 
  return TRUE;
}

int paddleRender(Paddle a_paddle, SDL_Renderer* a_renderer)
{
  SDL_SetRenderDrawColor(a_renderer, 0, 0, 0, 255);
  SDL_RenderFillRect(a_renderer, &a_paddle.sprite_box);
  return TRUE;
}
