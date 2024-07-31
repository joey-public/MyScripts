#include <SDL2/SDL.h>
#include "./include/constants.h"
#include "./include/custom_types.h"

ScoreKeeper scoreKeeperSetup(SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  ScoreKeeper sk;
  SDL_Color font_color = a_pallete.c0;
  sk.x_position_px = 10;
  sk.y_position_px = 10;
  sk.font_size = 16;
  sk.score = 0;
  sk.score_cstr[0]="0"; 
  sk.score_cstr[1]="0"; 
  sk.score_cstr[2]="0"; 
  sk.score_cstr[3]="0"; 
  sk.font = TTF_OpenFont("./assests/instruction/Instruction.ttf", sk.font_size);
  SDL_Surface* tmp_surface = TTF_RenderText_Solid(sk.font, "0000" , font_color);
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
//  //start text rendering
//  TTF_Font* test_font;
//  int font_size = 28;
//  test_font = TTF_OpenFont("./assests/instruction/Instruction.ttf", font_size); 
//  SDL_Surface* test_surface = TTF_RenderText_Solid(test_font, "Hello!", a_pallete.c2); 
//  if(test_surface==NULL){
//    printf( "Unable to render text surface! SDL_ttf Error: %s\n", TTF_GetError() );
//  }
//  SDL_Texture* test_texture = SDL_CreateTextureFromSurface(a_renderer, test_surface);
//  if(test_texture==NULL){
//    printf( "Unable to create texture from rendered text! SDL Error: %s\n", SDL_GetError() );
//  }
//  SDL_FreeSurface(test_surface);
//  SDL_Color text_color = a_pallete.c2;//darkest color
//  SDL_SetRenderDrawColor(a_renderer, text_color.r, text_color.g, text_color.b, text_color.a);
//  SDL_RenderCopy(a_renderer, test_texture, NULL, NULL);
//  //end text rendering 

int scoreKeeperRender(ScoreKeeper a_score_keeper, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  SDL_Color color = a_pallete.c0;
  SDL_SetRenderDrawColor(a_renderer, color.r, color.g, color.b, color.a);
  SDL_RenderCopy(a_renderer, a_score_keeper.sprite, NULL, NULL);
  return TRUE;
}

void scoreKeeperDestroy(ScoreKeeper* a_score_keeper)
{
  SDL_DestroyTexture(a_score_keeper->sprite);
  TTF_CloseFont(a_score_keeper->font);
  a_score_keeper->sprite = NULL;
  a_score_keeper->font = NULL;
}
