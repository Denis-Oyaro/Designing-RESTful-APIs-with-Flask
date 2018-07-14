from Regal_tree_foods_models import  User, Product
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///regalTree.db')

DBSession = sessionmaker(bind=engine)
app = Flask(__name__)



def verify_password(username, password):
    if not username or not password:
        return False
     
    session = DBSession()
    users = session.query(User).filter_by(username = username)
    if not list(users):
        return False
    user = users.one()
    return user.verify_password(password)

#add /token route here to get a token for a user with login credentials
@app.route('/token')
def get_token():
    username = request.args.get('username')
    password = request.args.get('password')
    if not verify_password(username, password):
        return jsonify(error = 'Unauthorized access'), 401
        
    session = DBSession()
    user = session.query(User).filter_by(username = username).one()
    token = user.generate_auth_token()
    return jsonify(token = token)
    
    

@app.route('/users', methods = ['POST'])
def new_user():
    session = DBSession()
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify(error = "missing arguments"), 400
        
    if list(session.query(User).filter_by(username = username)):
        print "existing user"
        return jsonify(message = 'user already exists'), 200
    
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(username = user.username), 201

@app.route('/users/<int:id>')
def get_user(id):
    session = DBSession()
    users = session.query(User).filter_by(id=id)
    if not list(users):
        abort(400)
    user = users.one()
    return jsonify(username =  user.username)

@app.route('/resource')
def get_resource():
    username_or_token = request.args.get('username_or_token')
    password = request.args.get('password')
    serveResource = False
    if verify_password(username_or_token, password):
        username = username_or_token
        serveResource = True
    else:
        user_id = User.verify_auth_token(username_or_token)
        if user_id:
            session = DBSession()
            user = session.query(User).filter_by(id = user_id).one()
            username = user.username
            serveResource = True
            
    if not serveResource:
        return jsonify(error = 'Unauthorized access'), 401
    return jsonify({ 'data': 'Hello, %s!' % username })

@app.route('/products', methods = ['GET', 'POST'])
def showAllProducts():
    username_or_token = request.args.get('username_or_token')
    password = request.args.get('password')
    if not (verify_password(username_or_token, password) or User.verify_auth_token(username_or_token)):
        return jsonify(error = 'Unauthorized access'), 400
 
    session = DBSession()
    if request.method == 'GET':
        products = session.query(Product).all()
        return jsonify(products = [p.serialize for p in products])
    if request.method == 'POST':
        name = request.json.get('name')
        category = request.json.get('category')
        price = request.json.get('price')
        newItem = Product(name = name, category = category, price = price)
        session.add(newItem)
        session.commit()
        return jsonify(newItem.serialize)



@app.route('/products/<category>')
def showCategoriedProducts(category):
    username_or_token = request.args.get('username_or_token')
    password = request.args.get('password')
    if not (verify_password(username_or_token, password) or User.verify_auth_token(username_or_token)):
        return jsonify(error = 'Unauthorized access'), 400
        
    session = DBSession()
    if category == 'fruit':
        fruit_items = session.query(Product).filter_by(category = 'fruit').all()
        return jsonify(fruit_products = [f.serialize for f in fruit_items])
    if category == 'legumes':
        legume_items = session.query(Product).filter_by(category = 'legumes').all()
        return jsonify(legume_products = [l.serialize for l in legume_items])
    if category == 'vegetables':
        vegetable_items = session.query(Product).filter_by(category = 'vegetables').all()
        return jsonify(produce_products = [p.serialize for p in vegetable_items])
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
