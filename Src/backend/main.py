import flask
import flask_sqlalchemy

app = flask.Flask(__name__)
app.secret_key = b'8500724ec607b7b2fd7ef161bde8b8b0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = flask_sqlalchemy.SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    manager = db.Column(db.Boolean)
    balance = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.email = password

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/api/login', methods = ['POST'])
def login():
    if flask.request.form['username'] != None and flask.request.form['password'] != None: # to be changed
        return flask.request.form['username'] + flask.request.form['password'] # to be changed
    else:
        return {
            "status" : 0,
            "result" : -1,
        }

@app.route('/api/logout')
def logout():
    return "Logout"

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