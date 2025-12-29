from typing import List
import allure
from infra.modals.card_modal import CardModal
from infra.utils.soft_assert import SoftAssert
from infra.utils.logger_setup import get_logger

# קבלת ה-Logger
logger = get_logger("SyncVerifier")

class SyncVerifier:
    def __init__(self, expected_cards: List[CardModal], actual_cards: List[CardModal], soft_assert: SoftAssert):
        self.expected_cards = expected_cards
        self.actual_cards = actual_cards
        self.actual_cards_map = {card.title: card for card in actual_cards}
        self.soft_assert = soft_assert

    @allure.step("Step 1: Verify all Gmail cards exist in Trello with correct content")
    def verify_cards_existence_and_content(self):
        logger.info("Starting verification of existence and content...")
        for expected in self.expected_cards:
            if expected.title not in self.actual_cards_map:
                self._handle_missing_card(expected)
                continue
            
            actual = self.actual_cards_map[expected.title]
            self._verify_content(expected, actual)
            self._verify_labels(expected, actual)

    @allure.step("Step 2: Verify Trello Board Integrity (No Duplicates/Dirty Data)")
    def verify_board_integrity(self):
        logger.info("Starting integrity check...")
        titles_list = [c.title for c in self.actual_cards]
        
        for card in self.actual_cards:
            # Check for Dirty Data
            if card.title.lower().startswith("task:") or card.title.lower().startswith("meeting:"):
                msg = f"[BUG - DIRTY DATA] Found invalid card: '{card.title}'. Prefix should be removed."
                self.soft_assert.check(False, msg)

            # Check for Duplication
            if titles_list.count(card.title) > 1:
                msg = f"[BUG - DUPLICATION] Card '{card.title}' appears {titles_list.count(card.title)} times!"
                self.soft_assert.check(False, msg)

    # --- Private Helpers ---

    @allure.step("Checking missing card: {expected.title}")
    def _handle_missing_card(self, expected: CardModal):
        found_dirty = False
        for actual_title in self.actual_cards_map.keys():
            if expected.title in actual_title and ("Task" in actual_title or "Meeting" in actual_title):
                self.soft_assert.check(
                    False, 
                    f"[BUG - TITLE NOT CLEANED] Found '{actual_title}', expected clean '{expected.title}'."
                )
                found_dirty = True
                break
        
        if not found_dirty:
            self.soft_assert.check(False, f"[MISSING CARD] '{expected.title}' exists in Gmail but NOT in Trello.")

    def _verify_content(self, expected: CardModal, actual: CardModal):
        expected_lines = [line.strip() for line in expected.description.split('\n') if line.strip()]
        for line in expected_lines:
            self.soft_assert.check(
                line in actual.description,
                f"CONTENT MISMATCH in '{expected.title}': Expected text '{line}' missing."
            )

    def _verify_labels(self, expected: CardModal, actual: CardModal):
        if "Urgent" in expected.labels:
            self.soft_assert.check(
                "Urgent" in actual.labels,
                f"LABEL MISMATCH: '{expected.title}' expected 'Urgent' label."
            )