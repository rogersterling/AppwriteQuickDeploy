import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import random
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

def check_and_create_relationship():
    relationships = [
        ("FoodItem", "DailyEntry", "daily_entry_id", "food_items"),
        ("ExerciseItem", "DailyEntry", "daily_entry_id", "exercise_items"),
        ("CaffeineIntake", "DailyEntry", "daily_entry_id", "caffeine_intakes"),
        ("CaffeineSource", "CaffeineIntake", "caffeine_intake_id", "caffeine_sources"),
        ("SweetsIntake", "DailyEntry", "daily_entry_id", "sweets_intakes")
    ]

    for child, parent, child_key, parent_key in relationships:
        child_id = get_collection_id(child)
        parent_id = get_collection_id(parent)

        if not child_id or not parent_id:
            print(f"Error: Could not find collection IDs for {child} or {parent}")
            continue

        try:
            collection = databases.get_collection(DATABASE_ID, child_id)
            if any(attr['key'] == child_key for attr in collection['attributes']):
                print(f"Relationship attribute '{child_key}' already exists in {child}")
                continue

            databases.create_relationship_attribute(
                database_id=DATABASE_ID,
                collection_id=child_id,
                related_collection_id=parent_id,
                type='oneToMany',
                two_way=False,
                key=child_key,
                two_way_key=parent_key
            )
            print(f"Relationship attribute '{child_key}' created successfully in {child}")
        except Exception as e:
            print(f"Error checking or creating relationship for {child}: {str(e)}")

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

# Sample data
food_items = [
    {"name": "Chicken Breast", "portion_size": "100g", "protein": 31, "meal_type": "Lunch", "estimated_calories": 165},
    {"name": "Salmon", "portion_size": "150g", "protein": 39, "meal_type": "Dinner", "estimated_calories": 280},
    {"name": "Greek Yogurt", "portion_size": "200g", "protein": 20, "meal_type": "Breakfast", "estimated_calories": 130},
    {"name": "Protein Shake", "portion_size": "1 scoop", "protein": 25, "meal_type": "Snack", "estimated_calories": 120},
]

exercise_items = [
    {"type": "Running", "duration": 30, "intensity": "Moderate", "calories_burned": 300},
    {"type": "Weight Lifting", "duration": 45, "intensity": "Intense", "calories_burned": 200},
    {"type": "Yoga", "duration": 60, "intensity": "Light", "calories_burned": 150},
    {"type": "Swimming", "duration": 40, "intensity": "Moderate", "calories_burned": 400},
]

caffeine_sources = [
    {"name": "Coffee", "amount": "1 cup", "caffeine_content": 95},
    {"name": "Green Tea", "amount": "1 cup", "caffeine_content": 28},
    {"name": "Energy Drink", "amount": "1 can", "caffeine_content": 80},
]

def seed_data():
    check_and_create_relationship()

    for i in range(7):  # Create entries for 7 days
        date = (datetime.now() - timedelta(days=i)).isoformat()
        daily_entry = {
            "date": date,
            "protein_total": random.uniform(80, 150),
            "notes": f"Sample note for day {i+1}",
            "contextual_summary": f"Sample summary for day {i+1}"
        }
        daily_entry_id = create_document("DailyEntry", daily_entry)

        if daily_entry_id:
            # FoodItems
            for _ in range(random.randint(3, 6)):
                food = random.choice(food_items).copy()
                food["daily_entry_id"] = [daily_entry_id]
                create_document("FoodItem", food)

            # ExerciseItems
            for _ in range(random.randint(1, 3)):
                exercise = random.choice(exercise_items).copy()
                exercise["daily_entry_id"] = [daily_entry_id]
                create_document("ExerciseItem", exercise)

            # CaffeineIntake
            caffeine_intake = {
                "total_caffeine": random.uniform(0, 300),
                "daily_entry_id": [daily_entry_id]
            }
            caffeine_intake_id = create_document("CaffeineIntake", caffeine_intake)

            # CaffeineSources
            if caffeine_intake_id:
                for _ in range(random.randint(1, 3)):
                    source = random.choice(caffeine_sources).copy()
                    source["caffeine_intake_id"] = [caffeine_intake_id]
                    create_document("CaffeineSource", source)

            # SweetsIntake
            sweets_intake = {
                "consumed": random.choice([True, False]),
                "details": "Sample sweets intake details" if random.random() > 0.5 else None,
                "daily_entry_id": [daily_entry_id]
            }
            create_document("SweetsIntake", sweets_intake)

if __name__ == "__main__":
    print("Starting data seeding process...")
    seed_data()
    print("Data seeding process completed.")