from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __str__(self):
        return f"{self.title} - {self.desc}"


@app.route('/', methods= ["GET","POST"])
def hello_world():
    #return 'Hello, World!'
    
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title= title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html",db_data = all_todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods = ["POST","GET"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    return render_template("update.html",todo = todo)

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
