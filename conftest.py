import allure
import pytest
import os
from infra.clients.gmail_client import GmailClient
from infra.clients.trello_client import TrelloClient
from dotenv import load_dotenv
from infra.pages.board_page import BoardPage
from infra.utils.soft_assert import SoftAssert
from infra.pages.login_page import LoginPage

load_dotenv()

@pytest.fixture(scope="session")
def gmail_client():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'mock_gmail_data.json')
    return GmailClient(data_path)

@pytest.fixture(scope="session")
def trello_client():
    return TrelloClient()

@pytest.fixture
def soft_assert():
    """
    Fixture that provides soft assertion capability.
    Automatically raises an error at the end of the test if any checks failed.
    """
    asserter = SoftAssert()
    yield asserter
    asserter.assert_all()

@pytest.fixture(scope="session")
def browser_context_args(authenticated_context):
    return {
        "storage_state": authenticated_context,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "allure-results/videos",
        "record_video_size": {"width": 1920, "height": 1080}
    }


# --- UI Fixtures ---

@pytest.fixture(scope="session")
def authenticated_context(browser):
    """
    Performs login ONCE per session and saves the storage state.
    SECURE IMPLEMENTATION: No hardcoded credentials.
    """
    # 0. Login with existing state
    state_path = "state.json"

    if os.path.exists(state_path):
        print(f"✅ Loading existing authentication state from {state_path}")
        return state_path

    print("⚠️ No state.json found. Attempting automatic login (might fail due to 2FA)...")

    # 1. Load & Validate Credentials
    email = os.getenv("TRELLO_EMAIL")
    password = os.getenv("TRELLO_PASSWORD")
    
    if not email or not password:
        raise ValueError(
            "CRITICAL: Missing credentials! Please set TRELLO_EMAIL and TRELLO_PASSWORD in your .env file."
        )

    # 2. Setup Context
    video_dir = os.path.abspath("allure-results/login-video")
    context = browser.new_context(
        record_video_dir=video_dir,
        record_video_size={"width": 1920, "height": 1080},
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    
    # 3. Perform Login
    try:
        login_page = LoginPage(page)
        login_page.navigate("https://trello.com/login")
        login_page.login(email, password)
    
    # 4. Save State
        state_path = "state.json"
        context.storage_state(path=state_path)
    except Exception as e:
        print(f"Login failed! Check video in {video_dir}")
        try:
            page.close()
            context.close()
            
            files = os.listdir(video_dir)
            if files:
                latest_video = os.path.join(video_dir, files[-1])
                print(f"Attaching video to Allure: {latest_video}")
                
                allure.attach.file(
                    latest_video, 
                    name="Login Failure Video", 
                    attachment_type=allure.attachment_type.WEBM
                )
        except Exception as video_error:
            print(f"Failed to attach video: {video_error}")
        raise e
    finally:
        context.close()
    return state_path

@pytest.fixture
def board_page(page):
    """
    Instantiates the BoardPage object.
    
    Pre-condition: 
    The 'page' fixture is ALREADY logged in because 'browser_context_args' 
    injected the storage state automatically.
    """
    board_id = os.getenv('TRELLO_BOARD_ID', '2GzdgPlw')
    board_url = f"https://trello.com/b/{board_id}/droxi"
    
    page.goto(board_url)

    page.wait_for_load_state("domcontentloaded")
    if page.get_by_text("Sign up to see this board").is_visible() or \
       page.get_by_text("Log in to continue").is_visible():
        
        allure.attach(
            page.screenshot(), 
            name="Login_Failed_Redirect", 
            attachment_type=allure.attachment_type.PNG
        )
        raise Exception("CRITICAL: Authentication failed! The 'state.json' is invalid or expired. Please delete it and re-login.")

    try:
        page.wait_for_selector("#board", timeout=10000)
    except Exception:
        allure.attach(page.screenshot(), name="Board_Not_Found", attachment_type=allure.attachment_type.PNG)
        raise Exception(f"Failed to load board. Current URL: {page.url}")
    
    return BoardPage(page)