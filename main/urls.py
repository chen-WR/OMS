from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, logins, logouts, home, product, cart, checkout

urlpatterns = [
	path('', index, name='index'),
	path('login/', logins, name='logins'),
	path('logout/', logouts, name='logouts'),
	path('home/', home, name='home'),
	path('product/', product, name='product'),
	path('cart/', cart, name='cart'),
	path('checkout/', checkout, name='checkout'),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)