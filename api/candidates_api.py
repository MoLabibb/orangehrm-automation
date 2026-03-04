# api/candidates_api.py

import requests
import datetime
from selenium.webdriver.remote.webdriver import WebDriver


class CandidatesAPI:
    BASE_URL = "https://opensource-demo.orangehrmlive.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": f"{self.BASE_URL}/web/index.php/recruitment/viewCandidates",
        })

    def login_with_browser_session(self, driver: WebDriver) -> None:
        """
        Extract cookies from authenticated Selenium session and inject into requests.
        """
        browser_cookies = driver.get_cookies()

        for cookie in browser_cookies:
            self.session.cookies.set(
                name=cookie["name"],
                value=cookie["value"],
                domain=cookie.get("domain", "").lstrip("."),
                path=cookie.get("path", "/"),
            )

        # Verify session works
        verify = self.session.get(
            f"{self.BASE_URL}/web/index.php/api/v2/recruitment/candidates",
            params={"limit": 1, "offset": 0}
        )

        if verify.status_code != 200:
            raise ConnectionError(
                f"Cookie bridge failed — status {verify.status_code}. "
                f"Response: {verify.text[:300]}"
            )

    def get_candidate_count(self) -> int:
        """Return total candidate count from API."""
        url = f"{self.BASE_URL}/web/index.php/api/v2/recruitment/candidates"
        params = {
            "limit": 50,
            "offset": 0,
            "model": "list",
            "sortField": "candidate.dateOfApplication",
            "sortOrder": "DESC"
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("meta", {}).get("total", 0)

    def add_candidate(self, first_name: str, last_name: str, email: str) -> dict:
        """Create a new candidate. Returns created candidate dict including id."""
        url = f"{self.BASE_URL}/web/index.php/api/v2/recruitment/candidates"
        payload = {
            "firstName": first_name,
            "middleName": "",
            "lastName": last_name,
            "email": email,
            "contactNumber": "",
            "keywords": "",
            "comment": "",
            "dateOfApplication": datetime.date.today().isoformat(),
            "consentToKeepData": False
        }
        response = self.session.post(url, json=payload)

        if response.status_code not in (200, 201):
            raise ValueError(
                f"Add candidate failed — status {response.status_code}. "
                f"Body: {response.text[:500]}"
            )

        return response.json().get("data", {})

    def delete_candidate(self, candidate_id: int) -> None:
        """Delete a candidate by numeric ID."""
        url = f"{self.BASE_URL}/web/index.php/api/v2/recruitment/candidates"
        response = self.session.delete(url, json={"ids": [candidate_id]})

        if response.status_code not in (200, 204):
            raise ValueError(
                f"Delete candidate failed — status {response.status_code}. "
                f"Body: {response.text[:500]}"
            )