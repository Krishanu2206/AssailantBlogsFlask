from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, EmailField # type: ignore
from wtforms.validators import DataRequired, Email # type: ignore
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

##Create a flask instance
app = Flask(__name__)
##SETTING SECURITY FOR THE WEBFORMS 
app.config['SECRET_KEY'] = "I AM ASSAILANT"
##ADD DATABASE 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#MYSQL DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Krishanu%402206@localhost/users'
##INITIALISE THE DATABASE
db=SQLAlchemy(app)


##CREATE A MODEL
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(200), nullable=False, unique=True)
    date_added=db.Column(db.DateTime(), default=datetime.now())

    ##CREATE A STRING
    def __repr__(self):
        return '<Name %r>' %self.name

##CREATE A FORM CLASS
class UserForm(FlaskForm):
    name=StringField("What's your name", validators=[DataRequired()])
    email=EmailField("Enter your email", validators=[DataRequired()])
    submit=SubmitField("Submit")

class NamerForm(FlaskForm):
    name=StringField("What's your name", validators=[DataRequired()])
    submit=SubmitField("Submit")

##Create a route decorator
@app.route('/')

# def index():
#     return "<h2>Hello World!!</h2>"

def index():
    stuff = "This is <strong>bold</strong> text!"
    favourite_pizza= ["peperoni", "cheese", "mushrooms", 42]
    flash("WELCOME TO ASSAILANT'S BLOGAPP")
    return render_template("index.html", stuff=stuff, pizza=favourite_pizza)

##UPDATE DATABASE RECORD 
@app.route('/update/<int:id>', methods=['GET', 'POST']) ##if <id> is used.the id will be treated as a string.so we need to typecast.
def update(id):
    form=UserForm()
    user_to_update=User.query.get_or_404(id)
    if request.method== "POST":
        searchemail=request.form['email']
        existing_user=User.query.filter_by(email=searchemail).first()
        if existing_user and existing_user!=user_to_update:
            flash("Same email address found! Try another email.")
            return render_template('update.html', form=form, user_to_update=user_to_update)
        
        user_to_update.name=request.form['name']
        user_to_update.email=request.form['email']
        print(user_to_update.email)
        
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template('update.html', form=form, user_to_update=user_to_update)
        except:
            flash("Error in updating user")
            return render_template('update.html', form=form, user_to_update=user_to_update)
    else:
        return render_template('update.html', form=form, user_to_update=user_to_update)   
    
@app.route('/user/add', methods=['GET', 'POST'])

def add_user():
    name=None
    email=None
    form=UserForm()
    ##VALIDATE THE FORM
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user=User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        email=form.email.data
        form.name.data=''
        form.email.data=''
        flash("User added successfully")
    our_users=User.query.order_by(User.date_added)
    return render_template("add_user.html", name=name, email=email, form=form, our_users=our_users)


@app.route('/user/<name>')

def user(name):
    return render_template("user.html", name="john")


##FOR NAME FORMS
@app.route('/name', methods=['GET', 'POST'])

def name():
    name=None
    form=NamerForm()
    ##VALIDATE THE FORM
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("Form submitted successfully")
    return render_template("name.html", name=name, form=form)


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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
