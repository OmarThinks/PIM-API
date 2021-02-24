import unittest
from pydantic_models import (ProductPost, ProductUpdate, CategoryPost,
	CategoryUpdate,ProductCategoryPost,
	ProductExists, CategoryExists, ProductCategoryExists,
validate_model_id,
validate_model_id_pydantic, TestHere)
import json
from models import (NotReceived, validate_key,
MyModel, Product,Category,ProductCategory, populate_tables)

from pydantic import ValidationError

import base64

unittest.TestLoader.sortTestMethodsUsing = None


class pydanticTestCase(unittest.TestCase):
	"""This class represents the pydantic test models"""

	def setUp(self):
		#db_drop_and_create_all()
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
	def test_000001_test(self):

		# Populating
		populate_tables()
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_a_1_1_validate_model_id(self):
		# Model exists
		self.assertEqual(validate_model_id(Product,1),True)
		# Model does not exist
		self.assertEqual(validate_model_id(Product,10000000000),False)
		try:
			# model is not model
			validate_model_id(123,10000000000)
			self.assertEqual(True,False)
		except Exception as e:
			#print(str(e))
			self.assertEqual(str(e),"validate_model_id:expected the type "+
				"of SQLAlchemy, but found the type of <class 'int'> instead")
		print("Test a_1_1: validate_model_id success")


	def test_a_1_2_validate_model_id_pydantic(self):
		# Model exists: nOo errors raised
		validate_model_id_pydantic(Product,1)
		try:
			# Model does not exist
			self.assertEqual(validate_model_id_pydantic(Product,10000000000),False)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"there is no Product with this id: 10000000000")
		try:
			# model is not model
			validate_model_id(123,10000000000)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"validate_model_id:expected the type "+
				"of SQLAlchemy, but found the type of <class 'int'> instead")
		print("Test a_1_2: validate_model_id success")










	def test_b_001_00_Product(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 1 ) Product ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")




	def test_b_001_01_1_ProductPost(self):
		toValidate = {"name":" abcdef ","price":123.1,
		"quantity":400.12,"code":798}
		product = ProductPost(**toValidate)
		self.assertEqual(product.dict(),{"name":"abcdef","price":123.1,
		"quantity":400.12,"code":798})
		print("Test b_1_1_1:ProductPost Successful")

	def test_b_001_01_2_ProductPost(self):
		toValidate = {"code":789456611}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 
				'msg': 'field required', 'type': 'value_error.missing'}, 
				{'loc': ['price'], 'msg': 'field required', 'type': 
				'value_error.missing'}, {'loc': ['quantity'], 'msg': 
				'field required', 'type': 'value_error.missing'}, 
				{'loc': ['code'], 'msg': 
				'this code is already related to another product', 'type': 
				'value_error'}])
		print("Test b_1_1_2:ProductPost:Fail:all missing required, "+
			"code not unique")

	def test_b_001_01_3_ProductPost(self):
		toValidate = {"name":{},"price":{},
		"quantity":{},"code":{}}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 
				'msg': 'str type expected', 'type': 'type_error.str'}, 
				{'loc': ['price'], 'msg': 'value is not a valid float', 
				'type': 'type_error.float'}, {'loc': ['quantity'], 'msg': 
				'value is not a valid float', 'type': 'type_error.float'}, 
				{'loc': ['code'], 'msg': 'value is not a valid integer', 
				'type': 'type_error.integer'}])
		print("Test b_1_1_3:ProductPost:Fail:not string")


	def test_b_001_01_4_ProductPost(self):
		# name : short
		# price : very cheap
		# quantity : very small
		# code: very small
		toValidate = {"name":"   a   ","price":.00000000000001,
		"quantity":.000000001, "code":1}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()), [{'loc': ['name'], 
				'msg': 'ensure this value has at least 3 characters', 
				'type': 'value_error.any_str.min_length', 'ctx': 
				{'limit_value': 3}}, {'loc': ['price'], 'msg': 
				'ensure this value is greater than or equal to 0.1', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0.1}}, {'loc': ['quantity'], 
				'msg': 'ensure this value is greater than or equal to 0.001', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0.001}}, {'loc': ['code'], 'msg': 
				'ensure this value is greater than or equal to 2', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 2}}])
		print("Test b_1_1_4:ProductPost:Fail:short data")

	def test_b_001_01_5_ProductPost(self):
		# name : long
		# price : very expensive
		# quantity : very big
		# code: very big
		toValidate = {"name":"a"*700000,"price":10000000000000000000,
		"quantity":1000000000, "code":1000000000000000000000000000000000}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 'msg': 
				'ensure this value has at most 300 characters', 'type': 
				'value_error.any_str.max_length', 'ctx': {'limit_value': 300}}, 
				{'loc': ['price'], 'msg': 
				'ensure this value is less than or equal to 1000000', 
				'type': 'value_error.number.not_le', 'ctx': 
				{'limit_value': 1000000}}, {'loc': ['quantity'], 
				'msg': 'ensure this value is less than or equal to 100000000', 
				'type': 'value_error.number.not_le', 'ctx': 
				{'limit_value': 100000000}}, {'loc': ['code'], 'msg': 
				'ensure this value is less than or equal to 10000000000000'+
				'0000000000000', 'type': 'value_error.number.not_le', 'ctx': 
				{'limit_value': 100000000000000000000000000}}])
		print("Test b_1_1_5:ProductPost:Fail:big data")

	def test_b_001_01_6_ProductPost(self):
		# adding unknown attribute
		# This attribute will not be returned
		# Testing White spaces
		# Code default value
		toValidate = {"name":"   abacdegfgh   ","price":100,
		"quantity":10, "bla bla":"jgashgj"}
		product = ProductPost(**toValidate)
		#print(product.dict())
		self.assertEqual(product.dict(),{'name': 'abacdegfgh', 
			'price': 100.0, 'quantity': 10.0, 'code': None})
		print("Test b_1_1_6:ProductPost:Added unknown value:Cleaned")









	def test_b_001_02_01_ProductUpdate(self):
		toValidate = {"id":1,"name":" abcdef ","price":123.1,
		"quantity":400.12,"code":798}
		product = ProductUpdate(**toValidate)
		self.assertEqual(product.dict(),{"id":1,"name":"abcdef","price":123.1,
		"quantity":400.12,"code":798})
		print("Test b_1_2_1:ProductUpdate Successful")

	def test_b_001_02_02_ProductUpdate(self):
		toValidate = {"code":789456611}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 'msg': 
				'field required', 'type': 'value_error.missing'}, 
				{'loc': ['name'], 'msg': 'field required', 'type': 
				'value_error.missing'}, {'loc': ['price'], 'msg': 
				'field required', 'type': 'value_error.missing'}, 
				{'loc': ['quantity'], 'msg': 'field required', 'type': 
				'value_error.missing'}])
		print("Test b_1_2_2:ProductUpdate:Fail:all missing required")

	def test_b_001_02_03_ProductUpdate(self):
		toValidate = {"id":{},"name":{},"price":{},
		"quantity":{},"code":{}}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'value is not a valid integer', 'type': 
				'type_error.integer'}, {'loc': ['name'], 'msg': 
				'str type expected', 'type': 'type_error.str'}, 
				{'loc': ['price'], 'msg': 'value is not a valid float', 
				'type': 'type_error.float'}, {'loc': ['quantity'], 
				'msg': 'value is not a valid float', 'type': 
				'type_error.float'}, {'loc': ['code'], 'msg': 
				'value is not a valid integer', 'type': 
				'type_error.integer'}])
		print("Test b_1_2_3:ProductUpdate:Fail:not string")


	def test_b_001_02_04_ProductUpdate(self):
		# id: very small
		# name : short
		# price : very cheap
		# quantity : very small
		# code: very small
		toValidate = {"id":0,"name":"   a   ","price":.00000000000001,
		"quantity":.000000001, "code":1}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()), [{'loc': ['id'], 
				'msg': 'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 'ctx': 
				{'limit_value': 0}}, {'loc': ['name'], 'msg': 
				'ensure this value has at least 3 characters', 
				'type': 'value_error.any_str.min_length', 
				'ctx': {'limit_value': 3}}, {'loc': ['price'], 
				'msg': 'ensure this value is greater than or equal to 0.1', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0.1}}, {'loc': ['quantity'], 
				'msg': 'ensure this value is greater than or equal to 0.001', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0.001}}, {'loc': ['code'], 'msg': 
				'ensure this value is greater than or equal to 2', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 2}}])
		print("Test b_1_2_4:ProductUpdate:Fail:short data")

	def test_b_001_02_05_ProductUpdate(self):
		# id: nonexistent
		# name : long
		# price : very expensive
		# quantity : very big
		# code: very big
		toValidate = {"id":1000000,"name":"a"*700000,"price":10000000000000000000,
		"quantity":1000000000, "code":1000000000000000000000000000000000}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'there is no Product with this id: 1000000', 
				'type': 'value_error'}, {'loc': ['name'], 'msg': 
				'ensure this value has at most 300 characters', 
				'type': 'value_error.any_str.max_length', 'ctx': 
				{'limit_value': 300}}, {'loc': ['price'], 'msg': 
				'ensure this value is less than or equal to 1000000', 
				'type': 'value_error.number.not_le', 'ctx': 
				{'limit_value': 1000000}}, {'loc': ['quantity'], 
				'msg': 'ensure this value is less than or equal to 100000000', 
				'type': 'value_error.number.not_le', 'ctx': 
				{'limit_value': 100000000}}, {'loc': ['code'], 
				'msg': 'ensure this value is less than or equal to'+
				' 100000000000000000000000000', 'type': 
				'value_error.number.not_le', 'ctx': {'limit_value': 
				100000000000000000000000000}}])
		print("Test b_1_2_5:ProductUpdate:Fail:big data")

	def test_b_001_02_06_ProductUpdate(self):
		# id did not succeed, code will just be passed
		toValidate = {"id":1000000000000,"name":"abacdegfgh","price":100,
		"quantity":10, "code":"123456"}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 'msg': 
				'there is no Product with this id: 1000000000000', 
				'type': 'value_error'}])
		print("Test b_1_2_6:ProductUpdate: id did not succeed, "+
			"code will just be passed")

	def test_b_001_02_07_ProductUpdate(self):
		# id did not succeed, code will just be passed
		toValidate = {"id":1,"name":"abacdegfgh","price":100,
		"quantity":10, "code":"8754653216576"}
		product = ProductUpdate(**toValidate)
		self.assertEqual(product.dict(),{"id":1,"name":"abacdegfgh","price":100,
		"quantity":10, "code":8754653216576})
		print("Test b_1_2_7:ProductUpdate:new code")

	def test_b_001_02_08_ProductUpdate(self):
		# id did not succeed, code will just be passed
		toValidate = {"id":1,"name":"abacdegfgh","price":100,
		"quantity":10, "code":"789456611"}
		product = ProductUpdate(**toValidate)
		self.assertEqual(product.dict(),{"id":1,"name":"abacdegfgh","price":100,
		"quantity":10, "code":789456611})
		print("Test b_1_2_8:ProductUpdate:same code, same product")

	def test_b_001_02_09_ProductUpdate(self):
		# id did not succeed, code will just be passed
		toValidate = {"id":1,"name":"abacdegfgh","price":100,
		"quantity":10, "code":"8444441"}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['code'], 
				'msg': 'this code is already related to another product', 
				'type': 'value_error'}])
		print("Test b_1_2_9:ProductUpdate: id did not succeed, "+
			"code will just be passed")



	def test_b_001_03_01_ProductExists(self):
		# id small
		toValidate = {"id":0}
		try:
			product = ProductExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 'ctx': 
				{'limit_value': 0}}])
		print("Test b_1_3_1:ProductExists: id small")

	def test_b_001_03_02_ProductExists(self):
		# id does not exist
		toValidate = {"id":100000}
		try:
			product = ProductExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'there is no Product with this id: 100000', 
				'type': 'value_error'}])
		print("Test b_1_3_2:ProductExists: id does not exist")

	def test_b_001_03_03_ProductExists(self):
		# success
		toValidate = {"id":1}
		product = ProductExists(**toValidate)
		self.assertEqual(product.dict(),{"id":1})
		print("Test b_1_3_3:ProductExists:id exists")



























	def test_b_002_00_Category(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 2 ) Category ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")








	def test_b_002_01_1_CategoryPost(self):
		toValidate = {"name":" abcdef ","parent_id":1}
		category = CategoryPost(**toValidate)
		self.assertEqual(category.dict(),{"name":"abcdef","parent_id":1})
		
		# In case of 0 => None
		toValidate = {"name":" abcdef ","parent_id":0}
		category = CategoryPost(**toValidate)
		self.assertEqual(category.dict(),{"name":"abcdef","parent_id":None})
		
		print("Test b_2_1_1:CategoryPost Successful")

	def test_b_002_01_2_CategoryPost(self):
		toValidate = {}
		try:
			category = CategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 'msg': 
				'field required', 'type': 'value_error.missing'}, 
				{'loc': ['parent_id'], 'msg': 'field required', 'type': 
				'value_error.missing'}])
		print("Test b_2_1_2:CategoryPost:Fail:all missing required")

	def test_b_002_01_3_CategoryPost(self):
		toValidate = {"name":{},"parent_id":{}}
		try:
			category = CategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 'msg': 
				'str type expected', 'type': 'type_error.str'}, 
				{'loc': ['parent_id'], 'msg': 
				'value is not a valid integer', 'type': 'type_error.integer'}])
		print("Test b_2_1_3:CategoryPost:Fail:not string")


	def test_b_002_01_4_CategoryPost(self):
		# name : short
		# parent_id : small
		toValidate = {"name":"   a   ","parent_id":-1}
		try:
			category = CategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()), [{'loc': ['name'], 
				'msg': 'ensure this value has at least 3 characters', 
				'type': 'value_error.any_str.min_length', 'ctx': 
				{'limit_value': 3}}, {'loc': ['parent_id'], 'msg': 
				'ensure this value is greater than or equal to 0', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0}}])
		print("Test b_2_1_4:CategoryPost:Fail:short data")

	def test_b_002_01_5_CategoryPost(self):
		# name : long
		# parent_id : not unique
		toValidate = {"name":"a"*700000,"parent_id":1}
		try:
			category = CategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 
				'msg': 'ensure this value has at most 300 characters', 
				'type': 'value_error.any_str.max_length', 'ctx': 
				{'limit_value': 300}}])
		print("Test b_2_1_5:CategoryPost:Fail:big name")

	def test_b_002_01_6_CategoryPost(self):
		# adding unknown attribute
		# This attribute will not be returned
		# Testing White spaces
		toValidate = {"name":"   abacdegfgh   ","parent_id":"1",
		"bla bla":"jgashgj"}
		category = CategoryPost(**toValidate)
		#print(category.dict())
		self.assertEqual(category.dict(),{'name': 'abacdegfgh', 
			'parent_id': 1})
		print("Test b_2_1_6:CategoryPost:Added unknown value:Cleaned")

	def test_b_002_01_7_CategoryPost(self):
		# name : not unique
		# parent_id : non existent
		toValidate = {"name":"   Electronics   ","parent_id":1000000}
		try:
			category = CategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 
				'msg': 'this name is already related to another category', 
				'type': 'value_error'}, {'loc': ['parent_id'], 'msg': 
				'there is no Category with this id: 1000000', 
				'type': 'value_error'}])
		print("Test b_2_1_7:CategoryPost:Name not unique,"+
			" parent_id non existent")









	def test_b_002_02_01_CategoryUpdate(self):
		toValidate = {"id":2, "name":" abcdef ","parent_id":1}
		category = CategoryUpdate(**toValidate)
		self.assertEqual(category.dict(),{"id":2, 
			"name":"abcdef","parent_id":1})
		
		# In case of 0 => None
		toValidate = {"id":1, "name":" abcdef ","parent_id":0}
		category = CategoryUpdate(**toValidate)
		self.assertEqual(category.dict(),{"id":1,
			"name":"abcdef","parent_id":None})
		
		print("Test b_2_2_1:CategoryUpdate Successful")

	def test_b_002_02_02_CategoryUpdate(self):
		toValidate = {}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'field required', 'type': 'value_error.missing'}, 
				{'loc': ['name'], 'msg': 'field required', 'type': 
				'value_error.missing'}, {'loc': ['parent_id'], 'msg': 
				'field required', 'type': 'value_error.missing'}])
		print("Test b_2_2_2:CategoryUpdate:Fail:all missing required")

	def test_b_002_02_03_CategoryUpdate(self):
		toValidate = {"id":{},"name":{},"parent_id":{}}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 'msg': 
				'value is not a valid integer', 'type': 'type_error.integer'}, 
				{'loc': ['name'], 'msg': 'str type expected', 'type': 
				'type_error.str'}, {'loc': ['parent_id'], 'msg': 
				'value is not a valid integer', 'type': 
				'type_error.integer'}])
		print("Test b_2_2_3:CategoryUpdate:Fail:not string")


	def test_b_002_02_04_CategoryUpdate(self):
		# id: very small
		# name : short
		# parent_id : very small
		toValidate = {"id":0,"name":"   a   ","parent_id":-1}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()), [{'loc': ['id'], 
				'msg': 'ensure this value is greater than 0', 'type': 
				'value_error.number.not_gt', 'ctx': {'limit_value': 0}}, 
				{'loc': ['name'], 'msg': 
				'ensure this value has at least 3 characters', 'type': 
				'value_error.any_str.min_length', 'ctx': {'limit_value': 3}}, 
				{'loc': ['parent_id'], 'msg': 
				'ensure this value is greater than or equal to 0', 
				'type': 'value_error.number.not_ge', 'ctx': 
				{'limit_value': 0}}])
		print("Test b_2_2_4:CategoryUpdate:Fail:short data")

	def test_b_002_02_05_CategoryUpdate(self):
		# id: nonexistent
		# name : long
		# parent_id: non existent
		toValidate = {"id":1000000,"name":"a"*700000,"parent_id":100000}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 'msg': 
				'there is no Category with this id: 1000000', 'type': 
				'value_error'}, {'loc': ['name'], 'msg': 
				'ensure this value has at most 300 characters', 'type': 
				'value_error.any_str.max_length', 'ctx': {'limit_value': 
				300}}, {'loc': ['parent_id'], 'msg': 
				'there is no Category with this id: 100000', 'type': 
				'value_error'}])
		print("Test b_2_2_5:CategoryUpdate:Fail:big data")

	def test_b_002_02_06_CategoryUpdate(self):
		# id did not succeed, code will just be passed
		toValidate = {"id":1000000000000,"name":"abacdegfgh","price":100,
		"quantity":10, "code":"123456"}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 'msg': 
				'there is no Category with this id: 1000000000000', 
				'type': 'value_error'}, {'loc': ['parent_id'], 
				'msg': 'field required', 'type': 'value_error.missing'}])
		print("Test b_2_2_6:CategoryUpdate: id did not succeed, "+
			"code will just be passed")

	def test_b_002_02_07_CategoryUpdate(self):
		# id did not succeed, parent_id and name will just pass
		toValidate = {"id":100000000,"name":"Electronics","parent_id":100}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'there is no Category with this id: 100000000', 
				'type': 'value_error'}, {'loc': ['parent_id'], 
				'msg': 'there is no Category with this id: 100', 
				'type': 'value_error'}])
		print("Test b_2_2_7:CategoryUpdate:new code")

	def test_b_002_02_08_CategoryUpdate(self):
		# name of the same category repeated, parent_id = same category
		toValidate = {"id":1,"name":"Cars","parent_id":1}
		try:
			category = CategoryUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 
				'msg': 
				'this name is already related to another category', 
				'type': 'value_error'}, {'loc': ['parent_id'], 
				'msg': 'a category can not be a parent to itself', 
				'type': 'value_error'}])
		print("Test b_2_2_8:CategoryUpdate:same code, same category")


	def test_b_002_03_01_CategoryExists(self):
		# id small
		toValidate = {"id":0}
		try:
			product = CategoryExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 'ctx': 
				{'limit_value': 0}}])
		print("Test b_2_3_1:CategoryExists: id small")

	def test_b_002_03_02_CategoryExists(self):
		# id does not exist
		toValidate = {"id":100000}
		try:
			product = CategoryExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'there is no Category with this id: 100000', 
				'type': 'value_error'}])
		print("Test b_2_3_2:CategoryExists: id does not exist")

	def test_b_002_03_03_CategoryExists(self):
		# success
		toValidate = {"id":1}
		product = CategoryExists(**toValidate)
		self.assertEqual(product.dict(),{"id":1})
		print("Test b_2_3_3:CategoryExists:id exists")





































	def test_b_003_00_ProductCategory(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 3 ) ProductCategory ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")








	def test_b_003_01_1_ProductCategoryPost(self):
		toValidate = {"product_id":4,"category_id":1}
		pc = ProductCategoryPost(**toValidate)
		self.assertEqual(pc.dict(),{"product_id":4,"category_id":1})
		print("Test b_3_1_1:ProductCategoryPost Successful")

	def test_b_003_01_2_ProductCategoryPost(self):
		toValidate = {}
		try:
			pc = ProductCategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'], 
				'msg': 'field required', 'type': 'value_error.missing'}, 
				{'loc': ['category_id'], 'msg': 'field required', 
				'type': 'value_error.missing'}])
		print("Test b_3_1_2:ProductCategoryPost:Fail:all missing required")

	def test_b_003_01_3_ProductCategoryPost(self):
		toValidate = {"product_id":{},"category_id":{}}
		try:
			pc = ProductCategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'], 
				'msg': 'value is not a valid integer', 'type': 
				'type_error.integer'}, {'loc': ['category_id'], 
				'msg': 'value is not a valid integer', 'type': 
				'type_error.integer'}])
		print("Test b_3_1_3:ProductCategoryPost:Fail:not string")

	def test_b_003_01_4_ProductCategoryPost(self):
		# product_id : small
		# parent_id : small
		toValidate = {"product_id":-1,"category_id":-1}
		try:
			pc = ProductCategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()), [{'loc': 
				['product_id'], 'msg': 
				'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 
				'ctx': {'limit_value': 0}}, {'loc': ['category_id'], 
				'msg': 'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 
				'ctx': {'limit_value': 0}}])
		print("Test b_3_1_4:ProductCategoryPost:Fail:short data")

	def test_b_003_01_5_ProductCategoryPost(self):
		# product_id : non existent
		# parent_id : non existent
		toValidate = {"product_id":700000,"category_id":40000}
		try:
			pc = ProductCategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'], 
				'msg': 'there is no Product with this id: 700000', 
				'type': 'value_error'}, {'loc': ['category_id'], 
				'msg': 'there is no Category with this id: 40000', 
				'type': 'value_error'}])
		print("Test b_3_1_5:ProductCategoryPost:Fail:big name")

	def test_b_003_01_6_ProductCategoryPost(self):
		# adding unknown attribute
		# This attribute will not be returned
		toValidate = {"product_id":4,"category_id":6,"bal bla":{}}
		pc = ProductCategoryPost(**toValidate)
		#print(pc.dict())
		self.assertEqual(pc.dict(),{"product_id":4,"category_id":6})
		print("Test b_3_1_6:ProductCategoryPost:Added unknown value:Cleaned")

	def test_b_003_01_7_ProductCategoryPost(self):
		# product_id and category_id already linked
		toValidate = {"product_id":1,"category_id":1}
		try:
			pc = ProductCategoryPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['category_id'], 
				'msg': 'this product and this category are already linked', 
				'type': 'value_error'}])
		print("Test b_3_1_7:ProductCategoryPost:Name not unique,"+
			" parent_id non existent")







	def test_b_003_03_01_CategoryExists(self):
		# id small
		toValidate = {"id":0}
		try:
			product = ProductCategoryExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'ensure this value is greater than 0', 
				'type': 'value_error.number.not_gt', 'ctx': 
				{'limit_value': 0}}])
		print("Test b_3_3_1:ProductCategoryExists: id small")

	def test_b_003_03_02_CategoryExists(self):
		# id does not exist
		toValidate = {"id":100000}
		try:
			product = ProductCategoryExists(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['id'], 
				'msg': 'there is no ProductCategory with this id: 100000', 
				'type': 'value_error'}])
		print("Test b_3_3_2:ProductCategoryExists: id does not exist")

	def test_b_003_03_03_CategoryExists(self):
		# success
		toValidate = {"id":1}
		product = ProductCategoryExists(**toValidate)
		self.assertEqual(product.dict(),{"id":1})
		print("Test b_3_3_3:ProductCategoryExists:id exists")















	def test_here(self):
		#n = '0'*8
		#print(n)
		json.loads(json.dumps([{"loc": ["in_stock"],
			"msg": "You must at least enter one value to change",
			"type": "value_error"}]))
		toValidate = {}
		try:
			data = TestHere(**toValidate)
			#print(data)
			#print(data.dict())
		except Exception as e:
			print(json.loads(e.json()))
			pass
		print("Test")










































# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
