#first load image LUT
def parse(path):
  g = open(path, 'r')
  for l in g:
    yield eval(l)
    
import json


#input is path to metadata file
def build_image_lut(path):
  images={}

  i=0
  j=0
  for l in parse(path):
    try:
      i+=1
      image_url = l['imUrl']
      asin = l['asin']
      images[asin]=image_url
    except KeyError:
      j+=1
  return images
    
# takes about 16 min to go through 10G of data
print "starting LUT build..."
path ="/Users/alexegg/Development/dse/capstone/data/metadata.json"
image_lut=build_image_lut(path)
print "Finished LUT build..."

#read clothing data from simple_out csv or some file and load into PG
import csv
import psycopg2
connection="postgresql://postgres@localhost/sharknado-web"
conn = psycopg2.connect(connection)
cursor = conn.cursor()

items={}

path = "/Users/alexegg/Development/dse/capstone/UpsDowns/simple_out"
with open(path, 'rb') as reviews_file:
  reader = csv.reader(reviews_file, delimiter=' ')
  for row in reader:
    asin = row[1]
    image_url = image_lut[asin]
    if asin in items:
      continue
    else:
      items[asin]=True
      
    query =  "INSERT INTO items (asin, image_url) VALUES (%s, %s);"
    data = (asin, image_url)
    cursor.execute(query, data)
    
    
conn.commit()
cursor.close()
conn.close()


