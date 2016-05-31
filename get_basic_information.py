# -*- coding: utf-8 -*-
import datetime
import json
import os
import pycurl

from StringIO import StringIO

trade_date = datetime.datetime.now()
while trade_date.weekday() >= 5:
    trade_date = trade_date - datetime.timedelta(1)
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

        google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + stock_id

        html_text = StringIO()
        
        got_html = False
        while not got_html:
            try:
                c = pycurl.Curl()
                c.setopt(c.URL, google_stock_url)
                c.setopt(c.WRITEFUNCTION, html_text.write)
                c.setopt(c.FOLLOWLOCATION, True)
                c.perform()
                response_code = c.getinfo(pycurl.HTTP_CODE)
                c.close()
                got_html = True
            except:
                continue

        if response_code == 200:
            google_stock_json_str = html_text.getvalue()[6:-3]
            google_stock_data = json.loads(google_stock_json_str)

            price = google_stock_data['l_fix']

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

        result_file.write(stock_id + '\t' + price + '\t' + buy_amount + '\t' + sell_amount + '\t' + buy_price + '\t' + sell_price + '\t')
        result_file.write(fi_buy + '\t' + it_buy + '\t' + dealer_buy + '\n')

print 'Done.'
#raw_input()
