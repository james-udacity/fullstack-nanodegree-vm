from flask import Flask, request, render_template, url_for
from dao import DAO, Item
from forms import CreateItemForm, DeleteForm

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'development key'

dao = DAO()
cats = dao.getCategories()
print "hello"


@app.route("/")
@app.route("/catalog")
def index():
    items = dao.getItems()
    print items
    return render_template('index.html', categories=cats, items=items)

@app.route("/catalog.json")
def catalogJSON():
    return dao.serialize(cats)

@app.route("/catalog/<category_name>")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    category = dao.getCategory(category_name)
    if request.method == 'GET':
        items = dao.getItemsInCategory(category)
        print items.__len__()
        return render_template('showCategory.html', category=category, categories=cats, items=items)

@app.route("/catalog/items/create", methods=['POST', 'GET'])
def createItem():
    if request.method == 'GET':
        form = CreateItemForm()
        form.category.choices = [(g.get('pk'), g.get('name')) for g in cats]
        return render_template('create.html', form=form)
    else:
        f = request.form
        item = Item({'cat_id':f['category'], 'description':f['description'],\
            'title':f['title']})
        dao.createItem(item)
        return "fff"


@app.route("/catalog/<category>/<item_name>")
def showItem(category, item_name):
    item = dao.getItemByName(item_name)
    return render_template('show.html', item=item, category_name=category)

@app.route("/catalog/<category_name>/<item_name>/edit", methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if request.method == 'GET':
        form = CreateItemForm()
        form.category.choices = [(g.get('pk'), g.get('name')) for g in cats]
        item = dao.getItemByName(item_name)
        form.category.process_data(item.get('cat_id'))
        form.title.process_data(item.get('title'))
        form.description.process_data(item.get('description'))
        return render_template('edit.html', form=form)
    else:
        return 'do stuff'

@app.route("/catalog/<category_name>/<item_name>/delete", methods=['GET','POST'])
def deleteItem(category_name, item_name):
    if request.method == 'GET':
        form = DeleteForm()
        return render_template('delete.html', form=form)
    else:
        if request.form['btnYes'] is not None:
            dao.deleteItem(item_name)
        print request.form
        return "dfd"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
