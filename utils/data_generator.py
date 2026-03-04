# utils/data_generator.py

import random
import string
import time


class DataGenerator:

    @staticmethod
    def generate_username(prefix: str = "QA_Admin") -> str:
        return f"{prefix}_{int(time.time())}"

    @staticmethod
    def get_password() -> str:
        return "Admin@123"


    @staticmethod
    def generate_candidate_first_name() -> str:
        suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        return f"QA{suffix.capitalize()}"  

    @staticmethod
    def generate_candidate_last_name() -> str:
        suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
        return f"Test{suffix.capitalize()}"  

    @staticmethod
    def generate_candidate_email() -> str:
        timestamp = int(time.time())
        return f"qa.candidate.{timestamp}@test.com"