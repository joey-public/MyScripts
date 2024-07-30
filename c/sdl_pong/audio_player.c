#include <SDL2/SDL_mixer.h>
#include "./include/constants.h"
#include "./include/custom_types.h"

AudioPlayer audioPlayerSetup()
{
  AudioPlayer audio_player;
  audio_player.sound_ball_wall_collision = Mix_LoadWAV("./assests/wall_ball_hit_noise.wav");
  if(audio_player.sound_ball_wall_collision==NULL){
    printf("Failed to load ball_wall_collision sound effect!");
  }
  audio_player.sound_ball_paddle_collision = Mix_LoadWAV("./assests/paddle_ball_hit_noise.wav");
  if(audio_player.sound_ball_paddle_collision==NULL){
    printf("Failed to load ball_paddle_collision sound effect!");
  }
  return audio_player;
}

void destroyAudioPlayer(AudioPlayer* a_audio_player)
{
  Mix_FreeChunk(a_audio_player->sound_ball_wall_collision);
  Mix_FreeChunk(a_audio_player->sound_ball_paddle_collision);
  a_audio_player->sound_ball_wall_collision = NULL;
  a_audio_player->sound_ball_paddle_collision = NULL;
}

