def test_add_backpack_to_cart(pom_login, pom_inventory, user_credentials):
    # Log in first
    pom_login.navigate()
    pom_login.login(user_credentials["username"], user_credentials["password"])
    
    # Verify we landed on inventory page
    assert pom_inventory.inventory_container.is_visible()
    
    # Add item and verify the cart badge updates
    pom_inventory.add_item_to_cart("sauce-labs-backpack")
    assert pom_inventory.get_cart_count() == "1"
