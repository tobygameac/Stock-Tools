import datetime
import os
import sys

data_directory = 'price_records\\'

stock_list_file_path = 'list.txt'
with open(stock_list_file_path) as stock_list_file:
    stock_ids = stock_list_file.readlines()

for stock_id in stock_ids:
    stock_id = stock_id.rstrip()

    records_path = data_directory + str(stock_id) + '.txt'

    dates = []
    high = []
    low = []
    close = []

    with open(records_path, 'r') as records_file:
        lines = records_file.readlines()

        for line in lines:
            tokens = line.split()
            try:
                h = float(tokens[4])
                l = float(tokens[5])
                c = float(tokens[6])
            except:
                continue

            dates.append(tokens[0]);
            high.append(h)
            low.append(l)
            close.append(c)


    total_days = len(close)

    ma_path = data_directory + str(stock_id) + '_ma.txt'

    ma_days = [5, 10, 20, 60]

    with open(ma_path, 'w') as ma_file:
        
        for i in range(ma_days[0] - 1, total_days):
            ma_file.write(dates[i] + ' ')
            for ma_day in ma_days:
                if i >= ma_day - 1:
                    average = sum(close[i - ma_day + 1 : i + 1]) / float(ma_day)
                    ma_file.write(str(round(average, 2)) + ' ')
                    
            ma_file.write('\n')
                    
    
    kd_path = data_directory + str(stock_id) + '_kd.txt'

    with open(kd_path, 'w') as kd_file:

        alpha = 1.0 / 3.0

        kd_n = 9

        old_k = 0
        old_d = 0
        
        for i in range(kd_n - 1, total_days):
            highest = max(high[i - kd_n + 1 : i + 1])
            lowest = min(low[i - kd_n + 1 : i + 1])

            if highest != lowest:
                rsv = 100.0 * (close[i] - lowest) / (highest - lowest) 

                k = alpha * rsv + (1 - alpha) * old_k
                d = alpha * k + (1 - alpha) * old_d
            else:
                k = old_k
                d = old_d

            if i == (kd_n - 1):
                k = 50.0
                d = 50.0

            old_k = k
            old_d = d

            kd_file.write(dates[i] + ' ' + str(round(rsv, 2)) + ' ' + str(round(k, 2)) + ' ' + str(round(d, 2)) + '\n')
