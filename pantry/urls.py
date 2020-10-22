from django.urls import path
from .import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name = 'home'),
	path('productview/<str:cat>/', views.productview, name = 'ProductView'),
    path('logout', views.Logout, name='LogOut'),
    path('signup', views.Signup, name='signup'),
    path('login', views.Login, name='login'),
    path('cart/<int:idz>/<str:typer>/<int:quant/', views.cart, name='cart'),
    path('wishlist/<int:idz>/<str:typer>/<int:quant>/', views.wishlist, name='wishlist'),
]

""" path('grocery/', views.grocery, name = 'Grocery'),
    path('fruits/', views.fruits, name = 'Fruits'),
	path('vegetables/', views.vegetables, name = 'Vegetables'),
	path('search_results/', views.search_results, name = 'search_results'),
	path('about/', views.about, name = 'AboutUs'),
	path('contact/', views.contact, name = 'ContactUs'),
	path('tracker/', views.tracker, name = 'TrackingStatus'),
	path('search/', views.search, name = 'Search'),
	
	path('order/', views.order, name = 'order'),
    path('grocery/', views.grocery, name = 'Grocery'),
	path('fruits/', views.fruits, name = 'Fruits'),
	path('vegetables/', views.vegetables, name = 'Vegetables'),
	path('search_results/', views.search_results, name = 'search_results'),
	path('about/', views.about, name = 'AboutUs'),
	path('contact/', views.contact, name = 'ContactUs'),
	path('tracker/', views.tracker, name = 'TrackingStatus'),
	path('search/', views.search, name = 'Search'),
	path('productview/<str:cat>/', views.productview, name = 'ProductView'),
	path('order/', views.order, name = 'order'),
     path('admin/', admin.site.urls),
    path('wishlist/<int:idz>/<str:typer>/<int:quant>/', user_views.wishlist, name='wishlist'),
    path('cart/<int:idz>/<str:typer>/<int:quant>/', user_views.cart, name='cart'),
    path('orders/', user_views.history, name='history'),
    path('profile/', user_views.profile, name='profile'),

    
    path('cancel_order/<int:idz>/', user_views.cancel_order, name='cancel_order'),
    """

