import os
import time
from flask import render_template, request, redirect, session, flash
from ecommerce import app, db
import datetime
import json
from ecommerce.models import Product, Category, User
from ecommerce import bcrypt

# BdApps Config
APP_ID = 'APP_061652'
PASSWORD = "bf15849c24ff29c8b2f7ea13f609fb95"


@app.route('/')
def hello_world(welcome=None):
    return render_template("index.html", welcome=welcome)


# SMS Listener
@app.route('/api/products', methods=['GET', 'POST'])
def productApi():
    if request.method == 'POST':
        payload = request.json
        count = payload.get('count')
        page = payload.get('page')
        if count is not None and page is not None:
            payload = []
            products = Product.query.all()
            if count > len(products):
                count = len(products)
                page = 1
                totalPages = 1
            else:
                totalPages = int(len(products)/count)
                pagesLeft = int(totalPages/page)
                if pagesLeft == 0:
                    return json.dumps({
                        'status': 'error',
                        'description': 'Invalid parameters!'
                    })
            if page == 1: start = 0
            else: start = page-1*count
            for product_ in range(start, start+count):
                product_ = products[product_]
                cat = Category.query.filter_by(id=product_.category_id).first()
                payload.append({
                    'prod_name': product_.name,
                    'prod_img': product_.image,
                    'prod_color': product_.color,
                    'prod_price': product_.price,
                    'prod_stock': product_.stock,
                    'prod_manufacturer': product_.brandName,
                    'prod_size': product_.size,
                    'prod_description': product_.description,
                    'prod_category': {
                        'cat_name': cat.name,
                        'cat_id': cat.id,
                    }
                })

            actualPayload = [{
                'status': 'success',
                'payload': payload,
                'count': len(payload),
                'page': page,
                'totalPages': totalPages
            }]
            return json.dumps(actualPayload)

        return json.dumps({
            'status': 'error',
            'description': 'All parameters were not passed!.'
        })
    else:

        print(Product.query.all())
        return render_template("index.html", welcome="Product Page")


@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        print(Product.query.all())
        payload = request.json()
        return payload
    else:
        return render_template("store.html", welcome="Product Page")


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        print(Product.query.all())
        payload = request.json()
        return payload
    else:
        return render_template("about.html", welcome="Product Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Post request")
        username, password = request.form['username'], request.form['password']
        user = User.query.filter_by(name=username).first()
        if bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect('/admin')
        else:
            return render_template('login.html', welcome="Wrong Username or Password!")
    else:
        return render_template('login.html', welcome=None   )


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        print("Post request")
        print(request.form)
        return redirect('/admin')
    else:
        if 'username' in session:
            return render_template('admin.html', welcome=session['username'])
        return redirect('/login')


@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        print("Post request")
        productDict = request.form
        name = productDict['prod_name']
        price = productDict['prod_price']
        stock = productDict['prod_stock']
        brand = productDict['prod_manufacturer']
        size = productDict['prod_size']
        category = productDict['prod_category']
        color = productDict['prod_color']
        description = productDict['prod_description']
        image = request.files['prod_img']

        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if image and image.filename:
            filename = image.filename
            print(app.config['UPLOAD_FOLDER'])
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        singleProduct = Product()
        singleProduct.name = name
        singleProduct.price = price
        singleProduct.color = color
        singleProduct.stock = stock
        singleProduct.brandName = brand
        singleProduct.size = size
        singleProduct.category_id = category
        singleProduct.description = description
        singleProduct.image = image.filename
        db.session.add(singleProduct)
        db.session.commit()
        return redirect('/admin')
    else:
        if 'username' in session:
            return render_template('admin.html', welcome=session['username'])
        else:
            return redirect('/login')


# @app.route('/register', methods=['GET', 'POST'])
# def register():


# @app.route('/is_subscribed', methods=['GET', 'POST'])
# def check_sub():
#     if request.method == 'POST':
#         subscriber = SubscriptionManagement(APP_ID, PASSWORD)
#         address = 'tel:Nzk2ODgzYjM1YjZhMDFhNjJjYTI3ZDBmMzhjZGU0NDMzMWQ2YWQ0N2FlNjRiODE5ZTRjMTg3ZTIyNTM1ZGI3ZDpyb2Jp'
#         isSubbed = subscriber.isSubscribed(address)
#         if not isSubbed:
#             isSubb = subscriber.makeSubscriber(address)
#         return render_template("index.html", welcome=f"Made Subscriber: {request.json}")
#
#     subscriber = SubscriptionManagement(APP_ID, PASSWORD)
#     address = 'tel:' + request.args.get('tel')
#     isSubbed = subscriber.isSubscribed(address)
#
#     return render_template("index.html", welcome=f"The request is {address, isSubbed} HELLO WORLD")
#
#
# # USSD LISTENER
# @app.route('/ussd/ussd_listener', methods=['GET', 'POST'])
# def ussd_listener():
#     if request.method == "POST":
#         receiver = USSDReceiver(request.json)
#         sender = USSDSender(APP_ID, PASSWORD)
#         subscription = SubscriptionManagement(APP_ID, PASSWORD)
#
#         text = json.dumps(receiver.getPayload(), indent=4)
#
#         ussdOperation = receiver.getUssdOperation()
#         sessionId = receiver.getSessionId()
#         address = receiver.getSourceAddress()
#         message = receiver.getMessage()
#
#         responseMessage = 'To confirm send 1 in the next pop-up.'
#         value = False
#
#         if ussdOperation == 'mo-cont' and message == '1':
#             subscription.removeSubscriber(address)
#             sent = sender.sendUSSD('Sad to see you go!', sessionId, address, 'mt-fin')
#             if not sent:
#                 sender.sendUSSD('Some error occurred! Try again...', sessionId, address, 'mt-fin')
#             return
#
#         if subscription.isSubscribed(address):
#             responseMessage = 'Awesome! You are already subscribed.\n\n 1. Unsubscribe'
#             sent = sender.sendUSSD(responseMessage, sessionId, address)
#             if not sent:
#                 sender.sendUSSD('Some error occurred! Try again...', sessionId, address)
#
#         else:
#             sent = sender.sendUSSD(responseMessage, sessionId, address, 'mt-fin')
#             if not sent:
#                 sender.sendUSSD('Some error occurred! Try again...', sessionId, address, 'mt-fin')
#             else:
#                 value = subscription.makeSubscriber(address)
#
#         with open('ussd.txt', 'a', encoding='utf-8') as file:
#             file.write(f"sent: {sessionId, address, message, ussdOperation, sent} value:{value}\ntext: {text}")
#             file.close()
#
#         return f"sent: {sessionId, address, message, ussdOperation, sent} value:{value}\n"
#
#     return render_template('index.html', welcome="USSD Listener ")
#
#
# @app.route('/subscription/notification', methods=['GET', 'POST'])
# def subscription_notification_callback():
#     if request.method == "POST":
#         with open('subscribed.txt', 'a+', encoding='utf-8') as subscriber:
#             x = datetime.datetime.now()
#             text = json.dumps(request.json, indent=4)
#             print(text)
#             x = f'\n{str(x)} , {text}\n'
#             subscriber.write(x)
#             subscriber.close()
#         return render_template("index.html", welcome=f"subscription_notification_callback: {request.json}")
#     return render_template("index.html", welcome=f"subscription_notification_callback: Working")
