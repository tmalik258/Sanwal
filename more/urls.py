from django.urls import path

from . import views

app_name = 'more'

urlpatterns = [
	# Subscription
	path('subscribe/', views.SubscribeView, name="subscribe"),
	path('become_seller/', views.BecomeSellerView, name="become-seller"),
]