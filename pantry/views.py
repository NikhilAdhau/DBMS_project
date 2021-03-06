from django.shortcuts import render, redirect
from django.http import HttpResponse
from math import ceil
from .models import Product, Cart, Wishlist, Wishlist_item, Product_category, Order_item, Order, Cart_item
import re
from django.contrib.auth.models import User
import smtplib 
from email.message import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'MERCHANT_KEY'

def index(request):
    allProds = []
    catx = Product.objects.values('category')
    cats = {item['category'] for item in catx}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        allProds.append([cat, product])

    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None
    params = {'list' : allProds, 'cart':carx }
    print("I ma in ")
    return render(request, 'pantry/index.html', params)

def grocery(request):
    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None

    allProds = []
    catx = Product.objects.values('category')
    cats = {item['category'] for item in catx}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        allProds.append([cat, product])

    # allProds = [params, params, params]
    params = {'list': allProds, 'cart': carx}
    return render(request, 'pantry/grocery.html', params)


def fruits(request):
    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None
    allProds = []
    catx = Product.objects.values('category')
    cats = {item['category'] for item in catx}
    for cat in cats:
        if cat == 'Fruit':
            product = Product.objects.filter(category=cat)
            allProds.append([cat, product])
            params = {'list' : allProds , 'cart': carx}
    return render(request, 'pantry/fruits.html', params)


def vegetables(request):
    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None

    allProds = []
    catx = Product.objects.values('category')
    cats = {item['category'] for item in catx}
    for cat in cats:
        if cat == 'vegetables':
            product = Product.objects.filter(category=cat)
            allProds.append([cat, product])
            params = {'list' : allProds, 'cart': carx}
    return render(request, 'pantry/vegetables.html', params)

def register(request):
    carx = None
    if request.user.is_authenticated:
	    carx = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        forms = UserRegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            username = forms.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created. Log In to continue')
            return redirect('login')
    else:
        forms = UserRegisterForm()
    return render(request, 'pantry/register.html', {'form': forms, 'cart': carx})

def Login(request):
    if request.method == 'POST':
        loginusername = request.POST['loginuname']
        passw = request.POST['loginpass']

        user = authenticate(username=loginusername, password=passw)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
    return redirect('home')

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def Signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been successfully created")
        return redirect('home')
    else:
        return redirect('home')

def productview(request, cat):
    product = Product.objects.all()
    a = []
    for i in product:
        if cat == i.category:
            #a.append(i)
            if Cart_item.objects.filter(p_id = i):
                if Wishlist_item.objects.filter(p_id = i):
                    a.append([i,True,True])
                else:
                    a.append([i, True, False])
            else:
                if Wishlist_item.objects.filter(p_id = i):
                    a.append([i,False,True])
                else:
                    a.append([i,False, False])
    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None
    return render(request, 'pantry/productview.html', {'list': a, 'cart': carx})


@login_required
def cart(request,idz, typer):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_qs = Cart_item.objects.filter(cart_id = cart)

    sum1 = 0
    product = []
    for car in cart_qs:
        product.append(Product.objects.get(p_id = car.p_id.p_id))
        price = Product.objects.get(p_id = car.p_id.p_id).price
        sum1 = sum1 + price * car.prod_quantity
        cart.total_cost = sum1
    cart.save()
    print(cart.total_cost)
    cart_qs = zip(product, cart_qs)
    return render(request, 'pantry/cart.html', {'cart1': cart_qs, 'sum' : sum1, 'cart':len(Cart_item.objects.filter(cart_id = cart.cart_id))})

@login_required
def update_cart(request, idz, typer):
    mode = str(typer)
    id1 = int(idz)
    product = Product.objects.filter(p_id = id1).first()
    #cart, created = Cart.objects.get_or_create(user = request.user)
    cart, created = Cart.objects.get_or_create(user = request.user)

    #print(type(cart), created)
    cart_item, created = Cart_item.objects.get_or_create(cart_id = cart, p_id = product)
    if mode == 'add':
        cart_item.prod_quantity = cart_item.prod_quantity +  1 
        cart_item.save()
        print (cart_item.prod_quantity )
        messages.success(request, 'Added to cart')
    elif mode == 'sub':
        cart_item.prod_quantity = cart_item.prod_quantity - 1 
        cart_item.save()
        if cart_item.prod_quantity == 0:
            cart_item.delete()
    elif mode == 'delete':
        messages.success(request, 'Item deleted')
        cart_item.delete()
    elif mode == 'save':
        update_wishlist(request, idz, 'add')
        cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #
#
@login_required
def wishlist(request, idz, typer):
    wishlist = Wishlist.objects.filter(user = request.user)
    product = []
    if len(wishlist):
        wishlist_qs = Wishlist_item.objects.filter(wishlist_id = wishlist[0])
        for i in wishlist_qs:
            product.append(Product.objects.get(p_id = i.p_id.p_id))
        wishlist_qs = zip(product, wishlist_qs)
        return render(request, 'pantry/wishlist.html', {'cart1': wishlist_qs})
    return render(request, 'pantry/wishlist.html')

@login_required
def update_wishlist(request, idz, typer):
    mode = str(typer)
    id1 = int(idz)
    #product = get_object_or_404(Product ,p_id = id1)
    product = Product.objects.filter(p_id = id1).first()
    wishlist, created = Wishlist.objects.get_or_create(user = request.user)
    print(type(wishlist), created)
    wishlist_item, created = Wishlist_item.objects.get_or_create(wishlist_id = wishlist, p_id = product)
    if mode == 'add':
        messages.success(request, "Added to wishlist")
        pass
    elif mode == 'delete':
        wishlist_item.delete()
        messages.success(request, "Item deleted")
    elif mode == 'move':
        update_cart(request, idz, 'add')
        wishlist_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def profile(request):
    return render(request, 'pantry/profile.html')

def search_results(request):
    if request.user.is_authenticated:
        if len(Cart.objects.filter(user = request.user)):
            carx = len(Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user)))
        else:
            carx = None
    else: 
        carx = None
    search = request.GET.get('Search', 'default')
    products = Product.objects.all()
    a = []

    for i in products:
        if re.search(search, i.p_name, re.IGNORECASE):
            a.append(i)
    params = {'list': a, 'cart': carx}
    return render(request, 'pantry/search.html', params)

@login_required
def checkout(request):
    if request.method=="POST":
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order.objects.create(user = request.user, order_amount = Cart.objects.get(user=request.user).total_cost, order_address=address, order_city=city, order_state=state, order_phone=phone)
        cartitem = Cart_item.objects.filter(cart_id = Cart.objects.get(user = request.user))
        for i in cartitem:
            Order_item.objects.create(order_id = order, p_id = Product.objects.get(p_id = i.p_id.p_id), quantity=i.prod_quantity)
        
        
        param_dict={

                'MID': 'MERCHANT_ID',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(order.order_amount),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        return  render(request, 'pantry/paytm.html', {'param_dict': param_dict})
    return render(request, 'pantry/checkout.html', {'totalprice': Cart.objects.get(user = request.user).total_cost})


@csrf_exempt
#@login_required
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            a = Order.objects.get(order_id = int(response_dict['ORDERID']))
            a.order_success = True
            a.save()
            Cart.objects.get(total_cost = a.order_amount).delete()
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls() 
            s.login("wethestockedpantry@gmail.com", "Thestockedpantry@1234")
            msg = EmailMessage()
            subject = "Regarding Your Order"
            message = "Dear " + str(a.user) + ",\n your order with order id " + str(a.order_id) + " was successfully placed.\n\nThank you for using The Stocked Pantry.\n\nRegards,\nThe Stocked Pantry"
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = "wethestockedpantry@gmail.com"
            msg['To'] = a.user.email
            s.send_message(msg)
            s.quit()
        else:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls() 
            s.login("wethestockedpantry@gmail.com", "Thestockedpantry@1234")
            msg = EmailMessage()
            subject = "Regarding Your Order"
            message = "Dear " + str(a.user) + ",\nWe regret to inform you that your order with order id " + str(a.order_id) + " was not successfull because " + response_dict['RESPMSG'] +  ".\n\nThank you for using The Stocked Pantry.\n\nRegards,\nThe Stocked Pantry"
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = "wethestockedpantry@gmail.com"
            msg['To'] = a.user.email
            s.send_message(msg)
            s.quit()
    return render(request, 'pantry/paymentstatus.html', {'response': response_dict})


def Order_history(request):
    order2 = []
    order = Order.objects.filter(user = request.user)
    order.reverse()
    for i in order:
        a = []
        a.append(i.order_id)
        l = Order_item.objects.filter(order_id = i)
        productname = []
        for j in l:
            productname.append(Product.objects.get(p_id = j.p_id.p_id).p_name)
        
        pname = ''
        for j in productname:
            pname += j + ', '
        a.append(pname[:-2])
        a.append(i.date)
        if i.cancelled == True:
            a.append("Cancelled")
        elif i.deliverred == True:
            a.append("Delivered")
        elif i.shipped == True:
            a.append("Shipped")
        else:
            a.append("Processing")
        a.append(i.order_amount)
        order2.append(a)
    return render(request, 'pantry/order.html', {'order': order2})

def Order_cancel(request, idz):
    order = Order.objects.get(order_id = idz)
    order.cancelled = True
    order.save()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls() 
    s.login("wethestockedpantry@gmail.com", "Thestockedpantry@1234")
    msg = EmailMessage()
    subject = "Regarding Your Order Cancellation"
    message = "Dear " + str(request.user) + ",\n your order with order id " + str(idz) + " was cancelled"
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = "wethestockedpantry@gmail.com"
    msg['To'] = request.user.email
    s.send_message(msg)
    s.quit()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))