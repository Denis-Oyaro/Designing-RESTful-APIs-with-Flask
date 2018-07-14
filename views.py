from findARestaurant import findARestaurant
from restaurant_models import Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)



engine = create_engine('sqlite:///restaruants.db')

DBSession = sessionmaker(bind=engine)
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        return getAllRestaurants()
    else:
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        return makeARestaurant(location, mealType)
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return getARestaurant(id)
    elif request.method == 'PUT':
        name = request.args.get('name', '')
        address = request.args.get('address', '')
        image = request.args.get('image', '')
        return updateRestaurant(name, address, image, id)
    else:
        return deleteRestaurant(id)


def getAllRestaurants():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants = [i.serialize for i in restaurants])
    
def makeARestaurant(location, mealType):
    session = DBSession()
    restaurant_info = findARestaurant(mealType, location)
    restaurant = Restaurant(restaurant_name = restaurant_info['name'], restaurant_address = restaurant_info['address'], restaurant_image = restaurant_info['image'])
    session.add(restaurant)
    session.commit()
    return jsonify(restaurant = restaurant.serialize)
    
def getARestaurant(id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    return jsonify(restaurant = restaurant.serialize)
    
def updateRestaurant(name, address, image, id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    if name:
        restaurant.restaurant_name = name
    if address:
        restaurant.restaurant_address = address
    if image:
        restaurant.restaurant_image = image
    session.add(restaurant)
    session.commit()
    return jsonify(restaurant = restaurant.serialize)
    
def deleteRestaurant(id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.delete(restaurant)
    session.commit()
    return "Deleted restaurant with id {}".format(id)
 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
