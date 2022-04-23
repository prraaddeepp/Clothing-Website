import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from men_clothes_library import gents
from women_clothes_library import women_clothes
import secrets
from bson.objectid import ObjectId
from model import get_clothes,get_totals,add_to_cart_men,add_to_cart_women,remove_items_from_cart


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
        # user_current = contactdb.find_one({'username': request.form['firstname']})
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        message = request.form['subject']
        contactdb.insert_one({'firstname': firstname, 'lastname': lastname, 'email': username, 'message':message})
        session['username'] = request.form['firstname']
        return redirect('/contacts')
    else:
        return render_template('contacts.html')


def render_cart_template(mongo):
    cart_clothes= get_clothes(mongo)
    total,main_total= get_totals(mongo)
    return render_template('cart.html',clothes=cart_clothes,total=total,main_total=main_total)

@app.route('/add_cart/<clothID>')
def add_cart(clothID):
    add_to_cart_men(mongo,clothID)
    return render_cart_template(mongo)

@app.route('/add_cart_women/<clothID>')
def add_cart_women(clothID):
    add_to_cart_women(mongo,clothID)
    return render_cart_template(mongo)

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
        num = cardnumber                                     # this function adds every digit of the card number to a list and,
        validlist=[]
        credit_check = False
        num =  int(num)
        if type(num) != int:
            raise TypeError("The input must be a number")

        if num <= 0 or len(str(num)) > 16:
            raise ValueError("Number can't be negative and the length can't be greater than 16")         
        
        num =  str(num)
        #while not credit_check:
        for i in num:
            validlist.append(int(i))
        for i in range(0,len(num),2):                                             # applying Luhn Algorithm to check whether resulting sum is divisible by ten
            validlist[i] = validlist[i] * 2
            if validlist[i]  >= 10:
                validlist[i] =  (validlist[i]//10 + validlist[i]%10)
        
        if sum(validlist)% 10 == 0:
            credit_check = True
            print("This is a VALID CARD!")
            return render_template('successful_transaction.html')
        
        else:
            credit_check = False
            print('INVALID CARD NUMBER')
            return render_template('repeat_transaction.html')


    # return render_template('checkout.html')

    

