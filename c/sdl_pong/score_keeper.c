#include <SDL2/SDL.h>
#include "./include/constants.h"
#include "./include/custom_types.h"

ScoreKeeper scoreKeeperSetup(SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  ScoreKeeper sk;
  SDL_Color font_color = a_pallete.c0;
  sk.x_position_px = 10;
  sk.y_position_px = 10;
  sk.font_size = 12;
  sk.score = 0;
  sprintf(sk.score_cstr, "%d", sk.score);
  sk.font = TTF_OpenFont("./assests/instruction/Instruction.ttf", sk.font_size);
  SDL_Surface* tmp_surface = TTF_RenderText_Solid(sk.font, sk.score_cstr , font_color);
  if(tmp_surface==NULL){
    printf( "Unable to render text surface! SDL_ttf Error: %s\n", TTF_GetError() );
  }
  sk.sprite = SDL_CreateTextureFromSurface(a_renderer, tmp_surface);
  if(sk.sprite==NULL){
    printf( "Unable to create texture from rendered text! SDL Error: %s\n", SDL_GetError() );
  }
  SDL_FreeSurface(tmp_surface);
  return sk;
}

int scoreKeeperUpdate(ScoreKeeper* a_score_keeper, float a_delta_time, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  if(!(a_score_keeper->update_score==a_score_keeper->score) && a_score_keeper->score <= 999){
    a_score_keeper->update_score = a_score_keeper->score;
    snprintf(a_score_keeper->score_cstr, 5, "%d", a_score_keeper->score);
    SDL_Color font_color = a_pallete.c0;
    SDL_Surface* tmp_surface = TTF_RenderText_Solid(a_score_keeper->font, a_score_keeper->score_cstr , font_color);
    if(tmp_surface==NULL){
      printf( "Unable to render text surface! SDL_ttf Error: %s\n", TTF_GetError() );
    }
    a_score_keeper->sprite = SDL_CreateTextureFromSurface(a_renderer, tmp_surface);
    if(a_score_keeper->sprite==NULL){
      printf( "Unable to create texture from rendered text! SDL Error: %s\n", SDL_GetError() );
    }
    SDL_FreeSurface(tmp_surface);
  }
  else{
      //do nothing
  }
  return TRUE;
}

int scoreKeeperRender(ScoreKeeper a_score_keeper, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  SDL_Color color = a_pallete.c3;
  SDL_Rect src;
  src.x = 0;
  src.y = 0;
  src.w = 50;
  src.h = 50;
  SDL_SetRenderDrawColor(a_renderer, color.r, color.g, color.b, color.a);
  SDL_RenderCopy(a_renderer, a_score_keeper.sprite, &src, &src);
  return TRUE;
}

void scoreKeeperDestroy(ScoreKeeper* a_score_keeper)
{
  SDL_DestroyTexture(a_score_keeper->sprite);
  TTF_CloseFont(a_score_keeper->font);
  a_score_keeper->sprite = NULL;
  a_score_keeper->font = NULL;
}
