#ifndef BALL_H
#define BALL_H

#include "custom_types.h"

extern const int BALL_WIDTH;
extern const int BALL_HEIGHT;
extern const float BALL_VELOCITY_MAG;


Ball ballSetup();
int ballUpdate(Ball* a_ball, Paddle a_paddle, AudioPlayer a_audio_player, float a_delta_time);
int ballRender(Ball a_ball, SDL_Renderer* a_renderer);

#endif
