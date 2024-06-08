from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Ahmed.Hashim02@localhost/ToDoList_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Todo(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    done=db.Column(db.Boolean , default = False)  # default added

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    todo_list=Todo.query.all()      # to display all enteries of todo table
    return render_template('base.html',todo_list=todo_list)

@app.route('/add',methods=['POST'])
def add():
    name=request.form.get("name")     # name is fetched from form
    new_task=Todo(name=name,done=False)
    db.session.add(new_task)   # added to DB 
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo=Todo.query.get(todo_id)
    todo.done=not todo.done
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo=Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
