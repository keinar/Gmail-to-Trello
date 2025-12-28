# Gmail-to-Trello Automation Sync

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