from flask import Flask, request, render_template, url_for, redirect, flash
from dao import DAO
from forms import CreateItemForm, DeleteForm
import datetime
import pymongo

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'development key'

dao = DAO()


@app.route("/login", methods=['POST'])
def login():
    print request
    return ""

@app.route("/logout", methods=['POST'])
def logout():
    print request
    return ""

@app.route("/")
@app.route("/catalog")
def index():
    cats = dao.getCategories()
    items = dao.getItems()
    print items
    return render_template('index.html', categories=cats, items=items)

@app.route("/catalog.json")
def catalogJSON():
    return dao.toJSON()

@app.route("/catalog/<category_name>")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    cats = dao.getCategories()
    category = dao.getCategory(category_name)
    items = dao.getItemsInCategory(category)
    return render_template('showCategory.html', category=category, \
            categories=cats, items=items)

@app.route("/catalog/items/create", methods=['POST', 'GET'])
def createItem():
    if request.method == 'GET':
        form = CreateItemForm()
        cats = dao.getCategories()
        form.category.choices = [(g['_id'], g['name']) for g in cats]
        return render_template('create.html', form=form)
    else:
        f = request.form
        item = formToRecord(f)
        dao.createItem(item)
        flash('Item ' + item['title'] + " created.")
        return redirect(url_for('index'))

def formToRecord(f):
    item = {'cat_id':f['category'], 'description':f['description'],\
        'title':f['title'], 'timestamp':datetime.datetime.utcnow()}
    return item

@app.route("/catalog/<category>/<item_name>")
def showItem(category, item_name):
    item = dao.getItemByName(item_name)
    return render_template('show.html', item=item, category_name=category)

@app.route("/catalog/<category_name>/<item_name>/edit", methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if request.method == 'GET':
        form = CreateItemForm()
        cats = dao.getCategories()
        form.category.choices = [(g['_id'], g['name']) for g in cats]
        item = dao.getItemByName(item_name)
        form._objectId = item['_id']
        form.category.process_data(item.get('cat_id'))
        form.title.process_data(item.get('title'))
        form.description.process_data(item.get('description'))
        return render_template('edit.html', form=form)
    else:
        f = request.form
        item = formToRecord(f)
        dao.updateItem(f['_objectId'], item)
        flash('Item ' + item['title'] + " updated.")
        return redirect(url_for('index'))

@app.route("/catalog/<category_name>/<item_name>/delete", methods=['GET','POST'])
def deleteItem(category_name, item_name):
    if request.method == 'GET':
        form = DeleteForm()
        return render_template('delete.html', form=form)
    else:
        if request.form['btnYes'] is not None:
            dao.deleteItem(item_name)
            flash('Item ' + item_name + " deleted.")
            return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
