from flask import Flask,render_template,request,redirect,session
from pgfunc import fetch_data , insert_products, insert_sales,sales_per_product,sales_per_day,add_user,loggin_in,updateproducts,add_stock,stockremaining
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

#@app.route("/login")
#def login():
 #   return render_template("login.html")

@app.route('/login', methods=["POST","GET"])
def login():
   login = loggin_in()
   email = []
   password = []
   for i in login:
         email, password = i
         # print(email,password)
   return render_template('login.html', login=login)

    





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

   

@app.route('/addstock')
def addstock():
    if request.form == "POST":
        pid=request.form["pid"]
        quantity=request.form["quantity"]
        mystock=(pid,quantity,'now()')
        add_stock(mystock)
        return redirect("/stock")
    


#@app.context_processor
#def inject_processor()
# :@app.context_processor
#def my_context_processor():
 #   user_id = request.args.get('user_id')
  #  user = get_user(user_id)
   # return dict(user=user)

#  def get_remaining(quantity, int):
#    return u'{1}{0:.2f}' (format(int, quantity))
# return dict(get_remaining=get_remaining)
#@app.context_processor
#ef my_stock_remaining():
  #  reminingstock = stockremaining
   # user = reminingstock
    #return dict(user=user)

    
@app.context_processor
def my_stock_remaining():
    remaining_stock = stockremaining()  # Call the function to get the value
    return dict(remaining_stock=remaining_stock)

#@app.context_processor
#def my_stock_remaining():
  #  remaining_stock = stockremaining()  # Call the function to get the value
   # return dict(remaining_stock=remaining_stock)



if __name__ == '__main__':
    app.run(debug=True)
