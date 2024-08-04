#ifndef CUSTOM_TYPES_H
#define CUSTOM_TYPES_H

#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>

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


typedef struct ColorPallete{
//  SDL_Color dark = {r=55, g=88, b=32, a=255};
  SDL_Color c0;
  SDL_Color c1;
  SDL_Color c2;
  SDL_Color c3;
}ColorPallete;

typedef struct ScoreKeeper{
  int score;
  int font_size;
  int update_score;
  char score_cstr[4];
  int x_position_px;
  int y_position_px;
  SDL_Texture* sprite;
  TTF_Font* font;
}ScoreKeeper;

typedef struct MainLoopArgs {
  SDL_Window* window;
  SDL_Renderer* renderer;
  AudioPlayer audio_player;
  GameInputState game_input_state;
  ColorPallete color_pallete;
  ScoreKeeper score_keeper;
  Ball ball;
  Paddle paddle;
  float delta_time;
  int game_is_running; 
  int current_game_state;
}MainLoopArgs;

#endif
