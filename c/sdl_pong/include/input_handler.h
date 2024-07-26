#ifndef INPUT_HANDLER_H
#define INPUT_HANDLER_H

#include "custom_types.h"

GameInputState gameInputStateSetup();
int processInput(GameInputState* a_game_input_ptr);

#endif
