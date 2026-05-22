import re
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom UI marker to all scenarios in this file
pytestmark = pytest.mark.ui

# Crucial: Ensure this targets the new inventory feature file explicitly
scenarios("../features/inventory.feature")

@given(parsers.parse('the user logs into Swag Labs with username "{username}" and password "{password}"'))
def login_step(pom_login, username, password):
    pom_login.navigate()
    pom_login.login(username, password)
    assert "inventory.html" in pom_login.page.url

@given("the catalog is explicitly set to the default A to Z sorting mode")
def set_default_sorting_step(pom_inventory):
    # Select default 'az' first to satisfy the dependency requirement
    pom_inventory.sort_products_by_value("az")
    
    # Assert it applied correctly before moving forward
    displayed_names = pom_inventory.get_all_product_names()
    assert displayed_names == sorted(displayed_names), "Catalog failed to initialize to standard A to Z order."

@when(parsers.parse('the user filters products by "Name (Z to A)" using selection value "{sort_value}"'))
def sort_products_step(pom_inventory, sort_value):
    # Select 'za' from the dropdown menu
    pom_inventory.sort_products_by_value(sort_value)

@then("the displayed items must be perfectly organized in alphabetical descending order")
def verify_sorting_step(pom_inventory):
    displayed_names = pom_inventory.get_all_product_names()
    expected_sorted_order = sorted(displayed_names, reverse=True)
    
    assert displayed_names == expected_sorted_order, (
        f"Inventory sorting defect detected!\n"
        f"Actual UI Layout Order:   {displayed_names}\n"
        f"Expected Sorted Z-A Order: {expected_sorted_order}"
    )
