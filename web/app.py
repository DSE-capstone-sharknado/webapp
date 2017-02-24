from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from models import User
import os
import rec_sys
import s3_utils
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(12))

    def __init__(self, aid):
        self.aid = aid

    def __repr__(self):
        return '<aid %r>' % self.aid

class ModelParamsSet(db.Model):
    __tablename__ = "model_params_sets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))

    def __init__(self, asin):
        self.asin = asin

    def __repr__(self):
        return '<E-mail %r>' % self.asin
        
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(12))
    image_url = db.Column(db.String(255))

    def __init__(self, asin):
        self.asin = asin

    def __repr__(self):
        return '<asin %r>' % self.asin


def connect_db():
  """Connects to the specific database."""
  pass


def get_db():
  """Opens a new database connection if there is none yet for the
  current application context.
  """
  pass


  
  
@app.route('/')
def hello_world():
    return render_template('index.html.haml')
    
@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/users/')
def get_users():
  return "get_users"

@app.route('/users/<int:uid>/')    
def get_user():
  return "get_user"

@app.route('/users/<int:u>/rankings')
def get_rankings(u):
  
  model_config_id = request.args.get('model_id', '')
  model_config = ModelParamsSet.query.get(model_config_id)
  params_url = model_config.url
  item_bias, user_factors, item_factors = s3_utils.S3Utils.fetch_model_params(params_url)
  
  recsys = rec_sys.RecSys.factory(item_bias, user_factors, item_factors )
  
  #run the ranking for this user acorss all products are return the top 10?
  #get all items
  items = Item.query.all()

   
  rankings=[]
  for i in items:
    rank = recsys.rank(u, i.id)
    rankings.append({'rank': rank, 'asin': i.asin, 'image_url': i.image_url})
    
  #sort and get top-ten
  # rankings = sorted(rankings, key=rankings.get, reverse=True)
  # top_ten = rankings
  
  return jsonify(rankings)
  
  
# Save new model
@app.route('/models', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')
  
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)