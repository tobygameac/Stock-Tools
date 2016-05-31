#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
  std::ifstream twse_list_web_file("twse_list_web.txt");
  std::ofstream list_file("list.txt");
  bool is_stock = false;
  std::string line;
  const size_t MAX_LENGTH = 9999;
  char buffer[MAX_LENGTH];
  while (twse_list_web_file.getline(buffer, MAX_LENGTH)) {
    std::vector<std::string> tokens;
    std::istringstream ss(buffer);
    std::string token;
    while (ss >> token) {
      tokens.push_back(token);
    }
    if (tokens.size() == 1) {
      is_stock = tokens[0] == "股票";
    } else {
      if (is_stock) {
        list_file << tokens[0] << "\n";
      }
    }
  }
  twse_list_web_file.close();
  list_file.close();
  return 0;
}
