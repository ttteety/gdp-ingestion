import aiohttp 
import asyncio 
import pandas as pd 
from sqlalchemy import create_engine
from typing import List, Dict 
import logging 
from api_extractor import APIExtractor 
from setup_postgres import create_postgres_container
from utility import read_config



async def extract_gdp(url: str) -> List:
    """
    Asynchronously extracts GDP data from World Bank API

    Args:
        url (str): The World Bank API URL

    Returns:
        List: List of DGP data
    """
    world_bank_api = APIExtractor(url)
    gdp = []
    
    async with aiohttp.ClientSession() as session:
        page = 1
        per_page = 1000
        tasks = []
        
        while True:
            task = world_bank_api.extract_api(session, page, per_page)
            tasks.append(task)
            page += 1
            
            if len(tasks) >= 50:
                items = await asyncio.gather(*tasks)
                for item in items:
                    gdp.extend(item)
                tasks = []
                if not  item:
                    break 
                
    logging.info(f"Lenght of items are: {len(gdp)}")
    return gdp 

def load_data(df: pd.DataFrame, connection_params: Dict[str,str], schema_name: str, table_name: str) -> None:
    """
    Load data into a PostgreSQL table.

    Args:
        df (pd.DataFrame): DataFrame containing data to be loaded
        connection_params (Dict[str,str]): Connection parameters for PostgreSQL
        schema_name (str): Name of the schema
        table_name (str): Name of the table
        
    Returns:
        None
        
    Description:
        This function loads data from a DataFrame into a PostgreSQL table.
        It creates the schema if it doens't exist and replaces the existing data in the table.
    """
    db_username = connection_params.get('user')
    db_password = connection_params.get('password')
    db_host = connection_params.get('host')
    db_port = connection_params.get('port')
    db_name = connection_params.get('db_name')
    
    engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    conn = engine.connect()
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='replace', index=False)
    logging.info(f"Data has been loaded successfully into {schema_name}.{table_name}")
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = read_config("config/config.yaml")
    connection_params = config.get('dev').get('database')
    endpoint = config.get('dev').get('gdp_endpoint')    
    gdp_url = endpoint.get('url')
    schema_name = endpoint.get('schema_name')
    table_name = endpoint.get('table_name')
    
    create_postgres_container(connection_params)
    gdp = asyncio.run(extract_gdp(gdp_url))
    df = pd.json_normalize(gdp)
    load_data(df, connection_params,  schema_name, table_name)

