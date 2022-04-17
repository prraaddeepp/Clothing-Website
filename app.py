import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from men_clothes_library import gents
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

@app.route('/add_cart/<clothid>')
def AddCart(clothid):
    
        collection=mongo.db.Men
        clothes=collection.find_one({'_id':ObjectId(clothid)})
        collection2=mongo.db.cart
        collection2.insert_one(clothes)
        cart_clothes=collection2.find({})
        return render_template('cart.html',clothes=cart_clothes)