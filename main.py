from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from hashlib import sha3_512
from models import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(16)


def hash_password(password):
    return sha3_512(password.encode("utf-8")).hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
def home(name="Home"):
    bin = 0
    if request.method == "POST":
        
        query = request.form["item"]
        packs = []

        for key, value in request.form.items():
            if "pq" in key:
                packs.append(value)

        
        products = Product.select().where(Product.name == query)

        product = next((prod for prod in products if all(pack in prod.pack for pack in packs)), None)
        
        cant_recycle = ["foil", "tissue", "paper_towels", "plastic_film", "garden_waste", "polystyrene", "clean_film"]
        if request.form["option"] == "yes" or any(packaging in product.pack for packaging in cant_recycle):
            bin = 2
        else:
            bin = 1


        if product != None:
            return render_template("product_page.html", prod=product, bin=bin, title="Product Page")
        else:
            flash("Product not in our database")
            return render_template("home.html", title=name)
    else:
        return render_template("home.html", title=name)


@app.route("/login", methods=["GET", "POST"])
def log_in(name="Log In"):
    
    if request.method == "POST":
        user = request.form["user_name"]
        password = request.form["user_password"]

        registered_user = User.select().where(User.name == user.lower()).first()

        if registered_user and registered_user.password == hash_password(password):
            flash('You were successfully logged in')
            session["user"] = user
            return redirect(url_for("admin_page"))

        flash("Invalid credentials")

    return render_template("login.html", title=name)


@app.route("/admin", methods=["GET", "POST"])
def admin_page(name="admin"):
    if "user" in session:

        if request.method == "POST":
            prod = request.form["product"]
            descrip = request.form["description"]
            pack = request.form["packaging"]

            pack_list = pack.split()

            Product.create(name=prod, description=descrip, pack=pack_list)

            return render_template("admin_page.html", title=name)
        else:
            return render_template("admin_page.html", title=name)

    else:
        flash("You must be logged in")
        return redirect(url_for("log_in"))


@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for("log_in"))


if __name__ == "__main__":
    app.run()