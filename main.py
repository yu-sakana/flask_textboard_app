from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

db_uri = "sqlite:///test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)

class Textboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_date = db.Column(db.DateTime, nullable=False,
                                default=datetime.utcnow)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, post_date, name, article, thread_id):
        self.post_date = post_date
        self.name = name
        self.article = article
        self.thread_id = thread_id


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_name = db.Column(db.String(80), unique=True)
    articles = db.relationship('Textboard', backref='thread', lazy=True)

    def __init__(self, thread_name, articles=[]):
        self.thread_name = thread_name
        self.articles = articles


@app.route("/")
def main():
    threads = Thread.query.all()
    # print("\n---------------------------------------------")
    # print(text)
    # print(type(text))
    # print("---------------------------------------------\n")
    return render_template("index.html", threads=threads)

@app.route("/thread", methods=["POST"])
def thread():
    thread_get = request.form["thread"]
    threads = Thread.query.all()
    thread_list = []
    threads = Thread.query.all()
    for th in threads:
        thread_list.append(th.thread_name)
        #print("----" + th.threadname + "----")
    if thread_get in thread_list:
        thread = Thread.query.filter_by(thread_name=thread_get).first()
        articles = Textboard.query.filter_by(thread_id=thread.id).all()
        return render_template("thread.html",
                                articles=articles,
                                thread=thread_get)
    else:
        thread_new = Thread(thread_get)
        db.session.add(thread_new)
        db.session.commit()
        articles = Textboard.query.filter_by(thread_id=thread_new.id).all()
        return render_template("thread.html",
                                articles=articles,
                                thread=thread_get)

@app.route("/result", methods=["POST"])
def result():
    date = datetime.now()
    article = request.form["article"]
    name = request.form["name"]
    thread = request.form["thread"]
    #print(article)
    #print(name)
    #print("------------------------------------------------------------")
    #print(thread)
    #print("------------------------------------------------------------")
    thread = Thread.query.filter_by(thread_name=thread).first()
    #print(thread)
    #print("------------------------------------------------------------")
    admin = Textboard(post_date=date, name=name, article=article, thread_id=thread.id)
    db.session.add(admin)
    db.session.commit()
    return render_template("write_result.html", article=article, name=name, now=date)

if __name__ == "__main__":
    app.run(debug=False)
