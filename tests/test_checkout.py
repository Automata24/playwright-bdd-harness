import re
import math
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Apply the custom UI marker to all scenarios in this file
pytestmark = pytest.mark.ui

# Automatically loads every scenario found in the feature file
scenarios("../features/checkout.feature")

@given(parsers.parse('the user logs into Swag Labs with username "{username}" and password "{password}"'))
def login_step(pom_login, username, password):
    pom_login.navigate()
    pom_login.login(username, password)
    assert "inventory.html" in pom_login.page.url, f"Authentication failure for: {username}"

@when("the user adds two items to the cart")
def add_items_step(pom_inventory):
    items = ["sauce-labs-backpack", "sauce-labs-bike-light"]
    for item in items:
        pom_inventory.add_item_to_cart(item)
    assert pom_inventory.get_cart_count() == "2", "Cart did not increment to exactly 2 items."

@when("proceeds to checkout")
def go_to_checkout_step(pom_inventory):
    pom_inventory.go_to_checkout()
    assert "checkout-step-one.html" in pom_inventory.page.url

@when(parsers.parse('inputs their profile data "{first_name}", "{last_name}", and "{postal_code}"'))
def input_profile_step(pom_checkout, first_name, last_name, postal_code):
    pom_checkout.fill_information(
        first_name=first_name, 
        last_name=last_name, 
        postal_code=postal_code
    )
    assert "checkout-step-two.html" in pom_checkout.page.url

@then("the calculated subtotal and final total should perfectly balance with the UI values")
def verify_pricing_step(pom_checkout):
    # Senior Audit Engine Logic (Extracting UI text elements dynamically)
    price_elements = pom_checkout.page.locator(".inventory_item_price").all()
    extracted_prices = [float(re.search(r"\d+\.\d+", el.text_content()).group()) for el in price_elements]
    computed_subtotal = sum(extracted_prices)

    raw_subtotal_label = pom_checkout.page.locator(".summary_subtotal_label").text_content()
    raw_tax_label = pom_checkout.page.locator(".summary_tax_label").text_content()
    raw_total_label = pom_checkout.page.locator(".summary_total_label").text_content()

    ui_subtotal = float(re.search(r"\d+\.\d+", raw_subtotal_label).group())
    ui_tax = float(re.search(r"\d+\.\d+", raw_tax_label).group())
    ui_total = float(re.search(r"\d+\.\d+", raw_total_label).group())

    # Ensure robust floating-point evaluation
    assert math.isclose(computed_subtotal, ui_subtotal, rel_tol=1e-9), (
        f"Subtotal calculation anomaly. Computed: ${computed_subtotal}, UI Output: ${ui_subtotal}"
    )

    computed_final_total = ui_subtotal + ui_tax
    assert math.isclose(computed_final_total, ui_total, rel_tol=1e-9), (
        f"Financial Defect! Calculated: ${computed_final_total}, UI Total: ${ui_total}"
    )

    # Conclude transaction
    pom_checkout.finish_checkout()
    assert "checkout-complete.html" in pom_checkout.page.url
