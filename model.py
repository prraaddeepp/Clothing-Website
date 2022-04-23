from flask_pymongo import PyMongo
from bson.objectid import ObjectId

def get_totals(mongo):
    cart_collection=mongo.db.cart
    total=sum(c['Price'] for c in cart_collection.find({}))
    main_total=total+(20/100*total)
    if type(total) not in [int,float]:
        raise TypeError("The total price must be a number")
    if type(total) not in  [int,float]:
        raise TypeError("The total money to pay must be a number.")
    if total < 0 or main_total<0:
            raise ValueError("The price to pay can't be negative.")  

    return [total,main_total]

def get_clothes(mongo):
    cart_collection=mongo.db.cart
    cart_clothes=cart_collection.find({})
    return cart_clothes

def add_to_cart_men(mongo,clothID):
    collection1=mongo.db.Men
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    collection2=mongo.db.cart
    collection2.insert_one(clothes)

def add_to_cart_women(mongo,clothID):
    collection1=mongo.db.Women
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    collection2=mongo.db.cart
    collection2.insert_one(clothes)

def remove_items_from_cart(mongo,clothID):
    collection2=mongo.db.cart
    cloth_to_remove=collection2.find_one({'_id':ObjectId(clothID)})
    collection2.delete_one(cloth_to_remove)