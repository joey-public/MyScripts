#include "./include/ball.h"
#include "./include/constants.h"
#include "./include/custom_types.h"
#include "./include/paddle.h"
#include <stdlib.h>
#include <math.h>
#include <SDL2/SDL_mixer.h>

const int BALL_WIDTH = 20;//pixels
const int BALL_HEIGHT = 20;//pixels
const float BALL_VELOCITY_MAG = 150;

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
  int variation = (int) 0.1f * BALL_VELOCITY_MAG;
  ball.x_velocity = _rand_int_range(BALL_VELOCITY_MAG-variation, BALL_VELOCITY_MAG+variation);
  ball.y_velocity = sqrt(pow(BALL_VELOCITY_MAG,2) + pow(ball.x_velocity, 2));
  ball.sprite_box.x = (int) ball.x_position; 
  ball.sprite_box.y = (int) ball.y_position; 
  ball.sprite_box.w = BALL_WIDTH;
  ball.sprite_box.h = BALL_HEIGHT;
  return ball;
}

//TODO: move wall and paddle collision detections outsode of the ball update method.
//THe ball should just update its position and its sprite_box
//collisions should be handeled in the top level update function, it just makes more sense.
int ballUpdate(Ball* a_ball, Paddle a_paddle, AudioPlayer a_audio_player, float a_delta_time)
{
  //update the ball position
  a_ball->x_position += a_ball->x_velocity * a_delta_time;
  a_ball->y_position += a_ball->y_velocity * a_delta_time;
  //check for collisions with walls
  int left_wall_collision = a_ball->x_position < 0; 
  int right_wall_collision = a_ball->x_position > SCREEN_WIDTH-BALL_WIDTH; 
  int top_wall_collision = a_ball->y_position < 0;
  if(left_wall_collision){
    Mix_PlayChannel(-1, a_audio_player.sound_ball_wall_collision, 0);
    a_ball->x_position = 0;
    a_ball->x_velocity = -1 * a_ball->x_velocity;
  }
  if(right_wall_collision){
    Mix_PlayChannel(-1, a_audio_player.sound_ball_wall_collision, 0);
    a_ball->x_position = SCREEN_WIDTH-BALL_WIDTH;
    a_ball->x_velocity = -1 * a_ball->x_velocity;
  }
  if(top_wall_collision){
    Mix_PlayChannel(-1, a_audio_player.sound_ball_wall_collision, 0);
    a_ball->y_position = 0;
    a_ball->y_velocity = -1 * a_ball->y_velocity;
  }
  a_ball->sprite_box.x = (int) a_ball->x_position;
  a_ball->sprite_box.y = (int) a_ball->y_position;
  return TRUE;
}

int ballRender(Ball a_ball, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  SDL_Color color = a_pallete.c0;
  SDL_SetRenderDrawColor(a_renderer, color.r, color.g, color.b, color.a);
  SDL_RenderFillRect(a_renderer, &a_ball.sprite_box);
  return TRUE;
}
