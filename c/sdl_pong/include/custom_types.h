#ifndef CUSTOM_TYPES_H
#define CUSTOM_TYPES_H

#include <SDL2/SDL.h>

typedef struct GameInputState{
  int left;
  int right;
  int left_and_right;
  int none;
}GameInputState;

typedef struct Paddle {
  SDL_Rect sprite_box;
  float x_position;
  float speed;
} Paddle;

typedef struct Ball {
  SDL_Rect sprite_box;
  float x_position;
  float y_position;
  float speed;
}Ball;

#endif
