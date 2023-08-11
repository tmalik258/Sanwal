from django.conf import settings
import json

from store.models import (Product, ProductSpecificationValue)



class Basket():
	"""
	A base Basket class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		basket = self.session.get(settings.BASKET_SESSION_ID)

		if settings.BASKET_SESSION_ID not in request.session:
			basket = self.session[settings.BASKET_SESSION_ID] = {}
		self.basket = basket

	def add(self, product, qty, attributes):
		"""
		Adding and updating the users basket session data
		"""
		product_id = str(product.id)
		if attributes:
			for id in attributes:
				product_id += '-' + id

		if product.discount_price:
			discount_price = float(product.discount_price)
		else:
			discount_price = ''
		if product_id not in self.basket:
			self.basket[product_id] = {
				'regular_price': float(product.regular_price),
				'discount_price': discount_price,
				'qty': int(qty),
			}
		else:
			self.basket[product_id]['qty'] = int(self.basket[product_id]['qty']) + int(qty)

		self.save()

	def update(self, item_key, qty):
		"""
		Updating the users basket session data
		"""

		if item_key in self.basket:
			self.basket[item_key]['qty'] = int(qty)

		self.save()

	def delete(self, item_key):
		"""
		Deleting and updating the users basket session data
		"""
		if item_key in self.basket:
			del self.basket[item_key]
			self.save()

	def __iter__(self):
		"""
		Collect the product_id in the session data to query the database and return products
		"""

		def serialize_product(product, attributes, key):
			# Convert the Product object to a dictionary
			product_data = {
				'id': product.id,
				'title': product.title,
				'description': product.description,
				'image': product.img.first().image.url,
				'attributes': {key.specification.name: key.value for key in attributes},
				'key': key
			}
			return product_data

		dict_keys = self.basket.keys()
		product_ids = [pid.split('-')[0] for pid in dict_keys]
		products = Product.products.filter(id__in=product_ids)
		product_dict = {str(product.id): product for product in products}

		basket = self.basket.copy()

		for key in dict_keys:
			ids = key.split('-')
			product_id = ids[0]
			attribute_ids = ids[1:]
			attributes = ProductSpecificationValue.objects.filter(id__in=attribute_ids)

			basket[str(key)]['product'] = serialize_product(product_dict.get(product_id), attributes, key)

		for item in basket.values():
			item['total_price'] = item['regular_price'] * item['qty']
			yield item

	def __len__(self):
		"""
		Get the basket data and count the qty of items
		"""
		return sum(item['qty'] for item in self.basket.values())

	def get_discount_price(self):
		return float(self.get_before_discount()) - float(self.get_total_price())

	def get_before_discount(self):
		return sum(item['regular_price'] * item['qty'] for item in self.basket.values())

	def get_total_price(self):
		return sum(item['discount_price'] * item['qty'] if item['discount_price'] != '' else item['regular_price'] * item['qty'] for item in self.basket.values())

	def save(self):
		self.session.modified = True

	def clear(self):
		del self.session[settings.BASKET_SESSION_ID]
		self.save()