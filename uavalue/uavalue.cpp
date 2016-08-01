#include <cstdio>
#include <sstream>
#include <string>
#include <set>

char buffer[999999];

int main() {
  while (gets(buffer)) {
    std::string s(buffer);
    if (s.find("漲幅") != std::string::npos) {
      for (int i = 0; s[i]; ++i) {
        if ((s[i] < '0' || s[i] > '9') && (s[i] != '.') && (s[i] != '-')) {
          s[i] = ' ';
        }
      }
      std::istringstream ss(s);
      std::string id;
      float cagr, average_eps, last_4q_eps, possible_price, possible_earned;
      ss >> id >> cagr >> average_eps >> last_4q_eps >> possible_price >> possible_earned;
      printf("%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n", id.c_str(), cagr, average_eps, last_4q_eps, possible_price, possible_earned);
    }
  }
  return 0;
}
