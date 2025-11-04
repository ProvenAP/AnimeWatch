#include <filesystem>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>

int main() {
    std::vector<std::string> imgs;
    for (auto& entry : std::filesystem::directory_iterator("images")) {
        imgs.push_back(entry.path().string());
    }

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));

        std::ifstream in("image-service.txt");
        int idx;
        if (!(in >> idx)) {
            in.close();
            continue; 
        }
        in.close();
        int pick = idx % imgs.size();
        
        std::ofstream out("image-service.txt", std::ios::trunc);
        out << imgs[pick];
        out.close();
    }
    return 0;
}
