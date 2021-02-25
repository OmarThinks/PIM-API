# PIM-API:

Minimal Product Information Management with Django-Ninja

## Initializiation:

Just to make sure that you environment is set up as mine.  
Run these scripts.

<b>

```bash
virtualenv env --python=python3.7.9
source env/Scripts/activate
pip install -r requirements.txt
```

</b>




## Testing:




Run these scripts.
<b>

```bash
python models_test.py
python pydantic_test.py
```

</b>

**There is also a postman collection to test API endpoints.**


### `models.py`:
This file contains all the SQLAlchemy models.  
### `pydatic_models.py`:
This file contains all the pydantic classes, for validation and 
sanitization of user inputs.  




## Used tech stack:
### SQLAchemy:
This is the ORM

### unittest:
This enables me to run unittesting.

### pydantic:
for validation and sanitization of user inputs

### dajngo ninja:
**To make django look more like FastAPI**




## Running the API:

<b>

```bash
./manage.py runserver
```

<a href="http://127.0.0.1:8000/api/" target="_blank">http://127.0.0.1:8000/api/</a>

</b>


## Documentation:


<b>
<a href="http://127.0.0.1:8000/api/docs" target="_blank">
http://127.0.0.1:8000/api/docs</a>

</b>










## Endpoints:


### Make sure that everything is working correctly:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/" target="_blank">
		http://127.0.0.1:8000/api/</a></td>
	</tr>
	<tr>
		<td>2</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/ping" target="_blank">
		http://127.0.0.1:8000/api/ping</a></td>
	</tr>
</table>




### Database endpoints:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/drop_create" target="_blank">
		http://127.0.0.1:8000/api/drop_create</a></td>
	</tr>
	<tr>
		<td>2</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/populate" target="_blank">
		http://127.0.0.1:8000/api/populate</a></td>
	</tr>
</table>



### Documentation endpoints:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/docs" target="_blank">
		http://127.0.0.1:8000/api/docs</a></td>
	</tr>
</table>


### Product endpoints:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/products" target="_blank">
		http://127.0.0.1:8000/api/products</a></td>
	</tr>
	<tr>
		<td>2</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/products/1" target="_blank">
		http://127.0.0.1:8000/api/products/{id}</a></td>
	</tr>
	<tr>
		<td>3</td>
		<td>POST</td>
		<td>http://127.0.0.1:8000/api/products</td>
	</tr>
	<tr>
		<td>4</td>
		<td>DELETE</td>
		<td>http://127.0.0.1:8000/api/products/{id}</td>
	</tr>
	<tr>
		<td>5</td>
		<td>PUT</td>
		<td>http://127.0.0.1:8000/api/products/{id}</td>
	</tr>
</table>








### Category endpoints:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/categories" target="_blank">
		http://127.0.0.1:8000/api/categories</a></td>
	</tr>
	<tr>
		<td>2</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/categories/1" target="_blank">
		http://127.0.0.1:8000/api/categories/{id}</a></td>
	</tr>
	<tr>
		<td>3</td>
		<td>POST</td>
		<td>http://127.0.0.1:8000/api/categories</td>
	</tr>
	<tr>
		<td>4</td>
		<td>DELETE</td>
		<td>http://127.0.0.1:8000/api/categories/{id}</td>
	</tr>
	<tr>
		<td>5</td>
		<td>PUT</td>
		<td>http://127.0.0.1:8000/api/categories/{id}</td>
	</tr>
</table>








### ProductCategory endpoints:

<table>
	<tr>
		<th>Number</th>
		<th>Method</th>
		<th>Endpoint</th>
	</tr>
	<tr>
		<td>1</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/product/categories" target="_blank">
		http://127.0.0.1:8000/api/product/categories</a></td>
	</tr>
	<tr>
		<td>2</td>
		<td>GET</td>
		<td><a href="http://127.0.0.1:8000/api/product/categories/1" target="_blank">
		http://127.0.0.1:8000/api/product/categories/{id}</a></td>
	</tr>
	<tr>
		<td>3</td>
		<td>POST</td>
		<td>http://127.0.0.1:8000/api/product/categories</td>
	</tr>
	<tr>
		<td>4</td>
		<td>DELETE</td>
		<td>http://127.0.0.1:8000/api/product/categories/{id}</td>
	</tr>
</table>

















# CRUD Rules:


## 1) Product:



<table>
	<tr>
		<th>Name</th>
		<th>Type</th>
		<th>Unique</th>
		<th>Nullable</th>
		<th>Min</th>
		<th>Max</th>
		<th>PrimaryKey</th>
		<th>ForeignKey</th>
	</tr>
	<tr>
		<th>id</th>
		<td>Integer</td>
		<td>True</td>
		<td>False</td>
		<td>1</td>
		<td></td>
		<td>True</td>
		<td></td>
	</tr>
	<tr>
		<th>name</th>
		<td>String</td>
		<td>False</td>
		<td>False</td>
		<td>min len = 3</td>
		<td>max len = 300</td>
		<td>False</td>
		<td></td>
	</tr>
	<tr>
		<th>price</th>
		<td>Float</td>
		<td>False</td>
		<td>False</td>
		<td>0.1</td>
		<td>1000000</td>
		<td>False</td>
		<td></td>
	</tr>
	<tr>
		<th>quantity</th>
		<td>float</td>
		<td>False</td>
		<td>False</td>
		<td>.001</td>
		<td>100000000</td>
		<td>False</td>
		<td></td>
	</tr>
	<tr>
		<th>code</th>
		<td>Integer</td>
		<td>True</td>
		<td>True</td>
		<td>3</td>
		<td>100000000000000000000000000</td>
		<td>False</td>
		<td></td>
	</tr>
</table>








1. Each product has a unique `id`
2. Each product has a `name`, `price` and `quantity`, they are not unique, 
and they can not be equal to `null`
3. `name` is string
	- Example: "Cheese"
4. `price` is float
	- Example: $0.5
5. `quantity` is float
	- Example: 0.5 kg
6. each product has a `code`, it is integer
	- https://www.barcodelookup.com/
	- Example: 1234567
7. `code` can be equal to `null`
	- Example: new unregistered product
8. `code` must be unique, unless if it was null
	- There can be lots of products with code equal to null
9. When deleting a Product
	1. catogories will not be affected
	2. all `ProductCategory` related to this product will be deleted
		- Do not confuse with `Category`
		- Categories will not be affected





## 2) Category:






<table>
	<tr>
		<th>Name</th>
		<th>Type</th>
		<th>Unique</th>
		<th>Nullable</th>
		<th>Min</th>
		<th>Max</th>
		<th>PrimaryKey</th>
		<th>ForeignKey</th>
	</tr>
	<tr>
		<th>id</th>
		<td>Integer</td>
		<td>True</td>
		<td>False</td>
		<td>1</td>
		<td></td>
		<td>True</td>
		<td></td>
	</tr>
	<tr>
		<th>name</th>
		<td>String</td>
		<td>True</td>
		<td>False</td>
		<td>min len = 3</td>
		<td>max len = 300</td>
		<td>False</td>
		<td></td>
	</tr>
	<tr>
		<th>parent_id</th>
		<td>Integer</td>
		<td>False</td>
		<td>True</td>
		<td>1</td>
		<td></td>
		<td>False</td>
		<td>Category.id</td>
	</tr>
</table>




















1. Each category has a unique `id`
2. Each category has a `name`, `parent_id`
3. `name` is unique, and can not be equal to `null`
4. `parent_id` can be equal to `null`
5. each category can only have one parent
6. each category can unlimited amount of children
7. When deleting a Category
	1. If it has children, all them will have a `null` parent
	2. Products will not be affected at all
	3. ProductCategory related to this Category will be deleted
		- Do not confuse Product and ProductCategory
		- Product will not be affected be the deletion


## 2) ProductCategory:












<table>
	<tr>
		<th>Name</th>
		<th>Type</th>
		<th>Unique</th>
		<th>Nullable</th>
		<th>Min</th>
		<th>Max</th>
		<th>PrimaryKey</th>
		<th>ForeignKey</th>
	</tr>
	<tr>
		<th>id</th>
		<td>Integer</td>
		<td>True</td>
		<td>False</td>
		<td>1</td>
		<td></td>
		<td>True</td>
		<td></td>
	</tr>
	<tr>
		<th>category_id</th>
		<td>Integer</td>
		<td>False</td>
		<td>False</td>
		<td>1</td>
		<td></td>
		<td>False</td>
		<td>Category.id</td>
	</tr>
	<tr>
		<th>product_id</th>
		<td>Integer</td>
		<td>False</td>
		<td>False</td>
		<td>1</td>
		<td></td>
		<td>False</td>
		<td>Product.id</td>
	</tr>
</table>












1. Each ProductCategory has a unique `id`
2. Each ProductCategory has a `product_id`, `category_id`, 
they can not be equal to null
3. the pair of (`product_id`, `category_id`) is unique
4. a ProductCategory will be deleted **Automatically** in any of those cases
	1. Associated Product is deleted
	2. Associated Category is deleted
5. When deleting a ProductCategory
	1. Associated Product will not be affected
	2. Associated Category will not be affected




# Errors:


<b>
Errors are pydantic type of errors, because I use Django ninja
</b>


Example:

```JSON
{
    "detail": [
        {
            "loc": [
                "body",
                "product",
                "name"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "product",
                "price"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "product",
                "quantity"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```















# What is a good API:

- A good a API authenticated and validated that no one can manipulate 
it and get information he is not supposed to have access to.
- Secure
- Tested






















