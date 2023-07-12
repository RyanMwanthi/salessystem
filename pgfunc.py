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

def loggin_in():
  q="SELECT email,password FROM users"
  cur.execute(q)
  ep=cur.fetchall()
  print(ep)
  
  return(ep)


def updateproducts(products):
    
        
        id = products[0]
        name = products[1]
        buying_price = products[2]
        selling_price = products[3]
        
        editquery = "UPDATE products SET name = %s, buying_price = %s, selling_price = %s WHERE id = %s"
        cur.execute(editquery, (name, buying_price, selling_price, id))
        conn.commit()
        return editquery


def add_stock(s):
   st=str(s)
   stock="INSERT INTO stock(pid,quantity,created_at)" "VALUES" + st
   cur.execute(stock)
   conn.commit
   return stock



def stockremaining():
   rem="SELECT * FROM remaining_stock "
   cur.execute(rem)
   rm=cur.fetchall()
   return(rm)



#def stockremaining(remaining_stock):
 #  id = remaining_stock[0]
  # cur.execute("SELECT remaining_stock FROM remaining_stock WHERE id = %s", (id,))
   #result = cur.fetchone()
   #r3eturn result[0] if result else None

  