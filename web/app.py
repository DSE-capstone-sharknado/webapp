from flask import Flask
app = Flask(__name__)
import model


def connect_db():
  """Connects to the specific database."""
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv


def get_db():
  """Opens a new database connection if there is none yet for the
  current application context.
  """
  if not hasattr(g, 'sqlite_db'):
      g.sqlite_db = connect_db()
  return g.sqlite_db

def get_model():
  model_id = request.args.get('model_id', '')
  if model_id is None:
    db = get_db()
    cur = db.execute('select id from models order by id desc limit 1')
    model_id = cur.fetch()
  return model.Model.factory(model_id)
  
  
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users/')
def get_users():
  pass

@app.route('/users/<id:uid>/')    
def get_user():
  pass

@app.route('/users/<id:uid>/rankings')
def get_rankings(uid):
  model = get_model()
  #run the ranking for this user acorss all products are return the top 10?
  #get all items
  db = get_db()
  cur = db.execute('select id from items')
  items = cur.fetchall() 
  rankings={}
  for i in items:
    rank = model.predict(uid, i)
    rankings.append(rank)
  #sort and get top-ten
  rankings = sorted(rankings, key=rankings.get, reverse=True)
  top_ten = rankings[0:10]
  return top_ten
  
  
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)