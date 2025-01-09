from sqlite_handler import create_database_from_csv

# Create the database from your CSV file
success = create_database_from_csv('bodyhub_status_log.csv')

if success:
    print("Database created successfully!")
else:
    print("Error creating database")