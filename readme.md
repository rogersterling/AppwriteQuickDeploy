# Appwrite Full-Stack Quick Setup

## Project Overview

This project provides a streamlined method for rapidly deploying full-stack applications using the Appwrite API. While the example implementation demonstrates a Diet Tracker app, the core concept is to enable developers to swiftly prototype and set up backend infrastructure for various application ideas.

## Key Features

- Rapid backend setup using Appwrite
- Automated collection creation and relationship management
- Index creation for optimized queries
- Data seeding for testing and development

## Future Enhancements

To fully realize the potential of this project, the following enhancements are planned:

1. **Data Model Abstraction**: Implement a single configuration file that defines the entire data model. This will allow new applications to be created by modifying just one file, rather than adjusting multiple scripts.

2. **Extended Appwrite Integration**: Incorporate additional Appwrite features such as authentication, storage, and serverless functions setup through the API.

The ultimate goal is to provide developers with a comprehensive toolkit that handles the backend setup, allowing them to focus primarily on front-end development and core application logic.

## Current Implementation: Diet Tracker

The following documentation outlines the current implementation, which serves as a proof of concept for the quick setup methodology.

### Data Model

The application uses the following collections:

1. DailyEntry
2. FoodItem
3. ExerciseItem
4. CaffeineIntake
5. CaffeineSource
6. SweetsIntake

### Relationships

- DailyEntry has one-to-many relationships with FoodItem and ExerciseItem
- DailyEntry has one-to-one relationships with CaffeineIntake and SweetsIntake
- CaffeineIntake has a one-to-many relationship with CaffeineSource

## API Endpoints

Note: These endpoints are managed by Appwrite and follow Appwrite's API structure. The exact endpoints will depend on your Appwrite project configuration.

### DailyEntry

- **Create a new daily entry**
  - Method: POST
  - Endpoint: `/databases/{databaseId}/collections/{dailyEntryCollectionId}/documents`
  - Required fields: date, protein_total

- **Get a daily entry**
  - Method: GET
  - Endpoint: `/databases/{databaseId}/collections/{dailyEntryCollectionId}/documents/{documentId}`

- **Update a daily entry**
  - Method: PATCH
  - Endpoint: `/databases/{databaseId}/collections/{dailyEntryCollectionId}/documents/{documentId}`

- **Delete a daily entry**
  - Method: DELETE
  - Endpoint: `/databases/{databaseId}/collections/{dailyEntryCollectionId}/documents/{documentId}`

Similar endpoints exist for FoodItem, ExerciseItem, CaffeineIntake, CaffeineSource, and SweetsIntake collections.

## Authentication

Authentication is handled by Appwrite. Users need to be authenticated to perform write operations on the collections. Read operations are set to "any", allowing public access to read data.

## Permissions

Permissions are set at the collection level:

- Read: Any user can read data from all collections
- Write: Only authenticated users can write to the collections

## Indexes

Indexes have been created to improve query performance:

- DailyEntry: Index on the "date" field
- FoodItem: Fulltext index on the "name" field
- ExerciseItem: Index on the "type" field
- CaffeineIntake: Index on the "total_caffeine" field
- SweetsIntake: Index on the "consumed" field

## Setup and Configuration

The project uses environment variables for configuration. Ensure you have a `.env` file with the following variables:

- APPWRITE_ENDPOINT
- APPWRITE_PROJECT_ID
- APPWRITE_API_KEY
- APPWRITE_DATABASE_ID

## Scripts

The project includes several Python scripts for setting up and managing the Appwrite backend:

1. `1_setup_appwrite.py`: Creates the initial database
2. `2_create_collections.py`: Creates all necessary collections
3. `3_create_relationships.py`: Sets up relationships between collections
4. `4_create_indexes.py`: Creates indexes for improved query performance
5. `5_set_permissions_NOT_WORKING_SET_MANUALLY.py`: Sets permissions for collections (note: this script is not working, set permissions manually)
6. `6_validation.py`: Validates the setup of collections, attributes, and relationships
7. `7_seed_data.py`: Populates the database with sample data for testing

To set up the project, run these scripts in order. Make sure to set permissions manually as script 5 is not functioning correctly.

## Error Handling

The scripts include basic error handling and logging. Check the console output for any errors during setup and execution.

## Data Seeding

The `7_seed_data.py` script provides functionality to populate the database with sample data. This can be useful for testing and development purposes.

## Customization

To adapt this setup for a different application:

1. Modify the data model in `spec.md`
2. Adjust the collection creation script (`2_create_collections.py`)
3. Update the relationship creation script (`3_create_relationships.py`)
4. Modify the index creation script (`4_create_indexes.py`) as needed
5. Adjust the data seeding script (`7_seed_data.py`) to match your new data model

## Conclusion

This project aims to streamline the process of setting up a full-stack application using Appwrite. By automating the backend setup, developers can rapidly prototype and iterate on their application ideas. Future enhancements will further simplify the customization process, making it even easier to spin up new applications with minimal configuration.

For more detailed information about using Appwrite's API, refer to the official Appwrite documentation.