from models import ProductLego
from test_shop_class import Lego
from regie import Webgain
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from twitterBot import set_api

def post_random_product():
    #Set the api to create status
    api=set_api()

    #Randomly choose a product, update datas and set the tracked link
    lego=Lego()
    session=lego.create_session()
    random_product=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name).filter(ProductLego.productId < 100000).order_by(func.random()).limit(1)).first()
    res=lego.single_page_datas_extraction(random_product[1])
    trackedl=Webgain("1639880", "268085").create_aff_link(random_product[1])
    msg="Le jouet LEGO {0} avec {1} pièces est disponible dans la boutique LEGO pour {2}€ \nProfitez-en maintenant\n{3}".format(res["name"], res["nb_pieces"], res["price"], trackedl)
    
    #Post message
    api.update_status(msg)

post_random_product()