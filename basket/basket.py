from decimal import Decimal

from store.models import Product



class Basket():
	"""
	A base Basket class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		basket = self.session.get('skey')

		if 'skey' not in request.session:
			basket = self.session['skey'] = {}
		self.basket = basket

	def add(self, product, qty):
		"""
		Adding and updating the users basket session data
		"""
		product_id = str(product.id)

		if product.discount_price:
			discount_price = float(product.discount_price)
		else:
			discount_price = ''
		if product_id not in self.basket:
			self.basket[product_id] = {
				'price': float(product.price),
				'discount_price': discount_price,
				'qty': int(qty)
			}
		else:
			self.basket[product_id]['qty'] = int(self.basket[product_id]['qty']) + int(qty)

		self.save()

	def update(self, product, qty):
		"""
		Updating the users basket session data
		"""
		product_id = str(product.id)

		if product_id in self.basket:
			self.basket[str(product_id)]['qty'] = int(qty)

		self.save()

	def delete(self, product):
		"""
		Deleting and updating the users basket session data
		"""
		product_id = str(product.id)
		if product_id in self.basket:
			del self.basket[product_id]
			self.save()

	def __iter__(self):
		"""
		Collect the product_id in the session data to query the database and return products
		"""
		product_ids = self.basket.keys()
		products = Product.products.filter(id__in=product_ids)
		basket = self.basket.copy()

		for product in products:
			basket[str(product.id)]['product'] = product

		for item in basket.values():
			item['total_price'] = item['price'] * item['qty']
			yield item

	def __len__(self):
		"""
		Get the basket data and count the qty of items
		"""
		return sum(item['qty'] for item in self.basket.values())

	def get_discount_price(self):
		return float(self.get_before_discount()) - float(self.get_total_price())

	def get_before_discount(self):
		return sum(item['price'] * item['qty'] for item in self.basket.values())

	def get_total_price(self):
		return sum(item['discount_price'] * item['qty'] if item['discount_price'] != '' else item['price'] * item['qty'] for item in self.basket.values())

	def save(self):
		self.session.modified = True

	def clear(self):
		del self.session['skey']
		self.save()