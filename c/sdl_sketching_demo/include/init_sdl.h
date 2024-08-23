#ifndef INIT_SDL_H
#define INIT_SDL_H
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>
#include <stdbool.h>

bool init(SDL_Window** a_window, SDL_Renderer** a_renderer);
bool  initSdl();
bool  initMixer(int a_sample_rate);
bool  initTTF();
bool  initWindow(SDL_Window** a_window, int a_width, int a_height);
bool  initRenderer(SDL_Renderer** a_renderer, SDL_Window* a_window);
bool  initilizeSdl(SDL_Window** a_window, SDL_Renderer** a_renderer, int a_width, int a_height);

#endif
