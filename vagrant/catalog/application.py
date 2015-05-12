from flask import Flask
from flask import request
from flask import render_template
from dao import DAO

BLITZ_DATABASE = r'./catalog_blitz.db'

app = Flask(__name__)
app.config.from_object(__name__)

db = DAO()

print "hello"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/catalog.json")
def catalogJSON():
    return "Catalog JSON"

@app.route("/catalog/<category>")
def showCategory(category):
    return category

@app.route("/catalog/<category>/item/create", methods=['POST'])
def createItem(category, item):
    return "Stuff"

@app.route("/catalog/<category>/item")
def showItem(category, item):
    return "Stuff"

@app.route("/catalog/<category>/item/edit")
def editItem(category, item):
    return "Stuff"

@app.route("/catalog/<category>/item/delete", methods=['POST'])
def deleteItem(category, item):
    return "Stuff"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
