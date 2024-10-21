from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_key = b'8500724ec607b7b2fd7ef161bde8b8b0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column()
    manager: Mapped[bool] = mapped_column()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0
        self.manager = False

    def __repr__(self):
        return '<User %r>' % self.username
    
class History(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    def __init__(self, amount):
        self.amount = amount
        self.date = datetime.now()
    
    def __repr__(self):
        return '<History %r>' % self.id

user_history = sqlalchemy.Table(
    "user_history",
    Base.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey(User.id), primary_key=True),
    sqlalchemy.Column('history_id', sqlalchemy.ForeignKey(History.id), primary_key=True),
)

@app.route('/api/register', methods = ['POST'])
def register():
    if request.form['username'] != None and request.form['password'] != None:
        try:
            user = db.session.execute(db.select(User).filter_by(username=request.form['username'])).scalar_one()
        except(sqlalchemy.exc.NoResultFound):
            user = User(request.form['username'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            return {
                "status" : 0,
                "result" : 0,
            }
        else:
            return {
                "status" : 0,
                "result" : -2,
            }
    else:
        return {
            "status" : 0,
            "result" : -1,
        }

@app.route('/api/login', methods = ['POST'])
def login():
    if request.form['username'] != None and request.form['password'] != None:
        try:
            user = db.session.execute(db.select(User).filter_by(username=request.form['username'])).scalar_one()
            if user.password == request.form['password']:
                session['username'] = user.username
                return {
                        "status" : 0,
                        "result" : 0,
                    }
            else:
                return {
                    "status" : 0,
                    "result" : -3,
                }
        except(sqlalchemy.exc.NoResultFound):
            return {
                "status" : 0,
                "result" : -2,
            }
    else:
        return {
            "status" : 0,
            "result" : -1,
        }

@app.route('/api/logout')
def logout():
    try:
        session.pop('username', None)
    except(Exception):
        return {
                "status" : 0,
                "result" : -1,
            }
    else:
        return {
                "status" : 0,
                "result" : 0,
            }

@app.route('/api/balance')
def balance():
    return "Balance"

@app.route('/api/fund')
def fund():
    return "Fund"

@app.route('/api/consumption')
def consumption():
    return "Consumption"

if __name__ == "__main__":
    app.run(debug=True)