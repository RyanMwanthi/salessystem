from flask import Flask,render_template,request,redirect
from pgfunc import fetch_data , insert_products, insert_sales


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
    print(prods)
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





        




app.run(debug=True)





