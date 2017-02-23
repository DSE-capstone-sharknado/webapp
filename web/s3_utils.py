import numpy as np

class S3Utils(object):
  def __init__(self):
    super(S3Utils, self).__init__()
  
  #should get file_name from database of models
  #class method
  def fetch_model_params(s3_fn):
    #s3.get(s3_fn) #store in cache on disk parse
    fn="bpr-breg0.50-ureg0.50-lr0.20-k10-epochs10.npz"
    coeffs = np.load(fn)
    item_bias = coeffs['item_bias']
    user_factors = coeffs['user_factors']
    item_factors = coeffs['item_factors']
    
    return item_bias, user_factors, item_factors