import pymongo
from bson import ObjectId

# Create a connection to the local MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access a specific database or create a new one
db = client["admin"]

# Access a specific collection within the database
collection = db["t"]

print("connection done")

###############################################   Insertion   #########################################
# to save data
# data = {"name": "RAM"}
# collection.insert_one(data)

# To save img
# with open("C:/Users/kumar/PycharmProjects/mdb/pk.png", "rb") as image_file:
#     binary_data = image_file.read()
#     document = {"image_data": binary_data}
#     collection.insert_one(document)


# with open("C:/Users/kumar/PycharmProjects/mdb/t1.mp4", "rb") as video_file:
#     binary_data = video_file.read()
#     document = {"video_data": binary_data}
#     collection.insert_one(document)

###############################################   Extraction   #########################################

# Query to retrieve the document containing the image data
query = {"_id": ObjectId("652d441fd9418e9339f8e261")}  # Replace "document_id" with the actual document's _id

# Retrieve the document
document = collection.find_one(query)

if document:
    # Extract image data from the document
    image_data = document.get("video_data")
    print(image_data)
    if image_data:
        with open("output_vid.mp4", "wb") as image_file:
            image_file.write(image_data)

# Close the MongoDB connection
client.close()
