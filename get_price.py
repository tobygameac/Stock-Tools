import datetime
import json
import os
import pycurl

from StringIO import StringIO

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

directory = str(year) + str(month).zfill(2) + str(day).zfill(2) + '\\'

if not os.path.exists(directory):
    os.makedirs(directory)

stock_list_filename = 'list.txt'
stock_list_file = open(stock_list_filename)

stock_ids = stock_list_file.readlines()
stock_list_file.close()


price_text_filename = directory + 'price.txt'

with open(price_text_filename, 'w') as price_text_file:
    for stock_id in stock_ids:
        stock_id = stock_id.rstrip() 
        google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + stock_id
        storage = StringIO()
        
        got_html = False
        while not got_html:
          try:
              c = pycurl.Curl()
              c.setopt(c.URL, google_stock_url)
              c.setopt(c.WRITEFUNCTION, storage.write)
              c.setopt(c.FOLLOWLOCATION, True)
              c.perform()
              response_code = c.getinfo(pycurl.HTTP_CODE)
              c.close()
              got_html = True
          except:
              print 'try again : ' + stock_id
              continue
        if response_code == 200:
            json_str = storage.getvalue()[6:-3]
            json_data = json.loads(json_str)
            price_text_file.write(stock_id + '\t' + json_data['l_fix'] + '\n')

    price_text_file.close()

print 'done'
