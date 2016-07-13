import csv
import datetime
import os
import sys
import urllib2 

records_directory = 'price_records\\'

if not os.path.exists(records_directory):
    os.makedirs(records_directory)

current_date = datetime.date.today()

stock_list_file_path = 'list.txt'
with open(stock_list_file_path) as stock_list_file:
    stock_ids = stock_list_file.readlines()

for stock_id in stock_ids:
    stock_id = stock_id.rstrip()
    print 'Fetching : ' + stock_id

    records_path = records_directory + str(stock_id) + '.txt'

    last_date_in_file = datetime.date(1993, 1, 1)

    with open(records_path, 'a+') as records_file:
        lines = records_file.readlines()
        if len(lines) > 0:
            tokens = lines[-1].replace('/', ' ').split(' ')
            if len(tokens) > 2:
                last_date_in_file = datetime.date(int(tokens[0]), int(tokens[1]), int(tokens[2]))

        print 'Start from : ' + str(last_date_in_file.year) + '-' + str(last_date_in_file.month)

        for year in range(last_date_in_file.year, current_date.year + 1):
            
            is_the_first_month = False

            start_month = 1
            if year == last_date_in_file.year:
                start_month = last_date_in_file.month
                is_the_first_month = True

            last_month = 12
            if year == current_date.year:
                last_month = current_date.month

            for month in range(start_month, last_month + 1):
                is_the_first_month = is_the_first_month and (month == start_month)

                date_str_without_day = str(year) + str(month).zfill(2)
                url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report' + date_str_without_day + '/' + date_str_without_day + '_F3_1_8_' + str(stock_id) + '.php&type=csv'

                got_html = False
                while not got_html:
                    try:
                        response = urllib2.urlopen(url)
                        got_html = response.code == 200
                    except:
                        continue
                
                csv_lines = csv.reader(response)
                
                for csv_line in csv_lines:
                    if len(csv_line) == 9 and csv_line[0][0] == ' ':
                        csv_line[0] = csv_line[0][1:]
                        
                        is_new_date = True

                        tokens = csv_line[0].split('/')
                        line_date = datetime.date(int(tokens[0]) + 1911, int(tokens[1]), int(tokens[2]))
                        csv_line[0] = str(int(tokens[0]) + 1911) + '/' + tokens[1] + '/' + tokens[2]
                        
                        if is_the_first_month:
                            if line_date <= last_date_in_file:
                                is_new_date = False
                                #print 'Skipped : ' + str(line_date)

                        if is_new_date:
                            print 'Added : ' + str(line_date)
                            output_line = ''
                            for column in range(8):
                                output_line = output_line + csv_line[column] + ' '
                            output_line = output_line + csv_line[8] + '\n'
                            records_file.write(output_line)

print 'Done'
