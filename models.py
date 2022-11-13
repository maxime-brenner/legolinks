from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

class ProductLego(declarative_base()):
	__tablename__="productLego"

	productId=Column(Integer, primary_key=True)
	link_lego=Column(String(255))
	link_amazon=Column(String(255))
	number_piece=Column(Integer)