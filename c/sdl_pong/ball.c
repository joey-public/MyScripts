#include "./include/ball.h"
#include "./include/constants.h"
#include "./include/custom_types.h"

const int BALL_WIDTH = 20;//pixels
const int BALL_HEIGHT = 20;//pixels

Ball ballSetup()
{
  Ball ball;
  ball.x_position = SCREEN_WIDTH/2.0;
  ball.y_position = SCREEN_HEIGHT/2.0;
  ball.x_velocity = 20.0f;
  ball.y_velocity = -40.0f;
  ball.sprite_box.x = (int) ball.x_position; 
  ball.sprite_box.y = (int) ball.y_position; 
  ball.sprite_box.w = BALL_WIDTH;
  ball.sprite_box.h = BALL_HEIGHT;
  return ball;
}

int ballUpdate(Ball* a_ball, float a_delta_time)
{
  //https://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)Randomization.html
  //when you get a collision invert x and y vel 
  //keep vel magnitude constant, but slighly randomize the x and y components
  //check for collision with walls and update velocities accordingly
  //check for collision with paddle and update velocities accordingly
  a_ball->x_position += a_ball->x_velocity * a_delta_time;
  a_ball->y_position += a_ball->x_velocity * a_delta_time;
  a_ball->sprite_box.x = (int) a_ball->x_position;
  a_ball->sprite_box.y = (int) a_ball->y_position;
  return TRUE;
}

int ballRender(Ball a_ball, SDL_Renderer* a_renderer)
{
  SDL_SetRenderDrawColor(a_renderer, 0, 0, 0, 255);
  SDL_RenderFillRect(a_renderer, &a_ball.sprite_box);
  return TRUE;
}


