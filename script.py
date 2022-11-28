from shops import lego_data_from_html, amazon_price_from_html
from dbUtilities import connect_to_db, add_column, read_datas, view_columns_names
from models import ProductLego
from test_shop_class import Lego
from regie import Webgain
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.sql.expression import func
import requests


Session=sessionmaker(bind=connect_to_db()["engine"])
session=Session()

#query=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name))

#for p in session.query(ProductLego): print(p.productId, p.product_name)

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

lego=Lego()



#print(lego.multiple_product_extraction("https://www.lego.com/fr-fr/themes/super-mario"))

#print(lego.single_page_datas_extraction("https://www.lego.com/fr-fr/product/super-mario-64-question-mark-block-71395"))

#amazon_price_from_html("https://www.amazon.fr/stores/page/1B219DA7-55D7-4F81-8901-6D08B96D2A1F?channel=hp-r4-ss-starwars-q4")

random_product=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name).filter(ProductLego.productId < 100000).order_by(func.random()).limit(1)).first()
res=lego.single_page_datas_extraction(random_product[1])
trackedl=Webgain("1639880", "268085").create_aff_link(random_product[1])
print("Le jouet LEGO {0} avec {1} pièces est disponible dans la boutique LEGO pour {2}€ \nProfitez-en maintenant\n{3}".format(res["name"], res["nb_pieces"], res["price"], trackedl))

#for p in random_product: print(p)