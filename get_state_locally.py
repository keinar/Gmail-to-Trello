from playwright.sync_api import sync_playwright
import time
import os

def generate_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("--- Opening Trello Login ---")
        page.goto("https://trello.com/login")

        print("🛑 ACTION REQUIRED: Please log in manually in the browser window.")
        print("1. Enter email & password.")
        print("2. Enter the 2FA code if sent to your email.")
        print("3. Wait until you see your Trello Boards page.")
        
        try:
            page.wait_for_selector("[data-testid='header-member-menu-button']", timeout=120000) # 2 דקות
            print("✅ Login detected!")
        except:
            print("❌ Timeout waiting for login. Did you finish?")
            
        state_path = "state.json"
        context.storage_state(path=state_path)
        print(f"✅ State saved to '{state_path}'")
        
        browser.close()

if __name__ == "__main__":
    generate_state()