from django.core.management.base import BaseCommand
from sqlalchemy import create_engine,text

class Command(BaseCommand):
    help = 'Fetch data using SQLAlchemy from the PostgreSQL database'

    def handle(self, *args, **kwargs):
        
        DATABASE_URL = "postgresql://nehal:1234@localhost:5432/social"
        engine = create_engine(DATABASE_URL)

        
        query = text("SELECT * FROM myapp_customuser")

        
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

            
            for row in rows:
                print(row)