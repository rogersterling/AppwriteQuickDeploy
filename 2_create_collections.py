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
        
        return collection['$id']
    except Exception as e:
        print(f"Error creating collection {name}: {str(e)}")
        return None

def create_attribute(databases, DATABASE_ID, collection_id, attr):
    try:
        # Check if attribute already exists
        existing_attributes = databases.list_attributes(DATABASE_ID, collection_id)
        if any(existing_attr['key'] == attr['key'] for existing_attr in existing_attributes['attributes']):
            print(f"Attribute '{attr['key']}' already exists. Skipping creation.")
            return

        if attr['type'] == 'string':
            databases.create_string_attribute(
                database_id=DATABASE_ID,
                collection_id=collection_id,
                key=attr['key'],
                size=attr['size'],
                required=attr['required']
            )
        elif attr['type'] == 'integer':
            databases.create_integer_attribute(
                database_id=DATABASE_ID,
                collection_id=collection_id,
                key=attr['key'],
                required=attr['required']
            )
        elif attr['type'] == 'float':
            databases.create_float_attribute(
                database_id=DATABASE_ID,
                collection_id=collection_id,
                key=attr['key'],
                required=attr['required']
            )
        elif attr['type'] == 'boolean':
            databases.create_boolean_attribute(
                database_id=DATABASE_ID,
                collection_id=collection_id,
                key=attr['key'],
                required=attr['required']
            )
        elif attr['type'] == 'datetime':
            databases.create_datetime_attribute(
                database_id=DATABASE_ID,
                collection_id=collection_id,
                key=attr['key'],
                required=attr['required']
            )
        print(f"Attribute created: {attr['key']} (Type: {attr['type']})")
    except Exception as e:
        print(f"Error creating attribute {attr['key']}: {str(e)}")

def delete_all_collections():
    try:
        existing_collections = databases.list_collections(DATABASE_ID)
        for collection in existing_collections['collections']:
            print(f"Deleting collection: {collection['name']} (ID: {collection['$id']})")
            databases.delete_collection(DATABASE_ID, collection['$id'])
        print("All collections deleted.")
    except Exception as e:
        print(f"Error during collection deletion: {str(e)}")

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
            {"key": "date", "type": "datetime", "required": True},
            {"key": "protein_total", "type": "float", "required": True},
            {"key": "notes", "type": "string", "size": 1000, "required": False},
            {"key": "contextual_summary", "type": "string", "size": 2000, "required": False}
        ]
    },
    {
        "name": "FoodItem",
        "attributes": [
            {"key": "name", "type": "string", "size": 100, "required": True},
            {"key": "portion_size", "type": "string", "size": 50, "required": True},
            {"key": "protein", "type": "float", "required": True},
            {"key": "meal_type", "type": "string", "size": 20, "required": True},
            {"key": "estimated_calories", "type": "float", "required": False}
        ]
    },
    {
        "name": "ExerciseItem",
        "attributes": [
            {"key": "type", "type": "string", "size": 50, "required": True},
            {"key": "duration", "type": "integer", "required": True},
            {"key": "intensity", "type": "string", "size": 20, "required": False},
            {"key": "calories_burned", "type": "float", "required": False}
        ]
    },
    {
        "name": "CaffeineIntake",
        "attributes": [
            {"key": "total_caffeine", "type": "float", "required": True}
        ]
    },
    {
        "name": "CaffeineSource",
        "attributes": [
            {"key": "name", "type": "string", "size": 50, "required": True},
            {"key": "amount", "type": "string", "size": 20, "required": True},
            {"key": "caffeine_content", "type": "float", "required": True}
        ]
    },
    {
        "name": "SweetsIntake",
        "attributes": [
            {"key": "consumed", "type": "boolean", "required": True},
            {"key": "details", "type": "string", "size": 500, "required": False}
        ]
    }
]

# Main execution
if __name__ == "__main__":
    print_env_vars()
    delete_all_collections()
    print(f"Total collections to create: {len(collections)}")
    for index, collection in enumerate(collections, start=1):
        print(f"\nAttempting to create collection {index}/{len(collections)}: {collection['name']}")
        collection_id = create_collection(collection['name'], collection['attributes'])
        if collection_id:
            print(f"{collection['name']} ID: {collection_id}")
            for attr in collection['attributes']:
                create_attribute(databases, DATABASE_ID, collection_id, attr)
        else:
            print(f"Failed to create {collection['name']}")
        print("---")
    print("Script execution completed.")