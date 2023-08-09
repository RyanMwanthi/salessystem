import psycopg2
from werkzeug.security import check_password_hash,generate_password_hash




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


# def add_user(user):
#     conn = psycopg2.connect("dbname=duka user=postgres password=12345")
#     cur = conn.cursor()
#     full_name, email, password, created_at = user
#     password_hash = generate_password_hash(password)
#     cur.execute("INSERT INTO users (full_name, email, password, created_at) VALUES (%s, %s, %s, %s)", (full_name, email, password_hash, created_at))
#     conn.commit()
#     cur.close()
#     conn.close()



# admins / users register
# def register():
   

def login_user(email, password):
    a="SELECT email,password FROM users;"
    cur.execute(a)
    data=cur.fetchall()
    return data

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
     
    q = " SELECT * FROM remaining_stock;"
    cur.execute(q)
    res = cur.fetchall()
    return res

def remstock_perproduct(product_id=None):
   rem="""
SELECT 
            
            COALESCE(s.stock_quantity, 0) - COALESCE(sa.sales_quantity, 0) AS closing_stock
            FROM
                (SELECT pid, SUM(quantity) AS stock_quantity FROM stock GROUP BY pid) AS s
            LEFT JOIN
                (SELECT pid, SUM(quantity) AS sales_quantity FROM sales GROUP BY pid) AS sa
            ON s.pid = sa.pid
            WHERE s.pid = %s
            GROUP BY s.stock_quantity,sa.sales_quantity;
   """
   cur.execute(rem,(product_id,))
   rm=cur.fetchall()
   if rm:
      return rm[0]
   else:
      return None



def getpid():
   q="SELECT id FROM products"
   cur.execute(q)
   results = cur.fetchall()
   return results
   