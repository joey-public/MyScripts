# Pong Design Document

## Core Game Loop

A ball bouncees around the screen. The player controlls a paddle and hits the ball before it reaches the bottom of the screen. 

If the ball reached the bottom of the screen then its game over. 

## Features

### Have to Have 

- A paddle the player can move left and right
- A ball that bounces around the screen
- Some juice that makes hitting the ball feel better
- A sore counter/survive timer
- A start Screen
- A end Screen

### Nice to Have 

- A high score tracker
- A pause screen
- Increase the speed of the ball as score goes up (might have to have this)
- Infinte mode, the ball goes back to the top of the screen 
- A theme
- Randomly move the paddle from bottom to left, right or top of the screen
- controllabled paddle hit stregth 
- controllable paddle angle
- Power Ups:
    - Ball Buffs and debuffs
    - Paddle Buffs and Debuffs you can get 

## Naming Conventions

|             | Example    |
| :------     | :--------- |
| Files       | file_name  |
| Directories | DirName    |
| Variables   | var_name   |
| Constants   | CONST_NAME |
| Functions   | funcName   |
| Types       | TypeName   |

## Custom Game Types

| Type           | Purpose                                               | Comment                  |
| :------------- | :---------------------------------------------------- | :----------------------- |
| Paddle         | The Paddle                                            | Controlled by the player |
| Ball           | The ball                                              |                          |
| GameInputState | Object that holds the current state of the user input |                          |

## Tasks

- TODO setupPaddle(), setupBall, setupWall() functions
- TODO make all game objects provate to main function, not gloabl (maybe use typedef?)
- TODO: create close() fucntion that deletes everything
- TODO: smooth out paddle movement
- TODO: seperate paddle into its own file
- TODO: seperte ball into its own file
- TODO: make a types.h that has all the typedefs
- TODO: move all constants to a seperate file
