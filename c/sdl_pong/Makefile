#OBJS specifies which files to compile as part of the project
OBJS = pong.c constants.c paddle.c ball.c init_sdl.c input_handler.c audio_player.c score_keeper.c

#CC specifies which compiler we're using
#CC = g++ #for cpp
CC = gcc
  

#COMPILER_FLAGS specifies the additional compilation options we're using
# -Wall show all warnings
COMPILER_FLAGS = -Wall -std=c99 

DEBUG_FLAGS = -g

#LINKER_FLAGS specifies the libraries we're linking against
LINKER_FLAGS = -lm -lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer


#OBJ_NAME specifies the name of our exectuable
OBJ_NAME = ./build/pong

#This is the target that compiles our executable
all : $(OBJS)
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
db : $(OBJS)
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) $(DEBUG_FLAGS) -o $(OBJ_NAME)  
run : 
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
	$(OBJ_NAME)
rundb :
	gdb $(OBJ_NAME)
web:
	emcc $(OBJS) -o ./build/web_pong.html -sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sUSE_SDL_TTF=2 -sUSE_SDL_MIXER=2 --preload-file ./assests/
clean : 
	rm ./build/*
