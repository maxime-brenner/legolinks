import requests, re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.orm import sessionmaker
from datas.models import ProductLego
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class Shop():
    def __init__(self):
        self.header={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fr-FR,fr-FR;q=0.9,en;q=0.8'
            }
        

    #Get a page from a url and parse it
    def parser(self, url):
        #Connect to the page
        req=requests.get(url, headers=self.header, allow_redirects=True)
        soup=BeautifulSoup(req.text, 'html.parser')
        print(req.status_code, req.url)

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
    def __init__(self):
        super().__init__()
        self.domain=self.domain="https://www.lego.com{0}"

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
                    res=self.single_page_datas_extraction(link)
                    print("Add new product {0} in db".format(productId,) )

                    try:
                        
                        session.execute(insert(ProductLego).values({ProductLego.productId:productId, ProductLego.link_lego:link, ProductLego.product_name:name, ProductLego.theme:res["theme"], ProductLego.nb_pieces:res["nb_pieces"]}))
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
        theme=soup.find("div", {"class":"ProductOverviewstyles__Container-sc-1a1az6h-2 dkHUOp"}).find("span", {"itemprop":"brand"}).getText()

        #Check if sales are available
        try:
            sale=float(soup.find('span', {"data-test":"product-price-sale"}).getText().replace('Sale Price','').replace(',','.').replace('€',''))
            reduction=((price-sale)/price)*100
        except AttributeError:
            sale=0
            reduction=0

        return {"name": name, "price": price, "sale": sale, "reduction":reduction,"nb_pieces": int(nb_pieces), "theme":theme}

class Amazon(Shop):

    def __init__(self):
        super().__init__()
        self.domain="https://www.amazon.fr"

    #Open a browser via Selenium, load all the page and extract datas
    def multiple_product_extraction(self, url):

        #Open a browser via Selenium
        driver=webdriver.Chrome()
        driver.get(url)
        options=webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        #Scroll the page for loading all the elements
        
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        #Search for the links of the products
        elements=driver.find_elements(By.CLASS_NAME, "style__overlay__2qYgu.ProductGridItem__overlay__1ncmn")
        
        
        for e in elements:
            link=e.get_attribute("href")
            
            #Extract the id of the product
            try:
                id=int(re.search("\d{5}", link).group(0))
                session=self.create_session()
                to_check=session.query(ProductLego).filter(ProductLego.productId==id).first()

                #If not in the database, put the product in it
                if to_check is None:
                    print("This article is not in the database: {id}".format(id=id,))

                    try:
                        newlego=ProductLego(productId=id, link_amazon=link)
                        session.add(newlego)
                        session.commit()
                    except Exception as e:
                        print("Erreur lors de la mise à jour de l'article {id}: {e}".format(id=id, e=e,))

                #If known, add the amazon link
                else:
                    print("Article already in the database :{id}".format(id=id,))

                    try:
                        to_check.link_amazon=link
                        session.commit()
                    except Exception as e:
                        print("Erreur lors de l'ajout de l'article {id}: {e}".format(id=id, e=e,))
                    

            except Exception as e:
                print("Erreur :{e}".format(e=e))
                pass

    #Extract datas from a single page
    def single_page_datas_extraction(self, url):

        #Initiate session
        session=self.create_session()

        #Prepare the page  
        soup=self.parser(url)

        #Extract price
        left=soup.find('span', {"class":"a-price-whole"}).getText().replace(",","")
        fraction=soup.find('span', {"class":"a-price-fraction"}).getText()

        price="{left}.{fraction}".format(left=left, fraction=fraction)	
        price=float(price)
        #float_price=float((re.search('(\d+,\d+)', price.getText()).group(0)).replace(",", "."))

        try:
            ancient=soup.find('span', {"class":"a-price a-text-price"}).find('span', {"class":"a-offscreen"}).getText().replace(",",".").replace("€","")
            ancient=float(ancient)
            sale="%.2f" % ((ancient-price)/ancient)
        except:
            ancient=None
            sale=None
            pass

        return {"price": price, "ancient":ancient, "sale":sale}


		

