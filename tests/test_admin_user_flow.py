# tests/test_admin_user_flow.py

import pytest
import time
from pages.login_page import LoginPage
from pages.admin_page import AdminPage


def test_admin_user_flow(driver):

    print("\n" + "="*55)
    print("  UI TEST — Admin User Flow")
    print("="*55)

    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)

    # Step 1: Login
    login_page.login("Admin", "admin123")
    print("✅ Login successful")

    # Step 2: Navigate to Admin page
    admin_page.go_to_admin()
    print("✅ Navigated to Admin page")

    # Step 3: Get initial record count
    initial_count = admin_page.get_record_count()
    print(f"✅ Initial record count: {initial_count}")

    # Step 4: Add new user
    admin_page.click(admin_page.add_button)
    unique_user = f"QA_Admin_{int(time.time())}"
    admin_page.add_user("a", unique_user, "Admin@123")
    print(f"✅ New user created: {unique_user}")

    # Step 5: Verify count increased by 1
    new_count = admin_page.get_record_count()
    assert new_count == initial_count + 1, (
        f"Expected {initial_count + 1} records after add, got {new_count}"
    )
    print(f"✅ Record count increased: {initial_count} → {new_count}")

    # Step 6: Delete the created user
    admin_page.delete_user(unique_user)
    print(f"✅ User deleted: {unique_user}")

    # Step 7: Reset filter and verify count returned
    admin_page.reset_filter_with_refresh()
    final_count = admin_page.get_record_count()
    assert final_count == initial_count, (
        f"Expected count to return to {initial_count}, got {final_count}"
    )
    print(f"✅ Final record count restored: {final_count}")

    print("="*55)
    print("  UI TEST PASSED ✓")
    print("="*55 + "\n")