from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

psql_url = os.getenv("PSQL_URL")

def get_db_engine():
    return create_engine(psql_url, pool_size=3, max_overflow=0)