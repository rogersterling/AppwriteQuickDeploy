import os
import json
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

def get_collection_id(collection_name):
    try:
        collections = databases.list_collections(DATABASE_ID)
        for collection in collections['collections']:
            if collection['name'] == collection_name:
                return collection['$id']
        return None
    except Exception as e:
        print(f"Error getting collection ID for {collection_name}: {str(e)}")
        return None

def create_relationship(parent_collection, parent_property, child_collection, type='oneToMany'):
    try:
        parent_id = get_collection_id(parent_collection)
        child_id = get_collection_id(child_collection)
        
        if not parent_id or not child_id:
            print(f"Error: Could not find collection IDs for {parent_collection} or {child_collection}")
            return

        databases.create_relationship_attribute(
            database_id=DATABASE_ID,
            collection_id=parent_id,
            related_collection_id=child_id,
            type=type,
            two_way=False,
            key=parent_property,
            two_way_key='parent_' + parent_collection.lower()
        )
        print(f"Relationship created: {parent_collection}.{parent_property} -> {child_collection}")
    except Exception as e:
        print(f"Error creating relationship {parent_collection}.{parent_property} -> {child_collection}: {str(e)}")

def setup_relationships(data_model):
    relationships = []
    for collection in data_model['collections']:
        for attribute in collection['attributes']:
            if attribute.get('type') == 'relationship':
                relationships.append((
                    collection['name'],
                    attribute['key'],
                    attribute['related_collection'],
                    attribute['relationship_type']
                ))

    if not relationships:
        print("No relationships defined in the data model. Skipping relationship creation.")
        return

    for parent, prop, child, rel_type in relationships:
        create_relationship(parent, prop, child, rel_type)

if __name__ == "__main__":
    # Load data model from JSON file
    with open('_dataModel.json', 'r') as f:
        data_model = json.load(f)

    setup_relationships(data_model)
    print("Relationship setup completed.")