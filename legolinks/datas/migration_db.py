import sqlalchemy
from sqlalchemy.orm import sessionmaker
from ....legolinks.models import ProductLego


def connect_to_db():
	engine=sqlalchemy.create_engine('sqlite:///legoDB.db')
	connection=engine.connect()
	metadata=sqlalchemy.MetaData()

	return {"engine":engine, "connection":connection, "metadata":metadata}

def show_all_datas():
    Session=sessionmaker(bind=connect_to_db()["engine"])
    session=Session()

    query=session.execute(sqlalchemy.select(ProductLego.productId, ProductLego.link_lego, ProductLego.link_amazon, ProductLego.product_name, ProductLego.theme))

    for p in session.query(ProductLego): print(p.productId, p.product_name, p.theme, p.link_lego, p.link_amazon)

show_all_datas()

