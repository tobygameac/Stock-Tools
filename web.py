import pycurl

def PrintRawLine(s):
    strs = s.replace('>', '<').split('<')
    print strs[2]          

target = input('target id : ')
day = 30

filename = str(target) + '_' + str(day) + 'days.html'

print 'output in : ' + str(filename)

# As long as the file is opened in binary mode, both Python 2 and Python 3
# can write response body to it without decoding.
with open(filename, 'wb') as f:
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco.djhtm?a=' + str(target) + '&b=' + str(day))
    c.setopt(c.WRITEDATA, f)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()
    c.close()

html = open(filename)
lines = html.readlines()
lines_count = len(lines)
for i in range(lines_count):
    if (i >= 266 and i < 270) or (i >= 272 and i < 276):
        PrintRawLine(lines[i])
