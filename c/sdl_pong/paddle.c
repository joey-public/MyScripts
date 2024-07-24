#include "./include/paddle.h"
#include "./include/constants.h"
#include "./include/custom_types.h"


//Paddle Constants
const float PADDLE_SPEED = 2000;
const int PADDLE_WIDTH = 80;
const int PADDLE_HEIGHT = 10;
const int PADDLE_Y_POS = 480-PADDLE_HEIGHT-10;
const int PADDLE_MAX_X = 640-PADDLE_WIDTH-5;
const int PADDLE_MIN_X = 5;

Paddle paddleSetup()
{
  Paddle paddle;
  paddle.x_position = SCREEN_WIDTH/2; 
  paddle.sprite_box.x = (int) SCREEN_WIDTH/2;
  paddle.sprite_box.y = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  paddle.speed = 0.0f; 
  return paddle;
}

int paddleUpdate(Paddle* a_paddle, GameInputState a_current_input_state, float a_delta_time)
{
  int can_move_left = a_paddle->x_position > PADDLE_MIN_X;
  int can_move_right = a_paddle->x_position < PADDLE_MAX_X;
  int moving_left = a_current_input_state.left & !a_current_input_state.right;  
  int moving_right = a_current_input_state.right & !a_current_input_state.left;  
  //(*a_paddle).x_position += PADDLE_SPEED*a_delta_time;
  if(moving_left & can_move_left)
  {
    printf("move left\n");
    a_paddle->x_position -= PADDLE_SPEED*a_delta_time;
  }
  else if(moving_left & !can_move_left)
  {
    printf("TOO FAR LEFT!\n");
    a_paddle->x_position = PADDLE_MIN_X;
  }
  else if(moving_right & can_move_right)
  {
    printf("move right\n");
    a_paddle->x_position += PADDLE_SPEED*a_delta_time;
  }
  else if(moving_right & !can_move_right)
  {
    printf("TOO FAR RIGHT!\n");
    a_paddle->x_position = PADDLE_MAX_X;
  }
  a_paddle->sprite_box.x = (int) (*a_paddle).x_position;
  return TRUE;
}

int paddleRender(Paddle a_paddle, SDL_Renderer* a_renderer)
{
//  printf("Paddle Y pos = %d\n", a_paddle.sprite_box.y);
  SDL_SetRenderDrawColor(a_renderer, 0, 0, 0, 255);
  SDL_RenderFillRect(a_renderer, &a_paddle.sprite_box);
  return TRUE;
}
