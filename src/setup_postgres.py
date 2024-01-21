import docker 
import logging 
from typing import Dict

def create_volume(volume_name: str) -> None:
    """
    Create a Docker volume if it doesn't exist.

    Args:
        volume_name (str): The name of the Docker volume.
        
    Returns:
        None
    """
    # Docker client
    client = docker.from_env()
    
    # Check if the volume exists
    try:
        volume = client.volumes.get(volume_name)
        logging.info(f"Volume '{volume_name}' already exists.")
    except:
        # Create the volume if it doesn't exist
        client.volumes.create(volume_name)
        logging.info(f"Volume '{volume_name}' created.")        


def create_postgres_container(
    connection_params:Dict[str, str], 
    container_name:str="postgres"
) -> None:
    """
    Create and start a PostgreSQL Docker container.
    
    Args:
        connection_params (Dict[str, str]): Connection parameters for PostgreSQL,
            Requires 'db_name', 'user', 'password', 'port'
        container_name (str, optional): Name for the Docker container (default is 'postgres')
        
    Returns:
        None
        
    """
    client = docker.from_env()
    
    postgres_image = "postgres:latest"
    environment = {
        "POSTGRES_DB": connection_params.get('db_name'),
        "POSTGRES_USER": connection_params.get('user'),
        "POSTGRES_PASSWORD": connection_params.get('password')
    }
    db_port = connection_params.get('port')

    # Create Docker volume    
    volume_name = "postgres_volume"
    create_volume(volume_name)
    
    try:
        container = client.containers.get(container_name)
        
        if container.status == "exited":
            logging.info(f"Starting container '{container_name}'...")
            container.restart()
            logging.info(f"Container '{container_name}' restarted.")
        else:
            logging.info(f"Container '{container_name}' is running.")

    except docker.errors.NotFound:
            
        container = client.containers.run(
            image = postgres_image,
            name = container_name,
            detach = True,
            ports = {"5432/tcp": db_port},
            environment = environment,
            volumes = {volume_name: {"bind": "/var/lib/postgresql/data", "mode": "rw"}}
        )
        
        logging.info(f"PostgresSQL container '{container_name}' is running on port {db_port}")


