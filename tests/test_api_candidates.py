# tests/test_api_candidates.py

import pytest
from api.candidates_api import CandidatesAPI
from utils.data_generator import DataGenerator


class TestCandidatesAPI:
    """API tests for OrangeHRM Recruitment Candidates."""

    def test_add_candidate_increases_count_by_one(self, api_client: CandidatesAPI):

        print("\n" + "="*55)
        print("  API TEST — Add Candidate")
        print("="*55)

        # Get baseline count
        count_before = api_client.get_candidate_count()
        print(f"✅ Current candidate count: {count_before}")

        # Generate unique candidate data
        first_name = DataGenerator.generate_candidate_first_name()
        last_name = DataGenerator.generate_candidate_last_name()
        email = DataGenerator.generate_candidate_email()
        print(f"✅ Generated candidate data: {first_name} {last_name} <{email}>")

        # Add candidate via API
        candidate = api_client.add_candidate(first_name, last_name, email)
        self.created_candidate_id = candidate["id"]
        print(f"✅ Candidate created via API — id: {self.created_candidate_id}")

        # Verify count increased
        count_after = api_client.get_candidate_count()
        assert count_after == count_before + 1, (
            f"Expected {count_before + 1} candidates after add, got {count_after}"
        )
        print(f"✅ Count increased: {count_before} → {count_after}")

        print("="*55)
        print("  API TEST PASSED ✓")
        print("="*55 + "\n")

    def test_delete_candidate_decreases_count_by_one(self, api_client: CandidatesAPI):

        print("\n" + "="*55)
        print("  API TEST — Delete Candidate")
        print("="*55)

        # Create a candidate to delete
        first_name = DataGenerator.generate_candidate_first_name()
        last_name = DataGenerator.generate_candidate_last_name()
        email = DataGenerator.generate_candidate_email()
        candidate = api_client.add_candidate(first_name, last_name, email)
        candidate_id = candidate["id"]
        print(f"✅ Test candidate created — id: {candidate_id}")

        # Baseline count after creation
        count_before = api_client.get_candidate_count()
        print(f"✅ Count before delete: {count_before}")

        # Delete via API
        api_client.delete_candidate(candidate_id)
        print(f"✅ Candidate deleted — id: {candidate_id}")

        # Verify count decreased
        count_after = api_client.get_candidate_count()
        assert count_after == count_before - 1, (
            f"Expected {count_before - 1} candidates after delete, got {count_after}"
        )
        print(f"✅ Count decreased: {count_before} → {count_after}")

        print("="*55)
        print("  API TEST PASSED ✓")
        print("="*55 + "\n")