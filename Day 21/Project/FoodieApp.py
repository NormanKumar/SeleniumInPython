from flask import Flask,request,jsonify

app = Flask(__name__)

restaurants = []
dishes = []
feedbacks = []    
orders = []
users = [] 
             
@app.route('/api/v1/restaurants',methods=['POST'])
def registerRestaurant():
    data = request.json
    newdata = {"rid": len(restaurants) + 1000,
               "name":data.get("name"),
               "category":data.get("category"),
               "location":data.get("location"),
               "image":data.get("image"),
               "contact":data.get("contact"),
               "dishes": [],
               "feedback":[],
               "rating":0,
               "orders":[],
               "approved":False,
               "disabled":False
               }
    for restaurant in restaurants:
        if restaurant['name'].upper() == newdata['name'].upper() and restaurant['location'].upper() == newdata['location'].upper():
            return {"message":"Restaurant Already Exist"},409          
    restaurants.append(newdata)
    return jsonify(newdata),201

@app.route('/api/v1/restaurants/<int:rid>',methods=['PUT'])
def updateRestaurant(rid):
    for restaurant in restaurants:
        if rid == restaurant['rid']:
            restaurant.update(request.json)
            return jsonify({
                "message": "Updated restaurant",
                "data": restaurant
            }), 200
    return {"message":"Restaurant Not Found"},404

@app.route('/api/v1/restaurants/<int:rid>/disable',methods=['PUT'])
def disableRestaurant(rid):
    data = request.json
    for restaurant in restaurants:
         if restaurant["rid"] == rid:
            restaurant["disabled"] = data.get("disabled")  
            if restaurant["disabled"] == True:
                return jsonify({
                    "message": "Restaurant disabled",
                    "data": restaurant
                }), 200
            else:
                return jsonify({
                    "message":"Restaurant abled",
                    "data":restaurant
                }),200                
    return {"message":"Restaurant Not Found"},404 

@app.route('/api/v1/restaurants/<int:rid>',methods=['GET'])
def viewProfileRestaurant(rid):
    for restaurant in restaurants:
        if rid == restaurant['rid']:
            return jsonify(restaurant),200
    return {"message":"Restaurant Not Found"},404

@app.route('/api/v1/restaurants',methods=['GET'])
def allRestaurants():
    return jsonify(restaurants),200

@app.route('/api/v1/restaurants/<int:rid>/delete',methods=['DELETE'])
def deleteRestaurant(rid):
    for restaurant in restaurants:
        if restaurant['rid'] == rid:
            restaurants.remove(restaurant)
            return {"message":"Restaurant Removed"},200
    return {"message":"Restaurant Not Found"},404



@app.route('/api/v1/restaurants/<int:rid>/dishes',methods=['POST'])
def addingDishToRestaurant(rid):
    data = request.json
    for restaurant in restaurants:
        if rid == restaurant['rid']:
            newdata = {"rid": rid,
                       "did":len(dishes)+2000,
                       "name":data.get('name'),
                       "type":data.get('type'),
                       "price":data.get('price'),
                       "time":data.get('time'),
                       "image":data.get('image'),
                       "disabled":False
                    }
            break
    else:
        return {"message": "Restaurant Not Found"}, 404
    for dish in dishes:
        if newdata['name'].lower() == dish['name'].lower() and newdata['rid'] == dish['rid']:
            return {'message':"Dish Already Exist"},409
    dishes.append(newdata)
    restaurant['dishes'].append(newdata)
    return jsonify(newdata),201

@app.route('/api/v1/dishes/<int:did>',methods=['PUT'])
def updateDish(did):
    for dish in dishes:
        if did == dish['did']:
            dish.update(request.json)
            return jsonify({
                "message": "Updated dish",
                "data": dish
                }), 200
    return {"message":"Dish Not Found"},404

@app.route('/api/v1/dishes/<int:did>/status',methods=['PATCH'])
def statusDish(did):
    data = request.json
    for dish in dishes:
        if did == dish['did']:
            dish['disabled'] = data.get('disabled')
            if dish['disabled'] == True:
                return jsonify({
                    "message": "Dish disabled",
                    "data": dish
                }), 200
            else:
                return jsonify({
                    "message": "Dish abled",
                    "data": dish
                }),200
    return {"message":"Dish Not Found"},404 

@app.route('/api/v1/dishes/<int:did>/delete',methods=['DELETE'])
def deleteDish(did):
    for dish in dishes:
        if dish['did'] == did:
            dishes.remove(dish)
            return {"message":"Dish Removed"},200
    return {"message":"Dish Not Found"},404

@app.route('/api/v1/dishes',methods=['GET'])
def allDishes():
    return jsonify(dishes),200



@app.route("/api/v1/admin/restaurants/<int:rid>/approve",methods=['PATCH'])
def approveRestaurant(rid):
    data = request.json
    for restaurant in restaurants:
        if restaurant['rid'] == rid:
            restaurant['approved'] = data.get('approved')
            if restaurant['approved'] == True:
                return jsonify({
                    "message":"Restaurant Approved",
                    "data":restaurant
                }),200
            else:
                return jsonify({
                    "message":"Restaurant Not Approved",
                    "data":restaurant
                }),200
    return {"message":"Restaurant Not Found"},404

@app.route("/api/v1/admin/restaurants/<int:rid>/disable",methods=['PATCH'])
def statusRestaurant(rid):
    data = request.json
    for restaurant in restaurants:
        if restaurant['rid'] == rid:
            restaurant['disabled'] = data.get('disabled')
            if restaurant['disabled'] == True:
                return jsonify({
                    "message":"Restaurant Disabled",
                    "data":restaurant
                }),200
            else:
                return jsonify({
                    "message":"Restaurant Abled",
                    "data":restaurant
                }),200
    return {"message":"Restaurant Not Found"},404

@app.route('/api/v1/admin/feedback',methods=['GET'])
def getFeedbacks():
    return jsonify(feedbacks),200

@app.route('/api/v1/admin/orders',methods=['GET'])
def getorders():
    return jsonify(orders),200

@app.route('/api/v1/users/register',methods=['POST'])
def registerUsers():
    data = request.json
    newdata = {"uid":len(users)+3000,
               "name":data.get('name'),
               "email":data.get('email'),
               'password':data.get('password'),
               'orders':[]
            }    
    for user in users:
        if user['email'].upper() == newdata["email"].upper():
            return{"message":"User Already Exists"},409
    users.append(newdata)
    return jsonify(newdata),201
          
@app.route('/api/v1/restaurants/search',methods=['GET'])
def searchRestaurant():
    name = request.args.get('name')
    location = request.args.get('location')
    dish_name = request.args.get('dish')
    rating = request.args.get('rating')
    results = []
    found_location = False
    found_name = False
    found_dish = False
    found_rating = False
    for restaurant in restaurants:
        if restaurant['disabled'] or not restaurant['approved']:
            continue
        if location and restaurant['location'].lower() == location.lower():
            found_location = True
        if name and restaurant['name'].lower() == name.lower():
            found_name = True
        match = True
        if name and name.lower() not in restaurant['name'].lower():
            match = False
        if location and location.lower() != restaurant['location'].lower():
            match = False
        if dish_name:
            has_dish = False
            for dish in dishes:
                if dish['rid'] == restaurant['rid'] and dish_name.lower() in dish['name'].lower():
                    has_dish = True
                    found_dish = True
                    break
            if not has_dish:
                match = False
        if rating:
            if restaurant.get('rating', 0) >= float(rating):
                found_rating = True
            else:
                match = False
        if match:
            results.append(restaurant)
    if not results:
        if location and not found_location:
            return {"message": "Location unserviceable"}, 404
        if name and not found_name:
            return {"message": "Restaurant not found"}, 404
        if dish_name and not found_dish:
            return {"message": "No dish found in this restaurant/location"}, 404
        if rating and not found_rating:
            return {"message": "No restaurant in rating range"}, 404
        return {"message": "No restaurants found"}, 404
    return jsonify(results), 200
        
@app.route('/api/v1/orders', methods=['POST'])
def orderFood():
    data = request.json
    uid = data.get('uid')
    rid = data.get('rid')
    dishordered = data.get('dishes')
    if not uid or not rid or not dishordered:
        return {"message": "Add at least one dish"}, 400
    for user in users:
        if user['uid'] == uid:
            break
    else:
        return {"message": "User not found"}, 404
    for restaurant in restaurants:
        if restaurant['rid'] == rid:
            break
    else:
        return {"message": "Restaurant not found"}, 404
    if restaurant['disabled'] or not restaurant['approved']:
        return {"message": "Restaurant not available"}, 400
    total_price = 0
    valid_dishes = []
    for dish_name in dishordered:
        dish_found = False
        for dish in dishes:
            if dish['rid'] == rid and dish['name'].lower() == dish_name.lower() and not dish['disabled']:
                total_price += dish['price']
                valid_dishes.append(dish['name'])
                dish_found = True
                break
        if not dish_found:
            return {
                "message": f"Dish '{dish_name}' is not available in this restaurant. Choose correctly."
            }, 400
    new_order = {
        "oid": len(orders) + 4000,
        "uid": uid,
        "rid": rid,
        "dishes": valid_dishes,
        "total": total_price,
        "status": "Placed"
    }
    orders.append(new_order)
    user['orders'].append(new_order)
    restaurant['orders'].append(new_order)
    return jsonify({
        "message": "Order placed successfully",
        "data": new_order
    }), 201

@app.route('/api/v1/ratings', methods=['POST'])
def ratingFood():
    data = request.json
    oid = data.get('oid')
    rating_value = data.get('rating')
    feedback = data.get('feedback')
    for order in orders:
        if order['oid'] == oid:
            rid = order['rid']
            for restaurant in restaurants:
                if restaurant['rid'] == rid:
                    restaurant['feedback'].append({
                        "rating": rating_value,
                        "comment": feedback
                    })
                    feedbacks.append({
                        "rid": rid,
                        "rating": rating_value,
                        "comment": feedback
                    })
                    ratings = [f['rating'] for f in restaurant['feedback']]
                    restaurant['rating'] = sum(ratings) / len(ratings)
                    return jsonify({
                        "message": "Feedback added",
                        "rating": restaurant['rating']
                    }), 201
    return {"message": "Order not found"}, 404

@app.route('/api/v1/<int:uid>/update',methods=['PUT'])
def updateUser(uid):
    for user in users:
        if user['uid'] == uid:
            user.update(request.json)
            return jsonify({
                "message":"User Profile Updated",
                "data":user
            }),200
    return {"message":"User Not Found"},404

@app.route('/api/v1/<int:uid>/delete',methods=['DELETE'])
def deleteUser(uid):
    for user in users:
        if user['uid'] == uid:
            users.remove(user)
            return {"message":"User Profile Deleted"},200
    return {"message":"User Not Found"},404        


     
@app.route('/api/v1/users/<int:uid>/orders', methods=['GET'])
def viewOrdersByUser(uid):
    for user in users:
        if user['uid'] == uid:
            if not user['orders']:      
                return {"message": "No Orders Yet"}, 200
            return jsonify(user['orders']), 200
    return {"message": "User Not Found"}, 404

@app.route('/api/v1/restaurants/<int:rid>/orders', methods=['GET'])
def viewOrdersByRestaurant(rid):
    for restaurant in restaurants:
        if restaurant['rid'] == rid:
            if not restaurant['orders']:
                return {"message": "No Orders Yet"}, 200
            return jsonify(restaurant['orders']), 200
    return {"message": "Restaurant Not Found"}, 404



@app.route('/test/reset', methods=['POST'])
def reset_data():
    restaurants.clear()
    dishes.clear()
    users.clear()
    orders.clear()
    feedbacks.clear()  
    return {"message": "reset done"}, 200


            
if __name__ == '__main__':
    app.run(debug=True)            