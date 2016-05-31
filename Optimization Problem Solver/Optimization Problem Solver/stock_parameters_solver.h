#pragma once

#define IL_STD

#include <fstream>
#include <iostream>
#include <iomanip>

#include <ilcplex\ilocplex.h>
#include <ilconcert\iloexpression.h>

class StockParametersSolver {

public:

  void Solve() {
    IloEnv environment;
    IloNumVarArray variables(environment);
    IloExpr expression(environment);

    const size_t VARIABLE_COUNT = 5;

    for (size_t i = 0; i < VARIABLE_COUNT; ++i) {
      variables.add(IloNumVar(environment, -IloInfinity, IloInfinity));
    }

    std::ifstream stock_data("stock.txt");

    double need_amount = 750;

    double price, buy_amount, sell_amount, buy_price, sell_price;
    double fi_buy, it_buy, dealer_buy;
    double new_price;

    while (stock_data >> price >> buy_amount >> sell_amount >> buy_price >> sell_price
      >> fi_buy >> it_buy >> dealer_buy
      >> new_price) {
      if ((buy_amount + sell_amount) < need_amount) {
        continue;
      }

      double buy_percent = buy_amount / (buy_amount + sell_amount);
      double wave = (price - buy_price) / buy_price;
      double earned = (new_price - price) / price;

      expression += IloPower((
        variables[0] * (fi_buy > 0)
        + variables[1] * (it_buy > 0)
        + variables[2] * (dealer_buy > 0)
        + variables[3] * (buy_amount > sell_amount)
        + variables[4] * buy_percent
        //+ variables[5] * price
        //+ variables[6] * buy_price
        //+ variables[7] * sell_price
      ) - earned, 2.0);
    }

    IloModel model(environment);

    model.add(IloMinimize(environment, expression));

    IloCplex cplex(model);

    cplex.setOut(environment.getNullStream());

    if (!cplex.solve()) {
      std::cout << "Failed to optimize the model.\n";
    } else {
      std::cout << "Solved.\n";
    }

    IloNumArray result(environment);

    cplex.getValues(result, variables);

    std::cout << "Minimum : at (";
    for (size_t i = 0; i < VARIABLE_COUNT; ++i) {
      std::cout << std::fixed << std::setprecision(3) << result[i] << ((i == (VARIABLE_COUNT - 1)) ? ")\n" : ", ");
    }
  }

};
