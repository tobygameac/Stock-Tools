# -*- coding: utf-8 -*-
import codecs
import datetime

from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pool_size = 6

broker_id = '922H'
records_directory = 'price_records\\'

def PoolInitilizer(trade_date):
    global date_str
    date_str = str(trade_date.year) + '-' + str(trade_date.month) + '-' + str(trade_date.day)

def GetLineValue(s):
    strs = s.replace('>', '<').split('<')
    if len(strs) <= 2:
        return ''
    try:
        value = strs[2].replace(',', '').rstrip()
        return value
    except:
        return ''

def BrokerAnalysis(stock_id):
    stock_id = stock_id.rstrip()

    url = 'https://cathaysec.nvesto.com/tpe/' + stock_id + '/brokerAnalysis#!/fromdate/' + date_str + '/todate/' + date_str + '/broker/' + broker_id

    values = []


    try:
        driver = webdriver.Chrome()

        driver.get(url)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "chart1")))
        
        page_source = driver.page_source

    except:
        try:
            driver.close()
        except:
            return []

        return []

    try:
        driver.close()
    except:
        return []

    values.append(stock_id)

    for line in page_source.split('\n'):
        if '<div class="tex_value24 tex_black">' in line:
            values.append(int(GetLineValue(line)))

    if len(values) > 5:
        values = values[ : 2] + values[-2 : ]
    
    if len(values) < 5:
        return []

    return values


if __name__ == '__main__':
    
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

    date_str = str(trade_date.year) + '-' + str(trade_date.month) + '-' + str(trade_date.day)

    pool = Pool(pool_size, PoolInitilizer, (trade_date, ))
    broker_analysis_values = pool.map(BrokerAnalysis, stock_ids)

    broker_analysis_file_path = 'broker_analysis.txt'

    with open(broker_analysis_file_path, 'w') as broker_analysis_file:
        for values in broker_analysis_values:
            
            if len(values) != 5:
                continue

            for value in values[ : -1]:
                broker_analysis_file.write(str(value) + '\t')
            broker_analysis_file.write(str(values[-1]) + '\n')
