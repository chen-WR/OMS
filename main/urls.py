from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, register, logins, logouts, home, product, cart, checkout, ordered, updateCart, viewOrder, generateSecretKey, updateSecretKey

urlpatterns = [
	path('', index, name='index'),
	path('register/', register, name='register'),
	path('login/', logins, name='logins'),
	path('logout/', logouts, name='logouts'),
	path('home/', home, name='home'),
	path('product/', product, name='product'),
	path('cart/', cart, name='cart'),
	path('checkout/', checkout, name='checkout'),
	path('ordered/<confirmation_number>/', ordered, name='ordered'),
	path('updateCart/', updateCart, name='updateCart'),
	path('viewOrder/<confirmation_number>/', viewOrder, name='viewOrder'),
	path('generate/', generateSecretKey, name='generate'),
	path('update/', updateSecretKey, name='update'),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)