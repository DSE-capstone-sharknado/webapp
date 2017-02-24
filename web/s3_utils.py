import numpy as np

class S3Utils(object):
  def __init__(self):
    super(S3Utils, self).__init__()
  
  #should get file_name from database of models
  #class method
  @classmethod
  def fetch_model_params(cls, s3_fn):
    #s3.get(s3_fn) #store in cache on disk parse
    #hack, just load this from disk for now!
    fn="tmp/%s"%s3_fn
    coeffs = np.load(fn)
    item_bias = coeffs['item_bias']
    user_factors = coeffs['user_factors']
    item_factors = coeffs['item_factors']
    
    return item_bias, user_factors, item_factors