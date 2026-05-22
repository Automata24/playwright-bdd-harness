import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom API marker to all scenarios in this file
pytestmark = pytest.mark.api

# Connect automatically to the new delete feature schema
scenarios("../features/api_delete_cart.feature")

@given("the DummyJSON API environment is active", target_fixture="api_context")
def init_api_context(playwright):
    request_context = playwright.request.new_context(base_url="https://dummyjson.com")
    yield request_context
    request_context.dispose()

@when(parsers.parse('the user logs in with username "{username}" and password "{password}" via API'), target_fixture="auth_data")
def api_login_step(api_context, username, password):
    response = api_context.post(
        "/auth/login",
        headers={"Content-Type": "application/json"},
        data={"username": username, "password": password}
    )
    assert response.status == 200
    return response.json()

@when(parsers.parse('creates a dynamic cart session with product IDs "{product_ids}" and quantities "{quantities}"'), target_fixture="created_cart_data")
def create_cart_step(api_context, auth_data, product_ids, quantities):
    dynamic_user_id = auth_data["id"]
    id_list = [int(p_id.strip()) for p_id in product_ids.split(",")]
    qty_list = [int(qty.strip()) for qty in quantities.split(",")]
    
    payload_products = [{"id": p_id, "quantity": qty} for p_id, qty in zip(id_list, qty_list)]

    response = api_context.post(
        "/carts/add",
        headers={"Content-Type": "application/json"},
        data={"userId": dynamic_user_id, "products": payload_products}
    )
    assert response.status == 201, f"Setup Error: Pre-requisite cart addition failed with {response.status}"
    return response.json()

@when("executes a HTTP DELETE operation against an authorized test seed cart ID", target_fixture="delete_response")
def delete_cart_step(api_context, created_cart_data):
    # Senior Strategy: Confirm the mock data payload generated successfully first
    assert "products" in created_cart_data, "Pre-requisite generation payload missing structural map layout."
    
    # Target a supported mock test seed ID slot (1-50) to allow the API to simulate the deletion successfully
    target_mock_id = 1
    
    print("\n" + "="*50)
    print(f"DEBUG: SIMULATING DELETION DESTRUCT SEQUENCE ON SEED ID: {target_mock_id}")
    print("="*50 + "\n")

    # Dispatch the standard HTTP DELETE request
    response = api_context.delete(f"/carts/{target_mock_id}")
    return response

@then(parsers.parse("the system must confirm deletion with status code {status_code:d}"))
def check_delete_status_code(delete_response, status_code):
    assert delete_response.status == status_code, (
        f"DELETE request rejected or compromised. Server state code: {delete_response.status}"
    )

@then("the returned payload state must show the record is deleted")
def verify_deletion_payload(delete_response):
    payload = delete_response.json()

    # Visual Inspection Console Output Trace
    print("\n" + "="*50)
    print("DEBUG: RECEIVED TERMINAL DELETION ACKNOWLEDGEMENT PAYLOAD:")
    print(json.dumps(payload, indent=4))
    print("="*50 + "\n")

    # Audit the deletion metadata flags explicitly returned by the API microservice
    assert "isDeleted" in payload, "Schema Contract Broken: API skipped outputting 'isDeleted' validation key."
    assert payload["isDeleted"] is True, "Data Integrity Defect: 'isDeleted' flag evaluates to False on a deleted resource."
    
    # Confirm a timestamp anchor exists for auditing logging trails
    assert "deletedOn" in payload, "Missing server-side audit field 'deletedOn'."
