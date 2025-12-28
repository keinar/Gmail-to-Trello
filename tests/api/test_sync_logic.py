import pytest
from infra.verifiers.sync_verifier import SyncVerifier

class TestGmailTrelloSync:
    
    def test_verify_gmail_cards_synced_to_trello(self, gmail_client, trello_client, soft_assert):
        """
        Task 2: Validate sync logic using a dedicated Logic Verifier.
        """
        expected_cards = gmail_client.get_expected_cards()
        actual_cards = trello_client.get_all_cards()
        
        print(f"\n[INFO] Verifying {len(expected_cards)} expected cards against {len(actual_cards)} actual cards.")

        verifier = SyncVerifier(expected_cards, actual_cards, soft_assert)
        
        # Step A: Check that Gmail cards exist in Trello with correct data
        verifier.verify_cards_existence_and_content()
        
        # Step B: Check that Trello doesn't contain garbage (Integrity)
        verifier.verify_board_integrity()