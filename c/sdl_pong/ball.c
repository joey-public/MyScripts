#include "./include/ball.h"
#include "./include/constants.h"
#include "./include/custom_types.h"
#include <stdlib.h>

const int BALL_WIDTH = 20;//pixels
const int BALL_HEIGHT = 20;//pixels
const float BALL_VELOCITY_MAG = 200;

//https://stackoverflow.com/questions/2999075/generate-a-random-number-within-range/2999130#2999130
int _rand_int(int n) 
{
    int divisor = RAND_MAX/(n+1);
    int retval;
    do { 
        retval = rand() / divisor;
    } while (retval > n);
    return retval;
}

int _rand_int_range(int min, int max)
{
    int range = max-min;
    return min + _rand_int(max+range);
}

Ball ballSetup()
{
  Ball ball;
  ball.x_position = _rand_int(SCREEN_WIDTH);
  ball.y_position = 0;
  ball.x_velocity = _rand_int_range(BALL_VELOCITY_MAG-50, BALL_VELOCITY_MAG+50);
  ball.y_velocity = 0;
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
  int left_wall_collision = a_ball->x_position < 0; //create a SCREEN RECT constant to make this shit easier
  int right_wall_collision = a_ball->x_position > SCREEN_WIDTH-BALL_WIDTH; //create a SCREEN RECT constant to make this shit easier
  if(left_wall_collision | right_wall_collision){
    a_ball->x_velocity = -1 * (_rand_int_range(8,12) / 10.0f) * a_ball->x_velocity;
  }
  a_ball->x_position += a_ball->x_velocity * a_delta_time;
  a_ball->y_position += a_ball->y_velocity * a_delta_time;
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


