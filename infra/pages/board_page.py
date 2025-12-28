from infra.pages.base_page import BasePage
from typing import List, Dict
import allure
from infra.utils.logger_setup import get_logger

logger = get_logger("BasePage")


class BoardPage(BasePage):
    CARD_ELEMENT = "[data-testid='card-name']"  
    CARD_CONTAINER = "[data-testid='trello-card']"
    
    CLOSE_MODAL_BTN = "[aria-label='Close dialog']"
    MODAL_TITLE_INPUT = "[data-testid='card-back-title-input']"
    MODAL_DESC_P = '[class="ak-renderer-document"]'
    MODAL_LABELS_LIST = "[data-testid='card-label']"
    MODAL_COLUMN_STATUS = "button:has([data-testid='DownIcon'])"

    def debug_print_modal_header(self):
        """
        Helper method to dump the HTML structure of the card modal header.
        Use this to find the correct locator for the list name.
        """
        try:
            header = self.page.locator(".window-header")
            print("\n--- DEBUG: MODAL HEADER HTML ---")
            print(header.inner_html())
            print("--------------------------------\n")
        except Exception as e:
            print(f"Could not print header: {e}")

    @allure.step("Get all cards containing label: {label_text}")
    def get_cards_with_label(self, label_text: str) -> List[any]:
        """
        Filters all visible cards to find those that have the specific label.
        Returns a list of Playwright Locator objects.
        """
        all_cards = self.page.locator(self.CARD_CONTAINER).all()
        matching_cards = []

        for card in all_cards:
            # Check if this card has the label (by text or color attribute if needed)
            # Trello labels often have the text inside them or in title attribute
            if card.get_by_text(label_text).count() > 0 or \
               card.locator(f"[title*='{label_text}']").count() > 0:
                matching_cards.append(card)
        
        return matching_cards

    @allure.step("Open card by title: {title}")
    def open_card_by_title(self, title: str):
        logger.info(f"Attempting to open card: '{title}'")
        
        card_locator = self.page.locator(self.CARD_ELEMENT).filter(has_text=title).first
        
        try:
            card_locator.wait_for(state="visible", timeout=5000)
            card_locator.click()
        except Exception as e:
            self._take_screenshot(f"failed_to_find_{title}")
            logger.error(f"Could not find card '{title}'. Available cards text: {self.page.locator(self.CARD_ELEMENT).all_inner_texts()}")
            raise e
        
        self.wait_for_selector(self.MODAL_TITLE_INPUT)

    @allure.step("Extract details from open card modal")
    def get_modal_details(self) -> Dict[str, any]:
        self.wait_for_selector(self.MODAL_TITLE_INPUT)
        
        # Handle description safely (might be empty)
        desc_text = ""
        if self.page.locator(self.MODAL_DESC_P).count() > 0:
            desc_text = self.page.locator(self.MODAL_DESC_P).inner_text()
        try:
            status_element = self.page.locator(self.MODAL_COLUMN_STATUS).first
            status_text = status_element.inner_text().strip()
        except Exception:
            logger.warning("Could not extract status using DownIcon locator.")
            status_text = "UNKNOWN"
        return {
            "title": self.page.input_value(self.MODAL_TITLE_INPUT),
            "description": desc_text,
            "labels": self.page.locator(self.MODAL_LABELS_LIST).all_inner_texts(),
            "status": status_text
        }

    @allure.step("Close card modal")
    def close_modal(self):
        self.click(self.CLOSE_MODAL_BTN)