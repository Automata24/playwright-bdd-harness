import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom API marker to all scenarios in this file
pytestmark = pytest.mark.api

# Connect automatically to the negative scenarios feature file schema
scenarios("../features/api_negative_scenarios.feature")

@given("the dynamic DummyJSON REST context is ready", target_fixture="api_context")
def init_api_context(playwright):
    request_context = playwright.request.new_context(base_url="https://dummyjson.com")
    yield request_context
    request_context.dispose()

# -------------------------------------------------------------------------
# Endpoint 1 Steps: Authentication Payload Rejection Validation
# -------------------------------------------------------------------------
@when(parsers.parse('an unauthorized POST login request is dispatched with username "{username}" and password "{password}"'), target_fixture="api_failure_response")
def dispatch_invalid_login(api_context, username, password):
    response = api_context.post(
        "/auth/login",
        headers={"Content-Type": "application/json"},
        data={
            "username": username,
            "password": password
        }
    )
    return response

# -------------------------------------------------------------------------
# Endpoint 2 Steps: Product Out-of-Bounds Lookup Validation
# -------------------------------------------------------------------------
@when(parsers.parse('an out of bounds GET request is executed for non existent product ID "{out_of_bounds_id}"'), target_fixture="api_failure_response")
def lookup_invalid_product(api_context, out_of_bounds_id):
    response = api_context.get(f"/products/{out_of_bounds_id}")
    return response

# -------------------------------------------------------------------------
# Shared Assertion Steps: Status & Message Schema Integrity Checking
# -------------------------------------------------------------------------
@then(parsers.parse("the API endpoint must reject the operation with status code {status_code:d}"))
def verify_failure_status_code(api_failure_response, status_code):
    # Confirm that the server securely blocks the request with the expected error status code
    assert api_failure_response.status == status_code, (
        f"Defensive Error Boundary Blown! Expected status code: {status_code}, "
        f"but API returned: {api_failure_response.status}"
    )

@then(parsers.parse('the failure payload must explicitly state the system error message "{expected_error}"'))
def verify_failure_message_payload(api_failure_response, expected_error):
    payload = api_failure_response.json()

    # Visual Inspection Console Output Trace (Enabled via your permanent -s flag configuration)
    print("\n" + "="*50)
    print(f"DEBUG: CAPTURED EXPECTED BOUNDARY FAILURE RESPONSE:")
    print(json.dumps(payload, indent=4))
    print("="*50 + "\n")

    # Audit the structural error contract returned by the API microservice
    assert "message" in payload, (
        f"API Contract Violation: Error response missing standard 'message' data key. "
        f"Keys found: {list(payload.keys())}"
    )
    
    actual_error_message = payload["message"]
    assert actual_error_message == expected_error, (
        f"Error string validation mismatch.\n"
        f"Expected String: '{expected_error}'\n"
        f"Actual Returned: '{actual_error_message}'"
    )
