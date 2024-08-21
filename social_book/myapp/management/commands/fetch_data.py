from django.core.management.base import BaseCommand
from sqlalchemy import create_engine,text

class Command(BaseCommand):
    help = 'Fetch data using SQLAlchemy from the PostgreSQL database'

    def handle(self, *args, **kwargs):
        # Set up the SQLAlchemy engine using the Django settings
        DATABASE_URL = "postgresql://nehal:1234@localhost:5432/social"
        engine = create_engine(DATABASE_URL)

        # Define the SQL query to fetch data from a table
        query = text("SELECT * FROM myapp_customuser")

        # Execute the query and fetch the data
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

            # Print out each row
            for row in rows:
                print(row)