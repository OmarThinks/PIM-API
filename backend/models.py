import os
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, func
import json
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from flask_sqlalchemy import SQLAlchemy
import types
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute


from __init__ import (Base, engine, session)

SUPPORTED_TYPES = [int,str,float,bool,type(None),list]
RESTRICTED_FIELDS=["password"]




# This is the only old code that will need to change
# Here I am not using flask_sqlalchemy
# This will happen in case of needing to establish relationships
# between models
#from flask_sqlalchemy.model import DefaultMeta

"""
NotReceived
This class is used when the dada is not received
By default, it will have the value of None
None != Not received
"""
class NotReceived():
	pass



"""
validate_key

- Inputs:
	- the_object: dict or object
		- The Object, or the dict of the data to be validated
		- Example:
			- user_to_insert (as an object)
			- {"id":1,"username":"abc","password":"pass"}
	- key: str:
		- the key of the dict that contains the data
		- Example:
			- "id"
	- id: bool : default = False
		- Should we pass the id or not
		- True: let the id pass
		- False: do not le the id pass (Default)
	- unsupported : bool: default = False
		- pass unsupported data types, not in SUPPORTED_TYPES list
		- If the type was unsupported, it must have the simple function
		- True: let it pass
		- False: do not let it pass (Default)
	- dangerous : bool: default = False
		- pass dangerous keys, in SUPPORTED_TYPES list
		- True: let it pass
		- False: do not let it pass (Default)
- Function:
	- telling us whether we should let this key of this object or dict pass or not
- Output:
	- True: let ths pass
	- False: do not let this key pass
"""
def validate_key(the_object,key:str,
	id:bool=False,
	unsupported:bool = False,
	dangerous:bool=False):
	if type(the_object) == dict:
		the_attribute = the_object[key]
	else:
		the_attribute = getattr(the_object, key)

	# Validating fields startng with "_"
	if key[0] == "_":
		return False
	# Validating NotReceived
	if type(the_attribute) == type(NotReceived):
		return False
	# Validating id
	if key.lower() == "id" and id == False:
		return False
	# Validating supported types
	if ((type(the_attribute)not in SUPPORTED_TYPES) and (unsupported==True)):
		if type(the_attribute) == types.MethodType:
			return False
		if key in ["metadata","query"]:
			return False
		if type(type(the_attribute)) == DeclarativeMeta:
			return True
		if ((type(the_attribute) == InstrumentedList)):
			return True
		return False
	if type(the_attribute) not in SUPPORTED_TYPES:
		return False
	# validating dangerous fields
	if ((key.lower() in RESTRICTED_FIELDS) and (dangerous==False)):
		return False
	return True


"""
get_dict

- Inputs:
	- the_object: dict or object
		- The Object, or the dict of the data to be validated
		- Example:
			- user_to_insert (as an object)
			- {"id":1,"username":"abc","password":"pass"}
	- id: bool : default = False
		- Should we pass the id or not
		- True: let the id pass
		- False: do not le the id pass (Default)
	- unsupported : bool: default = False
		- pass unsupported data types, not in SUPPORTED_TYPES list
		- If the type was unsupported, it must have the simple function
		- True: let it pass
		- False: do not let it pass (Default)
	- dangerous : bool: default = False
		- pass dangerous keys, in SUPPORTED_TYPES list
		- True: let it pass
		- False: do not let it pass (Default)
- Function:
	- convert the object or the dict to a validated dict of fileds
	- The fuelds will be validated, and you will get the clean fields
		and their values only
- Output:
	- dict clean
"""
def get_dict(the_object,id:bool=False,
	unsupported:bool = False,
	dangerous:bool=False):
	keys_list=[]
	if type(the_object)==dict:
		for key in the_object:
			keys_list.append(key)
	else:
		keys_list = dir(the_object)
	toReturn = {}
	for key in keys_list:
		if validate_key(the_object,key,id,unsupported,dangerous):
			if type(the_object)==dict:
				toReturn[key] = the_object[key]
				continue
			toReturn[key] = getattr(the_object,key)
	return toReturn



class MyModel():
	# For creating the model
	def __init__(self, **kwargs):
		#dangerous = True, we may need to enter the password
		validated_kwargs = get_dict(kwargs,dangerous=True,id=False)
		for key in validated_kwargs:
			setattr(self,key,validated_kwargs[key])
	# For inserting the model in the db
	def insert(self):
		#print(self)
		try:
			session.add(self)
			session.commit()
		except:
			session.rollback()
	# For updating the model
	def update(self,**kwargs):
		try:
			#restrcted = True, we may need to update the password
			validated_kwargs = get_dict(kwargs,dangerous=True)
			for key in validated_kwargs:
				setattr(self,key,validated_kwargs[key])
			session.commit()
		except:
			session.rollback()
	# For deleting the model from the db
	def delete(self):
		try:
			session.delete(self)
			session.commit()
		except:
			session.rollback()
	# getting the attributes of the model, inculding id, but not dangerous fields
	def simple(self):
		# Prepare to delete all the keys starting with "_", or key == "id"
		validated_self = get_dict(self, id=True)
		toReturn = {}
		for key in validated_self:
			toReturn[key] = validated_self[key]
		return toReturn
	# For printng the model
	def __repr__(self):
		#print("rpr")
		return json.dumps(self.simple())
	# For getting the model and the forigen keys of the model
	def deep(self):
		toReturn = {}
		validated_self = get_dict(self, id=True,unsupported=True)
		for key in validated_self:
			if validate_key(self,key,id=True) == True:
				# Here key is normal or id, not unsupported
				toReturn[key] = validated_self[key]
				continue
			# If it has this function, then it is a column in the table
			try:
				toReturn[key] = validated_self[key].simple()
			except Exception as e:
				toReturn[key] = []
				children_list = validated_self[key]
				for child in children_list:
					toReturn[key].append(child.simple())
		return toReturn
	@classmethod
	def query(cls, **kwargs):
		return session.query(cls, **kwargs)




class Product(Base,MyModel):
	#__metaclass__=MyModel
	__tablename__="product"
	# Autoincrementing, unique primary key
	id = Column(Integer(), primary_key=True)
	# String product name
	name = Column(String(), unique=False, nullable=False) # REQUIRED
	# name could be like "fish"
	# name should not be unique
	price =  Column(Float(), unique=False, nullable=False) # REQUIRED
	# price the the price of selling
	# it should be float, because it it can have parts
	# It should not be unique
	# It can never be null, What are you selling then?
	quantity = Column(Float() , unique = False, nullable=False) # REQUIRED
	# how many of the object do you have
	# It should be float, because it can be divided
	# Example: 2.5 Kg of cheese
	# It can not be unique
	# It is required, it can not be equal to null
	code =  Column(Integer(), unique=True, nullable=True) # OPTIONAL
	# code in the barcode on the product
	# https://www.barcodelookup.com/
	# This should be a number
	# Each barcode should be unique
	# It can have the value of null, 
	# 	because the product may be unregistered

	categories = relationship("ProductCategory",cascade="all, delete-orphan",
		passive_deletes=False,backref="product")



	def __init__(self,**kwargs):
		MyModel.__init__(self,**kwargs)	
		





class Category(Base,MyModel):
	#__metaclass__=MyModel
	__tablename__="category"
	# Autoincrementing, unique primary key
	id = Column(Integer(), primary_key=True)
	# String category name
	name = Column(String(), unique=True, nullable=False) # REQUIRED
	# name could be like "Electronics"
	# name must be unique
	parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)

	parent = relationship('Category', remote_side=[id], backref="children")

	#products = relationship("Category",cascade="all, delete-orphan",
	#	passive_deletes=False,backref="product_category")

	products = relationship("ProductCategory",cascade="all, delete-orphan",
		passive_deletes=False,backref="category")

	def __init__(self,**kwargs):
		MyModel.__init__(self,**kwargs)	
	
	def simple(self):
		toReturn=MyModel.simple(self)
		if "parent" in toReturn:
			del toReturn["parent"]
		return toReturn





"""
This is the assoiation atble between products and Categories
"""
class ProductCategory(Base,MyModel):
	"""docstring for ProductCategory"""
	__tablename__="product_category"
	# Autoincrementing, unique primary key
	id = Column(Integer(), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), 
		nullable=False, unique=False)
	# This is the id of the product
	# This links the products and this table
	# It should not be null
	# If the product is deleted, the record should be deleted too
	category_id = Column(Integer, ForeignKey('category.id'), 
		nullable=False, unique=False)
	# This is the id of the category
	# This links the categories and this table
	# It should not be null
	# If the category is deleted, the record should be deleted too



def create_all():
	session.close()
	Base.metadata.create_all(engine)
	




def db_drop_and_create_all():
	session.close()
	#db.drop_all()
	#db.create_all()
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)



def populate_tables():
	db_drop_and_create_all()
	products = list()
	products.append(Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611))
	products.append(Product(name="CPU",price=1,
		quantity=9, code=789999884))
	products.append(Product(name="Mouse",price=2,
		quantity=9, code=789451))
	products.append(Product(name="Mobile",price=20.1,
		quantity=9, code=8444441))
	products.append(Product(name="Printer",price=90.4,
		quantity=2))

	session.add_all(products)
	session.commit()

	categories = list()
	categories.append(Category(name="Electronics")) #1
	categories.append(Category(name="Camera", parent_id=1)) #2
	categories.append(Category(name="Eletronic Cameras", parent_id=2)) #3
	categories.append(Category(name="Manual Cameras", parent_id=2)) #4
	
	categories.append(Category(name="Cars")) #5
	categories.append(Category(name="Sport Cars", parent_id=5)) #6
	categories.append(Category(name="Electric Cars", parent_id=5)) #7
	categories.append(Category(name="Tractors", parent_id=5)) #8
	categories.append(Category(name="Tesla", parent_id=7)) #9
	
	categories.append(Category(name="Clothes")) #10
	categories.append(Category(name="Shirts", parent_id=10)) #11
	categories.append(Category(name="Trousers", parent_id=10)) #12
	categories.append(Category(name="Jackets", parent_id=10)) #13


	session.add_all(categories)
	session.commit()




	pc = list()
	pc.append(ProductCategory(product_id=1, category_id=1)) #1
	pc.append(ProductCategory(product_id=1, category_id=2)) #2
	pc.append(ProductCategory(product_id=1, category_id=3)) #3
	pc.append(ProductCategory(product_id=1, category_id=4)) #4
	pc.append(ProductCategory(product_id=1, category_id=5)) #5

	pc.append(ProductCategory(product_id=2, category_id=1)) #6
	pc.append(ProductCategory(product_id=2, category_id=2)) #7
	pc.append(ProductCategory(product_id=2, category_id=3)) #8
	pc.append(ProductCategory(product_id=2, category_id=4)) #9
	pc.append(ProductCategory(product_id=2, category_id=5)) #10

	pc.append(ProductCategory(product_id=3, category_id=1)) #11
	pc.append(ProductCategory(product_id=3, category_id=2)) #12
	pc.append(ProductCategory(product_id=3, category_id=3)) #13
	pc.append(ProductCategory(product_id=3, category_id=4)) #14
	pc.append(ProductCategory(product_id=3, category_id=5)) #15

	session.add_all(pc)
	session.commit()


