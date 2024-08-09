PROJ_DIR = ./sdl_project_template
SRC_DIR = $(PROJ_DIR)/src
INC_DIR = $(PROJ_DIR)/include
BUILD_DIR = $(PROJ_DIR)/build
MAKEFILE_TEMPLATE = ~/MyScripts/c/sdl_templates/Makefile
SDL_MAIN_TEMPLATE = ~/MyScripts/c/sdl_templates/main.c

all:
	echo Use make sdl_proj to make a new sdl project


sdl_proj: 
	echo Making a new SDL Project
	mkdir $(PROJ_DIR); cd $(PROJ_DIR); touch README.md
	mkdir $(SRC_DIR); mkdir $(INC_DIR); mkdir $(BUILD_DIR)
	cp $(MAKEFILE_TEMPLATE) $(PROJ_DIR)/Makefile
	cp $(SDL_MAIN_TEMPLATE) $(PROJ_DIR)/src/main.c


