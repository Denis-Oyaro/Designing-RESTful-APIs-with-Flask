from bagels_models import User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine 


engine = create_engine('sqlite:///bagelShop.db')

DBSession = sessionmaker(bind=engine)
app = Flask(__name__)


@app.route('/users', methods = ['POST'])
def registerUser():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify(error = "please provide a username and password"), 400
    session = DBSession()
    if list(session.query(User).filter_by(username = username)):
        return jsonify(message = "{} already exists".format(username)), 200
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(username = user.username), 201
    



@app.route('/bagels', methods = ['GET','POST'])
def showAllBagels():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        if not verify_password(username, password):
            return "Access denied", 401
        session = DBSession()
        bagels = session.query(Bagel).all()
        return jsonify(bagels = [bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if not verify_password(username, password):
            return "Access denied", 401
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = Bagel(name = name, description = description, picture = picture, price = price)
        session = DBSession()
        session.add(newBagel)
        session.commit()
        return jsonify(newBagel.serialize)


def verify_password(username, password):
    if not username or not password:
        return False
     
    session = DBSession()
    users = session.query(User).filter_by(username = username)
    if not list(users):
        return False
    user = users.one()
    return user.verify_password(password)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
