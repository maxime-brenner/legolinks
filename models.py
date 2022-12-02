from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

class ProductLego(declarative_base()):
	__tablename__="productLego"

	productId=Column(Integer, primary_key=True)
	product_name=Column(String(100))
	link_lego=Column(String(255))
	link_amazon=Column(String(255))
	nb_pieces=Column(Integer)
	theme=Column("theme", String(100))
	collection=Column("collection", String(100))


#class Minifigs(declarative_base()):

	#__tablename__="minifigs"

