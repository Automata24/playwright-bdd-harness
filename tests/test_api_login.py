import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom API marker to all scenarios in this file
pytestmark = pytest.mark.api

# Load the dedicated API feature file configurations
scenarios("../features/api_login.feature")

@given("the DummyJSON authentication endpoint is initialized", target_fixture="api_context")
def init_api_context(playwright):
    # Strategy: Initialize an isolated request context map for API lifecycle
    request_context = playwright.request.new_context(base_url="https://dummyjson.com")
    yield request_context
    request_context.dispose()

@when(parsers.parse('a POST request is dispatched with user "{username}" and password "{password}"'), target_fixture="api_response")
def dispatch_post_request(api_context, username, password):
    # Execute the HTTP POST call passing JSON payloads inline
    response = api_context.post(
        "/auth/login",
        headers={"Content-Type": "application/json"},
        data={
            "username": username,
            "password": password
        }
    )
    return response

@then(parsers.parse("the response status code must be {status_code:d}"))
def verify_status_code(api_response, status_code):
    # Confirm endpoint response matches target expectations
    assert api_response.status == status_code, (
        f"API status code deviation detected! Expected: {status_code}, Found: {api_response.status}"
    )

@then("the response payload must return a valid token string")
def verify_response_payload(api_response):
    # Parse text payload to standard dictionary map
    payload = api_response.json()
    
    # Verify structural safety properties of the endpoint
    assert "accessToken" in payload, (
        f"Security Failure: 'accessToken' key is missing from payload maps. Payload keys found: {list(payload.keys())}"
    )
    assert isinstance(payload["accessToken"], str) and len(payload["accessToken"]) > 0, (
        "The generated authentication token is null or structurally compromised."
    )
