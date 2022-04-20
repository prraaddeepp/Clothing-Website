from flask_pymongo import PyMongo

def get_totals(mongo):
    cart_collection=mongo.db.cart
    total=sum(c['Price'] for c in cart_collection.find({}))
    main_total=total+(20/100*total)
    return [total,main_total]

def get_clothes(mongo):
    cart_collection=mongo.db.cart
    cart_clothes=cart_collection.find({})
    return cart_clothes

'''def add_to_cart_men(mongo,clothID):
    collection1=mongo.db.Men
    clothes=collection1.find_one({'_id':ObjectId(clothID)})
    collection2=mongo.db.cart
    collection2.insert_one(clothes)'''