import pytest
import allure
from infra.pages.board_page import BoardPage
from infra.verifiers.ui_verifier import UIVerifier
import os

@allure.feature("Trello UI Automation")
class TestTrelloUI:

    @pytest.fixture(autouse=True)
    def setup(self, soft_assert):
        """Initializes the Verifier for each test"""
        self.verifier = UIVerifier(soft_assert)

    @allure.story("Scenario 1: Urgent Cards Validation")
    @allure.description("Locate all cards with 'Urgent' label and verify they are displayed correctly.")
    def test_verify_urgent_cards_visualization(self, board_page: BoardPage):
        
        # 1. Act: Find cards
        print("\n[INFO] Finding Urgent cards on board...")
        urgent_cards = board_page.get_cards_with_label("Urgent")
        
        print(f"[INFO] Found {len(urgent_cards)} cards.")

        # 2. Assert: Delegate verification to logic layer
        self.verifier.verify_urgent_cards_visuals(urgent_cards)


    @allure.story("Scenario 2: Specific Card Content Validation")
    @allure.description("Open 'summarize the meeting' card and validate deep details in the modal.")
    def test_verify_specific_card_content(self, board_page: BoardPage):
        
        card_title = "summarize the meeting"
        
        # 1. Act: Open Card
        try:
            board_page.open_card_by_title(card_title)
        except Exception:
            pytest.fail(f"CRITICAL: Could not find card '{card_title}' on the board to click on.")

        # 2. Act: Extract Details
        current_details = board_page.get_modal_details()
        print(f"[DEBUG] Extracted UI Details: {current_details}")

        expected_status = os.getenv("TRELLO_DEFAULT_LIST", "To Do")
        # 3. Assert: Verify against expectations
        expected_data = {
            "title": card_title,
            "description": "For all of us Please do so",
            "label": "New",
            "status": expected_status
        }
        
        self.verifier.verify_card_details(current_details, expected_data)

        # 4. Cleanup
        board_page.close_modal()