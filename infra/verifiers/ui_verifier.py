import allure
from typing import Dict, List
from playwright.sync_api import Locator
from infra.utils.soft_assert import SoftAssert
from infra.utils.logger_setup import get_logger

logger = get_logger("UIVerifier")

class UIVerifier:
    def __init__(self, soft_assert: SoftAssert):
        self.soft_assert = soft_assert

    @allure.step("Verify visual indication of 'Urgent' cards")
    def verify_urgent_cards_visuals(self, cards: List[Locator]):
        """
        Iterates over a list of card elements and verifies they have
        visual indications of urgency (Red label or text).
        """
        if not cards:
            logger.warning("No urgent cards provided for verification.")
            return

        for index, card in enumerate(cards):
            card_text = card.inner_text()
            title = card_text.split('\n')[0]
            
            is_visually_urgent = "Urgent" in card_text or "red" in card.inner_html()
            
            self.soft_assert.check(
                is_visually_urgent,
                f"[UI] Card '{title}' is missing visual 'Urgent' indicator (Label/Text)."
            )
            
            if is_visually_urgent:
                logger.info(f"Card '{title}' verified as visually Urgent.")

    @allure.step("Verify Card Modal Details")
    def verify_card_details(self, actual_details: Dict[str, any], expected_data: Dict[str, any]):
        """
        Compares the data extracted from the UI Modal against expected values.
        """
        # 1. Title Verification
        self.soft_assert.check(
            actual_details["title"] == expected_data["title"],
            f"[UI] Title Mismatch. Expected: '{expected_data['title']}', Got: '{actual_details['title']}'"
        )

        # 2. Description Verification (Contains check)
        clean_actual_desc = actual_details["description"].replace("\n", " ").strip()
        self.soft_assert.check(
            expected_data["description"] in clean_actual_desc,
            f"[UI] Description Mismatch.\nExpected to contain: '{expected_data['description']}'\nGot: '{clean_actual_desc}'"
        )

        # 3. Label Verification
        self.soft_assert.check(
            expected_data["label"] in actual_details["labels"],
            f"[UI] Missing Label. Expected '{expected_data['label']}' in {actual_details['labels']}"
        )

        # 4. Status/Column Verification
        self.soft_assert.check(
            expected_data["status"] in actual_details["status"],
            f"[UI] Wrong Column. Expected '{expected_data['status']}', Got: '{actual_details['status']}'"
        )