import allure
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeout
from infra.utils.logger_setup import get_logger

logger = get_logger("BasePage")

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        try:
            logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    @allure.step("Click on element: {selector}")
    def click(self, selector: str):
        try:
            logger.info(f"Clicking element: {selector}")
            self.page.click(selector)
        except PlaywrightTimeout:
            logger.error(f"Timeout while trying to click: {selector}")
            self._take_screenshot("click_timeout")
            raise
        except Exception as e:
            logger.error(f"Error clicking {selector}: {e}")
            raise

    @allure.step("Fill text '{text}' into {selector}")
    def fill(self, selector: str, text: str):
        try:
            logger.info(f"Filling text into {selector}")
            self.page.fill(selector, text)
        except Exception as e:
            logger.error(f"Failed to fill text into {selector}: {e}")
            raise

    @allure.step("Get text from {selector}")
    def get_text(self, selector: str) -> str:
        try:
            self.wait_for_selector(selector)
            text = self.page.inner_text(selector)
            logger.info(f"Retrieved text from {selector}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            return ""

    @allure.step("Wait for selector: {selector}")
    def wait_for_selector(self, selector: str, state='visible', timeout=10000) -> Locator:
        try:
            return self.page.wait_for_selector(selector, state=state, timeout=timeout)
        except PlaywrightTimeout:
            logger.error(f"Element not found within {timeout}ms: {selector}")
            self._take_screenshot("element_not_found")
            raise

    def _take_screenshot(self, name: str):
        """Helper to attach screenshot to Allure on failure"""
        try:
            png_bytes = self.page.screenshot()
            allure.attach(
                png_bytes, 
                name=f"Screenshot_{name}", 
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.warning(f"Could not take screenshot: {e}")