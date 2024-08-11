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

def set_collection_permissions(collection_name, read_permission, write_permission):
    collection_id = get_collection_id(collection_name)
    if not collection_id:
        print(f"Failed to set permissions for {collection_name}: Collection not found")
        return

    try:
        databases.update_collection(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            name=collection_name,
            permissions={
                "read": [read_permission],
                "write": [write_permission],
                "create": [write_permission],
                "update": [write_permission],
                "delete": [write_permission]
            }
        )
        print(f"Permissions set for collection {collection_name}")
    except Exception as e:
        print(f"Error setting permissions for collection {collection_name}: {type(e).__name__}: {str(e)}")

# Define permissions for each collection
collections_permissions = [
    {"name": "DailyEntry", "read": "any", "write": "user:{{user_id}}"},
    {"name": "FoodItem", "read": "any", "write": "user:{{user_id}}"},
    {"name": "ExerciseItem", "read": "any", "write": "user:{{user_id}}"},
    {"name": "CaffeineIntake", "read": "any", "write": "user:{{user_id}}"},
    {"name": "CaffeineSource", "read": "any", "write": "user:{{user_id}}"},
    {"name": "SweetsIntake", "read": "any", "write": "user:{{user_id}}"}
]

# Set permissions for each collection
for collection in collections_permissions:
    set_collection_permissions(collection["name"], collection["read"], collection["write"])

print("Permissions setting process completed.")