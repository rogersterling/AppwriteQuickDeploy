import os
import json
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

        attribute_type = attr['type'].lower()
        kwargs = {
            "database_id": DATABASE_ID,
            "collection_id": collection_id,
            "key": attr['key'],
            "required": attr.get('required', False)
        }

        if attribute_type == 'string':
            databases.create_string_attribute(**kwargs, size=attr.get('size', 255))
        elif attribute_type == 'integer':
            databases.create_integer_attribute(**kwargs)
        elif attribute_type == 'float':
            databases.create_float_attribute(**kwargs)
        elif attribute_type == 'boolean':
            databases.create_boolean_attribute(**kwargs)
        elif attribute_type == 'datetime':
            databases.create_datetime_attribute(**kwargs)
        elif attribute_type == 'enum':
            databases.create_enum_attribute(**kwargs, elements=attr['elements'])
        elif attribute_type == 'ip':
            databases.create_ip_attribute(**kwargs)
        elif attribute_type == 'email':
            databases.create_email_attribute(**kwargs)
        elif attribute_type == 'url':
            databases.create_url_attribute(**kwargs)
        elif attribute_type == 'relationship':
            databases.create_relationship_attribute(**kwargs, 
                                                    related_collection_id=attr['related_collection_id'],
                                                    type=attr['relationship_type'])
        else:
            print(f"Unsupported attribute type: {attr['type']}")
            return

        if attr.get('array', False):
            databases.update_attribute(DATABASE_ID, collection_id, attr['key'], array=True)

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

# Load data model from JSON file
with open('_dataModel.json', 'r') as f:
    data_model = json.load(f)

# Main execution
if __name__ == "__main__":
    print_env_vars()
    delete_all_collections()
    print(f"Total collections to create: {len(data_model['collections'])}")
    for index, collection in enumerate(data_model['collections'], start=1):
        print(f"\nAttempting to create collection {index}/{len(data_model['collections'])}: {collection['name']}")
        collection_id = create_collection(collection['name'], collection['attributes'])
        if collection_id:
            print(f"{collection['name']} ID: {collection_id}")
            for attr in collection['attributes']:
                create_attribute(databases, DATABASE_ID, collection_id, attr)
        else:
            print(f"Failed to create {collection['name']}")
        print("---")
    print("Script execution completed.")