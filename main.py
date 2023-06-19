from flask import Flask,render_template
import psycopg2

# create an object called app
#All HTML files are put inside ""templates" folder
#All CSS/JS/images are stored in a "static" folder
#__name__ is used to help flask where to access HTML files

# CODE STARTS HERE!!
from flask import Flask,render_template
import psycopg2

app = Flask(__name__)
 

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    #loading data from the database
    conn=psycopg2.connect("dbname=duka user= postgres password=12345")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    prods=cur.fetchall()
    cur.close()
    conn.close()    
    return render_template ('products.html',prods=prods)


@app.route("/sales")
def mysales():
    #import sales data from data base
    conn=psycopg2.connect("dbname=duka user= postgres password=12345")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    sales=cur.fetchall()
    cur.close()
    conn.close()  
    return render_template('sales.html',sales=sales)


app.run()





