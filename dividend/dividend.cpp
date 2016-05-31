#include <fstream>
#include <iostream>
#include <map>
#include <string>

int main() {
  std::string stock_id, stock_name, stock_per, stock_dividend, stock_pbr;
  std::map<std::string, std::string> stocks_name, stocks_per, stocks_dividend, stocks_pbr;
  std::ifstream twse_dividend_file("twse_dividend.txt");
  while (twse_dividend_file >> stock_id >> stock_name >> stock_per >> stock_dividend >> stock_pbr) {
    stocks_name[stock_id] = stock_name;
    stocks_per[stock_id] = stock_per;
    stocks_dividend[stock_id] = stock_dividend;
    stocks_pbr[stock_id] = stock_pbr;
  }
  twse_dividend_file.close();

  std::ofstream stock_information_file("information.txt");
  std::ifstream stock_list_file("list.txt");
  while (stock_list_file >> stock_id) {
    stock_information_file << stock_id << "\t" << stocks_name[stock_id] << "\t" << stocks_per[stock_id] << "\t" << stocks_dividend[stock_id] << "\t" << stocks_pbr[stock_id] << "\n";
  }
  stock_list_file.close();
  stock_information_file.close();
  return 0;
}
