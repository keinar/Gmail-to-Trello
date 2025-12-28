from typing import List
import allure
from infra.utils.logger_setup import get_logger

logger = get_logger("SoftAssert")

class SoftAssert:
    def __init__(self):
        self._errors: List[str] = []

    def check(self, condition: bool, message: str):
        """
        Verifies a condition. If False:
        1. Adds error to internal list.
        2. Logs it as ERROR.
        3. Attaches it to Allure report immediately.
        """
        if not condition:
            formatted_error = f"[FAILURE] {message}"
            self._errors.append(formatted_error)
            
            # Write to Log
            logger.error(formatted_error)
            
            # Attach to Allure Report
            with allure.step(f"Soft Assert Failed: {message[:50]}..."):
                allure.attach(
                    message, 
                    name="Failure Details", 
                    attachment_type=allure.attachment_type.TEXT
                )

    def assert_all(self):
        """
        Raises an AssertionError if any errors were collected.
        """
        if self._errors:
            error_count = len(self._errors)
            report = "\n".join(self._errors)
            
            # Attach full report to Allure before crashing
            allure.attach(report, name="Full Failure Report", attachment_type=allure.attachment_type.TEXT)
            
            raise AssertionError(f"Soft Assert failed with {error_count} errors. Check Allure report or logs for details.")