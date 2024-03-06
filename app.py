import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class database_model(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(200),nullable=False)

    def __init__(self,title,description):
        self.title = title
        self.description = description
    def __repr__(self):
        return f"Id:{self.id}, Title is {self.title},Descriptions is {self.description}"

@app.route("/")
def hello_world():   
    with app.app_context():
        # Query all records from the database_model
        all_records = database_model.query.all()
    return render_template("view.html",all_records = all_records)

@app.route("/add", methods = ['POST','GET'])
def submit():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']

        todo = database_model(title,description)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")    
    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):
    ItemToDelete = database_model.query.get(id)
    db.session.delete(ItemToDelete)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):
    if request.method == "POST":
        ItemToUpdate = database_model.query.get(id)
        ItemToUpdate.title = request.form['title']
        ItemToUpdate.description = request.form['description']
        db.session.commit()
        return redirect("/")
    ItemToUpdate = database_model.query.get(id)
    return render_template('update.html',Item = ItemToUpdate)
    

    

if __name__ == "__main__":
    with app.app_context():
      db.create_all() 
    app.run(debug=True)