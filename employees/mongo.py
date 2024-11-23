from pymongo import MongoClient


myClient = MongoClient("mongodb://localhost:27017")

mydatabase = myClient['Employee_Management'] 
employee_collection = mydatabase['Employee']

