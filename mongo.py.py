import pymongo
from bson import ObjectId


class mongoDB:
    def __init__(self, db, table):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = client[db]
        self.collection = self.db[table]

    def insert_data(self, data):
        self.collection.insert_one(data)

    def insert_image(self, img_path):
        with open(img_path, "rb") as image_file:
            binary_data = image_file.read()
            document = {"image_data": binary_data}
            self.collection.insert_one(document)

    def insert_video(self, video_path):
        with open(video_path, "rb") as video_file:
            binary_data = video_file.read()
            document = {"video_data": binary_data}
            self.collection.insert_one(document)

    def get_all_collection(self):
        object_ids = []
        for document in self.collection.find({}, {"_id": 1}):
            object_ids.append(document["_id"])
        return object_ids

    def get_img(self, object_id, output_path):
        query = {"_id": ObjectId(object_id)}

        document = self.collection.find_one(query)

        if document:
            # Extract image data from the document
            image_data = document.get("image_data")
            if image_data:
                with open(output_path, "wb") as image_file:
                    image_file.write(image_data)

    def get_img(self, object_id, output_path):
        query = {"_id": ObjectId(object_id)}

        document = self.collection.find_one(query)

        if document:
            # Extract image data from the document
            image_data = document.get("video_data")
            if image_data:
                with open(output_path, "wb") as video_file:
                    video_file.write(image_data)


dbconnect = mongoDB("admin", "t")
client.close()
