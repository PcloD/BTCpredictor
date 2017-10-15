from urllib2 import Request, urlopen, URLError
import json
import csv
import string
import time 
from time import mktime
import dateutil.parser
from datetime import datetime


csvf = open('./csv/output2.csv', 'rb')
out = open('okcoin5s.csv', 'a')
print(csvf.readline())
reader = csv.reader(csvf, delimiter='|')

def compare(item1, item2):
	t1 = time.strptime(item1[0], "%Y-%m-%d %H:%M:%S")
	t2 = time.strptime(item2[0], "%Y-%m-%d %H:%M:%S")
	dt1 = datetime.fromtimestamp(mktime(t1))
	dt2 = datetime.fromtimestamp(mktime(t2))
	if dt1 < dt2:
		return -1
	elif dt1 > dt2:
		return 1
	else:
		return 0

def comp(i1, i2):
	a = float(i1[0])
	b = float(i2[0])
	hi = a - b
	# print ("COMP", a, b, a-b)
	if a < b:
		return -1
	elif a > b:
		return 1
	else:
		return 0

l = []
i = 0
for row in reader:
	# t = row[0]
	# t = t[0:-6]
	
	# s = row[2]
	# s = s.split('"')
	# coinbase_price = s[2]
	# val = (t,coinbase_price)
	# l.append(val)
	
	s1 = row[5]
	s1 = s1.split('"')
	date = s1[2]
	ok_price = s1[16]

	ok_depth = row[6]
	ok_depth = ok_depth.split(':')
	# print (ok_depth)
	asks = ok_depth[1]
	bids = ok_depth[2]
	
	asklist = eval(asks[1:-8])
	bidlist = eval(bids[1:-3])
	
	vask = 0
	vbid = 0

	for a in asklist:
		vask += float(a[1])

	for b in bidlist:
		vbid += float(b[1])

	i += 1
	# print (i, vask)
	# print (i, vbid)
	# if i > 10:
	# 	break

	val = [date, ok_price, vask, vbid]
	l.append(val)
	# print(val)

# print l
l = sorted(l, cmp=comp)
# print('~~~~~~~~~~~~~~~~~~~~~~~~~')
# print l

for k in l:
	out.write(str(k[0]) + ',' + str(k[1])+ ',' + str(k[2]) + ',' + str(k[3]))
	out.write('\n')

# out.close()









# for row in reader:
# 	print ', '.join(row)



# ...     for row in spamreader:
# ...         print ', '.join(row)


# ["id"|"coinbase_sell"|"coinbase_spot_rate"|"okcoin_trades"|"coinbase_buy"|"okcoin_ticker"|"okcoin_depth"]
#  "id","coinbase_sell","coinbase_spot_rate","okcoin_trades","coinbase_buy","okcoin_ticker","okcoin_depth"


# print s[:100]
# s = s.replace('\\"','"')
# print s[:100]
# s = s.replace('=>',': ')
# print s[:100]
# s = s.replace('"{','{')

# print s[:100]
# print s[-30:]
# s = s.replace('}"','}')
# print s[-30:]
# s = s.replace('"[','[')
# print s[-30:]
# s = s.replace(']"',']')
# print s[-30:]
# s = s.replace('\n',' ')
# print s[-30:]


# x = json.load(df)
# wdf.write(s)
# print x




# # print s

# wdf.write(s)
# j = json.load(wdf)
# print j['coinbase_sell']


# s = df.readline()
# j = json.dumps(s)
# d = json.load(j)
# print d

# replace 
# '\"' with '"'
# => with : 
# '"{' with '{'
# '}"' with '}'
# '"[' with '['
# ']"' with ']'

# df = open('output', 'r')
# j = json.dumps(df)

# d = json.load(json.dumps(df))
# print d['id']
# s = df.readline()
# print s[2:4]



# for i in range(1,120):
# 	url = 'https://api.coinbase.com/v1/prices/historical?page=' + str(i)
# 	request = Request(url)

# 	try:
# 		f = open('coinbase10Data.csv', 'a')
# 		response = urlopen(request)
# 		data = response.read()
# 		f.write(data)
# 		f.write('\n')
# 		print str(i) + ' -> ' + str(len(data))

# 		# print data
# 		# print kittens[559:1000]

# 	except URLError, e:
# 	    print 'Error: No data. Got an error code:', e