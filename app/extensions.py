import pymongo

mongo = pymongo.MongoClient("mongodb://localhost:27017/") #Replace the current uri with your data base uri 
mydb = mongo["cool"] #Replace cool with your database name