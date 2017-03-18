from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template

import sys
# from models import User
import os
import rec_sys
import s3_utils
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

reviews = db.Table('reviews',
    db.Column('asin', db.String, db.ForeignKey('items.asin')),
    db.Column('aid', db.String, db.ForeignKey('users.aid'))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(30), unique=True)
    reviews = db.relationship('Item', secondary=reviews,
            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, aid):
        self.aid = aid

    def __repr__(self):
        return '<aid %r>' % self.aid

class ModelParamsSet(db.Model):
    __tablename__ = "model_params_sets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    gen = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name
        
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(12), unique=True)
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
    
# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

@app.route('/users/')
def get_users():
  return "get_users"

@app.route('/api/users/<int:u>/')    
def get_user(u):
  user = User.query.get(u)
  items = user.reviews
  result=[]
  for item in items:
    result.append({'asin': item.asin, 'image_url': item.image_url})
  return jsonify(result)


def top_n_rankings(u, n, model_config):
  
  item_bias, user_factors, item_factors = s3_utils.S3Utils.fetch_model_params(model_config)

  recsys = rec_sys.RecSys.factory(item_bias, user_factors, item_factors )

  items = Item.query.limit(Item.query.count()-1)
 
  rankings=[]
  for item in items:
    # i=asin_lut[item.id]
    i=item.id #temp hack until i add the LUT
    rank = recsys.rank(u, i)
    rankings.append({'rank': rank, 'asin': item.asin, 'image_url': item.image_url})
  
  #sort and get top-ten
  rankings = sorted(rankings, key=lambda r: r['rank'], reverse=True)
  rankings = rankings[0:n]
  return rankings

@app.route('/api/users/<int:u>/rankings')
def api_get_rankings(u):
  user = User.query.get(u)
  user_items = user.reviews
  rankings = top_n_rankings(u, 20)
  
  return jsonify(rankings)
  
@app.route('/users/<int:u>/rankings')
def get_rankings(u):
  user = User.query.get(u)
  user_items = user.reviews
  model_config_id = request.args.get('model_id', '')
  model_config = ModelParamsSet.query.get(model_config_id)
  
  rankings = top_n_rankings(u, 20, model_config)

  
  return render_template("rankings.html", user=user, rankings=rankings, user_items=user_items, model_config=model_config)
  
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
  
@app.route('/tsne')
def tsne():
  return render_template('tsne.html')
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)