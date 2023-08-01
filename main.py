from flask import Flask,render_template,request,redirect,flash,session,url_for,g
from pgfunc import fetch_data , insert_products, insert_sales,sales_per_product,stockremaining,sales_per_day,add_user,updateproducts,add_stock,remstock_perproduct
import pygal
import psycopg2
from werkzeug.security import generate_password_hash,check_password_hash
from pgfunc import login_user,existing_email,getpid
from barcode import Code128 
from barcode.writer import ImageWriter 
import barcode
from PIL import Image
import os
os.urandom(24)



# create an object called app
#All HTML files are put inside ""templates" folder
#All CSS/JS/images are stored in a "static" folder
#__name__ is used to help flask where to access HTML files

# CODE STARTS HERE!!

#connect to data base to use login form
conn = psycopg2.connect("dbname=duka user=postgres password=12345")
cur = conn.cursor()
 


app = Flask(__name__)
 

@app.route("/", methods=["GET"])
def home():
    if g.user:
        return render_template("index.html",user=session["user"])
    return redirect(url_for("login"))

@app.before_request
def before_request():
    g.user= None

    if 'user' in session:
        g.user=session["user"]

@app.route("/products")
def products():
    prods=fetch_data("products")
    
    return render_template("products.html", prods=prods)



@app.route("/sales")
def sales():
    sales=fetch_data("sales")
    prodz=fetch_data("products")
    return render_template("sales.html",sales=sales,prodz=prodz)


@app.route("/addproduct", methods=["POST","GET"])
def addproduct():
    if request.method == "POST":
        name=request.form["name"]     
        buying_price=request.form["buying_price"]
        selling_price=request.form["selling_price"]
        product=(name,buying_price,selling_price)
        insert_products(product)
        return redirect("/products")

@app.route("/addsales", methods=["POST","GET"])   
def addsales():
    
    if request.method=="POST":        
        pid=request.form["pid"]
        quantity=request.form["quantity"]
        print(quantity)
        sales=(pid,quantity,'now') #return pid if error
        insert_sales(sales)
        return redirect("/sales")

@app.route("/dashboard") 
def dashboard():   
   salesperprod=sales_per_product()
   prod=[]
   totalsales=[]
   for i in salesperprod:
       prod.append(i[0])
       totalsales.append(i[1])
   bar_chart=pygal.Bar()
   bar_chart.title="SALES PER PRODUCT"
   bar_chart.x_labels = prod
   bar_chart.add("Totalsales",totalsales)
   bar_chart=bar_chart.render_data_uri()
    
   salesperday=sales_per_day()
   sales=[]
   date=[]
   for i in salesperday:
       sales.append(i[0])
       date.append(i[1])
   chart=pygal.Line()
   chart.title="Sales Per Month"
   chart.x_labels = sales
   chart.add("Months",date)
   chart=chart.render_data_uri()


   stockrem=pygal.Bar()
   stockrem.title="Remaining Stock"
   remainingstock=stockremaining()
   stock=[]
   remm=[]
   for i in remainingstock:
       stock.append(i[1])
       remm.append(i[2])
   stockrem.x_labels = stock
   stockrem.add("Remaining",remm)
   stockrem=stockrem.render_data_uri() 

   print(remainingstock)    





      
   return render_template("dashboard.html",bar_chart=bar_chart,chart=chart,stockrem=stockrem)



app.secret_key = os.urandom(24)
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.pop("user", None)
        
        # Retrieve the user's email from the form
        email = request.form["email"]
        
        # Retrieve the user's hashed password from the database
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        if row is not None:
            hashed_password = row[0]
            
            # Check if the password matches the hashed password
            if check_password_hash(hashed_password, request.form["password"]):
                session['user'] = email
                return redirect(url_for('index'))
    
    return render_template("login.html")


        
       
        
        







@app.route("/register") 
def register():
   return render_template('register.html')



    
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        if existing_email(email):

            return "Email already exists"
        else:
            users = (full_name, email, password, "now")
            add_user(users)
            return redirect("/login")
    else:
        return render_template("register.html")
    
    
@app.route('/editproducts', methods=["POST", "GET"])
def editproducts():
   if request.method=="POST":
      id=request.form["id"]
      name = request.form["editname"]
      buying_price= request.form["editbuyprice"]
      selling_price=request.form["editsellprice"]
      print(name)
      print(buying_price)
      print(selling_price)
      products=(id,name,buying_price,selling_price)
      updateproducts(products)
      return redirect("/products")
   
@app.route("/stock")
def stock():
    stock=fetch_data("stock")
    prodx=fetch_data("products")
    return render_template("stock.html",stock=stock,prodx=prodx)

   

@app.route('/addstock',methods=["POST","GET"])
def addstock():
    if request.method == "POST":
        pid=request.form["pid"]
        quantity=request.form["quantity"]
        stock=(pid,quantity,'now')
        add_stock(stock)
        return redirect("/stock")
    


@app.context_processor
def inject_remaining_stock():
    def remaining_stock(product_id=None):
      stock = remstock_perproduct(product_id)
      return stock[0] if stock is not None else int('0')
    return {'remaining_stock': remaining_stock}


@app.context_processor
def generate_barcode():
    id_list = getpid()
    barcode_paths = []
    for pid_tuple in id_list:
        pid = pid_tuple[0]
        code = Code128(str(pid), writer=ImageWriter())
        barcode_path = f"static/barcodes/{pid}.png"
       
        code.save(barcode_path)
        barcode_paths.append(barcode_path)
    return {'generate_barcode': generate_barcode}

    



if __name__ == '__main__':
    app.run(debug=True)
