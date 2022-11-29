from shops import lego_data_from_html, amazon_price_from_html
from dbUtilities import connect_to_db, add_column, read_datas, view_columns_names
from models import ProductLego
from test_shop_class import Lego
from regie import Webgain
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.sql.expression import func
import requests
import tweepy
from twitterBot import set_api

def show_all_datas():
    Session=sessionmaker(bind=connect_to_db()["engine"])
    session=Session()

    query=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name, ProductLego.theme))

    for p in session.query(ProductLego): print(p.productId, p.product_name, p.theme)

#add_column(connect_to_db()["engine"], "productLego", sqlalchemy.Column('product_name', sqlalchemy.String(100)))
def up_db():
    for l in query:

        if l[2] is None:
            try:
                res=lego_price_from_html(l[1])
                up=session.execute(sqlalchemy.update(ProductLego).values({ProductLego.product_name:res["name"]}).where(ProductLego.productId==l[0]))
                session.commit()
            except :
                print("Error occurs")
                pass
        else:
            print("name already in table")

        print(l)





#print(lego.multiple_product_extraction("https://www.lego.com/fr-fr/themes/super-mario"))

#print(lego.single_page_datas_extraction("https://www.lego.com/fr-fr/product/super-mario-64-question-mark-block-71395"))

#amazon_price_from_html("https://www.amazon.fr/stores/page/1B219DA7-55D7-4F81-8901-6D08B96D2A1F?channel=hp-r4-ss-starwars-q4")



#for p in random_product: print(p)

def post_random_product():
    #Set the api to create status
    api=set_api()

    #Randomly choose a product, update datas and set the tracked link
    lego=Lego()
    random_product=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name).filter(ProductLego.productId < 100000).order_by(func.random()).limit(1)).first()
    res=lego.single_page_datas_extraction(random_product[1])
    trackedl=Webgain("1639880", "268085").create_aff_link(random_product[1])

    if res["sale"] != 0:
        msg="Le jouet {theme} {name} avec {nb_pieces} pièces est en promo dans la boutique LEGO pour {price}€ soit unr réduction de {reduction:.2f}%\nProfitez-en maintenant\n{trackedl}".format(theme=res["theme"],name=res["name"], nb_pieces=res["nb_pieces"], price=res["price"], reduction=res["reduction"], trackedl=trackedl)
    else:
        msg="Le jouet {theme} {name} avec {nb_pieces} pièces est disponible dans la boutique LEGO pour {price}€ \nProfitez-en maintenant\n{trackedl}".format(theme=res["theme"],name=res["name"], nb_pieces=res["nb_pieces"], price=res["price"], trackedl=trackedl)
    #Post message
    #api.update_status(msg)
    print(msg, res)

Lego().multiple_product_extraction("https://www.lego.com/fr-be/themes/city")