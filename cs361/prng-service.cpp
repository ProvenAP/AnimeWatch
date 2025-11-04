#include <fstream>
#include <random>
#include <string>
#include <thread>
#include <chrono>

int main() {
    
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<> dist(0, 100); 

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));

        std::ifstream in("prng-service.txt");
        std::string line;
        std::getline(in, line);
        in.close();

        if (line == "run") {
            int rnd = dist(gen);

            std::ofstream out("prng-service.txt", std::ios::trunc);
            out << rnd;
            out.close();
        }
    }
    return 0;
}
