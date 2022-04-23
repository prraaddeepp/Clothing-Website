import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from men_clothes_library import gents
from women_clothes_library import women_clothes
import secrets
from bson.objectid import ObjectId
from model import get_clothes,get_totals,add_to_cart_men,add_to_cart_women,remove_items_from_cart,credit_card_check


# # -- Initialization section --
app = Flask(__name__)

# # name of database
app.config['MONGO_DBNAME'] = 'database'

# # URI of database
# # Accessed from CONFIG VARS
secret_key = os.environ.get('MONGO_URI')
app.config['MONGO_URI'] = "mongodb+srv://admin:iamCool100!@cluster0.dhqv0.mongodb.net/Final_Project?retryWrites=true&w=majority"

# #Initialize PyMongo
mongo = PyMongo(app)
app.secret_key = secrets.token_urlsafe(16)

@app.route('/')
#INDEX Route
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return  render_cart_template(mongo)    



@app.route('/men')
def men():
    collection = mongo.db.Men
    # collection.insert_many(gents)
    clothes = collection.find({})
    return render_template('men.html', clothes=clothes)

@app.route('/contacts', methods = ['GET','POST'])
def contacts():
    if request.method == "POST":
        contactdb = mongo.db.contactdb
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        message = request.form['subject']
        contactdb.insert_one({'firstname': firstname, 'lastname': lastname, 'email': username, 'message':message})
        return redirect('/contacts')
    else:
        return render_template('contacts.html')


def render_cart_template(mongo):
    cart_clothes= get_clothes(mongo)
    total,main_total= get_totals(mongo)
    return render_template('cart.html',clothes=cart_clothes,total=total,main_total=main_total)

@app.route('/add_cart/<clothID>')
def add_cart(clothID):
    if session:
        add_to_cart_men(mongo,clothID)
        return render_cart_template(mongo)
    else:
        return redirect('/login')

        

@app.route('/add_cart_women/<clothID>')
def add_cart_women(clothID):
    if session:
        add_to_cart_women(mongo,clothID)
        return render_cart_template(mongo)
    else:
        return redirect('/login')

@app.route('/Remove/<clothID>')
def remove_items(clothID):
    remove_items_from_cart(mongo,clothID)
    return render_cart_template(mongo)


@app.route('/view_details/<clothID>')
def view_details(clothID):
    collection1=mongo.db.Men
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    return render_template('clothes.html', cloth=clothes, men_cloth= clothes)

@app.route('/women')
def women():
    collection = mongo.db.Women
    # collection.insert_many(women_clothes)
    clothes = collection.find({})
    return render_template('women.html', clothes=clothes)

@app.route('/view_details_women/<clothID>')
def view_details_women(clothID):
    collection2=mongo.db.Women
    clothes=collection2.find_one({'_id':ObjectId(clothID)})
    return render_template('clothes.html', cloth=clothes, women_cloth= clothes)

@app.route('/Checkout', methods = ['GET','POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    elif request.method == 'POST':
        cardnumber = request.form['cardnumber']
        num = cardnumber  
        
        if credit_card_check(num)==True:                                   # this function adds every digit of the card number to a list and,
            print("This is a VALID CARD!")
            customer_collection = {}
            cart = mongo.db.cart
            clothes = cart.find({})
            for cloth in clothes:
                customer_collection.update(cloth)
            user = mongo.db.Users
            email = request.form['email']
            current_user = user.find_one({'email':email})
            customer_collection.update(current_user)
            customer= mongo.db.customer
            customer.insert_one(customer_collection)
            return render_template('successful_transaction.html')
        
        else:
            credit_check = False
            print('INVALID CARD NUMBER')
            return render_template('repeat_transaction.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        users = mongo.db.Users
        #search for username in database
        login_user = users.find_one({'email': request.form['email']})

        #if username in database
        if login_user:
            db_password = login_user['password']
            #encode password
            password = request.form['password'].encode("utf-8")
            #compare password in database to password submitted in form
            if password == db_password:
                session['username'] = login_user['firstname']
                session['email'] = login_user['email']
                return render_template('index.html')
            else:
                return render_template('login.html', error1 = 'Invalid username or password combination.')
        else:
            return render_template('login.html', error2 = 'User not found!')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method == "POST":
        users = mongo.db.Users
        #search for username in database
        current_user = users.find_one({'email': request.form['email']})

        #if user not in database
        if not current_user:
            email = request.form['email']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            gender = request.form['gender']
            nation = request.form['nation']
            state = request.form['state']
            zipcode = request.form['zip']
            #encode password for hashing
            password = (request.form['password']).encode("utf-8")
            
            if email[len(email)-10:] != "@gmail.com":
                raise TypeError("Username should have valid domain @gmail.com")
            if firstname.isdigit():
                raise TypeError("First name should be string!")
            if lastname.isdigit():
                raise TypeError("Last name should be string!")
            if gender.isdigit():
                raise TypeError("Gender should be string!")
            if nation.isdigit():
                raise TypeError("Nation should be string!")            
            #add new user to database
            users.insert_one({'firstname':firstname, 'lastname':lastname, 'email': email, 'password': password, 'gender': gender, 'nation': nation, 'state':state, 'zip':zipcode})
            #store username in session
            session['username'] = request.form['firstname']
            return render_template('index.html')

        else:
            return render_template('signup.html', registration= 'User already exists!' )
            
    
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    #clear username from session data
    session.clear()
    return redirect('/')

    

