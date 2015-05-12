from blitzdb import Document, FileBackend

class Item(Document):
    pass

class Category(Document):
    pass

class DAO():
    def __init__(self, filename="./catalog_blitz.db"):
        self.backend = FileBackend(filename)

    def createCategory():
        pass

    def readCategory():
        pass

    def updateCategory():
        pass

    def deleteCategory():
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
        
    
