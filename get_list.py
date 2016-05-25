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


html_text = StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://www.emega.com.tw/js/StockTable.htm')
c.setopt(c.WRITEFUNCTION, html_text.write)
c.setopt(c.FOLLOWLOCATION, True)
c.perform()
c.close()

lines = html_text.getvalue().split('\n')

lines_count = len(lines)

list_file_path = 'list.txt'

with open(list_file_path, 'w') as list_file:
    for i in range(lines_count):
        stock_id = GetID(lines[i])
        if stock_id != '':
            google_stock_url = 'http://finance.google.com/finance/info?client=ig&q=TPE:' + str(stock_id)
            got_html = False
            while not got_html:
                try:
                    c = pycurl.Curl()
                    c.setopt(c.URL, google_stock_url)
                    c.setopt(c.FOLLOWLOCATION, True)
                    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
                    c.perform()
                    response_code = c.getinfo(pycurl.HTTP_CODE)
                    c.close()
                    if response_code == 200:
                        list_file.write(stock_id + '\n')
                    got_html = True
                except:
                    continue

    list_file.write('00632R\n')
