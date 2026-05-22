import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom API marker to all scenarios in this file
pytestmark = pytest.mark.api

# Parse the integrated E2E API feature file layout
scenarios("../features/api_cart.feature")

@given("the DummyJSON API environment is available", target_fixture="api_context")
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
    assert response.status == 200, f"Setup Failure: Authentication failed with code {response.status}"
    return response.json()

@when(parsers.parse('dispatches a POST request to generate a cart using dynamic profile ID with product IDs "{product_ids}" and quantities "{quantities}"'), target_fixture="cart_response")
def create_cart_with_dynamic_id(api_context, auth_data, product_ids, quantities):
    assert "id" in auth_data, "Database contract error: 'id' key missing from auth response."
    dynamic_user_id = auth_data["id"]
    
    # Senior Strategy: Dynamically parse comma-separated lists into structured integers
    id_list = [int(p_id.strip()) for p_id in product_ids.split(",")]
    qty_list = [int(qty.strip()) for qty in quantities.split(",")]
    
    assert len(id_list) == len(qty_list), "Data Error: The number of product IDs must match the number of quantities."

    # Construct the array payload by zipping the lists together dynamically
    payload_products = []
    for p_id, qty in zip(id_list, qty_list):
        payload_products.append({"id": p_id, "quantity": qty})

    print("\n" + "="*50)
    print(f"DEBUG: DYNAMICALLY GENERATED CARTS PAYLOAD:")
    print(json.dumps(payload_products, indent=2))
    print("="*50 + "\n")
    
    # Inject the user ID and the dynamically generated products list
    response = api_context.post(
        "/carts/add",
        headers={"Content-Type": "application/json"},
        data={
            "userId": dynamic_user_id,
            "products": payload_products
        }
    )
    return response

@then(parsers.parse("the system must confirm creation with status code {status_code:d}"))
def check_status_code(cart_response, status_code):
    # This now dynamically compares 201 against the actual server response state
    assert cart_response.status == status_code, (
        f"Cart creation failed. Server dropped unexpected status code: {cart_response.status}"
    )

@then("the api response total fields must perfectly balance with the product objects")
def validate_cart_financials(cart_response):
    payload = cart_response.json()

    print("\n" + "="*50)
    print("DEBUG: RECEIVED NEWLY CHAINED CART RECORD GENERATION:")
    print(json.dumps(payload, indent=4))
    print("="*50 + "\n")

    returned_items = payload["products"]
    calculated_total = 0.0
    calculated_quantity = 0

    for item in returned_items:
        price = float(item["price"])
        quantity = int(item["quantity"])
        line_total = float(item["total"])
        
        assert line_total == (price * quantity), f"Math breakdown on product ID {item.get('id')}"
        
        calculated_total += line_total
        calculated_quantity += quantity

    assert int(payload["totalQuantity"]) == calculated_quantity, "Total accumulated quantities do not match."
    assert float(payload["total"]) == calculated_total, "Global financial total calculation error."
