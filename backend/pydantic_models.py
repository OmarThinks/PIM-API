from typing import List, Optional
from pydantic import (BaseModel,
	ValidationError, validator, constr, conint, confloat)
import json
from models import (NotReceived, validate_key,
MyModel, Product,Category,ProductCategory,
	populate_tables, db_drop_and_create_all,get_dict,
	)
import base64





# General
id_con = conint(gt=0)





"""
validate_model_id
- Inputs:
	- model: the SQLAlchemy model
	- id: the int of the id
- Function:
	- Make sure that this model exists
	- raise error if it was not an integer
- Output:
	- True: This model exists
	- False: This model does not exist
"""

def validate_model_id(model,id:int):
	try:
		if model.query().get(id) == None:
			return False
		return True
	except:
		raise ValueError("validate_model_id:expected the "+
			"type of SQLAlchemy, but found "+
			"the type of "+str(type(model))+" instead")




"""
validate_model_id_pydantic
- Inputs:
	- model: the SQLAlchemy model
	- id: the int of the id
- Function:
	- raise correct error if the model does not exist
- Output:
	- No output, only error are raised
"""
def validate_model_id_pydantic(model,id:int):
	model_name = model.__name__
	if validate_model_id(model,id) == True:
		pass
	else:
		raise ValueError("there is no "+ model_name +
		 " with this id: " +str(id))




# Product Constraints
product_name_con = constr(strip_whitespace=True, min_length=3,max_length=300)
price_con = confloat(ge=.1, le=1000000)
quantity_con = confloat(ge=.001, le=100000000)
code_con = conint(ge=2, le=100000000000000000000000000)



class ProductBasic(BaseModel):
	name : str
	price : float
	quantity : float
	code : int = None # code is nullable


"""
Used in both of Post or Update
"""
class ProductPost(BaseModel):
	name : product_name_con
	price : price_con
	quantity : quantity_con
	code : code_con = None # code is nullable
	
	@validator('code')
	def unique_code(cls, value):
		if value == None:
			return value
		same_code_products = Product.query().filter(Product.code == value).all()
		if len(same_code_products) == 0:
			return value
		raise ValueError("this code is already related to another product")

class ProductUpdate(BaseModel):
	id: id_con
	name : product_name_con
	price : price_con
	quantity : quantity_con
	code : code_con = None # code is nullable
	
	@validator('id')
	def id_exists(cls, value):
		validate_model_id_pydantic(Product,value)
		return value

	@validator('code')
	def unique_code(cls, value, values):
		if value == None:
			return value
		if "id" not in values:
			return value
		id = values["id"]
		same_code_products = Product.query().filter(Product.code == value).all()
		if len(same_code_products) == 0:
			return value
		if same_code_products[0].id == id:
			return value
		raise ValueError("this code is already related to another product")


class ProductExists(BaseModel):
	id: id_con
	@validator('id')
	def id_exists(cls, value):
		validate_model_id_pydantic(Product,value)
		return value






class CategoryBasic(BaseModel):
	name : str
	parent_id : int

# Category Constraints
category_name_con = constr(strip_whitespace=True, min_length=3,max_length=300)

"""
Used in both of Post or Update
"""
class CategoryPost(BaseModel):
	name : category_name_con
	parent_id : conint(ge=0)
	
	@validator('name')
	def unique_name_validation(cls, value):
		same_name_categories = Category.query().filter(
			Category.name == value).all()
		if len(same_name_categories) == 0:
			return value
		raise ValueError("this name is already related to another category")
	
	@validator('parent_id')
	def parent_id_validation(cls, value):
		# If parent_id = 0 -> It has no parent
		if value == 0:
			return None
		validate_model_id_pydantic(Category,value)
		return value

class CategoryUpdate(BaseModel):
	id: id_con
	name : category_name_con
	parent_id : conint(ge=0)
	
	@validator('id')
	def existing_id_validation(cls, value):
		validate_model_id_pydantic(Category, value)
		return value

	@validator('name')
	def unique_name_validation(cls, value, values):
		if "id" not in values:
			return value
		same_name_categories = Category.query().filter(
			Category.name == value).all()
		#There should be no category with the same name
		if len(same_name_categories) == 0:
			return value
		id = values["id"]
		# if there is a category with the same name, it must have the
		# 	same id
		if same_name_categories[0].id == id:
			return value
		raise ValueError("this name is already related to another category")

	@validator('parent_id')
	def parent_id_validation(cls, value, values):
		# If parent_id = 0 -> It has no parent
		if value == 0:
			return None
		validate_model_id_pydantic(Category,value)
		if "id" not in values:
			return value
		id = values["id"]
		if value == id:
			raise ValueError("a category can not be a parent to itself")
		return value


class CategoryExists(BaseModel):
	id: id_con
	@validator('id')
	def id_exists(cls, value):
		validate_model_id_pydantic(Category,value)
		return value





class ProductCategoryBasic(BaseModel):
	product_id : int
	category_id : int

"""
Used in both of Post or Update
"""
class ProductCategoryPost(BaseModel):
	product_id : id_con
	category_id : id_con
	
	@validator('product_id')
	def product_id_validation(cls, value):
		validate_model_id_pydantic(Product,value)
		return value
	@validator('category_id')
	def category_id_validation(cls, value, values):
		validate_model_id_pydantic(Category,value)

		# Make sure that these values do not already exist
		if "product_id" in values:
			result = ProductCategory.query().filter(
				ProductCategory.category_id==value,
				ProductCategory.product_id==values["product_id"]).all()
			if len(result)!=0:
				raise ValueError("this product and this"+
					" category are already linked")
		return value


class ProductCategoryExists(BaseModel):
	id: id_con
	@validator('id')
	def id_exists(cls, value):
		validate_model_id_pydantic(ProductCategory,value)
		return value





























the_tst=constr(strip_whitespace=True, min_length=1,max_length=5)



class TestHere(BaseModel):
  a: str = None
  b: str = None

  @validator('b')
  def check_a_or_b(cls, v, values):
    if 'a' not in values and not b:
      raise ValueError('either a or b is required')
    return b
