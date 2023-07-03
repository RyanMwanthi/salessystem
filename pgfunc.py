import psycopg2




try:
  conn=psycopg2.connect("dbname=duka user=postgres password=12345")

  cur = conn.cursor()
except Exception as e:
  print(e)  


def fetch_data(tbname):
  try:
    q="SELECT * FROM " + tbname + ";"
    cur.execute(q)
    records=cur.fetchall()
    return records
  except Exception as e:
    return e

def insert_products(v):
    vs=str(v)
    q="INSERT INTO products(name,buying_price,selling_price,stock_quantity)" "values" + vs
    cur.execute(q)
    conn.commit()
    return(q)

def insert_sales(v):
  vs=str(v)
  q="INSERT INTO sales(pid,quantity,created_at)" "values" +vs  #return created at if it fails
  cur.execute(q)
  conn.commit()
  return(q)



#sales products = spquery

def sales_per_product():
  spquery="SELECT * FROM sales_per_product"
  cur.execute(spquery)
  qu=cur.fetchall()
  
  return(qu)

def sales_per_day():
  spdayquery="SELECT * FROM sales_per_day"
  cur.execute(spdayquery)
  sp=cur.fetchall()
  print(sp)
  return(sp)

#adding users using register form
def add_user(v):
  vs=str(v)
  add="INSERT INTO users (full_name,email,password,created_at)" "values" +vs
  cur.execute(add)
  conn.commit()
  return(add)
  











    
  


