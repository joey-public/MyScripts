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
  paddle.sprite_box.x = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  return paddle;
}

int paddleUpdate()
{
  printf("Updating the Paddle!\n");
  return TRUE;
}

int paddleRender()
{
  printf("Rendering the Paddle!\n");
  return TRUE;
}

