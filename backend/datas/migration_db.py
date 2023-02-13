from sqlalchemy import select, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from shopclass.models import ProductLego
#from models import ProductLego as pl
import json
import collections



def connect_to_db():
	engine=create_engine('sqlite:///legoDB.db')
	connection=engine.connect()
	metadata=MetaData()

	return {"engine":engine, "connection":connection, "metadata":metadata}

def show_all_datas():
    Session=sessionmaker(bind=connect_to_db()["engine"])
    session=Session()

    query=session.execute(select(ProductLego.productId, ProductLego.link_lego, ProductLego.link_amazon, ProductLego.product_name, ProductLego.theme))

    for p in session.query(ProductLego): print(p.productId, p.product_name, p.theme, p.link_lego, p.link_amazon)
    
Session=sessionmaker(bind=connect_to_db()["engine"])
session=Session()

object_list=[]

q=session.execute(select(ProductLego.productId, ProductLego.link_lego, ProductLego.link_amazon, ProductLego.product_name, ProductLego.theme, ProductLego.nb_pieces))
for p in session.query(ProductLego): 
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
    
    
    
    print(p.productId, p.product_name, p.theme, p.link_lego, p.link_amazon)

#ProductLego(productid=i['productid'], name=i['name'], link_lego=i['link_lego'], nb_pieces=i['nb_pieces'], theme=i['theme'])


