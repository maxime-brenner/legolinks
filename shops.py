import os, requests, bs4, re
from sqlalchemy.orm import sessionmaker, declarative_base
from models import ProductLego



header={
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'fr-FR,fr-FR;q=0.9,en;q=0.8'
}

shops_variable={
	'lego' : {
		'domain':'https://www.lego.com',
		'price-product':['span', {"data-test":"product-price"}],

	},

}

def lego_price_from_html(url):
	file_name=str((re.search('(\d){5}', url).group(0)))+"lego.txt"

	if file_name not in os.listdir(os.getcwd()):
		req=requests.get(url)

		with open (file_name, 'w', encoding='UTF-8') as f:
			f.write(req.text)
			print("New product registed")
			
			file=open(file_name, 'r', encoding='UTF-8')

			soup=bs4.BeautifulSoup(file, 'html.parser')
			price=soup.find('span', {"data-test":"product-price"})
			print(price)
			float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))



		return float_price
		
	else:
		print("File already exists")
		file=open(file_name, 'r', encoding='UTF-8')
		soup=bs4.BeautifulSoup(file, 'html.parser')
		price=soup.find('span', {"data-test":"product-price"})
		print(price)
		float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

		return float_price

def amazon_price_from_html_from_file(url, header):
	
	file_name=str((re.search('(\d){5}', url).group(0)))+"amazon.html"

	if file_name not in os.listdir(os.getcwd()):
		req=requests.get(url, headers=header)

		with open (file_name, 'w', encoding='UTF-8') as f:
			f.write(req.text)
			print("New product registed")
			
			#file=open(file_name, 'r', encoding='UTF-8')

			#soup=bs4.BeautifulSoup(file, 'html.parser')
			#price=soup.find('span', {"data-test":"product-price"})
			#print(price)
			#float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))



		return "New product registed"
		
	else:
		print("File already exists")
		file=open(file_name, 'r', encoding='UTF-8')
		soup=bs4.BeautifulSoup(file, 'html.parser')
		price=soup.find('span', {"class":"a-price-whole"})
		print(price.getText())
		#float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

		return "File already exists"

def amazon_price_from_html(url, header):
	
	req=requests.get(url, headers=header)
	soup=bs4.BeautifulSoup(req.text, 'html.parser')
	price=soup.find('span', {"class":"a-price-whole"}).getText()+'.'+soup.find('span', {"class":"a-price-fraction"}).getText()
	print(price)
	#float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

		

def cdiscount_price_from_html(url, header):
	file_name=str((re.search('(\d){5}', url).group(0)))+"cdiscount.txt"

	if file_name not in os.listdir(os.getcwd()):
		req=requests.get(url, headers=header)

		with open (file_name, 'w', encoding='UTF-8') as f:
			f.write(req.text)
			print("New product registed")
			
			file=open(file_name, 'r', encoding='UTF-8')

			soup=bs4.BeautifulSoup(file, 'html.parser')
			price=soup.find('span', {"class":"fpPrice price priceColor jsMainPrice jsProductPrice hideFromPro"})
			print(price)
			float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))



		return float_price
		
	else:
		print("File already exists")
		file=open(file_name, 'r', encoding='UTF-8')
		soup=bs4.BeautifulSoup(file, 'html.parser')
		price=soup.find('span', {"class":"fpPrice price priceColor jsMainPrice jsProductPrice hideFromPro"})
		print(price)
		float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

		return float_price

def cultura_price_from_html(url):
	file_name=str((re.search('(\d){5}', url).group(0)))+"cultura.txt"

	if file_name not in os.listdir(os.getcwd()):
		req=requests.get(url)

		with open (file_name, 'w', encoding='UTF-8') as f:
			f.write(req.text)
			print("New product registed")
			
			file=open(file_name, 'r', encoding='UTF-8')

			soup=bs4.BeautifulSoup(file, 'html.parser')
			price=soup.find('div', {"class":"d-block price price--big"})
			print(price)
			float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))



		return float_price
		
	else:
		print("File already exists")
		file=open(file_name, 'r', encoding='UTF-8')
		soup=bs4.BeautifulSoup(file, 'html.parser')
		price=soup.find('div', {"class":"d-block price price--big"})
		print(price)
		float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

		return float_price


def to_float():
	soup=bs4.BeautifulSoup(file, 'html.parser')
	#links=soup.find_all("a", {"data-test":"product-leaf-title-link"}, href=True)

	price=soup.find_all('span', {"data-test":"product-price"})
	to_nb=re.search('(\d+,\d+)', price[0].getText()).group(0)

	to_nb=float(to_nb.replace(',', '.'))

	print(float(to_nb), type(to_nb))


def page_to_db_lego(url):

	Session=sessionmaker(bind=connect_to_db()["engine"])
	session=Session()

	#Get the page to extract some datas and parse it
	req=requests.get(url)
	soup=bs4.BeautifulSoup(req.text, 'html.parser')
	links=soup.find_all("a", {"data-test":"product-leaf-title-link"}, href=True)

	#Create connection to db
	conn=connect_to_db()["connection"]
	

	#Extract datas
	for link in links:
		productId=int(re.search('(\d+)$', link['href']).group(0))
		
		

		#Check if the ID is in the db
		try: 

			is_exist=session.query(ProductLego.productId).filter(ProductLego.productId==productId).with_entities(ProductLego.productId==productId).one()[0]

			print("{0}  already exists, {1}".format(productId, is_exist))

		#Else, insert new data's row
		except NoResultFound:

			print("Creating new datas {0}".format(productId, )) 

			dlink="http://lego.com"+link['href']
			to_insert=ProductLego(productId=productId, link_lego=dlink)
			session.add(to_insert)
			session.commit()

			print("Datas insert!")

	session.close()

	next=soup.find("a", {"data-test":"pagination-next"}, href=True)
	print(next["href"])

	if next["href"]:
		page_to_db_lego("http://lego.com"+next["href"])
	else:
		print("No more data to scrap")
		pass