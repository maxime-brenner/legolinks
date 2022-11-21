import shops
from dbUtilities import connect_to_db
from models import ProductLego
from sqlalchemy.orm import sessionmaker

#page_to_db_lego("https://www.lego.com/fr-fr/themes/star-wars")

Session=sessionmaker(bind=connect_to_db()["engine"])
session=Session()

for p in session.query(ProductLego): print(p.productId)