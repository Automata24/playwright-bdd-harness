import pytest
import random
import string
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage 


@pytest.fixture
def checkout_profile():
    """Generates realistic, completely non-hardcoded user profiles."""
    random_suffix = "".join(random.choices(string.digits, k=4))
    return {
        "first_name": f"Tester_{random_suffix}",
        "last_name": f"Automation_{random_suffix}",
        "postal_code": "".join(random.choices(string.digits, k=5))
    }

@pytest.fixture
def user_credentials():
    return {"username": "standard_user", "password": "secret_sauce"}

@pytest.fixture
def pom_login(page):
    return LoginPage(page)

@pytest.fixture
def pom_inventory(page):
    return InventoryPage(page)

@pytest.fixture
def pom_checkout(page):  # Add this new fixture
    return CheckoutPage(page)
