from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from .middlewares.auth import auth_middleware
from .models.order import Order
from .models.product import Product, Category
from .models.customer import Customer


# Home view
class Home(View):
    def get(self, request):
        cart = request.session.get('customer_session_cart')
        if not cart:
            request.session['customer_session_cart'] = {}
        get_allproducts = None
        get_allcaregories = Category.all_categories()
        categoryID = request.GET.get('categoryby')
        if categoryID:
            get_allproducts = Product.get_all_products_by_categoryid(categoryID)
        else:
            get_allproducts = Product.all_products()
        data = {}
        data['Allproducts'] = get_allproducts
        data['Allcaregories'] = get_allcaregories
        print("your customer_id are : ", request.session.get('customer_session_id'))
        print("your customer_email are : ", request.session.get('customer_session_email'))
        return render(request, "store/home.html", data)
    def post(self, request):
        products_ls = request.POST.get('productwise_id')
        # print("clicked product id : " , products_ls)
        remove_quantity = request.POST.get("remove")
        cart = request.session.get('customer_session_cart')
        if cart:
            quantity = cart.get(products_ls)
            if quantity:
                if remove_quantity:
                    if quantity <= 1:
                        cart.pop(products_ls)
                    else:
                        cart[products_ls] = quantity - 1
                else:
                    cart[products_ls] = quantity + 1
            else:
                cart[products_ls] = 1
        else:
            cart = {}
            cart[products_ls] = 1
        request.session['customer_session_cart'] = cart
        # print("your cart : ", request.session['customer_session_cart'])
        return redirect('StoreHomePage')


# Signup view
class Signup(View):
    def get(self, request):
        return render(request, "store/signup.html")
    def post(self, request):
        c_name = request.POST.get('customer_name')
        c_phone = request.POST.get('customer_phone')
        c_email = request.POST.get('customer_email')
        c_pass1 = request.POST.get('customer_password1')
        c_pass2 = request.POST.get('customer_password2')
        customer = Customer(name=c_name, phone=c_phone, email=c_email, password1=c_pass1, password2=c_pass2)
        filled_values = {'C_Name': c_name, 'C_Email': c_email, 'C_Phone': c_phone}
        # form validating
        error_message = None
        error_message = self.ValidateCustomer(customer)
        # form saving
        if not error_message:
            # print(c_name, c_phone, c_email, c_pass1, c_pass2)
            customer.password1 = make_password(customer.password1)
            customer.password2 = make_password(customer.password2)
            customer.save()
            return redirect("StoreHomePage")
        else:
            values = {'Filled_Values': filled_values, "Error": error_message}
            return render(request, "store/signup.html", values)
    def ValidateCustomer(self, customer):
        error_message = None
        if not customer.name:
            error_message = "Name Required"
        elif len(customer.name) < 3:
            error_message = "Name must be 3 char long or more"
        elif not customer.email:
            error_message = "Email Required"
        elif len(customer.email) < 3:
            error_message = "Email must be 3 char long or more"
        elif not customer.phone:
            error_message = "Phone Required"
        elif len(customer.phone) < 10:
            error_message = "Phone must be 10 digit long or more"
        elif not customer.password1:
            error_message = "Password Required"
        elif len(customer.password1) < 6:
            error_message = "Password must be 6 char long or more"
        elif not customer.password2:
            error_message = "Confirm Password Required"
        elif len(customer.password2) < 6:
            error_message = "Confirm Password must be 6 char long or more"
        elif customer.password1 != customer.password2:
            error_message = "Password and Confirm Password must be same"
        elif customer.isExist_Phone():
            error_message = "Phone Number already Registered"
        elif customer.isExist_Email():
            error_message = "Email already Registered"
        return error_message


# Login view
class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "store/login.html")
    def post(self, request):
        c_email = request.POST.get('customer_email')
        c_phone = request.POST.get('customer_phone')
        c_pass1 = request.POST.get('customer_password1')
        customer = Customer.getCustomer_by_email(email=c_email)
        error_message = None
        if customer:
            flag = check_password(c_pass1, customer.password1)
            flag = check_password(c_pass1, customer.password1)
            if flag:
                request.session['customer_session_id'] = customer.id  # store session by customer id
                request.session['customer_session_email'] = customer.email  # store session by customer email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('StoreHomePage')
                # return redirect("StoreHomePage")
                # return HttpResponseRedirect(reverse("CartPage"))
            else:
                error_message = "Email or Password Invalid"
        else:
            error_message = "Email or Password Invalid"
        # print(c_email, c_pass1, c_phone)
        return render(request, "store/login.html", {'Error': error_message})


def logout(request):
    request.session.clear()
    return redirect("LoginPage")


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('customer_session_cart').keys())
        cart_products = Product.get_products_by_id(ids)
        # print(cart_products)
        # print(ids)
        cart_data = {}
        cart_data['Cart_Products'] = cart_products
        return render(request, "store/cart.html", cart_data)


class Checkout(View):
    def post(self, request):
        ship_address = request.POST.get('shipping_address')
        ship_phone = request.POST.get('shipping_phone')
        customer_id = request.session.get('customer_session_id')  # get customer id
        cart = request.session.get('customer_session_cart')
        cart_productslist = Product.get_products_by_id(list(cart.keys()))
        for cart_product in cart_productslist:
            order = Order(product=cart_product,
                          customer=Customer(id=customer_id),
                          quantity=cart.get(str(cart_product.id)),
                          price=cart_product.product_sell_price,
                          address=ship_address,
                          phone=ship_phone)
            order.save()
        request.session['customer_session_cart'] = {}
        return redirect('OrderPage')


class PlaceOrder(View):
    # @method_decorator(auth_middleware)
    def get(self, request):
        customerid = request.session.get('customer_session_id')  # get customer id
        placed_orders = Order.objects.filter(customer=customerid).order_by('-ordered_date')
        return render(request, "store/order.html", {"Placed_Orders": placed_orders})

def profile(request):
    return render(request, "store/profile.html")
