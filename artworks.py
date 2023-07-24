# Author: Mahmoud Abusara
# Date: July 22nd, 2023
# Summary: A mini exhibition of ceramic art from around the world that coincide with the Islamic Abbasid Period.
# Runtime details: Python 3.10 with json, requests and pymongo version 3.10

import json
import requests
from pymongo import MongoClient

# I put the mongodb sensitive information in a config file to make it a bit better security wise
with open("config.json") as config_file:
    config = json.load(config_file)

# Get MongoDB credentials from the configuration file
mongodb_username = config.get("mongodb_username")
mongodb_password = config.get("mongodb_password")
mongodb_cluster = config.get("mongodb_cluster")
database_name = config.get("database_name")
collection_name = config.get("collection_name")

# Check if any of the required configurations is missing
if not (mongodb_username and mongodb_password and mongodb_cluster and database_name and collection_name):
    raise ValueError("Please provide all required MongoDB configurations in the config.json file.")

# Create the MongoDB connection string, this is from my personal mongoDB atlas cluster
mongo_connection_string = f"mongodb+srv://{mongodb_username}:{mongodb_password}@{mongodb_cluster}.3wcaexg.mongodb.net/{database_name}?retryWrites=true&w=majority"


# Function that takes array of artworks and inserts them into the mongoDB collection
def insert_artworks_into_mongodb(artworks):
    # Connect to MongoDB Atlas, Note that I'm running Python 3.10 so I'm not using the newer pymongo syntax/mongodb API to connect
    client = MongoClient(mongo_connection_string)

    try:
        # Access the database and collection
        database = client[database_name]
        collection = database[collection_name]

        # Insert each artwork into the MongoDB collection
        # Note, these art attributes are from the task requirements but the type and creation dates are shared among the exhibition artworks
        insert_one_artwork = lambda art: collection.insert_one({
            "athena_id": art["athena_id"],
            "accession_number": art["accession_number"],
            "tombstone": art["tombstone"],
            "images": art["images"],
            "type": art["type"],
            "creation_date_latest": art["creation_date_latest"],
            "creation_date_earliest": art["creation_date_earliest"],
            "mini_exhibition_identifier": "mini_" + str(art["athena_id"]),
        }) if not collection.find_one({"athena_id": art["athena_id"]}) else print(f"Artwork with athena_id {art['athena_id']} already exists. Skipping insertion.") # Ensure no duplicates are added

        list(map(insert_one_artwork, artworks))
        print("All new exhibition artworks inserted successfully")

    except Exception as e:
        print(f"Error occurred while inserting artwork: {e}")

    finally:
        # Close the MongoDB connection
        client.close()

# Note, I browsed the available exhibitions from the website you linked so I did not find this just using the API. I am a big fan of history, particularly Islamic history so this drew my attention
def get_islamic_art_exhibition():
    base_url = "https://openaccess-api.clevelandart.org/api/exhibitions/"
    search_params = {
        "title": "Art of the Islamic World",
        "limit": 1  # We set the limit to 1 as we want only one exhibition
    }

    try:
        response = requests.get(base_url, params=search_params)
        response.raise_for_status()  # Check for any errors in the response

        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]  # Return the first (and only) exhibition found
        else:
            print("No exhibition found for the Islamic art collection.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API call: {e}")
        return None


# From the Islamic art exhibition, find the oldest piece of art that belongs to the Abbasid Period
# Abbasid period is my favorite era of Islamic civilization
def get_oldest_abbasid_islamic_artwork(exhibition):
    base_url = "https://openaccess-api.clevelandart.org/api/artworks/"
    search_params = {
        "exhibition_history": exhibition,
        "created_after": 750, # These dates for when the Abbasid period starts/ends were taken from Wikipedia
        "created_before": 1258
    }

    try:
        response = requests.get(base_url, params=search_params)
        response.raise_for_status()  # Check for any errors in the response

        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            # Sort artworks by creation_date_earliest to find the oldest
            artworks = sorted(data["data"], key=lambda artwork: artwork["creation_date_earliest"]) # Sort the list to get the one with the earliest creation date
            oldest = artworks[0]
            return oldest # Note that oldest is based only on creation date earliest so there could be a lack of accuracy when comparing one piece of art with another
        else:
            print("No exhibition found for the Islamic art collection.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API call: {e}")
        return None


# Based on the chosen artwork,  create a mini exhibition which shares the oldest artworks which share the same art type and falls within the same time period
# I chose this because I was interested in seeing how ceramic art looked like around the world during the Abbasid Period. I chose the oldest five.
def get_oldest_ceramic_artworks(oldestAbbasidArtwork):
    base_url = "https://openaccess-api.clevelandart.org/api/artworks/"
    search_params = {
        "type": oldestAbbasidArtwork["type"],
        "created_before": oldestAbbasidArtwork["creation_date_latest"],
        "created_after": oldestAbbasidArtwork["creation_date_earliest"]
    }

    try:
        response = requests.get(base_url, params=search_params)
        response.raise_for_status()  # Check for any errors in the response
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            # Sort artworks by creation_date_earliest to find the oldest
            sortedArtworks = sorted(data["data"], key=lambda artwork: artwork["creation_date_earliest"]) # Sort the artworks to grab the five oldest
            return sortedArtworks[:5]
        else:
            print("No artworks found with the specified culture.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API call: {e}")
        return None

if __name__ == "__main__":
    exhibition = get_islamic_art_exhibition()
    
    # Print some exhibition info, including number of artworks
    if exhibition:
        print("Exhibition Title:", exhibition["title"])
        print("Organizer:", exhibition["organizer"])
        print("Opening Date:", exhibition["opening_date"])
        print("Closing Date:", exhibition["closing_date"])
        print("Number of Artworks In Exhibition:", len(exhibition["artworks"]))
    else:
        print("No exhibition found for this collection.")
    
    oldestAbbasidArtwork = get_oldest_abbasid_islamic_artwork(exhibition["title"])
    
    if oldestAbbasidArtwork:
        ceramicExhibition = get_oldest_ceramic_artworks(oldestAbbasidArtwork)
        insert_artworks_into_mongodb(ceramicExhibition)
    else:
        print("No oldest Abbasid artwork found.")
