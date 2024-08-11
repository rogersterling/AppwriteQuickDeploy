import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

def print_env_vars():
    print("Environment variables:")
    print(f"APPWRITE_ENDPOINT: {os.getenv('APPWRITE_ENDPOINT')}")
    print(f"APPWRITE_PROJECT_ID: {os.getenv('APPWRITE_PROJECT_ID')}")
    print(f"APPWRITE_DATABASE_ID: {os.getenv('APPWRITE_DATABASE_ID')}")
    print("APPWRITE_API_KEY: [REDACTED]")
    print("---")

def create_collection(name, attributes):
    try:
        # Check if collection already exists
        existing_collections = databases.list_collections(DATABASE_ID)
        for collection in existing_collections['collections']:
            if collection['name'] == name:
                print(f"Collection '{name}' already exists. Skipping creation.")
                return collection['$id']

        # If not exists, create new collection
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name=name
        )
        print(f"Collection created: {collection['name']}")
        
        for attr in attributes:
            # Check if attribute already exists
            existing_attributes = databases.list_attributes(DATABASE_ID, collection['$id'])
            if any(existing_attr['key'] == attr['key'] for existing_attr in existing_attributes['attributes']):
                print(f"Attribute '{attr['key']}' already exists. Skipping creation.")
                continue

            databases.create_string_attribute(
                database_id=DATABASE_ID,
                collection_id=collection['$id'],
                key=attr['key'],
                size=attr['size'],
                required=attr['required']
            )
            print(f"Attribute created: {attr['key']}")
        
        return collection['$id']
    except Exception as e:
        print(f"Error creating collection {name}: {str(e)}")
        return None

def cleanup_duplicate_collections():
    try:
        existing_collections = databases.list_collections(DATABASE_ID)
        collection_names = {}
        for collection in existing_collections['collections']:
            if collection['name'] in collection_names:
                print(f"Deleting duplicate collection: {collection['name']} (ID: {collection['$id']})")
                databases.delete_collection(DATABASE_ID, collection['$id'])
            else:
                collection_names[collection['name']] = collection['$id']
        print("Cleanup completed.")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

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

# Define collections and their attributes
collections = [
    {
        "name": "DailyEntry",
        "attributes": [
            {"key": "date", "size": 10, "required": True},
            {"key": "protein_total", "size": 10, "required": True},
            {"key": "notes", "size": 1000, "required": False},
            {"key": "contextual_summary", "size": 2000, "required": False}
        ]
    },
    {
        "name": "FoodItem",
        "attributes": [
            {"key": "name", "size": 100, "required": True},
            {"key": "portion_size", "size": 50, "required": True},
            {"key": "protein", "size": 10, "required": True},
            {"key": "meal_type", "size": 20, "required": True},
            {"key": "estimated_calories", "size": 10, "required": False}
        ]
    },
    {
        "name": "ExerciseItem",
        "attributes": [
            {"key": "type", "size": 50, "required": True},
            {"key": "duration", "size": 10, "required": True},
            {"key": "intensity", "size": 20, "required": False},
            {"key": "calories_burned", "size": 10, "required": False}
        ]
    },
    {
        "name": "CaffeineIntake",
        "attributes": [
            {"key": "total_caffeine", "size": 10, "required": True}
        ]
    },
    {
        "name": "CaffeineSource",
        "attributes": [
            {"key": "name", "size": 50, "required": True},
            {"key": "amount", "size": 20, "required": True},
            {"key": "caffeine_content", "size": 10, "required": True}
        ]
    },
    {
        "name": "SweetsIntake",
        "attributes": [
            {"key": "consumed", "size": 5, "required": True},
            {"key": "details", "size": 500, "required": False}
        ]
    }
]

# Main execution
if __name__ == "__main__":
    print_env_vars()
    cleanup_duplicate_collections()
    print(f"Total collections to create: {len(collections)}")
    for index, collection in enumerate(collections, start=1):
        print(f"\nAttempting to create collection {index}/{len(collections)}: {collection['name']}")
        collection_id = create_collection(collection['name'], collection['attributes'])
        if collection_id:
            print(f"{collection['name']} ID: {collection_id}")
        else:
            print(f"Failed to create {collection['name']}")
        print("---")
    print("Script execution completed.")