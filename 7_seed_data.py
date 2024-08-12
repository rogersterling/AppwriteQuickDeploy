import os
import json
import random
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from datetime import datetime, timedelta

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

def create_document(collection_name, data):
    collection_id = get_collection_id(collection_name)
    if not collection_id:
        print(f"Failed to create document for {collection_name}: Collection not found")
        return None

    try:
        document = databases.create_document(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            document_id=ID.unique(),
            data=data
        )
        print(f"Document created in {collection_name}: {document['$id']}")
        return document['$id']
    except Exception as e:
        print(f"Error creating document in {collection_name}: {str(e)}")
        return None

def generate_sample_data(attribute):
    attr_type = attribute['type']
    if attr_type == 'string':
        return f"Sample {attribute['key']}"
    elif attr_type == 'integer':
        return random.randint(1, 100)
    elif attr_type == 'float':
        return random.uniform(1.0, 100.0)
    elif attr_type == 'boolean':
        return random.choice([True, False])
    elif attr_type == 'datetime':
        return (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
    elif attr_type == 'enum':
        return random.choice(attribute['elements'])
    elif attr_type == 'relationship':
        return None  # Relationships will be handled separately
    else:
        return None

def seed_collection(collection, num_documents=5):
    for _ in range(num_documents):
        data = {}
        for attr in collection['attributes']:
            if attr['type'] != 'relationship':
                data[attr['key']] = generate_sample_data(attr)
        create_document(collection['name'], data)

def seed_relationships(data_model):
    for collection in data_model['collections']:
        for attr in collection['attributes']:
            if attr['type'] == 'relationship':
                related_collection = next(c for c in data_model['collections'] if c['name'] == attr['related_collection'])
                related_docs = databases.list_documents(DATABASE_ID, get_collection_id(related_collection['name']))
                
                if related_docs['documents']:
                    docs = databases.list_documents(DATABASE_ID, get_collection_id(collection['name']))
                    for doc in docs['documents']:
                        related_id = random.choice(related_docs['documents'])['$id']
                        databases.update_document(
                            DATABASE_ID,
                            get_collection_id(collection['name']),
                            doc['$id'],
                            {attr['key']: [related_id]}
                        )

def seed_data():
    with open('_dataModel.json', 'r') as f:
        data_model = json.load(f)

    for collection in data_model['collections']:
        seed_collection(collection)

    seed_relationships(data_model)

if __name__ == "__main__":
    print("Starting data seeding process...")
    seed_data()
    print("Data seeding process completed.")