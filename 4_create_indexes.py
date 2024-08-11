import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases

# Load environment variables
load_dotenv()

# Initialize Appwrite client
client = Client()
client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
client.set_key(os.getenv('APPWRITE_API_KEY'))

# Initialize the database service
databases = Databases(client)

# Use the database ID from environment variables
DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID')

def get_collection_id(collection_name):
    try:
        collections = databases.list_collections(DATABASE_ID)
        for collection in collections['collections']:
            if collection['name'] == collection_name:
                return collection['$id']
        print(f"Collection '{collection_name}' not found")
        return None
    except Exception as e:
        print(f"Error getting collection ID for '{collection_name}': {str(e)}")
        return None

def create_index(collection_id, key, type, attributes):
    try:
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key=key,
            type=type,
            attributes=attributes
        )
        print(f"Index '{key}' created successfully for collection '{collection_id}'")
    except Exception as e:
        print(f"Error creating index '{key}' for collection '{collection_id}': {str(e)}")

# Define indexes for each collection
indexes = [
    {"collection": "DailyEntry", "key": "idx_date", "type": "key", "attributes": ["date"]},
    {"collection": "FoodItem", "key": "idx_name", "type": "fulltext", "attributes": ["name"]},
    {"collection": "ExerciseItem", "key": "idx_type", "type": "key", "attributes": ["type"]},
    {"collection": "CaffeineIntake", "key": "idx_total_caffeine", "type": "key", "attributes": ["total_caffeine"]},
    {"collection": "SweetsIntake", "key": "idx_consumed", "type": "key", "attributes": ["consumed"]}
]

# Create indexes
for index in indexes:
    collection_id = get_collection_id(index["collection"])
    if collection_id:
        create_index(collection_id, index["key"], index["type"], index["attributes"])
    else:
        print(f"Skipping index creation for {index['key']} due to missing collection")

print("Index creation process completed.")