from django.urls import path
from django.views.generic import RedirectView
from . import views
from .middlewares.auth import auth_middleware

urlpatterns = [
    # path("", RedirectView.as_view(url="home/")),
    path("", views.Home.as_view(), name="StoreHomePage"),
    path("signup", views.Signup.as_view(), name="SignUpPage"),
    path("login", views.Login.as_view(), name="LoginPage"),
    path("logout", views.logout, name="LogoutPage"),
    path("profile", views.profile, name="ProfilePage"),
    path("cart", auth_middleware(views.Cart.as_view()), name="CartPage"),
    path("checkout", auth_middleware(views.Checkout.as_view()), name="CheckoutPage"),
    path("order", views.PlaceOrder.as_view(), name="OrderPage"),
]
