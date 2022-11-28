import requests, re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.orm import sessionmaker
from models import ProductLego


class Shop():
    def __init__(self):
        self.header={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fr-FR,fr-FR;q=0.9,en;q=0.8'
            }
        self.domain="https://www.lego.com{0}"

    #Get a page from a url and parse it
    def parser(self, url):
        #Connect to the page
        req=requests.get(url, headers=self.header, allow_redirects=True)
        soup=BeautifulSoup(req.text, 'html.parser')
        print(req.status_code)

        return soup
    
    #Etablish conncetion to database
    def connect_to_db(self):
        engine=create_engine('sqlite:///legoDB.db')
        connection=engine.connect()
        metadata=MetaData()

        return {"engine":engine, "connection":connection, "metadata":metadata}

    def create_session(self):
        Session=sessionmaker(bind=self.connect_to_db()["engine"])
        session=Session()

        return session

class Lego(Shop):

    #Get every products on a multi-products page and check if it's in the database.
    #Otherwise, add the product in the database
    def multiple_product_extraction(self, url):

        #Initiate session
        session=self.create_session()


        #Prepare the page  
        soup=self.parser(url)

        list_to_check=soup.find_all("li", {"data-test":"product-item"})
    
        for p in list_to_check:
            try:
                link=self.domain.format(p.find("a", {"data-test":"product-leaf-title-link"}, href=True)["href"])
                productId=int(re.search("([\d]{0,})$", link).group(0))
                name=p.find("span", {"class":"Markup__StyledMarkup-sc-nc8x20-0 dbPAWk"}).getText()
                print(link, productId, name)

                try:
                    new_product=session.query(ProductLego.productId).filter(ProductLego.productId == productId).scalar()
                    new_product is not None 
                    print("Add new product {0} in db".format(productId,) )

                    try:
                        
                        session.execute(insert(ProductLego).values({ProductLego.productId:productId, ProductLego.link_lego:link, ProductLego.product_name:name, ProductLego.theme:"LEGO Super Mario"}))
                        session.commit()
                        
                        print ("{0} succesfully add to the db".format(productId,))
                    except Exception as e:
                        print("Impossible to add product")
                        print(e)
                    
                except Exception as e:
                    print(e)
                    print("Product {0} already in the db".format(productId,))


            except TypeError:
                print("No link to analyze")
                pass

        try:
            next_link=soup.find("a", {"data-test":"pagination-next"}, href=True)["href"]
            print(next_link)
            self.multiple_product_extraction(self.domain.format(next_link))
        except:
            pass

        session.close()


    #Extract datas from a product page 
    def single_page_datas_extraction(self, url):

        #Prepare the page  
        soup=self.parser(url)

        #Extract datas
        price=float(soup.find('span', {"data-test":"product-price"}).getText().replace('Price','').replace(',','.').replace('€',''))
        
        name=soup.find("h1", {"data-test":"product-overview-name"}).find('span', {"class":"Markup__StyledMarkup-sc-nc8x20-0 dbPAWk"}).getText()
        nb_pieces=soup.find("div", {"data-test":"pieces-value"}).getText()

        try:
            sale=float(soup.find('span', {"data-test":"product-price-sale"}).getText().replace('Sale Price','').replace(',','.').replace('€',''))
            reduction=((price-sale)/price)*100
        except AttributeError:
            sale=0
            reduction=0

        return {"name": name, "price": price, "sale": sale, "reduction":reduction,"nb_pieces": int(nb_pieces)}