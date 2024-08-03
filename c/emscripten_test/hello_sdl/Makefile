all:
	emcc -o ./build/index.html -sUSE_SDL=2 main.c
run:
	emcc -o ./build/index.html -Wall -sUSE_SDL=2 main.c
	emrun ./build/index.html
clean:
	rm -r build/
