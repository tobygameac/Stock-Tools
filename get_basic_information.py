# -*- coding: utf-8 -*-
import datetime
import json
import os
import pycurl

from multiprocessing import Pool
from StringIO import StringIO

pool_size = 128

records_directory = 'price_records\\'

def PoolInitilizer(trade_date):
    global date_str
    date_str = str(trade_date.year) + '-' + str(trade_date.month) + '-' + str(trade_date.day)

def GetLineValue(s):
    strs = s.replace('>', '<').split('<')
    if len(strs) <= 2:
        return ''
    try:
        value = strs[2].replace(',', '').rstrip().decode('big5').encode('utf8')
        return value
    except:
        return ''

def FetchInformation(stock_id):

    stock_id = stock_id.rstrip()
    print 'Fetching : ' + stock_id

    url_text = StringIO()

    #google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + stock_id

    
    #got_good_response = false
    #while not got_good_response:
    #    try:
    #        c = pycurl.curl()
    #        c.setopt(c.url, google_stock_url)
    #        c.setopt(c.writefunction, url_text.write)
    #        c.setopt(c.followlocation, true)
    #        c.perform()
    #        response_code = c.getinfo(pycurl.http_code)
    #        c.close()
    #        got_good_response = true
    #    except:
    #        continue

    #if response_code == 200:
    #    google_stock_json_str = url_text.getvalue()[6:-3]
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

    got_good_response = False
    while not got_good_response:
        try:
            c = pycurl.Curl()
            #c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=1')
            c.setopt(c.URL, 'http://jdata.yuanta.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=1')
            #c.setopt(c.URL, 'http://5850web.moneydj.com/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=1')
            c.setopt(c.WRITEFUNCTION, url_text.write)
            c.setopt(c.FOLLOWLOCATION, True)
            c.perform()
            c.close()
            got_good_response = True
        except:
          print c.getinfo(pycurl.HTTP_CODE)
          continue

    buy_amount = sell_amount = buy_price = sell_price = '0'

    lines = url_text.getvalue().split('\n')
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

    got_good_response = False
    while not got_good_response:
        try:
            c = pycurl.Curl()
            #c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=' + stock_id + '&c=' + date_str + '&d=' + date_str)
            c.setopt(c.URL, 'http://jdata.yuanta.com.tw/z/zc/zcl/zcl.djhtm?a=' + stock_id + '&c=' + date_str + '&d=' + date_str)
            #c.setopt(c.URL, 'http://5850web.moneydj.com/z/zc/zcl/zcl.djhtm?a=' + stock_id + '&c=' + date_str + '&d=' + date_str)
            c.setopt(c.WRITEFUNCTION, url_text.write)
            c.setopt(c.FOLLOWLOCATION, True)
            c.perform()
            c.close()
            got_good_response = True
        except:
          continue

    fi_buy = it_buy = dealer_buy = 0

    lines = url_text.getvalue().split('\n')
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
        if len(lines) >= 60:
            tokens = lines[-4].split(' ')
            ma_5 = float(tokens[1])
            ma_10 = float(tokens[2])
            ma_20 = float(tokens[3])
            ma_60 = float(tokens[4])

            ma_good = (close_price >= ma_60) and (close_price >= ma_20) and (close_price >= ma_5)

            ma_good = ma_good and (ma_5 >= ma_10) and (ma_10 >= ma_20)

    kd_path = records_directory + str(stock_id) + '_kd.txt'

    kd_good = False

    kd_frames = 35;

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

    return stock_id, close_price, buy_amount, sell_amount, buy_price, sell_price, fi_buy, it_buy, dealer_buy, start_price, high_price, low_price, str(ma_good), str(kd_good)

if __name__ == '__main__':
    
    os.system('price_records.py')
    os.system('technical_analysis.py')

    output_directory = 'basic_information\\'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    stock_list_file_path = 'list.txt'
    with open(stock_list_file_path) as stock_list_file:
        stock_ids = stock_list_file.readlines()

    stock_list_file_path = 'list_otc.txt'
    with open(stock_list_file_path) as stock_list_file:
        stock_ids.extend(stock_list_file.readlines())


    with open(records_directory + '0050.txt', 'r') as records_file:
        lines = records_file.readlines()
        tokens = lines[-1].replace('/', ' ').split(' ')
        last_date_in_file = datetime.date(int(tokens[0]), int(tokens[1]), int(tokens[2]))

    trade_date = last_date_in_file

    pool = Pool(pool_size, PoolInitilizer, (trade_date, ))
    informations = pool.map(FetchInformation, stock_ids)

    result_file_path = output_directory + str(trade_date.year) + str(trade_date.month).zfill(2) + str(trade_date.day).zfill(2) + '.txt'
    with open(result_file_path, 'w') as result_file:
        for information in informations:
            for token in information[ : -1]:
                result_file.write(str(token) + '\t')
            result_file.write(information[-1] + '\n')
            
    print 'Done : get basic information'
