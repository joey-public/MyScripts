int init(SDL_Window** a_window, SDL_Renderer** a_renderer);
int initSdl();
int initWindow(SDL_Window** a_window);
int initRenderer(SDL_Renderer**, SDL_Window* a_window);
int setup();
//int setupPaddle();
int processInput(); //handle user input, return FALSE iff the game should quit
int update(float a_delta_time);
int render(SDL_Renderer* a_renderer);
