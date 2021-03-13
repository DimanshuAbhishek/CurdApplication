import re
from flask import Flask,render_template,jsonify
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,time,date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI']= 'mysql://root:Dimansu20@localhost/course'
db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    date_updated = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    date_created=db.Column(db.DateTime)
    description=db.Column(db.String)
    discount_price=db.Column(db.Float)
    title= db.Column(db.String)
    price=  db.Column(db.Integer)
    on_discount = db.Column(db.Boolean)

    def __init__(self,title,price,on_discount,description,date_created,discount_price):
        self.date_created=date_created
        self.description=description
        self.discount_price=discount_price
        self.on_discount=on_discount
        self.title=title
        self.price=price

    def __repr__(self):
        return f"id{self.id}"


@app.route("/")
def home():
    return

@app.route('/course/input',methods=["POST"])
def course():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        price = post_data.get('price')
        on_discount=post_data.get('on_discount')
        description=post_data.get('description')
        date_created=post_data.get('date_created')
        discount_price=post_data.get('discount_price')
        reg =Course(title,price,on_discount,description,date_created,discount_price)
        db.session.add(reg)
        db.session.commit()
        return jsonify('Add')
    return jsonify("error")
#to display Records
@app.route('/course',methods=["Get"])    
def all_course():
    all_course=db.session.query(Course.id,Course.date_created,Course.date_updated,Course.description,Course.on_discount,Course.price,Course.title)
    return jsonify(all_course)
#for search
@app.route('/course/<id>',methods=["GET"])
def searchbyid(id):
    serach_by_id=db.session.query(Course.id,Course.date_created,Course.date_updated,Course.description,Course.on_discount,Course.price,Course.title).filter(Course.id == id).first()
    return jsonify(serach_by_id)

#for delete a record
@app.route('/delet/<id>',methods=["GET"])
def course_delet(id):
    delet_course = db.session.query(Course.id).get(id)
    db.session.delete(delet_course)
    db.session.commit
    return jsonify("Deleted record")


#for updation

@app.route('/update_course/<id>',methods=["PUT"])
def update_course(id):
    if request.content_type == "application/json":
        put_data= request.get_json()
        title = put_data('title')
        date_updated=put_data('date_updated')
        price =put_data('price')
        on_discount=put_data('on_discount')
        description=put_data('description')
        date_created=put_data('date_created')
        discount_price=put_data('discount_price')
        record = db.session.query(Course).get(id)
        record.date_created=date_created
        record.date_updated=date_updated
        record.discount_price = discount_price
        record.price= price
        record.title=title
        record.description= description
        record.on_discount =on_discount
        db.session.commit()

        return jsonify('Updated Course')
    return jsonify("Some Error")



if __name__ == "main":
    app.run(debug=True)

