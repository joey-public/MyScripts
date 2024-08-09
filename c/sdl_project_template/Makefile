CC = gcc
COMPILER_FLAGS = -Wall -std=c99 
DEBUG_FLAGS = -g
LINKER_FLAGS = -lm -lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer

SRC_DIR = ./src
INC_DIR = ./include
BUILD_DIR = ./build

OBJS = $(SRC_DIR)/main.c
OBJ_NAME = $(BUILD_DIR)/main 

all : $(OBJS)
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
run : 
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
	$(OBJ_NAME)
clean : 
	rm $(BUILD_DIR)/*
