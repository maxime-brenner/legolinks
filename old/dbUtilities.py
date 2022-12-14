import sqlalchemy, re
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey

#Connect to sqlite db
def connect_to_db():
	engine=sqlalchemy.create_engine('sqlite:///legoDB.db')
	connection=engine.connect()
	metadata=sqlalchemy.MetaData()

	return {"engine":engine, "connection":connection, "metadata":metadata}

def create_session(engine):
	Session=sessionmaker(bind=engine)
	session=Session() 
 
	return session
    

#Query to create the db
def create_table():
	productLego=sqlalchemy.Table('productLego', metadata,
									sqlalchemy.Column('link', sqlalchemy.String(255)),
									sqlalchemy.Column('productId', sqlalchemy.Integer())
									)

	metadata.create_all(engine)

#Inserting values in the db
def insert_datas(table):
	for l in links:
		productId=re.search('(\d){5}', l['href']).group(0)
		new_link='https://www.lego.com'+l['href']
		print(new_link)

		
		query=sqlalchemy.update(table).values(link=new_link)
		connection.execute(query)

#Read all datas from a table
def read_datas(table, conn):
	
	results= conn.execute(sqlalchemy.select([table])).fetchall()
	return results

#Add column to a table
def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

#To view the columns name
def view_columns_names(table):
	columns = [m.key for m in table.__table__.columns]
	print (columns)



