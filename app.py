from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    todo_text = request.form['todo_text']
    todo = Todo(text=todo_text)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.get(todo_id)

    if request.method == "POST":
        todo.text = request.form["text"]
        db.session.commit()
        return redirect("/")

    return render_template("edit.html", todo=todo)

@app.route("/delete/<int:todo_id>", methods=["GET", "POST"])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

