# import asyncio
import aiohttp 
import logging
import json 

class APIExtractor:
    """
    APIExtractor class for extracting data from a remote API.

    Args:
        url (str): The base URL of the API.

    Attributes:
        base_url (str): The base URL of the API.

    Methods:
        extract_api: Extracts data from the API using asynchronous requests.

    """
    def __init__(self, url: str) -> None:
        """
        Initailizes the APIExtractor instance.

        Args:
            url (str): The base URL of the API.
        """
        self.base_url = url 
        
    async def extract_api(self, session:aiohttp.ClientSession, page:int=1, per_page:int=1000):
        """
        Extracts data from the API using asynchronous requests.

        Args:
            session (aiohttp.ClientSession): The aiohttp client session.
            page (int, optional): The page number for pagination (default is 1).
            per_page (int, optional): The number of items per page (default is 1000).

        Returns:
            List[Any]: The extracted data from the API.

        Raises:
            ValueError: If page or per_page are not integers or are less than 1.
            aiohttp.ClientResponseError: If there is an error during the API request.
            json.JSONDecodeError: If there is an error decoding JSON from the API response.
            IndexError: If there is an error extracting data from the API response.

        """
        if not isinstance(page, int) or not isinstance(per_page, int):
            raise ValueError("page and per_page must be integers")
        
        if page < 1 or per_page < 1:
            raise ValueError("page and per_page must be greater than or equal to 1")
        
        params = {
            "format": "json",
            "page": page,
            "per_page": per_page
        }
        
        try:
            async with session.get(self.base_url, params=params) as resp:
                if resp.status == 404:
                    logging.error(f"API endpoint not found. URL: {resp.url}")
                    exit()
                
                resp.raise_for_status() # Raise an HTTPError for bad responses
                
                data = await resp.json()
                
                if "message" in data[0]:
                    error_message = data[0].get("message")[0].get("value")
                    print(f"API error: {error_message}")
                    return []
                
                indicator = data[1]
                return indicator 
        except (aiohttp.client_exceptions.ClientResponseError, aiohttp.http_exceptions.HttpProcessingError, aiohttp.ClientResponseError) as e:
            logging.error(f"Error during API request: {e}")
            raise e 
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
        except IndexError as e:
            logging.error(f"Index error: {e}")
        return []
     