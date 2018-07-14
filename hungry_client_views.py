from flask import Flask, jsonify 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["25 per day"],
    storage_uri="redis://localhost:6379"
)


@app.route('/rate-limited')
@limiter.limit("100/30seconds", error_message = json.dumps({"data":"You hit the rate limit","error": 429}))
def index():
    return jsonify({'response':'This is a rate limited response'})
    
    
@app.route('/')
def index2():
    return jsonify({'response':'Are we rated limited?'})
    
@app.route('/unlimited')
@limiter.exempt
def index3():
    return jsonify({'response':'We are not rate limited'})

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)