# -*- coding: utf-8 -*-
import datetime
import json
import os
import pycurl

from StringIO import StringIO

os.system('price_records.py')
os.system('technical_analysis.py')

records_directory = 'price_records\\'


with open(records_directory + '0050.txt', 'r') as records_file:
    lines = records_file.readlines()
    tokens = lines[-1].replace('/', ' ').split(' ')
    last_date_in_file = datetime.date(int(tokens[0]), int(tokens[1]), int(tokens[2]))

#trade_date = datetime.datetime.now()
trade_date = last_date_in_file

year = trade_date.year
month = trade_date.month
day = trade_date.day
date_str = str(year) + '-' + str(month) + '-' + str(day)

output_directory = str(year) + str(month).zfill(2) + str(day).zfill(2) + '\\'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def GetLineValue(s):
    strs = s.replace('>', '<').split('<')
    if len(strs) <= 2:
        return ''
    try:
        value = strs[2].replace(',', '').rstrip().decode('big5').encode('utf8')
        return value
    except:
        return ''

check_days = 1

stock_list_file_path = 'list.txt'
with open(stock_list_file_path) as stock_list_file:
    stock_ids = stock_list_file.readlines()

result_file_path = output_directory + 'basic_information.txt'
with open(result_file_path, 'w') as result_file:
    for stock_id in stock_ids:
        
        stock_id = stock_id.rstrip()
        print 'Fetching : ' + stock_id

        html_text = StringIO()

        #google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + stock_id

        
        #got_html = false
        #while not got_html:
        #    try:
        #        c = pycurl.curl()
        #        c.setopt(c.url, google_stock_url)
        #        c.setopt(c.writefunction, html_text.write)
        #        c.setopt(c.followlocation, true)
        #        c.perform()
        #        response_code = c.getinfo(pycurl.http_code)
        #        c.close()
        #        got_html = true
        #    except:
        #        continue

        #if response_code == 200:
        #    google_stock_json_str = html_text.getvalue()[6:-3]
        #    google_stock_data = json.loads(google_stock_json_str)

        #    price = google_stock_data['l_fix']

        records_path = records_directory + str(stock_id) + '.txt'

        with open(records_path, 'r') as records_file:
            lines = records_file.readlines()
            tokens = lines[-1].split(' ')
            start_price = tokens[3]
            high_price = tokens[4]
            low_price = tokens[5]
            close_price = tokens[6]

        got_html = False
        while not got_html:
            try:
                c = pycurl.Curl()
                #c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=' + str(check_days))
                c.setopt(c.URL, 'http://jdata.yuanta.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=' + str(check_days))
                c.setopt(c.WRITEFUNCTION, html_text.write)
                c.setopt(c.FOLLOWLOCATION, True)
                c.perform()
                c.close()
                got_html = True
            except:
              continue

        lines = html_text.getvalue().split('\n')
        length = len(lines)
        for i in range(length):
            if GetLineValue(lines[i]) == '合計買超張數':
                buy_amount = GetLineValue(lines[i + 1])
            elif GetLineValue(lines[i]) == '合計賣超張數':
                sell_amount = GetLineValue(lines[i + 1])
            elif GetLineValue(lines[i]) == '平均買超成本':
                buy_price = GetLineValue(lines[i + 1])
            elif GetLineValue(lines[i]) == '平均賣超成本':
                sell_price = GetLineValue(lines[i + 1])
                break;

        got_html = False
        while not got_html:
            try:
                c = pycurl.Curl()
                #c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=' + stock_id + '&c=' + date_str + '&d=' + date_str)
                c.setopt(c.URL, 'http://jdata.yuanta.com.tw/z/zc/zcl/zcl.djhtm?a=' + stock_id + '&c=' + date_str + '&d=' + date_str)
                c.setopt(c.WRITEFUNCTION, html_text.write)
                c.setopt(c.FOLLOWLOCATION, True)
                c.perform()
                c.close()
                got_html = True
            except:
              continue

        lines = html_text.getvalue().split('\n')
        length = len(lines)
        for i in range(length):
            if GetLineValue(lines[i]) == '合計買賣超':
                fi_buy = GetLineValue(lines[i + 1])
                it_buy = GetLineValue(lines[i + 2])
                dealer_buy = GetLineValue(lines[i + 3])
                break;

        ma_path = records_directory + str(stock_id) + '_ma.txt'

        ma_good = False

        with open(ma_path, 'r') as ma_file:
            lines = ma_file.readlines()
            if len(lines) >= 20:
                tokens = lines[-4].split(' ')
                ma_5_1 = float(tokens[1])
                ma_10_1 = float(tokens[2])
                ma_20_1 = float(tokens[3])
                tokens = lines[-3].split(' ')
                ma_5_2 = float(tokens[1])
                ma_10_2 = float(tokens[2])
                ma_20_2 = float(tokens[3])
                tokens = lines[-2].split(' ')
                ma_5_3 = float(tokens[1])
                ma_10_3 = float(tokens[2])
                ma_20_3 = float(tokens[3])
                tokens = lines[-1].split(' ')
                ma_5_4 = float(tokens[1])
                ma_10_4 = float(tokens[2])
                ma_20_4 = float(tokens[3])

                ma_good = (close_price < ma_5_3) and (close_price > ma_5_4)

                ma_good = ma_good or ((ma_5_4 > ma_5_3) and (ma_5_1 < ma_20_1) and (ma_5_2 < ma_20_2) and (ma_5_3 > ma_20_3) and (ma_5_4 > ma_20_4))

                ma_good = ma_good or ((ma_5_4 > ma_5_3) and (ma_5_1 < ma_10_1) and (ma_5_2 < ma_10_2) and (ma_5_3 > ma_10_3) and (ma_5_4 > ma_10_4))

        kd_path = records_directory + str(stock_id) + '_kd.txt'

        kd_good = False

        
        kd_frames = 40;

        with open(kd_path, 'r') as kd_file:
            lines = kd_file.readlines()
            for check_days in range(1):
                if len(lines) >= 2 + check_days:
                    tokens = lines[-2 - check_days].split(' ')
                    previous_k = float(tokens[2])
                    previous_d = float(tokens[3])
                    tokens = lines[-1 - check_days].split(' ')
                    current_k = float(tokens[2])
                    cuttent_d = float(tokens[3])
                    kd_good = kd_good or ((previous_k < previous_d) and (current_k > cuttent_d) and (current_k > previous_k) and (current_k < kd_frames))

        result_file.write(stock_id + '\t' + close_price + '\t' + buy_amount + '\t' + sell_amount + '\t' + buy_price + '\t' + sell_price + '\t')
        result_file.write(fi_buy + '\t' + it_buy + '\t' + dealer_buy + '\t')
        result_file.write(start_price + '\t' + high_price + '\t' + low_price + '\t')
        result_file.write(str(ma_good) + '\t' + str(kd_good) + '\n')

print 'Done.'
#raw_input()
