from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"

db = SQLAlchemy(app)

class sentences(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(5000))
    date = db.Column(db.DateTime())

    def __init__(self, text):
        self.text = text
        self.date = datetime.utcnow()

db.create_all()

@app.route("/")
def home():
    random.seed()
    newsentence = sentences.query.all()
    newsentence = newsentence[random.randint(0, len(newsentence)-1)]
    return render_template("index.html", newsentence=newsentence)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/newpost", methods=["POST"])
def newpost():
    apost = createPost(request.form["post-text"])
    db.session.add(apost)
    db.session.commit()
    return redirect(url_for("home"))

def createPost(text):
    if (text != None) and (len(text)<=5000):
        return sentences(text)
    else:
        return None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
