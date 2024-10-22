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
    user_id: Mapped[int] = mapped_column()
    amount: Mapped[int] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount
        self.date = datetime.now()
    
    def __repr__(self):
        return '<History %r>' % self.id

@app.route('/api/register', methods = ['POST'])
def register():
    if request.form['username'] != None and request.form['password'] != None:
        try:
            user = db.session.execute(db.select(User).filter_by(username=request.form['username'])).scalar_one()
        except sqlalchemy.exc.NoResultFound:
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
        except sqlalchemy.exc.NoResultFound:
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
        return {
                "status" : 0,
                "result" : 0,
            }
    except Exception:
        return {
                "status" : 0,
                "result" : -1,
            }

@app.route('/api/balance')
def balance():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            return {
                    "status" : 0,
                    "result" : 0,
                    "balance" : user.balance,
                }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status" : 0,
                "result" : -2,
            }
    else:
        return {
                "status" : 0,
                "result" : -1,
            }

@app.route('/api/fund')
def fund():
    if 'username' in session:
        code = request.args.get('code')
        if code: # to be changed
            try:
                user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
                user.balance += 10
                user.verified = True
                history = History(user_id=user.id, amount=10)
                db.session.add(history)
                db.session.commit()
                return {
                    "status": 0,
                    "result": 0,
                    "balance": user.balance,
                }
            except sqlalchemy.exc.NoResultFound:
                return {
                    "status": 0,
                    "result": -3,
                }
        else:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/consumption')
def consumption():
    if 'username' in session:
        month = request.args.get('month')
        if month:
            try:
                user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
                histories = db.session.execute(db.select(History).filter_by(user_id=user.id).filter(sqlalchemy.extract('month', History.date) == month).filter(History.amount < 0)).scalars().all()
                total_consumption = sum([h.amount for h in histories])
                return {
                    "status": 0,
                    "result": 0,
                    "consumption": total_consumption,
                }
            except sqlalchemy.exc.NoResultFound:
                return {
                    "status": 0,
                    "result": -3,
                }
        else:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

if __name__ == "__main__":
    app.run(debug=True)