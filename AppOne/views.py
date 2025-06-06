from django.shortcuts import render, redirect
from datetime import datetime

# Create your views here.
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

url = "mongodb+srv://harshine:10152004@clusterfirst.xkuitu2.mongodb.net/"

client = MongoClient(url)

# Choose the database and collection
db = client['Project']  # Database Name
collection = db['ProjectSignup']  # Collection Name

current_user = None

def signup(request):
    global current_user
    if request.method == 'POST' and request.POST.get('btn') == 'signup':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        mob = request.POST.get('phnum')
        cart = []
        product_purchased = []
        contact = []
        existing_user = collection.find_one({'Name': uname})
        if existing_user:
            return render(request, 'signup.html', {'error': 'Username already exists'})

        userdetails = {
            "Name": uname,
            "Email": email,
            "Password": password,
            "Mobile": mob,
            "cart": cart,
            "product": product_purchased,
            "contact": contact,
        }
        collection.insert_one(userdetails)
        current_user = uname
        return render(request, 'index.html')
    return render(request, 'signup.html')

def signin(request):
    global current_user
    if request.method == 'POST' and request.POST.get('btn') == 'signin':
        uname = request.POST.get('uname')
        password = request.POST.get('pass')
        user = collection.find_one({'Name': uname, 'Password': password})
        if user:
            current_user = uname
            return render(request, 'index.html')
        else:
            return render(request, 'signin.html', {'error': 'Login Failed, Invalid username or password'})
    return render(request, 'signin.html')

def indexpage(request):
    return render(request, 'index.html')

def womenspage(request):
    global current_user
    if request.method == 'POST':
        if not current_user:
            return render(request, 'signin.html', {'error': 'Please login first'})
        pn = request.POST['addtocart']
        product_details = {
            'product_name': request.POST.get('product_name'),
            'original_price': request.POST.get('original_price'),
            'discounted_price': request.POST.get('discounted_price'),
            'size': request.POST.get('size'),
            'quantity': request.POST.get('quantity'),
        }
        collection.update_one(
            {'Name': current_user},
            {'$push': {'cart': product_details}}
        )
        return render(request, 'womens.html', {'message': 'Product added to cart!'})
    return render(request, 'womens.html')

def menspage(request):
    global current_user
    if request.method == 'POST':
        if not current_user:
            return render(request, 'signin.html', {'error': 'Please login first'})
        pn = request.POST['addtocart']
        product_details = {
            'product_name': request.POST.get('product_name'),
            'original_price': request.POST.get('original_price'),
            'discounted_price': request.POST.get('discounted_price'),
            'size': request.POST.get('size'),
            'quantity': request.POST.get('quantity'),
        }
        collection.update_one(
            {'Name': current_user},
            {'$push': {'cart': product_details}}
        )
        return render(request, 'mens.html', {'message': 'Product added to cart!'})
    return render(request, 'mens.html')

def kidspage(request):
    global current_user
    if request.method == 'POST':
        if not current_user:
            return render(request, 'signin.html', {'error': 'Please login first'})
        pn = request.POST['addtocart']
        product_details = {
            'product_name': request.POST.get('product_name'),
            'original_price': request.POST.get('original_price'),
            'discounted_price': request.POST.get('discounted_price'),
            'size': request.POST.get('size'),
            'quantity': request.POST.get('quantity'),
        }
        collection.update_one(
            {'Name': current_user},
            {'$push': {'cart': product_details}}
        )
        return render(request, 'kids.html', {'message': 'Product added to cart!'})
    return render(request, 'kids.html')

def addtocart(request):
    global current_user
    if not current_user:
        return render(request, 'signin.html', {'error': 'Please login first'})

    user = collection.find_one({'Name': current_user})
    cart_items = user.get('cart', [])

    message = ''
    total = sum(
        int(item['discounted_price']) * int(item['quantity'])
        for item in cart_items
        if item.get('discounted_price') and item.get('quantity')
    )

    if request.method == 'POST':
        if 'remove_index' in request.POST:
            try:
                remove_index = int(request.POST.get('remove_index'))
                if 0 <= remove_index < len(cart_items):
                    cart_items.pop(remove_index)
                    collection.update_one(
                        {'Name': current_user},
                        {'$set': {'cart': cart_items}}
                    )
                    message = 'Item removed successfully.'
                    total = sum(
                        int(item['discounted_price']) * int(item['quantity'])
                        for item in cart_items
                    )
            except Exception as e:
                message = f'Error removing item: {str(e)}'

        elif 'buy_now' in request.POST:
            if cart_items:
                collection.update_one(
                    {'Name': current_user},
                    {
                        '$push': {'product': {'$each': cart_items}},
                        '$set': {'cart': []}
                    }
                )
                return render(request, 'purchase.html', {
                    'purchased_items': cart_items,
                    'message': 'Thank you for your purchase!'
                })
            else:
                message = 'Cart is empty. Nothing to purchase.'

    return render(request, 'addtocart.html', {
        'cart_items': cart_items,
        'total': total,
        'message': message
    })

def checkout(request):
    global current_user
    if not current_user:
        return render(request, 'signin.html', {'error': 'Please login first'})

    user = collection.find_one({'Name': current_user})
    cart_items = user.get('cart', [])

    if cart_items:
        collection.update_one(
            {'Name': current_user},
            {
                '$push': {'product': {'$each': cart_items}},
                '$set': {'cart': []}
            }
        )
        message = "Thank You for Your Purchase! Your order has been successfully placed."
    else:
        message = "Your cart is empty."

    return render(request, 'addtocart.html', {
        'cart_items': [],
        'total': 0,
        'message': message
    })

def buy_now(request):
    global current_user
    if not current_user:
        return render(request, 'signin.html', {'error': 'Please login first'})

    user = collection.find_one({'Name': current_user})
    cart_items = user.get('cart', [])

    message = ''

    if request.method == 'POST':
        index_str = request.POST.get('buy_index')
        if index_str is not None and index_str.isdigit():
            buy_index = int(index_str)
            if 0 <= buy_index < len(cart_items):
                item_to_buy = cart_items.pop(buy_index)
                item_to_buy['purchase_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                collection.update_one(
                    {'Name': current_user},
                    {
                        '$push': {'product': item_to_buy},
                        '$set': {'cart': cart_items}
                    }
                )
                message = "Thank You for your purchase! Your order has been placed successfully."
            else:
                message = "Invalid item index."
        else:
            message = "No item selected to buy."

    user = collection.find_one({'Name': current_user})
    cart_items = user.get('cart', [])
    total = sum(int(item['discounted_price']) * int(item['quantity']) for item in cart_items)

    return render(request, 'addtocart.html', {
        'cart_items': cart_items,
        'total': total,
        'message': message
    })

def purchased_products(request):
    global current_user
    if not current_user:
        return render(request, 'signin.html', {'error': 'Please login first'})

    user = collection.find_one({'Name': current_user})
    purchased_items = user.get('product', [])

    return render(request, 'purchased.html', {
        'purchased_items': purchased_items
    })

def aboutpage(request):
    return render(request, 'about.html')

def contactpage(request):
    global current_user
    if request.method == 'POST' and request.POST.get('contactus') == 'submit':
        if not current_user:
            return render(request, 'signin.html', {'error': 'Please login first'})

        contactdetails = {
            'name': request.POST.get('name'),
            'mail': request.POST.get('email'),
            'subject': request.POST.get('subject'),
            'message': request.POST.get('message')
        }

        collection.update_one(
            {'Name': current_user},
            {'$push': {'contact': contactdetails}}
        )
        print("Form submitted successfully")
        return render(request, 'contact.html', {'message': 'Your contact details have been successfully added! Stay in touch!'})
    return render(request, 'contact.html')

