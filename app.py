from flask import Flask, request, render_template,\
                  redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

db_uri = "sqlite:///test.db"
# db_uri = os.environ.get('DATABASE_URL') #or "postgresql://localhost/flasknote"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    now_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread',
        backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.name

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_name = db.Column(db.String(80), unique=True, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Thread %r>' % self.thread_name


@app.route("/")
def index():
    threads = Thread.query.all()
    return render_template("index.html", threads=threads)

@app.route("/thread/<title>/")
def thread_detail_show(title):
    title = Thread.query.filter_by(thread_name=title).first()
    articles = Article.query.filter_by(thread_id=title.id).all()
    
    return render_template('thread.html',
                            thread=title.thread_name,
                            articles=articles)

@app.route("/result", methods=["POST"])
def article_add():
    res = request.form
    thread = Thread.query.filter_by(thread_name=res["thread"]).first()
    data = Article(name=res["name"],
                   article=res["article"],
                   thread_id=thread.id)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('thread_detail_show', title=res["thread"]))

@app.route("/create_thread", methods=["POST"])
def thread_create():
    thread_get = request.form["thread"]
    thread_list = []
    threads = Thread.query.all()
    thread_list = [th.thread_name for th in threads]
    if thread_get not in thread_list:
        thread_new = Thread(thread_name=thread_get)
        db.session.add(thread_new)
        db.session.commit()
    return redirect(url_for('thread_detail_show', title=thread_get))


if __name__ == "__main__":
    app.run()
