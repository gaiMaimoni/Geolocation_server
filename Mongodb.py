import requests
from pymongo import MongoClient,ASCENDING


class DB:

    def __init__(self, settings):
        self.is_connect = True
        self.exception_type = None
        try:
            self.client = MongoClient(settings["db_host"], settings["db_port"])
            self.db = self.client.Distances
            self.collection = self.db.a
            self.mh = self.db.max_hits
            # p = self.db.a.index_information()
            # self.db.a.drop_indexes()
            #
            # self.db.a.create_index('location_1', name="locations")
        except Exception as e:
            self.is_connect = False
            self.exception_type = type(e)
            print(e)

    def change_to_my_format(self, loc):
        alphanumeric = [character for character in loc if character.isalnum()]
        new_str = "".join(alphanumeric)
        return new_str.lower()

    def insert(self, location_1, location_2, distance):
        location_1 = self.change_to_my_format(location_1)
        location_2 = self.change_to_my_format(location_2)
        new_info = {"location_1": location_1, "location_2": location_2, "distance": distance, "hits": 1}
        try:
            self.collection.insert_one(new_info)
        except Exception as e:
            self.is_connect = False
            self.exception_type = type(e)

    def update(self,data):
        info = self.find_distances_by_locations(data["location_1"], data["location_2"], False)
        if info == None:
            data["hits"] = 0
            data["destination"] += " km"
            info = data
        else:
            self.collection.update({"_id": info["_id"]}, {"$set": {"distance": (str(data["distance"])+" km")}})
        # max_info = self.mh.find_one()
        # if max_info["hits"] < (info["hits"]):
        #         self.mh.update({"_id": max_info["_id"]}, {"$set": {"top":  info["_id"], "hits": info["hits"]}})
        return {"source": info["location_1"], "destination": info["location_2"], "hits": info["hits"]}

    def get_max_hits(self):
        max_info = self.mh.find_one()
        return self.collection.find_one({"_id": max_info["top"]})

    def find_distances_by_locations(self, loc_1, loc_2, updte_hits=True):
        loc_1 = self.change_to_my_format(loc_1)
        loc_2 = self.change_to_my_format(loc_2)
        try:
            
            data = self.collection.find_one({"$or": [{"location_1": loc_1, "location_2": loc_2}, {"location_2": loc_1, "location_1": loc_2}]})
            if data != None:
                self.collection.update({"_id": data["_id"]}, {"$set": {"hits": (data["hits"]+1)}})
                max_info = self.mh.find_one()
                if max_info["hits"] < (data["hits"]+1 and updte_hits):
                    self.mh.update({"_id": max_info["_id"]}, {"$set": {"top":  data["_id"], "hits": data["hits"]+1}})
        except Exception as e:
            self.is_connect = False
            self.exception_type = type(e)
            return None
        return data


if __name__ == '__main__':
    db = DB()
    db.find_distances_by_locations("telaviv", "jerusalem")
