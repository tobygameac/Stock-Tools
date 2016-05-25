# -*- coding: utf-8 -*-
import datetime
import os
import pycurl

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

directory = str(year) + str(month).zfill(2) + str(day).zfill(2) + '\\'

if not os.path.exists(directory):
    os.makedirs(directory)

def GetLineValue(s):
    strs = s.replace('>', '<').split('<')
    if len(strs) <= 2:
        return ''
    try:
        value = strs[2].replace(',', '').rstrip().decode('big5').encode('utf8')
        return value
    except:
        return ''


price_filename = directory + 'price.txt'
price_file = open(price_filename)
price_lines = price_file.readlines()
price_file.close()

price_table = dict()
for price_line in price_lines:
    stock_id, price = price_line.split()
    price_table[stock_id] = price

days = 5

stock_list_filename = 'list.txt'
stock_list_file = open(stock_list_filename)

stock_ids = stock_list_file.readlines()
stock_list_file.close()

html_filename = directory + 'temp.html'
#html_filename = str(target) + '_' + str(day) + 'days.html'

result_filename = directory + 'result.txt'
result_file = open(result_filename, 'w')

for stock_id in stock_ids:
    stock_id = stock_id.rstrip() 
    html_file = open(html_filename, 'wb')

    got_html = False
    while not got_html:
        try:
            c = pycurl.Curl()
            #c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=' + str(day))
            c.setopt(c.URL, 'http://jdata.yuanta.com.tw/z/zc/zco/zco.djhtm?a=' + stock_id + '&b=' + str(day))
            c.setopt(c.WRITEDATA, html_file)
            c.setopt(c.FOLLOWLOCATION, True)
            c.perform()
            c.close()
            got_html = True
        except:
          continue

    html_file.close()

    html_file = open(html_filename, 'r')

    lines = html_file.readlines()
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
    result_file.write(stock_id + '\t' + price_table[stock_id] + '\t' + buy_amount + '\t' + sell_amount + '\t' + buy_price + '\t' + sell_price + '\n')

    html_file.close()

result_file.close()
