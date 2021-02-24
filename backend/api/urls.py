import json


from django.contrib import admin
from django.urls import path
#from rest_framework import status
#from rest_framework.response import Response
from django.http import JsonResponse

from ninja import (NinjaAPI, Schema)


from pydantic_models import (ProductBasic, ProductPost, 
	ProductUpdate, CategoryPost,
	CategoryUpdate,ProductCategoryPost,ProductExists, 
	CategoryBasic, CategoryExists, 
	ProductCategoryExists,ProductCategoryBasic)

from models import (Product,Category,ProductCategory,
	populate_tables, db_drop_and_create_all,get_dict, create_all)
from pydantic import BaseModel



api = NinjaAPI()

create_all()


def jsoinify_error(e):
	response = JsonResponse({"detail":json.loads(e.json())})
	response.status_code = 400  
	return response


@api.get("/")
def add(request):
	return {"success": True}

@api.get("/ping")
def add(request):
	return {"success": True}

@api.get("/drop_create")
def add(request):
	db_drop_and_create_all()
	return {"success": True}

@api.get("/populate")
def add(request):
	populate_tables()
	return {"success": True}





"""
Product model

"""
@api.get("/products")
def get_products(request):
	all_products = Product.query().order_by("id").all()
	all_products = [product.simple() for product in all_products]
	return{"suucess":True, "products":all_products}

@api.get("/products/{id}")
def get_products(request, id):
	try:
		product_id = ProductExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	product = Product.query().get(product_id.id)
	return{"suucess":True, "product":product.deep()}

@api.post("/products")
def post_products(request, product:ProductPost):
	product = Product(**product.dict())
	product.insert()
	return{"suucess":True, "product":product.deep()}

@api.delete("/products/{id}")
def delete_products(request, id):
	try:
		product = ProductExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	product = Product.query().get(product.id).delete()
	return{"suucess" : True , 
		"result" : "product deleted successfully" }

@api.put("/products/{id}")
def put_products(request, id, product:ProductBasic):
	product = product.dict()
	product["id"] = id
	try:
		product = ProductUpdate(**product)
	except Exception as e:
		return jsoinify_error(e)
	product_record = Product.query().get(product.id)
	product_record.update(**product.dict())
	return{"suucess" : True , 
		"product" : product_record.deep()}





"""
Category model
"""

@api.get("/categories")
def get_categories(request):
	all_categories = Category.query().order_by("id").all()
	all_categories = [category.simple() for category in all_categories]
	return{"suucess":True, "categories":all_categories}

@api.get("/categories/{id}")
def get_categories(request, id):
	try:
		category_id = CategoryExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	category = Category.query().get(category_id.id)
	return{"suucess":True, "category":category.deep()}

@api.post("/categories")
def post_categories(request, category:CategoryPost):
	category = Category(**category.dict())
	category.insert()
	return{"suucess":True, "category":category.deep()}

@api.delete("/categories/{id}")
def delete_categories(request, id):
	try:
		category = CategoryExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	category = Category.query().get(category.id).delete()
	return{"suucess" : True , 
		"result" : "category deleted successfully" }

@api.put("/categories/{id}")
def put_categories(request, id, category:CategoryBasic):
	category = category.dict()
	category["id"] = id
	try:
		category = CategoryUpdate(**category)
	except Exception as e:
		return jsoinify_error(e)
	category_record = Category.query().get(category.id)
	category_record.update(**category.dict())
	return{"suucess" : True , 
		"category" : category_record.deep()}




"""
ProductCategory model
"""

@api.get("/product/categories")
def get_products_categories(request):
	all_pcs = ProductCategory.query().order_by("id").all()
	all_pcs = [category.simple() for category in all_pcs]
	return{"suucess":True, "categories":all_pcs}

@api.get("/product/categories/{id}")
def get_products_categories(request, id):
	try:
		pc_id = ProductCategoryExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	pc = ProductCategory.query().get(pc_id.id)
	return{"suucess":True, "product_category":pc.deep()}

@api.post("/product/categories")
def post_products_categories(request, product_category:ProductCategoryPost):
	product_category = ProductCategory(**product_category.dict())
	product_category.insert()
	return{"suucess":True, "product_category":product_category.deep()}

@api.delete("/product/categories/{id}")
def delete_products_categories(request, id):
	try:
		pc = ProductCategoryExists(id=id)
	except Exception as e:
		return jsoinify_error(e)
	pc = ProductCategory.query().get(pc.id).delete()
	return{"suucess" : True , 
		"result" : "Product Category deleted successfully" }






urlpatterns = [
	path("admin/", admin.site.urls),
	path("api/", api.urls),
]

