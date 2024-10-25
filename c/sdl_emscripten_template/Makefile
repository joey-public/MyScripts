# Thanks to Job Vranish (https://spin.atomicobject.com/2016/08/26/makefile-c-projects/)
TARGET_EXEC := main

BUILD_DIR := ./build
SRC_DIR := ./src
INCLUDE_DIR := ./include

TARGET = $(BUILD_DIR)/$(TARGET_EXEC)
SRC_FILES = $(wildcard $(SRC_DIR)/*.c)

CC := gcc
COMPILER_FLAGS := -Wall -std=c99 
DEBUG_FLAGS := -g
INCLUDE_FLAGS := -I$(INCLUDE_DIR)
LINKER_FLAGS = -lm -lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer

$(TARGET): $(SRC_FILES)
	$(CC) $(SRC_FILES) $(COMPILER_FLAGS) $(INCLUDE_FLAGS) $(LINKER_FLAGS) -o $(TARGET) 

