# -*- coding: utf-8 -*-
import csv
import datetime
import os
import pycurl
import sys
import urllib2 

from multiprocessing import Pool
from StringIO import StringIO

pool_size = 128

records_directory = 'price_records\\'

current_date = datetime.date.today()

def FetchTWSE(stock_id):
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

                got_good_response = False
                while not got_good_response:
                    try:
                        response = urllib2.urlopen(url)
                        got_good_response = response.code == 200
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

def FetchOTC(stock_id):
    stock_id = stock_id.rstrip()
    print 'Fetching : ' + stock_id

    records_path = records_directory + str(stock_id) + '.txt'

    last_date_in_file = datetime.date(1994, 1, 1)

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

                url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_download.php?d=' + str(year - 1911) + '/' + str(month).zfill(2) + '&stkno=' + str(stock_id)

                url_text = StringIO()

                got_good_response = False
                while not got_good_response:
                    try:
                        c = pycurl.Curl()
                        c.setopt(c.URL, url)
                        c.setopt(c.WRITEFUNCTION, url_text.write)
                        c.setopt(c.FOLLOWLOCATION, True)
                        c.perform()
                        c.close()
                        got_good_response = True
                    except:
                      continue

                csv_lines = csv.reader(url_text.getvalue().split('\n')[5:-1])

                for csv_line in csv_lines:
                    if len(csv_line) == 9 and csv_line[1] != '0':

                        #csv_line[1] = csv_line[1] + '000'
                        #csv_line[2] = csv_line[2] + '000'
                        
                        is_new_date = True

                        tokens = csv_line[0].split('/')

                        # Remove invalid character on the first date
                        while len(tokens[2]) > 0:
                            try:
                                line_day = int(tokens[2])
                                break
                            except:
                                tokens[2] = tokens[2][:-1]
                        
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

if __name__ == '__main__':

    if not os.path.exists(records_directory):
        os.makedirs(records_directory)

    stock_list_file_path = 'list.txt'
    with open(stock_list_file_path) as stock_list_file:
        stock_ids = stock_list_file.readlines()

    #for stock_id in stock_ids:
        #FetchTWSE(stock_id)

    pool = Pool(pool_size)
    pool.map(FetchTWSE, stock_ids)

    stock_list_file_path = 'list_otc.txt'
    with open(stock_list_file_path) as stock_list_file:
        stock_ids = stock_list_file.readlines()

    #for stock_id in stock_ids:
        #FetchOTC(stock_id)

    pool.map(FetchOTC, stock_ids)
    
    print 'Done : price records'
