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

# Function to create the database
def create_database():
    try:
        database = databases.create(database_id=os.getenv('APPWRITE_DATABASE_ID'), name=os.getenv('APPWRITE_DATABASE_NAME'))
        print(f"Database created: {database['name']}")
        return database['$id']
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return None

# Main execution
if __name__ == "__main__":
    db_id = create_database()
    if db_id:
        print(f"Database ID: {db_id}")
    else:
        print("Failed to create database")