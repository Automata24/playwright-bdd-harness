import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom UI marker to all scenarios in this file
pytestmark = pytest.mark.ui

# Automatically links to the login failure feature file
scenarios("../features/login_failure.feature")

@given("the user opens the Swag Labs login page")
def open_login_page_step(pom_login):
    pom_login.navigate()

@when(parsers.parse('the user attempts to log in with invalid username "{username}" and password "{password}"'))
def attempt_invalid_login_step(pom_login, username, password):
    # Execute the login using bad credentials
    pom_login.login(username, password)

@then(parsers.parse('a security error message saying "{expected_error}" must be displayed'))
def verify_error_message_step(pom_login, expected_error):
    # Senior Strategy: Ensure the element is visible on screen first
    assert pom_login.error_message.is_visible(), "The application failed to render the authentication error container."
    
    # Extract text from the DOM element as the single source of truth
    actual_error = pom_login.error_message.text_content()
    
    # Assert exact textual alignment
    assert actual_error == expected_error, (
        f"Authentication error message mismatch.\n"
        f"Expected: '{expected_error}'\n"
        f"Actual:   '{actual_error}'"
    )
    
    # Verify the user was safely blocked and not routed forward
    assert "inventory.html" not in pom_login.page.url, (
        f"Security Defect! User was incorrectly routed into the catalog app. URL: {pom_login.page.url}"
    )
