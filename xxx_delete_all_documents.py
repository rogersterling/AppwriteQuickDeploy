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

def delete_all_documents(collection_name):
    collection_id = get_collection_id(collection_name)
    if not collection_id:
        print(f"Failed to delete documents from {collection_name}: Collection not found")
        return

    try:
        documents = databases.list_documents(DATABASE_ID, collection_id)
        for doc in documents['documents']:
            databases.delete_document(DATABASE_ID, collection_id, doc['$id'])
            print(f"Deleted document from {collection_name}: {doc['$id']}")
    except Exception as e:
        print(f"Error deleting documents from {collection_name}: {str(e)}")

def delete_all_data():
    collections = ["DailyEntry", "FoodItem", "ExerciseItem", "CaffeineIntake", "CaffeineSource", "SweetsIntake"]
    for collection in collections:
        delete_all_documents(collection)

if __name__ == "__main__":
    print("Starting data deletion process...")
    delete_all_data()
    print("Data deletion process completed.")