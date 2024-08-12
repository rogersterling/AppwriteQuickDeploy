import os
import json
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.permission import Permission
from appwrite.role import Role

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

def set_collection_permissions(collection_name, permissions):
    collection_id = get_collection_id(collection_name)
    if not collection_id:
        print(f"Failed to set permissions for {collection_name}: Collection not found")
        return

    try:
        formatted_permissions = []
        for perm in permissions:
            action, role = perm.split('(')
            role = role.strip('")')
            if role == 'any':
                formatted_permissions.append(getattr(Permission, action)(Role.any()))
            elif role == 'users':
                formatted_permissions.append(getattr(Permission, action)(Role.users()))
            else:
                formatted_permissions.append(getattr(Permission, action)(Role.team(role)))

        databases.update_collection(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            name=collection_name,
            permissions=formatted_permissions
        )
        print(f"Permissions set for collection {collection_name}")
    except Exception as e:
        print(f"Error setting permissions for collection {collection_name}: {type(e).__name__}: {str(e)}")

def load_data_model():
    with open('_dataModel.json', 'r') as f:
        return json.load(f)

def set_permissions():
    data_model = load_data_model()
    
    for collection in data_model['collections']:
        if 'permissions' in collection:
            set_collection_permissions(collection['name'], collection['permissions'])
        else:
            print(f"No permissions specified for collection {collection['name']}")

if __name__ == "__main__":
    print("Starting permissions setting process...")
    set_permissions()
    print("Permissions setting process completed.")