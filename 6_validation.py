import os
import json
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def validate_collection_existence(collection_name):
    try:
        collections = databases.list_collections(DATABASE_ID)
        for collection in collections['collections']:
            if collection['name'] == collection_name:
                logging.info(f"Collection '{collection_name}' exists.")
                return collection['$id']
        logging.error(f"Collection '{collection_name}' does not exist.")
        return None
    except Exception as e:
        logging.error(f"Error validating collection '{collection_name}': {str(e)}")
        return None

def validate_collection_attributes(collection_id, expected_attributes):
    try:
        attributes = databases.list_attributes(DATABASE_ID, collection_id)
        existing_attributes = {attr['key']: attr['type'] for attr in attributes['attributes']}
        
        for attr, attr_type in expected_attributes.items():
            if attr not in existing_attributes:
                logging.error(f"Attribute '{attr}' is missing in the collection.")
            elif existing_attributes[attr] != attr_type:
                logging.error(f"Attribute '{attr}' has incorrect type. Expected {attr_type}, got {existing_attributes[attr]}.")
            else:
                logging.info(f"Attribute '{attr}' is correctly configured.")
    except Exception as e:
        logging.error(f"Error validating attributes for collection {collection_id}: {str(e)}")

def validate_relationship(parent_collection, child_collection, relationship_key):
    parent_id = validate_collection_existence(parent_collection)
    child_id = validate_collection_existence(child_collection)
    
    if parent_id and child_id:
        try:
            attributes = databases.list_attributes(DATABASE_ID, parent_id)
            for attr in attributes['attributes']:
                if attr['key'] == relationship_key and attr['type'] == 'relationship':
                    logging.info(f"Relationship '{relationship_key}' between {parent_collection} and {child_collection} exists.")
                    return
            logging.error(f"Relationship '{relationship_key}' between {parent_collection} and {child_collection} is missing.")
        except Exception as e:
            logging.error(f"Error validating relationship: {str(e)}")

def load_data_model():
    with open('_dataModel.json', 'r') as f:
        return json.load(f)

def run_validation():
    data_model = load_data_model()
    
    # Validate collections
    collections = [collection['name'] for collection in data_model['collections']]
    for collection in collections:
        validate_collection_existence(collection)
    
    # Validate attributes
    for collection in data_model['collections']:
        collection_id = validate_collection_existence(collection['name'])
        if collection_id:
            expected_attributes = {attr['key']: attr['type'] for attr in collection['attributes']}
            validate_collection_attributes(collection_id, expected_attributes)
    
    # Validate relationships
    relationships = []
    for collection in data_model['collections']:
        for attr in collection['attributes']:
            if attr.get('type') == 'relationship':
                relationships.append((collection['name'], attr['related_collection'], attr['key']))
    
    for parent, child, key in relationships:
        validate_relationship(parent, child, key)

if __name__ == "__main__":
    run_validation()
    logging.info("Validation process completed.")