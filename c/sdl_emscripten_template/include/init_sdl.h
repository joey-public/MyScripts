#ifndef INIT_SDL_H
#define INIT_SDL_H
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>

int init(SDL_Window** a_window, SDL_Renderer** a_renderer);
int initSdl();
int initMixer(int a_sample_rate);
int initTTF();
int initWindow(SDL_Window** a_window);
int initRenderer(SDL_Renderer** a_renderer, SDL_Window* a_window);

#endif
