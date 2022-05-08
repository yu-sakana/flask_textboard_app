from flask import Flask, request, render_template,\
                  redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

db_uri = "sqlite:///test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    now_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread',backref=db.backref('articles', lazy=True))
    def __repr__(self):
        return '<Article %r>' % self.name

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_name = db.Column(db.String(80), unique=True, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
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
def create_thread():
    thread_title = request.form["thread"]
    thread_list = []
    threads = Thread.query.all()
    thread_list = [th.thread_name for th in threads]
    if thread_title not in thread_list:
        thread_new = Thread(thread_name=thread_title)
        db.session.add(thread_new)
        db.session.commit()
    return redirect(url_for('thread_detail_show', title=thread_title))

@app.route("/api/get_info", methods=["GET"])
def get_infomation():
    def get_all_thread():
        thread_all_get = Thread.query.filter(Thread.id != None).all()
        thread_list = []
        for thread in thread_all_get:
            thread_detail = {"thread_name": thread.thread_name, "id": thread.id, "date": thread.post_date}
            thread_list.append(thread_detail)
        return jsonify(thread_list)

    def get_articles(api_thread_id):
        data = {api_thread_id: []}
        thread_api_get = Thread.query.filter_by(id=api_thread_id)
        articles = Article.query.filter_by(thread_id=api_thread_id).all()
        for article in articles:
            article_detail = {"thread_id": article.thread_id, "name": article.name, "article": article.article, "date": article.now_date}
            data[api_thread_id].append(article_detail)
        return jsonify(data)
    
    thread_id = request.args.get("thread_id")
    if thread_id is None:
        return get_all_thread()
    else:
        return get_articles(thread_id)

@app.route("/api", methods=["POST"])
def post_method():
    def make_thread(thread_title):
        thread_list = []
        threads = Thread.query.all()
        thread_list = [th.thread_name for th in threads]
        if thread_title not in thread_list:
            new_thread = Thread(thread_name=thread_title)
            db.session.add(new_thread)
            db.session.commit()
        return jsonify({'title': thread_title})

    def post_article(post_name,post_article,post_thread_id):
        if Thread.query.filter_by(id=post_thread_id) is not None:
            data = Article(name=post_name,article=post_article, thread_id=post_thread_id)
            db.session.add(data)
            db.session.commit()
        return jsonify({"name": post_name, "article": post_article, "Post_thread_id": post_thread_id})

    thread_title = request.args.get("thread_title")
    article = request.args.get("article")
    name = request.args.get("name", default='名無しさん', type=str)
    thread_id = request.args.get("thread_id")

    if thread_title is not None:
        return make_thread(thread_title)
    else:
        return post_article(name,article,thread_id)
    
if __name__ == "__main__":
    app.run()
