from flask import Flask, render_template

##Create a flask instance
app = Flask(__name__)

##Create a route decorator
@app.route('/')

# def index():
#     return "<h2>Hello World!!</h2>"

def index():
    stuff = "This is <strong>bold</strong> text!"
    favourite_pizza= ["peperoni", "cheese", "mushrooms", 42]
    return render_template("index.html", stuff=stuff, pizza=favourite_pizza)

@app.route('/user/<name>')

def user(name):
    return render_template("user.html", name=name)


#CREATE CUSTOM ERROR PAGES

##INVALID URL
@app.errorhandler(404)

def page_not_found(error):
    return render_template("404.html", e=error), 404

##INTERNAL SERVER ERROR
@app.errorhandler(500)

def page_not_found(error):
    return render_template("500.html", e=error), 500


if __name__ == "__main__":
    app.run(debug=True)
