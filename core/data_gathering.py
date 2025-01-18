# data_collector.py

import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """
    A class to collect gaming performance data from various sources including APIs,
    web scraping, and databases.
    """
    
    def __init__(self):
        """Initialize the DataCollector with a requests session."""
        self.session = requests.Session()
        logger.info("DataCollector initialized")
    
    async def fetch_api_data(self, 
                           api_url: str, 
                           player_id: str, 
                           api_key: Optional[str] = None) -> Dict:
        """
        Fetch player statistics from a game API.
        
        Args:
            api_url (str): Base URL of the gaming API
            player_id (str): Unique identifier for the player
            api_key (str, optional): API authentication key
            
        Returns:
            Dict: Player statistics from the API
            
        Raises:
            Exception: If API request fails
        """
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        
        try:
            response = await self.session.get(
                f"{api_url}/players/{player_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched API data for player {player_id}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Failed to fetch API data: {str(e)}")

    def scrape_web_data(self, url: str, player_username: str) -> Dict:
        """
        Scrape player statistics from gaming websites.
        
        Args:
            url (str): URL of the gaming statistics website
            player_username (str): Player's username on the website
            
        Returns:
            Dict: Scraped player statistics
            
        Raises:
            Exception: If web scraping fails
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example scraping pattern - adjust selectors based on website structure
            stats = {
                'accuracy': self._parse_stat(soup, 'accuracy-stat'),
                'reaction_time': self._parse_stat(soup, 'reaction-time-stat'),
                'decision_making': self._parse_stat(soup, 'decision-stat'),
                'teamwork': self._parse_stat(soup, 'teamwork-stat')
            }
            
            logger.info(f"Successfully scraped web data for player {player_username}")
            return stats
            
        except Exception as e:
            logger.error(f"Web scraping failed: {str(e)}")
            raise Exception(f"Failed to scrape web data: {str(e)}")

    def _parse_stat(self, soup: BeautifulSoup, stat_class: str) -> float:
        """
        Helper method to parse individual statistics from the webpage.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            stat_class (str): CSS class for the statistic
            
        Returns:
            float: Parsed statistic value
        """
        try:
            stat_element = soup.find('div', class_=stat_class)
            if stat_element:
                return float(stat_element.text.strip())
            return 0.0
        except (ValueError, AttributeError):
            logger.warning(f"Failed to parse stat with class {stat_class}")
            return 0.0

    def fetch_db_data(self, db_path: str, player_id: str) -> pd.DataFrame:
        """
        Fetch player statistics from a database.
        
        Args:
            db_path (str): Path to the SQLite database
            player_id (str): Unique identifier for the player
            
        Returns:
            pd.DataFrame: Historical player statistics
            
        Raises:
            Exception: If database query fails
        """
        try:
            conn = sqlite3.connect(db_path)
            query = """
                SELECT 
                    date,
                    accuracy,
                    reaction_time,
                    decision_making,
                    teamwork
                FROM player_stats
                WHERE player_id = ?
                ORDER BY date DESC
            """
            
            df = pd.read_sql_query(query, conn, params=(player_id,))
            conn.close()
            
            logger.info(f"Successfully fetched database data for player {player_id}")
            return df
            
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise Exception(f"Failed to fetch database data: {str(e)}")

    def cleanup(self):
        """Clean up resources used by the DataCollector."""
        self.session.close()
        logger.info("DataCollector resources cleaned up")