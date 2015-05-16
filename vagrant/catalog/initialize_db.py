import csv
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

# Drop database
client.drop_database('catalog')

db = client['catalog']

# Setup collections for Categories
categories = db['categories']
items = db['items']

# Populate DB from CSV file
with open('itemlist.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[0] == "Category":
            pass
        else:
            category_name = row[0]
            category = categories.find_one({'name': category_name})
            if category is None:
                categories.insert_one({'name': category_name})
                category = categories.find_one({'name': category_name})
            items.insert_one({'title': row[1], 'description': row[2],
                              'cat_id': str(category['_id'])})

# Close connection to DB
client.close()
