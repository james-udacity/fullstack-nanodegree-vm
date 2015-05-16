import json
import datetime
import requests
from dao import DAO
from sessions import MongoSessionInterface
from forms import CreateItemForm, DeleteForm
from flask import Flask, request, render_template, \
    url_for, redirect, flash, session

app = Flask(__name__)
app.config.from_object(__name__)
app.session_interface = MongoSessionInterface(db='catalog')
app.secret_key = '\xf3\xab\xbe\xa0{\xc9\xcc\x892]_H\xc7\xd2}*\x10\xf7\xa0\x8eI\xa0\xc3H'
METHODS = ['GET', 'POST']
dao = DAO()


def check_acl():
    """Checks to see if a valid session is present.
    If not, it notifies the user.
    """
    if session.get('email') is None:
        flash("You aren't authorized to create, edit, or delete items."
              " Please sign in.")
        return None
    return True


@app.route("/login", methods=['POST'])
def login():
    assertion = request.form['assertion']
    payload = {'assertion': assertion, 'audience': 'http://localhost:8080'}
    req = requests.post('https://verifier.login.persona.org/verify',
                      data=payload)
    result = json.loads(req.text)
    if result['status'] == 'okay':
        # Login successful
        session['email'] = result.get('email')
        session['expiration'] = result.get('expires')
    return json.dumps(result)


@app.route("/logout", methods=METHODS)
def logout():
    if request.method == 'GET':
        # Clear the session
        flash("Logged out.")
        session.clear()
        return redirect(url_for('index'))
    else:
        return ""


@app.route("/")
@app.route("/catalog")
def index():
    cats = dao.get_categories()
    items = dao.get_items()
    return render_template('index.html', categories=cats,
                           items=items, session=session)


@app.route("/catalog.json")
def catalog_json():
    return dao.to_json()


@app.route("/catalog/<category_name>")
@app.route("/catalog/<category_name>/items")
def show_category(category_name):
    cats = dao.get_categories()
    category = dao.get_category(category_name)
    items = dao.get_items_in_category(category)
    return render_template('showCategory.html', category=category,
                           categories=cats, items=items, session=session)


@app.route("/catalog/items/create", methods=METHODS)
def create_item():
    if check_acl() is None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        form = CreateItemForm()
        cats = dao.get_categories()
        form.category.choices = [(g['_id'], g['name']) for g in cats]
        return render_template('create.html', form=form, session=session)
    else:
        form = request.form
        item = form_to_record(form)
        dao.create_item(item)
        flash('Item ' + item['title'] + " created.")
        return redirect(url_for('index'))


def form_to_record(f):
    item = {'cat_id': f['category'], 'description': f['description'],
            'title': f['title'], 'timestamp': datetime.datetime.utcnow()}
    return item


@app.route("/catalog/<category>/<item_name>")
def show_item(category, item_name):
    item = dao.get_item_by_name(item_name)
    return render_template('show.html', item=item,
                           category_name=category, session=session)


@app.route("/catalog/<category_name>/<item_name>/edit", methods=METHODS)
def edit_item(category_name, item_name):
    # Check the session
    if check_acl() is None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        form = CreateItemForm()
        cats = dao.get_categories()
        form.category.choices = [(g['_id'], g['name']) for g in cats]
        item = dao.get_item_by_name(item_name)
        form._objectId = item['_id']
        form.category.process_data(item.get('cat_id'))
        form.title.process_data(item.get('title'))
        form.description.process_data(item.get('description'))
        return render_template('edit.html', form=form, session=session)
    else:
        form = request.form
        item = form_to_record(form)
        dao.update_item(form['_objectId'], item)
        flash('Item ' + item['title'] + " updated.")
        return redirect(url_for('index'))


@app.route("/catalog/<category_name>/<item_name>/delete", methods=METHODS)
def delete_item(category_name, item_name):
    # Check the session
    if check_acl() is None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        form = DeleteForm()
        return render_template('delete.html', form=form, session=session)
    else:
        if request.form['btnYes'] is not None:
            dao.delete_item(item_name)
            flash('Item ' + item_name + " deleted.")
            return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
