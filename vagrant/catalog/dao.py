from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

categories = ["Soccer", "Basketball", "Baseball", "Frisbee", "Snowboarding",
              "Rock Climbing", "Foosball", "Skating", "Hockey"]

class DAO():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['catalog']

        # Setup collections for Categories
        self.categories = self.db['categories']
        self.items = self.db['items']

        # Check to see if the db has no categories, if so
        # Populate it
        result = self.categories.find_one()
        if result == None:
            for category_name in categories:
                self.categories.insert_one({'name': category_name})

    # Constructs JSON object per rubric
    def toJSON(self):
        json = []
        categories = self.categories.find()
        for cat in categories:
            tempJson = {}
            tempJson['id'] = str(cat['_id'])
            tempJson['name'] = cat['name']
            items = self.getItemsInCategory(cat)
            list = []
            for item in items:
                i = {
                    'cat_id': tempJson['id'],
                    'id': str(item['_id']),
                    'description': item['description'],
                    'title': item['title']
                }
                list.append(i)
            if len(list) > 0:
                tempJson['Item'] = list
            json.append(tempJson)
        return dumps({'Category': json})

    def getCategories(self):
        return self.categories.find()

    def getItems(self):
        items = []
        cats = self.getCategories()
        for category in cats:
            temp = self.items.find({'cat_id': str(category['_id'])})
            for t in temp:
                t['category_name'] = category['name']
                items.append(t)
        return items

    def getItemsInCategory(self, category):
        print category
        items = self.items.find({"cat_id": str(category['_id'])})
        return items

    def getCategory(self, category_name):
        category = self.categories.find_one({"name": category_name})
        return category

    def getItemByName(self, item_name):
        item = self.items.find_one({'title': item_name})
        return item

    # Items

    def createItem(self, item):
        result = self.items.insert_one(item)
        return result.inserted_id

    def readItem(self, item):
        pass

    def updateItem(self, objectId, item):
        self.items.update({'_id': ObjectId(objectId)}, item)

    def deleteItem(self, item_name):
        item = self.getItemByName(item_name)
        if item is not None:
            self.items.delete_one({'_id': item['_id']})
