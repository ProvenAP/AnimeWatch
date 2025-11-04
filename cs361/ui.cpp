#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>

int main() {
    while (true) {
        std::cout << "Enter 1 to get an image, 2 to quit: ";
        int choice;
        std::cin >> choice;

        if (choice == 2) {
            std::cout << "Goodbye!\n";
            return 0;
        }
        else if (choice != 1) {
            std::cout << "Unknown option. Try again.\n\n";
            continue;
        }

        {
            std::ofstream out("prng-service.txt", std::ios::trunc);
            out << "run";
        }

        std::this_thread::sleep_for(std::chrono::seconds(1));

        int rnd;
        {
            std::ifstream in("prng-service.txt");
            in >> rnd;
        }

        {
            std::ofstream out("image-service.txt", std::ios::trunc);
            out << rnd;
        }

        std::this_thread::sleep_for(std::chrono::seconds(1));

        {
            std::ifstream in("image-service.txt");
            std::string path;
            std::getline(in, path);
            std::cout << "Selected: " << path << "\n\n";
        }
    }
    return 0;
}
