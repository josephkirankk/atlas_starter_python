import pymongo
import sys

class MongoDBManager:
    def __init__(self, uri):
        try:
            self.client = pymongo.MongoClient(uri)
            self.db = self.client.myDatabase
            self.config_collection = self.db["config"]
        except pymongo.errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
            sys.exit(1)

    def get_config_value(self, key):
        config_doc = self.config_collection.find_one({"name": key})
        if config_doc is None:
            print(f"No value found for key: {key}.")
            return None
        return config_doc["value"]

    def update_config(self, key, value):
        config_doc = self.config_collection.find_one({"name": key})
        if config_doc is None:
            self.config_collection.insert_one({"name": key, "value": value})
            print(f"{key} initialized to {value}.")
        else:
            self.config_collection.update_one({"name": key}, {"$set": {"value": value}})
            print(f"{key} updated to {value}.")

def main():
    mongo_manager = MongoDBManager(
        "mongodb+srv://mongodb:xxxx@uvdb.eobop5a.mongodb.net/?retryWrites=true&w=majority")

    # Update or initialize IP address
    mongo_manager.update_config("ip", "192.168.1.1")
    print(f"Current IP address value: {mongo_manager.get_config_value('ip')}")

    # Update or initialize another config key
    mongo_manager.update_config("example_key", "example_value")
    print(f"Current value for example_key: {mongo_manager.get_config_value('example_key')}")

if __name__ == "__main__":
    main()
