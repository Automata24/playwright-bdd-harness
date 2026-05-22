class InventoryPage:
    def __init__(self, page):
        self.page = page
        
        # Locators
        self.inventory_container = page.locator("[data-test='inventory-container']")
        self.shopping_cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.shopping_cart_link = page.locator("[data-test='shopping-cart-link']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.inventory_item_names = page.locator("[data-test='inventory-item-name']")

        # Dynamic locator generator for specific items
        # e.g., 'sauce-labs-backpack'
        self.add_to_cart_btn = lambda item_name: page.locator(f"[data-test='add-to-cart-{item_name}']")
        self.remove_from_cart_btn = lambda item_name: page.locator(f"[data-test='remove-{item_name}']")

    def add_item_to_cart(self, item_name: str):
        """Clicks the 'Add to cart' button for a specific item id suffix."""
        self.add_to_cart_btn(item_name).click()

    def get_cart_count(self) -> str:
        """Returns the number of items currently showing on the shopping cart badge."""
        if self.shopping_cart_badge.is_visible():
            return self.shopping_cart_badge.text_content()
        return "0"
    
    def go_to_checkout(self):
        """Navigates to the shopping cart and clicks the checkout button."""
        self.shopping_cart_link.click()
        self.checkout_button.click()

    def sort_products_by_value(self, value: str):
        """Selects a sorting option from the dropdown (e.g., 'za')."""
        self.sort_dropdown.select_option(value)

    def get_all_product_names(self) -> list:
        """Returns a list of all product name strings currently displayed on the page."""
        return self.inventory_item_names.all_text_contents()
