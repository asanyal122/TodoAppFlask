from flask import Flask,render_template,request,redirect
app=Flask(__name__)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todoname = db.Column(db.String(80), unique=False, nullable=False)
    desc = db.Column(db.String(120), unique=False, nullable=False)
    lastupdate=db.Column(db.DateTime,nullable=False)

    def __repr__(self):
        return f'{self.id} {self.todoname} {self.desc} {self.lastupdate}'

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        todoname=request.form['exampleInputTodo']
        desc=request.form['exampleInputDesc']
        todo=Todo(todoname=todoname,desc=desc,lastupdate=datetime.now())
        db.session.add(todo)
        db.session.commit()
    return render_template('index.html',allTodos=Todo.query.all())

@app.route('/delete/<int:id>')
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True,port=8000)
