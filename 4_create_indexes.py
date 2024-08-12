import os
import json
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

def load_data_model():
    with open('_dataModel.json', 'r') as f:
        return json.load(f)

def create_indexes():
    data_model = load_data_model()
    
    for collection in data_model['collections']:
        collection_id = get_collection_id(collection['name'])
        if not collection_id:
            print(f"Skipping index creation for {collection['name']} due to missing collection")
            continue
        
        for index in collection.get('indexes', []):
            create_index(collection_id, index['key'], index['type'], index['attributes'])

if __name__ == "__main__":
    create_indexes()
    print("Index creation process completed.")