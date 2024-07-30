#ifndef CUSTOM_TYPES_H
#define CUSTOM_TYPES_H

#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>

typedef struct GameInputState{
  int left;
  int right;
  int left_and_right;
  int none;
}GameInputState;

typedef struct Paddle {
  SDL_Rect sprite_box;
  float x_position;
  float y_position;
  float x_velocity;
  float x_acceleration;
} Paddle;

typedef struct Ball {
  SDL_Rect sprite_box;
  float x_position;
  float y_position;
  float x_velocity;
  float y_velocity;
}Ball;

typedef struct AudioPlayer {
  Mix_Chunk* sound_ball_paddle_collision;
  Mix_Chunk* sound_ball_wall_collision;
}AudioPlayer;



#endif
