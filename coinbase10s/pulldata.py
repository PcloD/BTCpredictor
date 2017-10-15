from urllib2 import Request, urlopen, URLError


for i in range(1,120):
	url = 'https://api.coinbase.com/v1/prices/historical?page=' + str(i)
	request = Request(url)

	try:
		f = open('coinbase10Data.csv', 'a')
		response = urlopen(request)
		data = response.read()
		f.write(data)
		f.write('\n')
		print str(i) + ' -> ' + str(len(data))

		# print data
		# print kittens[559:1000]

	except URLError, e:
	    print 'Error: No data. Got an error code:', e