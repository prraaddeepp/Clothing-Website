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

def credit_card_check(num):
        validlist=[]
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
            return True
        return False