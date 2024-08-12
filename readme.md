# Appwrite Full-Stack Quick Setup

## Project Overview

This project provides a streamlined method for rapidly deploying full-stack applications using the Appwrite API. The core concept is to enable developers to swiftly prototype and set up backend infrastructure for various application ideas using a single JSON configuration file.

## Key Features

- Rapid backend setup using Appwrite
- Data model abstraction through a single JSON configuration file
- Automated collection creation and relationship management
- Index creation for optimized queries
- Data seeding for testing and development

## How to Use

1. Create a project in the Appwrite GUI.
2. Obtain the API key and Project ID from your Appwrite project.
3. Copy the `.env-Sample` file to `.env` and enter your API key and Project ID.
4. Use an AI assistant (like Claude or ChatGPT) to generate a `dataModel.json` file for your app:
   - Copy the sample `dataModel.json` into the AI chat.
   - Describe your app idea and ask the AI to recreate the data model accordingly.
   - Copy the JSON output from the AI into the `dataModel.json` file in your project.
5. (Recommended) Update the `_spec.md` file similarly:
   - Use an AI to update the file based on your app idea.
   - Copy the AI's output back into the project's `_spec.md` file.
6. Run each script sequentially to set up your Appwrite backend.

## Data Model Configuration

The `dataModel.json` file is the core of your application's backend setup. It defines collections, attributes, indexes, and optionally, relationships. The setup scripts will use this file to configure your Appwrite backend automatically.

## Scripts

The project includes several Python scripts for setting up and managing the Appwrite backend:

1. `1_setup_appwrite.py`: Creates the initial database
2. `2_create_collections.py`: Creates all necessary collections based on `dataModel.json`
3. `3_create_relationships.py`: Sets up relationships between collections (if specified in `dataModel.json`)
4. `4_create_indexes.py`: Creates indexes for improved query performance
5. `5_set_permissions.py`: Sets permissions for collections
6. `6_validation.py`: Validates the setup of collections, attributes, and relationships
7. `7_seed_data.py`: Populates the database with sample data for testing

Run these scripts in order to set up your project.

## Customization

To adapt this setup for your application:

1. Modify the `dataModel.json` file to match your application's data structure.
2. Update the `_spec.md` file to provide context for your project.
3. Run the setup scripts to configure your Appwrite backend.

## Error Handling

The scripts include basic error handling and logging. Check the console output for any errors during setup and execution.

## Data Seeding

The `7_seed_data.py` script provides functionality to populate the database with sample data. This can be useful for testing and development purposes.

## Conclusion

This project streamlines the process of setting up a full-stack application using Appwrite. By using a single JSON configuration file, developers can rapidly prototype and iterate on their application ideas. The automated backend setup allows you to focus primarily on front-end development and core application logic.

For more detailed information about using Appwrite's API, refer to the official Appwrite documentation.