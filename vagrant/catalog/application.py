from flask import Flask, request, render_template, url_for
from dao import DAO

app = Flask(__name__)
app.config.from_object(__name__)

dao = DAO()
cats = dao.getCategories()
print "hello"


@app.route("/")
def index():
    return render_template('index.html', categories=cats)

@app.route("/catalog.json")
def catalogJSON():
    return dao.serialize(cats)

@app.route("/catalog/<category_name>")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    category = dao.getCategory(category_name)
    items = dao.getItemsInCategory(category)
    return render_template('showCategory.html', category=category, categories=cats)

@app.route("/catalog/<category>/item/create", methods=['POST'])
def createItem(category, item):
    return "Stuff"

@app.route("/catalog/<category>/item")
def showItem(category, item):
    return "Stuff"

@app.route("/catalog/<category>/<item>/edit", methods=['GET', 'POST'])
def editItem(category, item):
    if request.method == 'GET':
        return render_template('edit.html', item)

@app.route("/catalog/<category>/<item>/delete", methods=['POST'])
def deleteItem(category, item):
    return "Stuff"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
