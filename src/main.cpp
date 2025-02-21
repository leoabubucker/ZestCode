#include "main.h"

extern "C" void _exit(int status);

void initialize() {
	pros::delay(3000);
	dprintf(3, "hello world from debug\n");
	std::cout << "hello world2!" << std::endl;
	pros::delay(1000);
	std::cout << "e" << std::endl;
	std::abort();
}