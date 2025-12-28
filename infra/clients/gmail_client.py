import json
import os
import re
from typing import List, Dict
from infra.modals.cardModal import CardModal

class GmailClient:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path

    def _load_data(self) -> dict:
        """Loads the JSON data from the file."""
        if not os.path.exists(self.data_file_path):
            raise FileNotFoundError(f"Mock data file not found at: {self.data_file_path}")
        
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_expected_cards(self) -> List[CardModal]:
        """
        Parses the mock emails and returns a list of expected Trello Card objects
        applying the logic: Merging, Filtering, and Labeling.
        """
        raw_data = self._load_data()
        messages = raw_data.get('messages', [])
        
        print(f"[DEBUG] Loaded {len(messages)} raw messages from JSON.")
        
        # Dictionary to enforce uniqueness by Subject Title
        # Key = Normalized Title, Value = CardModal
        processed_cards: Dict[str, CardModal] = {}

        for msg in messages:
            raw_subject = msg.get('subject', '')
            body = msg.get('body', '')

            # --- Logic 1: Aggressive Subject Normalization ---
            # Remove "Task:" (case insensitive), remove "Meeting:", strip spaces
            # Also remove double spaces inside the title
            clean_title = re.sub(r"(?i)^(Task:|Meeting:)\s*", "", raw_subject).strip()
            clean_title = " ".join(clean_title.split()) 

            if not clean_title:
                continue # Skip empty titles if any

            # --- Logic 2: Urgency Check ---
            is_urgent = "urgent" in body.lower()

            if clean_title in processed_cards:
                # --- Logic 3: Merge Strategy ---
                existing_card = processed_cards[clean_title]
                
                # Append body only if it's not already there (simple de-duplication)
                if body and body not in existing_card.description:
                    if existing_card.description:
                        existing_card.description += f"\n{body}"
                    else:
                        existing_card.description = body
                
                # If THIS email is urgent, the whole card becomes urgent
                if is_urgent:
                    existing_card.add_label("Urgent")
            
            else:
                # --- Logic 4: Create New Card ---
                new_card = CardModal(
                    title=clean_title,
                    description=body,
                    labels=["New"]
                )
                if is_urgent:
                    new_card.add_label("Urgent")
                
                processed_cards[clean_title] = new_card

        return list(processed_cards.values())

# --- Execution for testing ---
if __name__ == "__main__":
    # Ensure the path is correct
    path = os.path.join(os.getcwd(), 'data', 'mock_gmail_data.json')
    client = GmailClient(path)
    
    try:
        cards = client.get_expected_cards()
        print(f"\n[SUCCESS] Final Unique Cards Count: {len(cards)}")
        print("-" * 50)
        for card in cards:
            print(f"Title: {card.title}")
            print(f"Labels: {card.labels}")
            print(f"Desc: {card.description.replace(chr(10), ' ')}") # Print desc in one line
            print("-" * 50)
    except Exception as e:
        print(f"[ERROR] {e}")