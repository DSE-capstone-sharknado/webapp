import numpy as np
import s3_utils

class Model(object):
  def __init__(self):
    super(Model, self).__init__()
    
    self.item_bias = np.zeros(self.num_items)
    self.user_factors = np.random.random_sample((self.num_users,self.D))
    self.item_factors = np.random.random_sample((self.num_items,self.D))
  
  #class factory method
  #pulls model paremters from s3 and build model
  def factory(model_id):
    #check DB for s3 fn
    fn=""
    item_bias, user_factors, item_factors = se_utils.fetch_model_params(fn)
    model = Model()
    model.load(item_bias, user_factors, item_factors)
    return model
    
  
  def load(self, item_bias, user_factors, item_factors):
    self.item_bias = item_bias
    self.user_factors = user_factors
    self.item_factors = item_factors
    

  def predict(self,u,i):
    return self.item_bias[i] + np.dot(self.user_factors[u],self.item_factors[i])