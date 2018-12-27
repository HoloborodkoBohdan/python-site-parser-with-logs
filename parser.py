import urllib.request
import os
import time
from bs4 import BeautifulSoup

time = time.strftime("%Y-%m-%d-%H-%M")

dir = os.path.dirname(os.path.abspath(__file__))

host = 'http://videx.ua'
file = open("log-{}.csv".format(time), "w")

for line in open("products.txt"):
	data = line.split(",")
	sku = data[1].strip()
	url = "{}/search/word={}/".format(host, data[0])
	print(url)
	url = urllib.request.urlopen(url)
	if url.getcode() == 200:
		soup = BeautifulSoup(url, "lxml")
		product_link = soup.find('a', attrs={'class': 'i'})
		if product_link:
			product_link = "{}{}".format(host, product_link.get('href'))
			print(product_link)
			product_url = urllib.request.urlopen(product_link)
			if product_url.getcode() == 200:
				soup = BeautifulSoup(product_url, "lxml")
				data = soup.find('a', attrs={'class': 'all popupLink popupWindow-popupGallery'}).get('href')
				href = "{}{}".format(host, data)
				print(href)
				img = urllib.request.urlopen(href).read()
				name = href[href.rfind(".")+1:].strip()
				path = "{}/images/{}.{}".format(dir, sku, name)
				f = open(path, "wb")
				f.write(img)
				f.close()
				#print(path)
			else:
				print("Не удалось открыть страницу товара {}".format(data[1]))
		else:
			print("{} не найден на сайте".format(sku), file=file)		
	else:
	 	print("Не получен HTTP ответ 200")