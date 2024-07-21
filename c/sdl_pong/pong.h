int init(SDL_Window** a_window, SDL_Renderer** a_renderer);
int initSdl();
int initWindow(SDL_Window** a_window);
int initRenderer(SDL_Renderer**, SDL_Window* a_window);
int processInput(GameInputState* a_game_input_ptr); //handle user input, return FALSE iff the game should quit
