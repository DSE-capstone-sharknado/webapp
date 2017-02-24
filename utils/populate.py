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
    if asin in items:
      continue
    else:
      items[asin]=True
      
    query =  "INSERT INTO items (asin, image_url) VALUES (%s, %s);"
    data = (asin, "...")
    cursor.execute(query, data)
    
    
conn.commit()
cursor.close()
conn.close()


