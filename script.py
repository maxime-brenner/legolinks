from shops import lego_data_from_html, amazon_price_from_html
from dbUtilities import connect_to_db, add_column, read_datas, view_columns_names
from models import ProductLego, Minifigs
from test_shop_class import Lego, Amazon
from regie import Webgain, AmazonPartner
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.sql.expression import func
#import requests
#import tweepy
from twitterBot import set_api
import json, collections

def show_all_datas():
    Session=sessionmaker(bind=connect_to_db()["engine"])
    session=Session()

    query=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.link_amazon, ProductLego.product_name, ProductLego.theme))

    for p in session.query(ProductLego): print(p.productId, p.product_name, p.theme, p.link_lego, p.link_amazon)

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

def post_thread_from_query(query, msg):
    api=set_api()

    product_message="Le jouet {theme} {name} avec {nb_pieces} pièces est disponible dans la boutique Amazon pour {price}€ \nProfitez-en maintenant\n{trackedl}"

    original_status=api.update_status(msg)

    for p in query: 
        link=p.link_amazon
        print(link)
        res=Amazon().single_page_datas_extraction(link)
        trackedl=AmazonPartner("legolinks-21").create_aff_link(link)
        new_product=api.update_status(status=product_message.format(theme=p.theme, name=p.product_name, nb_pieces=p.nb_pieces, price=res["price"], trackedl=trackedl), in_reply_to_status_id=original_status.id, )

def post_random_product():
    #Set the api to create status
    api=set_api()

    #Randomly choose a product, update datas and set the tracked link
    lego=Lego()
    session=lego.create_session()
    random_product=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name).filter(ProductLego.productId < 100000).order_by(func.random()).limit(1)).first()
    res=lego.single_page_datas_extraction(random_product[1])
    trackedl=Webgain("1639880", "268085").create_aff_link(random_product[1])

    if res["sale"] != 0:
        msg="Le jouet {theme} {name} avec {nb_pieces} pièces est en promo dans la boutique LEGO pour {price}€ soit unr réduction de {reduction:.2f}%\nProfitez-en maintenant\n{trackedl}".format(theme=res["theme"],name=res["name"], nb_pieces=res["nb_pieces"], price=res["price"], reduction=res["reduction"], trackedl=trackedl)
    else:
        msg="Le jouet {theme} {name} avec {nb_pieces} pièces est disponible dans la boutique LEGO pour {price}€ \nProfitez-en maintenant\n{trackedl}".format(theme=res["theme"],name=res["name"], nb_pieces=res["nb_pieces"], price=res["price"], trackedl=trackedl)
    #Post message
    api.update_status(msg)
    print(msg, res)


def post_thread():
    api=set_api()

    query=session.execute(sqlalchemy.select(ProductLego.productId,  ProductLego.product_name, ProductLego.link_lego, ProductLego.theme).filter(ProductLego.theme=="LEGO Super Mario").limit(6))

    original_message="Une sélection de 6 jouets LEGO SUper Mario disonibles dans la boutique LEGO\nDéroulez le thread pour continuer\n👇👇👇"
    product_message="Le jouet {theme} {name} avec {nb_pieces} pièces est disponible dans la boutique LEGO pour {price}€ \nProfitez-en maintenant\n{trackedl}"

    original_status=api.update_status(original_message)

    for p in query: 
        res=Lego().single_page_datas_extraction(p.link_lego)
        trackedl=Webgain("1639880", "268085").create_aff_link(p.link_lego)
        new_product=api.update_status(status=product_message.format(theme=p.theme, name=p.product_name, nb_pieces=res["nb_pieces"], price=res["price"], trackedl=trackedl), in_reply_to_status_id=original_status.id, )

 
def post_product_from_link(msg, link):

    api=set_api()

    trackedl=Webgain("1639880", "268085").create_aff_link(link)

    to_post=msg.format(trackedl=trackedl)

    api.update_status(to_post)

def post_minifig_day():

    api=set_api()

    minifig=session.execute(sqlalchemy.select(Minifigs.minifig_name, Minifigs.minifig_url, Minifigs.productlego_set).order_by(func.random()).limit(1)).first()
    name=minifig.name
    set=minifig.productlego_set


    to_post_msg="🗓️Tous les jours, découvrez une minifigurine LEGO🗓️\nAjd, c'est Abraham Lincoln, de la Grande Aventure Lego, sorti en 2014.\nIl est présent dans les sets: 71004, 71023A\nA demain pour une nouvelle minifigurine!"


#Amazon().amazon_price_from_html("https://www.amazon.fr/stores/page/2686D5FE-3511-4FBB-A7CD-D3ACC396BD11?channel=hp-r1-rs-deals-q4")


def add_lego():
    session=Lego().create_session()
    none=session.query(ProductLego.productId).filter(ProductLego.link_lego==None)
    for n in none: 

        print(n.productId)

        try:
            link="https://www.lego.com/fr-be/product/{id}".format(id=n.productId)
            res=Lego().single_page_datas_extraction(link)

            try: 
                n.product_name=res["name"]
                n.link_lego=link
                n.nb_pieces=res["nb_pieces"]
                n.theme=res["theme"]

                Lego().create_session.commit()
            except Exception as e:
                print(e)

        except:
            pass

session=Lego().create_session()
object_list=[]
q=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.link_amazon, ProductLego.product_name, ProductLego.theme, ProductLego.nb_pieces))
for p in q: 
    d=collections.OrderedDict()
    d["productid"]=p.productId
    d["name"]=p.product_name
    d["link_lego"]=p.link_lego
    d["link_amazon"]=p.link_amazon
    d["theme"]=p.theme
    d["nb_pieces"]=p.nb_pieces
    object_list.append(d)
    
j=json.dumps(object_list)

with open ('lego_db.js', 'w') as f:
    f.write(j)