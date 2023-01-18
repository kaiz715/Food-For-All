from flask import Flask,render_template, session, request, redirect, url_for, flash
import methods
import datetime
import os
import openai

openai.api_key = "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"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("Login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        org = request.form["organization"]
        address = request.form["address"]
        methods.add_foodbank(org, username, password, address)
        session["username"] = username
        return redirect(url_for("second"))

    return render_template("signup.html")

@app.route('/second', methods=['POST', 'GET'])
def second():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if methods.check_org_credentials(username, password) == False:
            return redirect(url_for("login"))
        session["username"] = username
    elif 'username' in session:
        pass
    else:
        return redirect("/")
    
    return render_template("second.html")

@app.route('/rform', methods=['POST', 'GET'])
def Rform():
    if request.method == 'POST':
        restaurant_name = request.form["Rname"]
        address = request.form["Radd"]
        datea = datetime.date.today()
        rid = methods.add_restauant(restaurant_name, address, datea)
        i=1
        while(request.form[f"fname{i}"]!=""):
            food_name = request.form[f"fname{i}"]
            quantity = request.form[f"quant{i}"]
            expiry_date = request.form[f"expd{i}"]
            date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date()
            methods.add_food(rid, food_name, int(quantity), date)
            i+=1

            if i ==5:
                break;

        return redirect("/")
        
    return render_template("Rform.html")

@app.route('/third', methods=['POST'])
def third():
    if request.method == "POST":
        radius = int(request.form["radius"])
        weight = int(request.form["weight"])
    foodBank_info = methods.get_foodBank_info(session["username"])
    source = foodBank_info["address"]

    restaurants = methods.find_restauants(source, radius, datetime.date.today())
    
    restaurantsInfo = []
    for i in range(len(restaurants)):
        restaurantsInfo.append(methods.get_restaurant_info(restaurants[i]))
    
    restaurantFoods = methods.list_foods(restaurants)

    
    return render_template("third.html", balls=source, restaurantsInfo = restaurantsInfo, restaurantFoods = restaurantFoods)

if __name__ == '__main__':
    app.run(debug=True)
