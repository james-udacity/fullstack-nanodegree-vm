from blitzdb import Document, FileBackend

class Item(Document):
    pass

class Category(Document):
    pass

categories = ["Soccer", "Basketball", "Baseball", "Frisbee", "Snowboarding"\
              "Rock Climbing", "Foosball", "Skating", "Hockey"]

class DAO():
    def __init__(self, filename="./catalog_blitz.db"):
        self.backend = FileBackend(filename)
        # Check to see if the db has no categories, if so
        # Populate it
        result = self.backend.filter(Category, {})
        if result.__len__() == 0:
            for category_name in categories:
                self.backend.save(Category({'name':category_name}))
                self.backend.commit()


    def serialize(self, obj):
        pass

    def getCategories(self):
        return self.backend.filter(Category, {})

    def getItems(self):
        ## Sort this by timestamp later
        return self.backend.filter(Item, {})

    def getItemsInCategory(self, category):
        pass

    def getCategory(self, category_name):
        category = self.backend.get(Category, {'name':category_name})
        print category
        return category

    def getItemByName(self, item_name):
        item = self.backend.get(Item, {'title':item_name})
        return item
    # Items

    def createItem(self, item):
        result = self.backend.save(item)
        self.backend.commit()
        return result

    def readItem(self, item):
        pass

    def updateItem(self, item):
        pass

    def deleteItem(self, item):
        pass
