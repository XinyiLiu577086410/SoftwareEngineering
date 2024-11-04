from flask import Flask, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
CORS(app)
app.secret_key = b'8500724ec607b7b2fd7ef161bde8b8b0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=False)
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

class Chat(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    module_id: Mapped[int] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    picture: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    def __init__(self, user_id, module_id, prompt, picture):
        self.user_id = user_id
        self.module_id = module_id
        self.prompt = prompt
        self.picture = picture
        self.date = datetime.now()

    def __repr__(self):
        return '<Chat %r>' % self.id

@app.route('/api/info', methods = ['GET'])
def info():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            return {
                "status": 0,
                "result": 0,
                "username": user.username,
                "balance": user.balance,
                "manager": user.manager,
            }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/users', methods = ['GET'])
def users():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            if user.manager:
                users = db.session.execute(db.select(User)).scalars().all()
                return {
                    "status": 0,
                    "result": 0,
                    "users": [{"username": u.username,
                               "group": 'Manger' if u.manager else 'User',
                               "balance": u.balance} for u in users],
                }
            else:
                return {
                    "status": 0,
                    "result": -3,
                }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }
    

@app.route('/api/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username != None and password != None:
        try:
            user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            user = User(username, password)
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
    app.logger.info(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    if username != None and password != None:
        try:
            user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
            if user.password == password:
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

@app.route('/api/fund', methods=['GET'])
def fund():
    app.logger.info(request.args.get('code'))
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
        current_month = datetime.now().month
        months = [(current_month - i - 1) % 12 + 1 for i in range(6)]
        months = months[::-1]
        month_names = [str(month) for month in months]
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            total_consumption = []
            for month in months:
                histories = db.session.execute(
                    db.select(History)
                    .filter_by(user_id=user.id)
                    .filter(sqlalchemy.extract('month', History.date) == month)
                    .filter(History.amount < 0)
                ).scalars().all()
                total_consumption.append(sum([h.amount for h in histories]))
            return {
                "status": 0,
                "result": 0,
                "consumption": {
                    "months": month_names,
                    "values": total_consumption,
                },
            }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -3,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/delete', methods = ['GET'])
def delete():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            if user.manager:
                username = request.args.get('username')
                if username:
                    try:
                        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
                        db.session.delete(user)
                        db.session.commit()
                        return {
                            "status": 0,
                            "result": 0,
                        }
                    except sqlalchemy.exc.NoResultFound:
                        return {
                            "status": 0,
                            "result": -5,
                        }
                else:
                    return {
                        "status": 0,
                        "result": -4,
                    }
            else:
                return {
                    "status": 0,
                    "result": -3,
                }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/histories', methods = ['GET'])
def history():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            if user.manager:
                users = db.session.execute(db.select(User)).scalars().all()
                chat = db.session.execute(db.select(Chat)).scalars().all()
                history = db.session.execute(db.select(History)).scalars().all()
                return {
                    "status": 0,
                    "result": 0,
                    "chat": [{"username": u.username,
                              "module_id": c.module_id,
                              "prompt": c.prompt,
                              "picture": c.picture,
                              "date": c.date} for c in chat for u in users if u.id == c.user_id],
                    "history": [{"username": u.username,
                                 "amount": h.amount,
                                 "date": h.date} for h in history for u in users if u.id == h.user_id],
                }
            else:
                return {
                    "status": 0,
                    "result": -3,
                }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/chat_history', methods = ['GET'])
def chat_history():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            chat = db.session.execute(db.select(Chat).filter_by(user_id=user.id)).scalars().all()
            return {
                "status": 0,
                "result": 0,
                "chat": [{"module_id": c.module_id,
                          "prompt": c.prompt,
                          "picture": c.picture,
                          "date": c.date} for c in chat],
            }
        except sqlalchemy.exc.NoResultFound:
            return {
                "status": 0,
                "result": -2,
            }
    else:
        return {
            "status": 0,
            "result": -1,
        }

@app.route('/api/chat', methods = ['POST'])
def chat():
    if 'username' in session:
        try:
            user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar_one()
            user.balance -= 1
            history = History(user_id=user.id, amount=-1)
            db.session.add(history)
            db.session.commit()
            return {
                "status": 0,
                "result": 0,
                "balance": user.balance,
                "picture": "",
            }
        except sqlalchemy.exc.NoResultFound:
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