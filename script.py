from shops import lego_price_from_html
from dbUtilities import connect_to_db, add_column, read_datas, view_columns_names
from models import ProductLego
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import requests



Session=sessionmaker(bind=connect_to_db()["engine"])
session=Session()

query=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.product_name))

#for p in session.query(ProductLego): print(p.collection)

#add_column(connect_to_db()["engine"], "productLego", sqlalchemy.Column('product_name', sqlalchemy.String(100)))

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







