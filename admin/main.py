import csv
import os
from flask import Flask, render_template, request,redirect, url_for
from data import db_session
from data.products import Product
from werkzeug.utils import secure_filename
from edit_form import EditForm
from add_form import AddForm

UPLOAD_FOLDER = '/static/img/product'

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = 'baker_admin_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('csv_files/products.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    products = list(reader)

db_session.global_init("db/assortment.db")

db_sess = db_session.create_session()
product = db_sess.query(Product).all()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db_sess = db_session.create_session()
    product = db_sess.query(Product).all()
    return render_template('index.html', product=product)


@app.route('/edit/<index>', methods=['GET', 'POST'])
def edit(index):
    form = EditForm()
    if request.method == 'GET':
        return render_template('edit.html', product=product, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(f'static/img/product/{filename}')
            db_sess = db_session.create_session()
            item = db_sess.query(Product).get(int(index))
            item.title = form.title.data
            item.about = form.content.data
            item.image_file_path = filename
            print(product[int(index) - 1].title)
            db_sess.add(item)
            db_sess.commit()
            return redirect("/admin")
        return redirect("/")


@app.route('/delete/<index>', methods=['GET', 'POST'])
def delete(index):
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    print(product[int(index) - 1].title)
    db_sess.delete(item)
    db_sess.commit()
    return redirect("/admin")


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if request.method == 'GET':
        return render_template('add.html', product=product, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(f'static/img/product/{filename}')
            db_sess = db_session.create_session()
            item = Product()
            item.title = form.title.data
            item.about = form.content.data
            item.image_file_path = filename
            db_sess.add(item)
            db_sess.commit()
            return redirect("/admin")
        return redirect("/")



def main():
    app.run()


if __name__ == '__main__':
    main()
