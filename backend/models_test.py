import json
import unittest
from models import (NotReceived, validate_key,
MyModel, Product,Category,ProductCategory,
	populate_tables, db_drop_and_create_all,get_dict,)
#from app import create_app
from __init__ import session


unittest.TestLoader.sortTestMethodsUsing = None

class modelsTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		#db_drop_and_create_all()
		#create_app()
		# create and configure the app
		#self.app = create_app(testing=True) #Flask(__name__)
		#self.client = self.app.test_client
		#db.app = self.app
		#db.init_app(self.app)
		#db.create_all()
		pass

	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_001_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")


	def test_002_test(self):
		db_drop_and_create_all()
		print("Test 2:db_drop_and_create_all")


	def test_0a_1_1_1_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key))
		self.assertEqual([False,False,True,True,True,False],validated)
		print("Test 0a_1_1_1 : validate_key: success")

	def test_0a_1_1_2_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,id=True))
		self.assertEqual([True,False,True,True,True,False],validated)
		print("Test 0a_1_1_2 : validate_key: success")

	def test_0a_1_1_3_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True))
		self.assertEqual([False,True,True,True,True,False],validated)
		print("Test 0a_1_1_3 : validate_key: success")

	def test_0a_1_1_4_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True))
		self.assertEqual([False,True,True,True,True,False],validated)
		print("Test 0a_1_1_4 : validate_key: success")

	def test_0a_1_1_5_validate_key(self):
		the_dict = {"iD":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived(), "unsupported":{}}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True, 
				unsupported=True))
		#print(validated)
		self.assertEqual([False,True,True,True,True,False,False],validated)
		print("Test 0a_1_1_5 : validate_key: success")

	def test_0a_1_1_6_validate_key(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		#print(type(type(product)))
		the_dict = {"ID":41,"password":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived(), "unsupported1":{}, "unsupported2":product}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True, 
				unsupported=True))
		#print(validated)
		self.assertEqual([False,True,True,True,True,False,False,True],validated)
		print("Test 0a_1_1_6 : validate_key: success")

	def test_0a_1_1_7_validate_key(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		the_dict = {"Id":41,"paSSword":"abc","username":"tryu",
		"bool1":True,"bool2":False,
		"nr":NotReceived(), "unsupported1":{}, "unsupported2":product}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key, unsupported=False))
		self.assertEqual([False,False,True,True,True,False,False,False],validated)
		print("Test 0a_1_1_7 : validate_key: success")

	def test_0a_1_1_8_validate_key(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		class tst(object):
			def __init__(self):
				self.Id = 41
				self.paSSword = "abc"
				self.username = "tryu"
				self.bool1 = True
				self.bool2 = False
				self.nr = NotReceived()
				self.unsupported1 = {}
				self.unsupported2 = product
		validation_obj = tst()
		validated = []
		for key in ["Id","paSSword","username","bool1","bool2","nr","unsupported1",
				"unsupported2"]:
			validated.append(validate_key(validation_obj,key, unsupported=False))
		self.assertEqual([False,False,True,True,True,False,False,False],validated)
		print("Test 0a_1_1_8 : validate_key: with object")


	def test_0a_1_2_1_get_dict(self):
		product = Product(name="Cheese",price=50.4,
			quantity=7.89, code=789456611)
		class tst(object):
			def __init__(self):
				self.Id = 41
				self.paSSword = "abc"
				self.username = "tryu"
				self.bool1 = True
				self.bool2 = False
				self.nr = NotReceived()
				self.unsupported1 = {}
				self.unsupported2 = product
		validation_obj = tst()
		the_dict = get_dict(validation_obj)
		self.assertEqual(the_dict,{"username":"tryu","bool1":True,"bool2":False})
		the_dict = get_dict(validation_obj, id=True,dangerous=True)
		self.assertEqual(the_dict,{"username":"tryu","bool1":True,"bool2":False,
			"paSSword":"abc","Id":41})
		print("Test 0a_1_2_1 : get_dict: with object")

	def test_0a_1_2_2_get_dict(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		the_dict = get_dict(product, id=True,dangerous=True)
		product.insert()
		the_dict = get_dict(product, id=True,dangerous=True)
		self.assertEqual(the_dict,{"name":"Cheese",
			"price":50.4,"id":1,"quantity":7.89,"code":789456611})
		product.delete()
		print("Test 0a_1_2_2 : get_dict: with object")

	def test_0a_1_2_3_get_dict(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		the_dict = {"Id":41,"paSSword":"abc","username":"tryu","bool1":True,
		"bool2":False,
		"nr":NotReceived(),"unsupported1":{},"unsupported2":product}
		validated = get_dict(the_dict, id=True,dangerous=True)
		self.assertEqual(validated,{"username":"tryu","bool1":True,"bool2":False,
			"paSSword":"abc","Id":41})

		validated = get_dict(the_dict)
		self.assertEqual(validated,{"username":"tryu","bool1":True,"bool2":False})
		print("Test 0a_1_2_3 : get_dict: with dict")











	def test_0a_1_2_1_MyModel(self):
		product = Product(name="Cheese",price=50.4,
		quantity=7.89, code=789456611)
		self.assertEqual(product.name,"Cheese")
		self.assertEqual(product.price,50.4)
		self.assertEqual(product.quantity,7.89)
		self.assertEqual(product.code,789456611)
		print("Test 0a_1_2_1 : MyModel: success")

	def test_0a_1_2_2_MyModel(self):
		try:
			product = Product(name="Cheese",price=50.4,
				quantity=7.89, code=789456611, bla="123")
		except Exception as e:
			self.assertEqual(str(e),"'bla' is an invalid "+
				"keyword argument for Product")
		print("Test 0a_1_2_2 : MyModel: success")

	def test_0a_1_2_3_MyModel(self):
		product = Product(name="Cheese",price=50.4,
			quantity=7.89, code=789456611)
		self.assertEqual(product.simple(),{"id":None,"name":"Cheese",
			"price":50.4, "quantity":7.89, "code":789456611})
		product.insert()
		self.assertEqual(product.simple(),{"name":"Cheese",
			"price":50.4, "quantity":7.89, "code":789456611, "id":1})
		#prod = Product(name="789",price=123,seller_id=1)
		#self.assertEqual(prod.simple(),{"name":"789","price":123,
		#	"seller_id":1,"id":None,"in_stock":None,"seller":None})
		#prod.insert()
		#self.assertEqual(prod.simple(),{"name":"789","price":123,
		#	"seller_id":1,"id":1,"in_stock":True})
		#prod.delete()
		product.delete()
		print("Test 0a_1_2_3 : MyModel: success")

	def test_0a_1_2_4_MyModel(self):
		#Trying to add the product with id, and seeing how the d will be neglected
		product = Product(name="Cheese",price=50.4,
			quantity=7.89, id=10000000,code=789456611)
		self.assertEqual(product.simple(),{"id":None,"name":"Cheese",
			"price":50.4, "quantity":7.89, "code":789456611})
		print("Test 0a_1_2_4 : MyModel: success")



	def test_0a_1_3_1_MyModel(self):
		db_drop_and_create_all()
		# Creating the product
		product_to_del = Product(name="Cheese",price=50.4,
			quantity=7.89, id=10000000,code=789456611)
		product_to_del.insert()
		#self.assertEqual(len(session.query(Product).all()),1)
		self.assertEqual(len(Product.query().all()),1)

		"""prod_to_del1 = Product(name = "abc",price=456,seller_id=user_to_del.id)
		prod_to_del2 = Product(name = "abcdef",price=4567,seller_id=user_to_del.id)
		db.session.add_all([prod_to_del1,prod_to_del2])
		db.session.commit()
		self.assertEqual(len(Product.query.all()),2)

		order_to_del1 = Order(
			user_id = user_to_del.id,product_id=prod_to_del1.id,amount=1)
		order_to_del2 = Order(
			user_id = user_to_del.id,product_id=prod_to_del2.id,amount=3)
		order_to_del3 = Order(
			user_id = user_to_del.id,product_id=prod_to_del2.id,amount=5)
		db.session.add_all([order_to_del1,order_to_del2,order_to_del3])
		db.session.commit()
		self.assertEqual(len(Order.query.all()),3)"""

		#img_to_delete1=Image(seller_id=1,name="abc",formatting = "png")
		#img_to_delete2=Image(seller_id=1,name="abce",formatting = "jpg")
		#db.session.add_all([img_to_delete1,img_to_delete2])
		#db.session.commit()
		#self.assertEqual(len(Image.query.all()),2)

		# Trying to delete

		#img_to_delete2.delete()
		#self.assertEqual(len(Image.query.all()),1)
		"""order_to_del3.delete()
		self.assertEqual(len(Order.query.all()),2)
		prod_to_del2.delete()
		self.assertEqual(len(Order.query.all()),1)
		self.assertEqual(len(Product.query.all()),1)"""
		product_to_del.delete()
		#self.assertEqual(len(Image.query.all()),0)
		"""self.assertEqual(len(Order.query.all()),0)
		self.assertEqual(len(Product.query.all()),0)
		self.assertEqual(len(Product.query.all()),0)"""

		print("Test 0a_1_3_1 : MyModel: relationships")


	def test_0a_1_4_1_MyModel(self):
		# Testing update
		# Creating the product
		product_to_del = Product(name="Cheese",price=50.4,
			quantity=7.89, id=10000000,code=789456611)
		product_to_del.insert()
		product_dict = get_dict(product_to_del,id=True,dangerous=True)
		self.assertEqual(product_dict,{"id":1,"name":"Cheese",
			"price":50.4, "quantity":7.89,"code":789456611})
		product_to_del.update(id=14,name="QUU",price=90,
			quantity=7000,code=0)
		product_dict = get_dict(product_to_del,id=True,dangerous=True)
		self.assertEqual(product_dict,{"id":1,"name":"QUU",
			"price":90, "quantity":7000,"code":0})
		product_to_del.delete()
		print("Test 0a_1_4_1 : MyModel: update")

	def test_0a_1_5_1_MyModel_deep(self):
		# Testing update
		# Creating the product
		product_to_del = Product(name="Cheese",price=50.4,
			quantity=7.89, id=10000000,code=789456611)
		product_to_del.insert()
		#prod = Product(name="789",price=123,seller_id=1)
		#prod.insert()
		#print(product_to_del.deep())
		self.assertEqual(product_to_del.deep(),
			{'categories': [], 'code': 789456611, 'id': 1, 
			'name': 'Cheese', 'price': 50.4, 'quantity': 7.89})
		"""self.assertEqual(prod.deep(),{'id': 1, 'in_stock': True,
			'name': '789', 'orders': [], 'price': 123.0, 'seller':
			{'id': 1, 'username': 'abc'}, 'seller_id': 1})"""
		print("Test 0a_1_5_1 : MyModel: deep")
















	def test_a_1_000_product_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 1 ) Product ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")

	def test_a_1_001_product_insert(self):
		db_drop_and_create_all()
		product1 = Product(name="Cheese",price=50.4,
			quantity=7.89, id=10000000,code=789456611)
		product1.insert()
		products = Product.query().all()

		self.assertEqual(len(products),1)
		print("Test a_1_1: product insert")


	def test_a_1_002_product_update(self):
		product1 = Product.query().get(1)
		#product1.name = "modified"
		product1.update(name="modified")
		product_1 = Product.query().get(1)

		self.assertEqual(product_1.name,"modified")
		print("Test a_1_2: product update")



	def test_a_1_003_product_delete(self):
		product1 = Product.query().get(1)
		product1.delete()
		products = Product.query().all()

		self.assertEqual(len(products),0)
		print("Test a_1_3: product delete")

	def test_a_1_004_populate(self):
		populate_tables()
		products = Product.query().all()

		self.assertEqual(len(products),5)
		print("Test a_1_4: Populate Tables")


	def test_a_1_005_product_values(self):
		product = Product.query().get(1)

		self.assertEqual(product.id,1)
		self.assertEqual(product.name,"Cheese")
		self.assertEqual(product.price,50.4)
		self.assertEqual(product.quantity,7.89)
		self.assertEqual(product.code,789456611)
		#print(product.categories)
		self.assertEqual(json.loads(str(product.categories)),
			[{"category_id": 1, "id": 1, "product_id": 1}, 
			{"category_id": 2, "id": 2, "product_id": 1}, 
			{"category_id": 3, "id": 3, "product_id": 1}, 
			{"category_id": 4, "id": 4, "product_id": 1}, 
			{"category_id": 5, "id": 5, "product_id": 1}])
		"""for prod in user.products:
			self.assertEqual(type(prod.id),int)
			self.assertEqual(type(prod.price),float)
			self.assertEqual(type(prod.in_stock),bool)
			self.assertEqual(type(prod.seller_id),int)
		for order in user.orders:
			self.assertEqual(type(order.id),int)
			self.assertEqual(type(order.user_id),int)
			self.assertEqual(type(order.product_id),int)
			self.assertEqual(type(order.amount),int)"""
		"""for image in user.images:
			self.assertEqual(type(image.id),int)
			self.assertEqual(type(image.seller_id),int)
			self.assertEqual(type(image.name),str)
			self.assertEqual(type(image.formatting),str)"""
		print("Test a_1_5: product values")


	def test_a_1_006_product_insert_wrong(self):
		products = Product.query().all()
		old_records_number = len(products)
		try:
			#This code will not be executed
			#There are missing required parameters
			product = Product()
			product.insert()
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"True != False")

		products = Product.query().all()
		new_records_number = len(products)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_1_6: product insert with missing"+
		 "required parameters")



	def test_a_1_007_product_delete_wrong(self):
		products = Product.query().all()
		old_records_number = len(products)
		try:
			#This code will not be executed
			#There is no product with the number 0
			product1 = Product.query().get(0)
			product1.delete()
			self.assertEqual(True,False)

		except Exception as e:
			self.assertEqual(str(e),"'NoneType' "+
				"object has no attribute 'delete'")
			#print(str(e))

		products = Product.query().all()
		new_records_number = len(products)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_1_7: product delete mistake, non-existent"+
		 "product id")



	def test_a_1_008_product_simple(self):
		product = Product.query().get(1).simple()
		#print(product)

		self.assertEqual(product,{'code': 789456611, 
			'id': 1, 'price': 50.4, 'name': 
			'Cheese', 'quantity': 7.89})
		print("Test a_1_8: product simple")

	def test_a_1_009_product_relationship_order(self):
		product = Product.query().get(1)
		"""orders=user.orders
		orders_ids=[order.id for order in orders]
		self.assertEqual(1 in orders_ids,True)
		self.assertEqual(2 in orders_ids,False)
		self.assertEqual(3 in orders_ids,False)
		self.assertEqual(4 in orders_ids,True)"""
		print("Test a_1_9:product relationship_order")

	def test_a_1_010_product_delete_relationships(self):
		#measuring lengths beofre actions
		#populate_tables()
		products_before = len(Product.query().all())
		categories_before = len(Category.query().all())
		pc_before = len(ProductCategory.query().all())

		# deleting the product
		prod_to_del = Product.query().get(1)
		
		prod_to_del.delete()
		self.assertEqual(len(Product.query().all()),products_before-1)
		self.assertEqual(len(Category.query().all()),categories_before)
		self.assertEqual(len(ProductCategory.query().all()),pc_before-5)

		print("Test a_1_10: product delete relationships")

	def test_a_1_011_product_deep(self):
		#measuring lengths beofre actions
		product = Product.query().get(4)
		#print(product.deep())
		self.assertEqual(product.deep(),
			{'categories': [], 'code': 8444441, 'id': 4, 
			'name': 'Mobile', 'price': 20.1, 'quantity': 9.0})
		print("Test a_1_11: product deep")

































	def test_a_2_000_category_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 2 ) Category ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")

	def test_a_2_001_category_insert(self):
		db_drop_and_create_all()
		category1 = Category(name="Cheese")
		category1.insert()
		categories = Category.query().all()

		self.assertEqual(len(categories),1)
		print("Test a_2_1: category insert")


	def test_a_2_002_category_update(self):
		category1 = Category.query().get(1)
		#category1.name = "modified"
		category1.update(name="modified")
		category_1 = Category.query().get(1)

		self.assertEqual(category_1.name,"modified")
		print("Test a_2_2: category update")



	def test_a_2_003_category_delete(self):
		category1 = Category.query().get(1)
		category1.delete()
		categories = Category.query().all()

		self.assertEqual(len(categories),0)
		print("Test a_2_3: category delete")

	def test_a_2_004_populate(self):
		populate_tables()
		categories = Category.query().all()

		self.assertEqual(len(categories),13)
		print("Test a_2_4: Populate Tables")


	def test_a_2_005_category_values(self):
		category = Category.query().get(1)
		self.assertEqual(category.id,1)
		self.assertEqual(category.name,"Electronics")
		self.assertEqual(category.parent_id,None)
		self.assertEqual(category.parent,None)
		self.assertEqual(str(category.children),
			'[{"id": 2, "name": "Camera", "parent_id": 1}]')
		#print(category.products)
		self.assertEqual(json.loads(str(category.products)),
			[{"category_id": 1, "id": 1, "product_id": 1}, 
			{"category_id": 1, "id": 6, "product_id": 2}, 
			{"category_id": 1, "id": 11, "product_id": 3}])
		
		category = Category.query().get(4)
		self.assertEqual(category.id,4)
		self.assertEqual(category.name,"Manual Cameras")
		self.assertEqual(category.parent_id,2)
		self.assertEqual(category.parent,Category.query().get(2))
		#print(category.children)
		self.assertEqual(str(category.children),
			'[]')
		#print(category.products)
		self.assertEqual(json.loads(str(category.products)),
			[{"category_id": 4, "id": 4, "product_id": 1}, 
			{"category_id": 4, "id": 9, "product_id": 2}, 
			{"category_id": 4, "id": 14, "product_id": 3}])
		print("Test a_2_5: category values")


	def test_a_2_006_category_insert_wrong(self):
		categories = Category.query().all()
		old_records_number = len(categories)
		try:
			#This code will not be executed
			#There are missing required parameters
			category = Category()
			category.insert()
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"True != False")

		categories = Category.query().all()
		new_records_number = len(categories)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_2_6: category insert with missing"+
		 "required parameters")



	def test_a_2_007_category_delete_wrong(self):
		categories = Category.query().all()
		old_records_number = len(categories)
		try:
			#This code will not be executed
			#There is no category with the number 0
			category1 = Category.query().get(0)
			category1.delete()
			self.assertEqual(True,False)

		except Exception as e:
			self.assertEqual(str(e),"'NoneType' "+
				"object has no attribute 'delete'")
			#print(str(e))

		categories = Category.query().all()
		new_records_number = len(categories)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_2_7: category delete mistake, non-existent"+
		 "category id")



	def test_a_2_008_category_simple(self):
		category = Category.query().get(1).simple()
		#print(category)
		self.assertEqual(category,{'id': 1, 'name': 'Electronics', 
			'parent_id': None})
		category = Category.query().get(4).simple()
		#print(category)
		self.assertEqual(category,{'id': 4, 'name': 
			'Manual Cameras', 'parent_id': 2})
		
		print("Test a_2_8: category simple")

	def test_a_2_009_category_relationship_order(self):
		category = Category.query().get(1)
		category.parent=None
		category = Category.query().get(4)
		print("Test a_2_9:category relationship")

	def test_a_2_010_category_delete_relationships(self):
		products_before = len(Product.query().all())
		categories_before = len(Category.query().all())
		pc_before = len(ProductCategory.query().all())

		# deleting the product
		category_to_del = Category.query().get(1)
		
		category_to_del.delete()
		self.assertEqual(len(Product.query().all()),products_before)
		self.assertEqual(len(Category.query().all()),categories_before-1)
		self.assertEqual(len(ProductCategory.query().all()),pc_before-3)



		print("Test a_2_10: category delete relationships")

	def test_a_2_011_category_deep(self):
		#measuring lengths beofre actions
		category = Category.query().get(5)
		#print(category.deep())
		self.assertEqual(category.deep(),
			{'children': 
			[{'id': 6, 'name': 'Sport Cars', 'parent_id': 5}, 
			{'id': 7, 'name': 'Electric Cars', 'parent_id': 5}, 
			{'id': 8, 'name': 'Tractors', 'parent_id': 5}], 
			'id': 5, 'name': 'Cars', 'parent': None, 'parent_id': None, 
			'products': 
			[{'category_id': 5, 'id': 5, 'product_id': 1}, 
			{'category_id': 5, 'id': 10, 'product_id': 2}, 
			{'category_id': 5, 'id': 15, 'product_id': 3}]})
		
		category = Category.query().get(4)
		#print(category.deep())
		self.assertEqual(category.deep(),
			{'children': [], 'id': 4, 'name': 'Manual Cameras', 
			'parent': {'id': 2, 'name': 'Camera', 'parent_id': None}, 
			'parent_id': 2, 'products': 
			[{'category_id': 4, 'id': 4, 'product_id': 1}, 
			{'category_id': 4, 'id': 9, 'product_id': 2}, 
			{'category_id': 4, 'id': 14, 'product_id': 3}]})
		print("Test a_2_11: category deep")
























	def test_a_3_000_pc_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 3 ) ProductCategory ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")

	def test_a_3_001_pc_insert(self):
		db_drop_and_create_all()
		populate_tables()
		pc1 = ProductCategory(product_id=3,category_id=7)
		pc1.insert()
		pcs = ProductCategory.query().all()

		self.assertEqual(len(pcs),16)
		print("Test a_3_1: pc insert")


	def test_a_3_002_pc_update(self):
		pc1 = ProductCategory.query().get(1)
		#pc1.name = "modified"
		pc1.update(name="modified")
		pc_1 = ProductCategory.query().get(1)

		self.assertEqual(pc_1.name,"modified")
		print("Test a_3_2: pc update")



	def test_a_3_003_pc_delete(self):
		pc1 = ProductCategory.query().get(1)
		pc1.delete()
		pcs = ProductCategory.query().all()

		self.assertEqual(len(pcs),15)
		print("Test a_3_3: pc delete")

	def test_a_3_004_populate(self):
		populate_tables()
		pcs = ProductCategory.query().all()

		self.assertEqual(len(pcs),15)
		print("Test a_3_4: Populate Tables")


	def test_a_3_005_pc_values(self):
		pc = ProductCategory.query().get(1)
		self.assertEqual(pc.id,1)
		self.assertEqual(pc.product_id,1)
		self.assertEqual(pc.category_id,1)
		#self.assertEqual(pc.parent,None)
		#self.assertEqual(str(pc.children),
		#	'[{"id": 2, "name": "Camera", "parent_id": 1}]')
		#print(pc.product.simple())
		self.assertEqual(pc.product.simple(),
			{'code': 789456611, 'id': 1, 'name': 'Cheese', 'price': 50.4, 
			'quantity': 7.89})
		#print(pc.category.simple())
		self.assertEqual(pc.category.simple(),
			{'id': 1, 'name': 'Electronics', 'parent_id': None})

		print("Test a_3_5: pc values")


	def test_a_3_006_pc_insert_wrong(self):
		pcs = ProductCategory.query().all()
		old_records_number = len(pcs)
		try:
			#This code will not be executed
			#There are missing required parameters
			pc = ProductCategory()
			pc.insert()
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"True != False")

		pcs = ProductCategory.query().all()
		new_records_number = len(pcs)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_3_6: pc insert with missing"+
		 "required parameters")



	def test_a_3_007_pc_delete_wrong(self):
		pcs = ProductCategory.query().all()
		old_records_number = len(pcs)
		try:
			#This code will not be executed
			#There is no pc with the number 0
			pc1 = ProductCategory.query().get(0)
			pc1.delete()
			self.assertEqual(True,False)

		except Exception as e:
			self.assertEqual(str(e),"'NoneType' "+
				"object has no attribute 'delete'")
			#print(str(e))

		pcs = ProductCategory.query().all()
		new_records_number = len(pcs)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_3_7: pc delete mistake, non-existent"+
		 "pc id")



	def test_a_3_008_pc_simple(self):
		pc = ProductCategory.query().get(1).simple()
		#print(pc)
		self.assertEqual(pc,{'category_id': 1, 
			'id': 1, 'product_id': 1})
		
		print("Test a_3_8: pc simple")

	def test_a_3_009_pc_relationship_order(self):
		pc = ProductCategory.query().get(1)
		#pc.parent=None
		#pc = ProductCategory.query().get(4)
		print("Test a_3_9:pc relationship")

	def test_a_3_010_pc_delete_relationships(self):
		products_before = len(Product.query().all())
		categories_before = len(Category.query().all())
		pc_before = len(ProductCategory.query().all())

		# deleting the product
		pc_to_del = ProductCategory.query().get(1)
		
		pc_to_del.delete()
		self.assertEqual(len(Product.query().all()),products_before)
		self.assertEqual(len(Category.query().all()),categories_before)
		self.assertEqual(len(ProductCategory.query().all()),pc_before-1)

		print("Test a_3_10: pc delete relationships")

	def test_a_3_011_pc_deep(self):
		#measuring lengths beofre actions
		pc = ProductCategory.query().get(5)
		#print(pc.deep())
		self.assertEqual(pc.deep(),
			{'category': {'id': 5, 'name': 'Cars', 'parent_id': None}, 
			'category_id': 5, 'id': 5, 'product': 
			{'code': 789456611, 'id': 1, 'name': 'Cheese', 'price': 50.4, 
			'quantity': 7.89}, 'product_id': 1})
		
		print("Test a_3_11: pc deep")






































# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
