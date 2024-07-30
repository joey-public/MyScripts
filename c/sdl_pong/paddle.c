#include "./include/paddle.h"
#include "./include/constants.h"
#include "./include/custom_types.h"


//Paddle Constants
const float PADDLE_MAX_SPEED = 1000;
const float TIME_TO_MAX_SPEED = 0.2;
const float PADDLE_ACC = PADDLE_MAX_SPEED/TIME_TO_MAX_SPEED;
const int PADDLE_WIDTH = 100;
const int PADDLE_HEIGHT = 10;
const int PADDLE_Y_POS = 480-PADDLE_HEIGHT-10;
const int PADDLE_MAX_X = 640-PADDLE_WIDTH-5;
const int PADDLE_MIN_X = 5;

Paddle paddleSetup()
{
  Paddle paddle;
  paddle.x_position = SCREEN_WIDTH/2.0; 
  paddle.sprite_box.x = (int) SCREEN_WIDTH/2;
  paddle.sprite_box.y = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  paddle.x_velocity = 0; 
  paddle.x_acceleration= PADDLE_ACC; 
  return paddle;
}

int paddleUpdate(Paddle* a_paddle, GameInputState a_current_input_state, float a_delta_time)
{
  int direction;
  int moving_left = a_current_input_state.left & !a_current_input_state.right;  
  int moving_right = a_current_input_state.right & !a_current_input_state.left;  
  a_paddle->x_velocity += a_paddle->x_acceleration*a_delta_time; //dv=a*dt
  if(moving_left){
    direction=-1;
  }
  else if(moving_right){
    direction=1;
  }
  else{
    direction=0;
    a_paddle->x_velocity=0.0f;
  }
  if(a_paddle->x_velocity >= PADDLE_MAX_SPEED){
    a_paddle->x_velocity = PADDLE_MAX_SPEED;
  }
  a_paddle->x_position += direction*a_paddle->x_velocity*a_delta_time; //dx=v*dt
  if(a_paddle->x_position < PADDLE_MIN_X){
    a_paddle->x_position = PADDLE_MIN_X;
  }
  if(a_paddle->x_position > PADDLE_MAX_X){
    a_paddle->x_position = PADDLE_MAX_X;
  }
  a_paddle->sprite_box.x = (int) a_paddle->x_position;
//  printf("\n--PADDLE--\n");
//  printf("\td:  %d\n", direction);
//  printf("\ta:  %f\n", a_paddle->x_acceleration);
//  printf("\tv:  %f\n", a_paddle->x_velocity);
//  printf("\txf: %f\n", a_paddle->x_position);
//  printf("\tx:  %d\n", a_paddle->sprite_box.x);
  return TRUE;
}

int paddleRender(Paddle a_paddle, SDL_Renderer* a_renderer)
{
//  printf("Paddle Y pos = %d\n", a_paddle.sprite_box.y);
  SDL_SetRenderDrawColor(a_renderer, 0, 0, 0, 255);
  SDL_RenderFillRect(a_renderer, &a_paddle.sprite_box);
  return TRUE;
}
