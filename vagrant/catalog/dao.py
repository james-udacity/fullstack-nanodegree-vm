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
        # Check to see if the categories have been initialized
        result = self.backend.filter(Category, {})
        if result.__len__() == 0:
            print "Empty db"

    def createCategories():
        
        pass

    # Items

    def createItem():
        pass

    def readItem():
        pass

    def updateItem():
        pass

    def deleteItem():
        pass
        
    
