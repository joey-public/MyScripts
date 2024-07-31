#ifndef AUDIO_PLAYER_H
#define AUDIO_PLAYER_H
#include <SDL2/SDL_mixer.h>
#include "custom_types.h"

AudioPlayer audioPlayerSetup();
void audioPlayerDestroy(AudioPlayer* a_audio_player);

#endif
