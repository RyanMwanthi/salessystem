import psycopg2


try:
  conn=psycopg2.connect("dbname=duka user=postgres password=12345")

  cur = conn.cursor()
except Exception as e:
  print(e)  


def fetch_data(tbname):
  try:
    q="SELECT * FROM" + tbname + ";"
    cur.excecute(q)
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
