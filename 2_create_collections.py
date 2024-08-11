import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

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

def create_collection(name, attributes):
    try:
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name=name
        )
        print(f"Collection created: {collection['name']}")
        
        for attr in attributes:
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
    # ... (rest of the collections remain the same)
]

# Main execution
if __name__ == "__main__":
    for collection in collections:
        collection_id = create_collection(collection['name'], collection['attributes'])
        if collection_id:
            print(f"{collection['name']} ID: {collection_id}")
        else:
            print(f"Failed to create {collection['name']}")