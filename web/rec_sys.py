import numpy as np


class RecSys(object):
  def __init__(self):
    super(RecSys, self).__init__()
    
    # self.item_bias = np.zeros(self.num_items)
    # self.user_factors = np.random.random_sample((self.num_users,self.D))
    # self.item_factors = np.random.random_sample((self.num_items,self.D))
  
  #class factory method
  #pulls model paremters from s3 and build model
  @staticmethod
  def factory(item_bias, user_factors, item_factors):
    model = RecSys()
    model.load(item_bias, user_factors, item_factors)
    return model
    
  
  def load(self, item_bias, user_factors, item_factors):
    self.item_bias = item_bias
    self.user_factors = user_factors
    self.item_factors = item_factors
    

  def rank(self,u,i):
    return self.item_bias[i] + np.dot(self.user_factors[u],self.item_factors[i])