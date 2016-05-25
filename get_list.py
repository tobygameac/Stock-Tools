import pycurl

from StringIO import StringIO

def IsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def GetID(s):
    strs = s.replace('&nbsp;', '').replace('>', '<').split('<')
    if len(strs) > 2 and IsInt(strs[2]):
        return strs[2]
    return ''

html_filename = 'list.html'
text_filename = 'list.txt'

print 'output html in : ' + html_filename

with open(html_filename, 'wb') as f:
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://www.emega.com.tw/js/StockTable.htm')
    c.setopt(c.WRITEDATA, f)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()
    c.close()

html = open(html_filename)
lines = html.readlines()
html.close()
lines_count = len(lines)

print 'output text in : ' + text_filename

with open(text_filename, 'w') as list_text_file:
    for i in range(lines_count):
        stock_id = GetID(lines[i])
        if stock_id != '':
            google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + str(stock_id)
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
                    if response_code == 200:
                        list_text_file.write(stock_id + '\n')
                        print stock_id
                    got_html = True
                except:
                    print 'try again : ' + stock_id
                    continue
    list_text.close()

print 'done'
