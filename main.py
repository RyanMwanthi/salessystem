from flask import Flask,render_template,request,redirect
from pgfunc import fetch_data , insert_products, insert_sales,sales_per_product,sales_per_day,add_user
import pygal


# create an object called app
#All HTML files are put inside ""templates" folder
#All CSS/JS/images are stored in a "static" folder
#__name__ is used to help flask where to access HTML files

# CODE STARTS HERE!!


app = Flask(__name__)
 

@app.route("/")
def home():
    return render_template("index.html")


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
        stock_quantity=request.form["stock_quantity"]
        print(name)
        print(buying_price)
        print(selling_price)
        print(stock_quantity)
        product=(name,buying_price,selling_price,stock_quantity)
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
   bar_chart.title="sales per product"
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




      
   return render_template("dashboard.html",bar_chart=bar_chart,chart=chart)

@app.route("/login")
def login():
    return render_template('login.html')




@app.route("/register") 
def register():
   return render_template('register.html')

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        full_name=request.form["full_name"]     
        email=request.form["email"]
        password=request.form["password"]
        users=(full_name,email,password,'now')
        add_user(users)
        return redirect('/login')
        


   
   
   





   





        




app.run(debug=True)





