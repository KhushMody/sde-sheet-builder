from ..models import db
import pandas as pd
from sqlalchemy import text
import logging
from ..utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def get_data(company_name):
    if company_name:
        # Use a raw SQL query to fetch all questions for the given company
        sql_query = text(f"SELECT * FROM question WHERE company = :company_name")
        
        # Execute the query with a parameter to prevent SQL injection
        result = db.session.execute(sql_query, {'company_name': company_name})

        # Fetch all rows and convert them to a list of dictionaries
        rows = result.mappings().all()

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(rows)
        logger.info(df.head())
        logger.info(f"DataFrame created with {len(df)} rows")

    else:
        df = pd.DataFrame()
    
    return df