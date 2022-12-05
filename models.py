from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from dbUtilities import connect_to_db

Base=declarative_base()

#class Association(Base):

	#__tablename__="association_table"

	#productlego_id= Column(ForeignKey("ProductLego.productId"), primary_key=True)
	#minifigs_id= Column(ForeignKey("minifigs.minifigId"), primary_key=True)
	#extra_data=Column(String(50))
	#minifigs=relationship("Minifigs", back_populates="productlego")
	#productlego=relationship("ProductLego", back_populates="minifigs")

class ProductLego(Base):

	__tablename__="productLego"

	productId=Column(Integer, primary_key=True)
	product_name=Column(String(100))
	link_lego=Column(String(255))
	link_amazon=Column(String(255))
	nb_pieces=Column(Integer)
	theme=Column("theme", String(100))
	collection=Column("collection", String(100))
	#minifigs=relationship("Association", back_populates="productlego")


class Minifigs(Base):

	__tablename__="minifigs"

	minifigId = Column(Integer, primary_key=True)
	minifig_name = Column(String(100))
	minifig_url = Column(String(255))
	#productlego=relationship("Association", back_populates="minifigs")


meta=MetaData()
newtab=Table("minifigs", meta,
			Column("productLego_set", ForeignKey("productLego.productId")),
)

meta.create_all(connect_to_db()["engine"])
