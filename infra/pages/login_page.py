from infra.pages.base_page import BasePage
import allure

class LoginPage(BasePage):
    EMAIL_INPUT = '[data-testid="username"]'
    LOGIN_BTN_INITIAL = '[data-testid="login-submit-idf-testid"]'
    PASSWORD_INPUT = '[data-testid="password"]'
    LOGIN_SUBMIT_BTN = '[data-testid="login-submit-idf-testid"]'
    HEADER_MEMBER_MENU = "[data-testid='header-member-menu-button']"
    
    @allure.step("Perform Login with user: {username}")
    def login(self, username, password):
        """Handles the Atlassian/Trello login flow"""
        self.wait_for_selector(self.EMAIL_INPUT)
        self.fill(self.EMAIL_INPUT, username)
        self.click(self.LOGIN_BTN_INITIAL)
        
        self.wait_for_selector(self.PASSWORD_INPUT)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_SUBMIT_BTN)
        self.page.wait_for_url("**trello.com/**", timeout=60000)
        self.page.wait_for_load_state('domcontentloaded', timeout=60000)
        try:
            self.wait_for_selector(self.HEADER_MEMBER_MENU, timeout=20000)
        except Exception:
            self._take_screenshot("login_failed_state")
            raise Exception("Login failed: Could not detect user session after submitting credentials.")