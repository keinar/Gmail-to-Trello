# Gmail-to-Trello Automation Sync

[![CI - Gmail to Trello Automation](https://github.com/keinar/Gmail-to-Trello/actions/workflows/ci.yml/badge.svg)](https://github.com/keinar/Gmail-to-Trello/actions/workflows/ci.yml)

[![Allure Report](https://img.shields.io/badge/Allure%20Report-View-orange)](https://keinar.github.io/Gmail-to-Trello/)

This project implements an automated synchronization system between a Mock Gmail Inbox and a Trello Board.
It includes API verification logic and UI validation using Playwright.

## Architecture

The project follows a clean **Separation of Concerns** architecture:

- **`infra/clients`**: Data fetchers (Gmail, Trello) responsible for API communication and parsing.
- **`infra/verifiers`**: Dedicated logic layer (`SyncVerifier`) containing the complex business rules and integrity checks.
- **`infra/pages`**: Page Object Model (POM) implementation for Playwright UI tests.
- **`infra/utils`**: Helper utilities including `SoftAssert` and Centralized Logging.
- **`tests/`**: Clean test scripts that delegate logic to the infrastructure layer.

## Prerequisites

- **Docker Desktop** (Recommended)
- *Or for local run:* Python 3.10+, Java (for Allure), and Node.js.

## 🛠 How to Run (Docker) - Recommended

The easiest way to run the tests is using Docker, which sets up the environment, browsers, and reporting tools automatically.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Gmail-to-Trello
    ```

2.  **Create `.env` file:**
    Create a `.env` file in the root directory with the following credentials:
    ```env
    TRELLO_API_KEY=your_key_here
    TRELLO_API_TOKEN=your_token_here
    TRELLO_BOARD_ID=2GzdgPlw
    TRELLO_EMAIL=droxiautomation@gmail.com
    TRELLO_PASSWORD=Droxi123456789
    ```

3.  **Run the tests:**
    ```bash
    docker-compose up --build
    ```
    *This command will:*
    * Build the container.
    * Run API Logic Tests (Task 2).
    * Run UI Automation Tests (Task 3).
    * Generate Allure Report.

4.  **View the Report:**
    Once execution finishes, open your browser at:
    **http://localhost:5050**

## 🔐 Authentication & 2FA Handling

Since Trello employs strict security measures (2FA/MFA) and Bot detection, automated login within the Docker container might fail.
To solve this, I implemented a **"Bring Your Own Cookie"** architecture using a local helper script.

**Steps to generate a valid session:**
1.  Ensure you have Python and Playwright installed locally:
    ```bash
    pip install playwright
    playwright install chromium
    ```
2.  Run the helper script:
    ```bash
    python get_state_locally.py
    ```
3.  A browser window will open. **Log in manually** to Trello (perform 2FA if requested).
4.  Once logged in, the script will automatically capture the session cookies, save them to `state.json`, and close.
5.  Now you can run the Docker tests, and they will use this valid session:
    ```bash
    docker-compose up --build
    ```

## Test Coverage

### Task 2: API & Logic Synchronization
- Verifies that emails are correctly converted to Trello cards.
- Validates **Merging Logic** (same subject emails).
- Validates **"Urgent" Labeling** logic.
- **Integrity Check**: Detects "Dirty Data" (uncleaned `Task:` prefixes) and duplications on the board.

### Task 3: UI Automation (Playwright)
- Implements **Page Object Model**.
- Logs into Trello using the GUI.
- Visually verifies "Urgent" cards.
- Opens specific cards to validate merged content and descriptions in the modal view.

### ⚠️ Note on API Logic Verification
The test `test_verify_gmail_cards_synced_to_trello` is designed to validate the Trello board state against the Mock Data requirements.
**Expected Result:** This test will **FAIL** (SoftAssert errors).
**Reason:** The current state of the provided Trello board contains discrepancies (e.g., "Task:" prefixes not removed, missing cards) compared to the assignment requirements. The automation correctly identifies and reports these 14 bugs.

## Project Structure

```text
/
├── infra/                  # Core Infrastructure
│   ├── clients/            # Gmail & Trello API Clients
│   ├── verifiers/          # Business Logic Verification
│   ├── pages/              # Playwright Page Objects
│   └── utils/              # Shared Utilities (Logger, SoftAssert)
├── tests/                  # Test Scripts
│   ├── api/                # Backend Logic Tests
│   └── ui/                 # Frontend UI Tests
├── data/                   # Mock Data (JSON)
├── docker-compose.yml      # Container Orchestration
├── Dockerfile              # Environment Definition
└── requirements.txt        # Python Dependencies

- **`Manual Test Plan.pdf`**: Contains the manual testing strategy and test cases (Task 1).