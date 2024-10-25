#ifndef INIT_SDL_H
#define INIT_SDL_H
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>
#include <stdbool.h>
#include <stdint.h>

bool initSdlAudioVideo();
bool initMixer(int a_sample_rate);
bool initTTF();
bool initWindow(SDL_Window** a_window, uint16_t a_window_width, uint16_t a_window_height);
bool initRenderer(SDL_Renderer** a_renderer, SDL_Window* a_window);
bool initSdl(SDL_Window** a_window, SDL_Renderer** a_renderer, uint16_t a_window_width, uint16_t a_window_height);

#endif
