import requests
import os
from typing import List
from infra.modals.card_modal import CardModal

class TrelloClient:
    def __init__(self):
        # Load credentials from environment variables
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.api_token = os.getenv('TRELLO_API_TOKEN')
        self.board_id = os.getenv('TRELLO_BOARD_ID')
        self.base_url = "https://api.trello.com/1"
        
        if not all([self.api_key, self.api_token, self.board_id]):
            raise ValueError("Missing Trello credentials in .env file")

    def get_all_cards(self) -> List[CardModal]:
        """Fetches all cards from the board and converts them to CardModal objects."""
        url = f"{self.base_url}/boards/{self.board_id}/cards"
        query = {
            'key': self.api_key,
            'token': self.api_token,
            'fields': 'name,desc,labels,idList' # Fetch only needed fields
        }
        
        response = requests.get(url, params=query)
        response.raise_for_status()
        
        trello_cards = []
        for card_json in response.json():
            label_names = [label['name'] for label in card_json.get('labels', []) if label.get('name')]
            
            card_obj = CardModal(
                title=card_json['name'],
                description=card_json['desc'],
                labels=label_names
            )
            trello_cards.append(card_obj)
            
        return trello_cards

# --- Debugging ---
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load the .env file
    
    client = TrelloClient()
    cards = client.get_all_cards()
    print(f"Connected to Trello! Found {len(cards)} cards on the board.")
    for card in cards[:3]: # Print first 3
        print(f"- {card.title} (Labels: {card.labels})")