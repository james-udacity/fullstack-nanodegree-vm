from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

class DAO(object):
    """Manages persistence for Catalog database.


        Attributes:
        client: A MongoClient object used to retrieve a database connection.
        database: A database object that we'll be persisting objects to
        categories: A MongoDB collection holding the list of categories.
        items: A MongoDB collection holding the list of items.
    """
    def __init__(self):
        """Initializes connection to MongoDB
        and populates collection objects.
        """
        self.client = MongoClient()
        self.database = self.client['catalog']

        # Setup collections for Categories
        self.categories = self.database['categories']
        self.items = self.database['items']

    def to_json(self):
        """Constructs a JSON objects to the specs listed in the rubric"""
        json = []
        json_categories = self.categories.find()
        for cat in json_categories:
            temp_json = {'id': str(cat['_id']), 'name': cat['name']}
            items = self.get_items_in_category(cat)
            temp_items = []
            for item in items:
                i = {
                    'cat_id': temp_json['id'],
                    'id': str(item['_id']),
                    'description': item['description'],
                    'title': item['title']
                }
                temp_items.append(i)
            if len(temp_items) > 0:
                temp_json['Item'] = temp_items
            json.append(temp_json)
        return jsonify({'Category': json})

    def get_categories(self):
        """Returns a Cursor holding all the categories in the collection."""

        return self.categories.find()

    def get_items(self):
        """Returns a Cursor holding all the items in the collection."""

        items = []
        cats = self.get_categories()
        for category in cats:
            temp = self.items.find({'cat_id': str(category['_id'])})
            for item in temp:
                item['category_name'] = category['name']
                items.append(item)
        return items

    def get_items_in_category(self, category):
        """Returns the items in a given category."""

        items = self.items.find({"cat_id": str(category['_id'])})
        return items

    def get_category(self, category_name):
        """Returns a category with the given name."""

        category = self.categories.find_one({"name": category_name})
        return category

    def get_item_by_name(self, item_name):
        """Returns the items with a given name."""

        item = self.items.find_one({'title': item_name})
        return item

    # Items

    def create_item(self, item):
        """Stores an item in the database."""

        result = self.items.insert_one(item)
        return result.inserted_id

    def read_item(self, item):
        """Not implemented."""

        pass

    def update_item(self, object_id, item):
        """Updates an item given an item object and an object id."""

        self.items.update({'_id': ObjectId(object_id)}, item)

    def delete_item(self, item_name):
        """Deletes an item given an item name"""

        item = self.get_item_by_name(item_name)
        if item is not None:
            self.items.delete_one({'_id': item['_id']})
