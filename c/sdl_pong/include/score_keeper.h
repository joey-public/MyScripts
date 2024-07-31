#ifndef SCORE_KEEPER_H
#define SCORE_KEEPER_H
#include "custom_types.h"

ScoreKeeper scoreKeeperSetup(SDL_Renderer* a_renderer, ColorPallete a_pallete);
int scoreKeeperUpdate(ScoreKeeper* a_score_keeper, float a_delta_time, SDL_Renderer* a_renderer, ColorPallete a_pallete);
int scoreKeeperRender(ScoreKeeper a_score_keeper, SDL_Renderer* a_renderer, ColorPallete a_pallete);
void scoreKeeperDestroy(ScoreKeeper* a_score_keeper);

#endif
