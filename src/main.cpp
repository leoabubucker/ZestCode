#include "main.h"

extern "C" void _exit(int status);

void initialize() {
	pros::delay(3000);
	std::cout << "hello world!" << std::endl;
	std::abort();
}