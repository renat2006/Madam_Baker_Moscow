from flask import Flask, render_template, url_for
from admin.data import db_session
from admin.data.products import Product
import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from admin.data import db_session
from admin.data.products import Product
from werkzeug.utils import secure_filename
from admin.edit_form import EditForm
from admin.add_form import AddForm

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = 'baker_admin_secret_key'

db_session.global_init("admin/db/assortment.db")


@app.route('/', methods=['GET', 'POST'])
def baker():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    # print(products[0].title)
    return render_template('index.html', products=products)


db_session.global_init("admin/db/assortment.db")

db_sess = db_session.create_session()
product = db_sess.query(Product).all()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db_sess = db_session.create_session()
    product = db_sess.query(Product).all()
    return render_template('admin/index.html', product=product)


@app.route('/edit/<index>', methods=['GET', 'POST'])
def edit(index):
    form = EditForm()
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    print(item.status_color)
    if request.method == 'GET':
        # print(form.content.default)
        form.content.default = item.about
        # print(form.content.default)
        return render_template('admin/edit.html', product=product, form=form, item=item)
    elif request.method == 'POST':
        # if form.title.validate(form):
        #     print(1)
        # if form.content.validate(form):
        #     print(2)
        # if form.submit.validate(form):
        #     print(3)
        # a = request.form['about_value']
        if form.validate_on_submit():
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(f'static/img/product/{filename}')
            # if item.title != form.title.data:
            item.title = form.title.data
            # print(form.content.data, item.about)
            item.about = request.form['about_value']
            # if item.image_file_path == 'static/img/product/':
            print(request.form['file'])
            if request.form['file']:
                item.image_file_path = filename
                f.save(f'static/img/product/{filename}')
            db_sess.add(item)
            db_sess.commit()
            return redirect("/admin")
        return render_template("404.html")


@app.route('/delete/<index>', methods=['GET', 'POST'])
def delete(index):
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    db_sess.delete(item)
    db_sess.commit()
    return redirect("/admin")


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if request.method == 'GET':
        return render_template('admin/add.html', product=product, form=form)
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
