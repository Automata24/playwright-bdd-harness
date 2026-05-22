import re
import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom API marker to all scenarios in this file
pytestmark = pytest.mark.api

# Connect automatically to the new products feature schema
scenarios("../features/api_products.feature")

@given("the DummyJSON API framework is ready", target_fixture="api_context")
def init_api_context(playwright):
    request_context = playwright.request.new_context(base_url="https://dummyjson.com")
    yield request_context
    request_context.dispose()

@when(parsers.parse('a GET request is dispatched to fetch product id "{product_id}"'), target_fixture="product_response")
def fetch_product_by_id(api_context, product_id):
    # Execute a clean REST GET operation against the API resource path
    response = api_context.get(f"/products/{product_id}")
    return response

@then(parsers.parse("the system must respond with status code {status_code:d}"))
def check_status_code(product_response, status_code):
    assert product_response.status == status_code, (
        f"API failed to locate target product. Code returned: {product_response.status}"
    )

@then("the product description string length must exceed 10 characters")
def audit_product_description(product_response):
    payload = product_response.json()
    
    # Audit Strategy: Print payload cleanly to terminal for instant debugging visibility
    print("\n" + "="*50)
    print(f"DEBUG: VERIFYING PRODUCT METRICS FOR: {payload.get('title', 'Unknown Title')}")
    print(json.dumps(payload, indent=4))
    print("="*50 + "\n")

    # Contract Validation: Confirm title exists and description meets textual parameters
    assert "description" in payload, "Database schema contract broken: 'description' key missing."
    desc_text = payload["description"]
    
    assert isinstance(desc_text, str) and len(desc_text) > 10, (
        f"Product description length boundary failed. Content: '{desc_text}'"
    )

@then("the primary thumbnail image must utilize an active URL string")
def audit_thumbnail_contract(product_response):
    payload = product_response.json()
    
    assert "thumbnail" in payload, "Database schema contract broken: 'thumbnail' key missing."
    thumbnail_url = payload["thumbnail"]
    
    # Assert structural type integrity
    assert isinstance(thumbnail_url, str) and len(thumbnail_url) > 0, "Thumbnail asset pointer string is empty or invalid."
    
    # Use standard regex to verify URL path formatting conventions
    url_pattern = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    assert url_pattern.match(thumbnail_url), f"Asset target does not match correct URL schema syntax: '{thumbnail_url}'"
