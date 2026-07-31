from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime
from models import db


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

bcrypt = Bcrypt(app)

db.init_app(app)

CORS(app)



# Expense Table Model

class Expense(db.Model):

    __tablename__ = "expenses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    expense_date = db.Column(
        db.Date,
        nullable=False
    )

    description = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    
    

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

# Home

@app.route("/")
def home():
    return render_template("auth.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


# Get Expenses

@app.route("/api/expenses/<int:user_id>", methods=["GET"])
def get_expenses(user_id):

    expenses = Expense.query.filter_by(
        user_id=user_id
    ).all()


    data=[]


    for expense in expenses:

        data.append({

            "id":expense.id,
            "title":expense.title,
            "amount":expense.amount,
            "category":expense.category,
            "date":str(expense.expense_date)

        })


    return jsonify(data)




# Add Expense

@app.route("/api/expenses", methods=["POST"])
def add_expense():

    data = request.json

    print(data)   # check received data


    new_expense = Expense(

        user_id=data.get("user_id"),

        title=data.get("title"),

        amount=float(data.get("amount")),

        category=data.get("category"),

        expense_date=datetime.strptime(
            data.get("date"),
            "%Y-%m-%d"
        ).date()

    )


    db.session.add(new_expense)

    db.session.commit()


    return jsonify({

        "message":"Expense added successfully"

    }),201


# Edit Expense

@app.route("/api/expenses/<int:id>", methods=["PUT"])
def edit_expense(id):

    expense = Expense.query.get(id)


    if not expense:

        return jsonify({
            "message":"Expense not found"
        }),404


    data=request.json


    expense.title=data.get("title")

    expense.amount=float(data.get("amount"))

    expense.category=data.get("category")

    expense.expense_date=datetime.strptime(
        data.get("date"),
        "%Y-%m-%d"
    ).date()


    db.session.commit()


    return jsonify({

        "message":"Expense updated successfully"

    })




# Delete One Expense

@app.route("/api/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):

    expense = Expense.query.get(id)


    if not expense:

        return jsonify({
            "message":"Expense not found"
        }),404


    db.session.delete(expense)

    db.session.commit()


    return jsonify({

    "message":"Expense deleted successfully"

})



# Delete All

@app.route("/api/expenses", methods=["DELETE"])
def delete_all_expenses():

    Expense.query.delete()

    db.session.commit()


    return jsonify({

        "message":"All expenses deleted"

    })
    
    
      
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")


    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:

        return jsonify({
            "message":"Email already exists"
        }),400



    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")



    user = User(

        name=name,

        email=email,

        password=hashed_password

    )


    db.session.add(user)

    db.session.commit()



    return jsonify({

        "message":"Registration successful"

    }),201
    
    
    
    
@app.route("/login", methods=["POST"])
def login():

    data = request.json


    email = data.get("email")

    password = data.get("password")



    user = User.query.filter_by(
        email=email
    ).first()



    if not user:

        return jsonify({

            "message":"User not found"

        }),404




    if bcrypt.check_password_hash(
        user.password,
        password
    ):


        return jsonify({

            "message":"Login successful",

            "user_id":user.id,

            "name":user.name

        })



    return jsonify({

        "message":"Wrong password"

    }),401

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    
    
    app.run(debug=True)