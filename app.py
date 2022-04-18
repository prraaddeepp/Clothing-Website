import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from men_clothes_library import gents
from women_clothes_library import women_clothes
import secrets
from bson.objectid import ObjectId


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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/add_cart/<clothID>')
def add_cart(clothID):
    collection1=mongo.db.Men
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    collection2=mongo.db.cart 
    collection2.insert_one(clothes)
    cart_clothes=collection2.find({})
    return render_template('cart.html',clothes=cart_clothes)

@app.route('/view_details/<clothID>')
def view_details(clothID):
    collection1=mongo.db.Men
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    return render_template('clothes.html', cloth=clothes)

@app.route('/women')
def women():
    collection = mongo.db.Women
    # collection.insert_many(women_clothes)
    clothes = collection.find({})
    return render_template('women.html', clothes=clothes)

@app.route('/view_details_w/<clothID>')
def view_details_w(clothID):
    collection1=mongo.db.Women
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    return render_template('clothes.html', cloth=clothes)

    

