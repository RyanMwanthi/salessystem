from flask import Flask,render_template
from pgfunc import fetch_data

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


    return render_template("sales.html",sales=sales)




app.run()





