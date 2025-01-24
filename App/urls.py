from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('products', views.products, name="products"),
    path('login', views.loginView, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutView, name="logout"),
    path('product/<int:id>', views.productLoad, name="product"),
    path('events', views.events, name="events"),
    path('checkout', views.checkout, name="checkout"),
    path('checkout/<int:productId>/address', views.checkoutAddress, name="checkoutAddress"),
    path('<int:id>/payment', views.payment, name="payment"),
    path('orderVerify', views.orderVerify, name="orderVerify"),
    path('verifyMail', views.verifyMail, name="verifyMail")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
